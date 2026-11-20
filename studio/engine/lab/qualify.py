"""Reproducible two-site acceptance exercise on private local Docker networks."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import secrets
import shutil
import subprocess
import tempfile
import time
from uuid import uuid4

LAB = Path(__file__).resolve().parent
SITES = ("a", "b")


def run(*args, data=None, check=True):
    return subprocess.run(args, input=data, capture_output=True, text=True, check=check)


def secret():
    return secrets.token_urlsafe(40)


def compose(root, site, *args, **kwargs):
    project = (root / "project").read_text()
    filename = "central.yaml" if site == "central" else "instance.yaml"
    return run("docker", "compose", "-p", project + "-" + site, "--env-file",
               str(root / (site + ".env")), "-f", str(LAB / filename), *args, **kwargs)


def save_env(root, site, **values):
    (root / (site + ".env")).write_text("".join(f"{k}={v}\n" for k, v in values.items()))


def ca(directory, name):
    key, cert = directory / (name + ".key"), directory / (name + ".pem")
    run("openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "3",
        "-subj", "/CN=" + name, "-addext", "basicConstraints=critical,CA:TRUE",
        "-keyout", key, "-out", cert)
    return key, cert


def issue(directory, name, authority, usage, target, hostname=None):
    key, csr, cert = (directory / (name + ext) for ext in (".key", ".csr", ".crt"))
    run("openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes", "-subj",
        "/CN=" + name, "-keyout", key, "-out", csr)
    ext = directory / (name + ".ext")
    ext.write_text("basicConstraints=critical,CA:FALSE\nextendedKeyUsage=" + usage +
                   ("\nsubjectAltName=DNS:" + hostname if hostname else "") + "\n")
    run("openssl", "x509", "-req", "-in", csr, "-CA", authority[1], "-CAkey", authority[0],
        "-CAcreateserial", "-days", "3", "-extfile", ext, "-out", cert)
    for source, suffix in ((key, ".key"), (cert, ".crt")):
        dest = target / (name + suffix)
        shutil.copyfile(source, dest)
        # Only the container gets its assigned subdirectory. The host parent is 0700.
        dest.chmod(0o444)


def prepare(root, image):
    project = "arch002-" + secrets.token_hex(5)
    (root / "project").write_text(project)
    digest = run("docker", "image", "inspect", "--format", "{{.Descriptor.Digest}}", image).stdout.strip()
    ref = image.split("@")[0].rsplit(":", 1)[0] + "@" + digest
    assert run("docker", "image", "inspect", "--format", "{{.Descriptor.Digest}}", ref).stdout.strip() == digest
    client = root / "profiles"
    client.mkdir()
    authority = ca(root, "server-authority")
    shutil.copyfile(authority[1], client / "servers.pem")
    save_env(root, "central", PG_ADMIN=secret(), DJANGO_KEY=secret(), STUDIO_DB_PASSWORD=secret(), PROFILE_DIR=client)
    profiles = {}
    for site in SITES:
        directory = root / ("tls-" + site)
        directory.mkdir()
        host = "api-" + site
        issue(root, "server-" + site, authority, "serverAuth", directory, host)
        for suffix in (".crt", ".key"):
            (directory / ("server-" + site + suffix)).rename(directory / ("server" + suffix))
        for version in ("first", "next"):
            issuer = ca(root, "issuer-" + site + "-" + version)
            issue(root, site + "-" + version, issuer, "clientAuth", client)
        shutil.copyfile(root / ("issuer-" + site + "-first.pem"), directory / "readers.pem")
        site_id, instance_id = str(uuid4()), str(uuid4())
        marker = "Atelier ARCH-002 " + site.upper()
        save_env(root, site, SITE_DB="site_" + site, SITE_ROLE="app_" + site,
                 SITE_PASSWORD=secret(), PG_ADMIN=secret(), SITE_ID=site_id,
                 INSTANCE_ID=instance_id, IMAGE_DIGEST=digest, ENGINE_IMAGE=ref, DJANGO_KEY=secret(),
                 TLS_DIR=directory, MARKER=marker, API_HOST=host, MGMT_NET=project+"-central_management_"+site)
        profiles[site] = dict(site_id=site_id, instance_id=instance_id, marker=marker, origin="https://"+host+":8443",
                              engine_version="1.0.0", image_digest=digest, ca="/run/studio/servers.pem",
                              cert="/run/studio/"+site+"-first.crt", key="/run/studio/"+site+"-first.key")
    (client / "profiles.json").write_text(json.dumps(profiles))
    return profiles


def manage(root, site, *args, **kwargs):
    service = "studio" if site == "central" else "engine"
    return compose(root, site, "exec", "-T", service, "python", "manage.py", *args, **kwargs)


def runtime(root, site, service):
    cid = compose(root, site, "ps", "-q", service).stdout.strip()
    result = run("docker", "inspect", "--format",
                 "{{.Image}} {{range $key, $val := .NetworkSettings.Networks}}{{$key}} {{end}}", cid).stdout.split()
    return cid, result[0], set(result[1:])


def snapshot(root, sites):
    cids = [runtime(root, site, svc)[0] for site in sites for svc in ("engine", "db", "gateway")]
    stats = run("docker", "stats", "--no-stream", "--format", "{{json .}}", *cids)
    return [{key: row[key] for key in ("Name", "CPUPerc", "MemUsage", "BlockIO")}
            for row in map(json.loads, stats.stdout.splitlines())]


def enroll(root, profiles):
    script = """
from django.contrib.auth.models import User,Group
from registre.models import Client,Site,SiteGrant
from workspace.access import OPERATOR_GROUP
u=User.objects.create_user(username='demo')
u.groups.add(Group.objects.create(name=OPERATOR_GROUP))
client=Client.objects.create(display_name='Atelier fictif',client_type='COMPANY')
"""
    for site in SITES:
        script += f"s=Site.objects.create(id='{profiles[site]['site_id']}',name='Site {site}',client=client)\n"
        script += "SiteGrant.objects.create(user=u,site=s,level='manage')\n"
    manage(root, "central", "shell", "-c", script)


def verify(root, profiles, site, expected=True, reason=None):
    result = manage(root, "central", "raccordement", "verifier", "demo", profiles[site]["site_id"],
                    site, check=False)
    assert (result.returncode == 0) == expected, (site, result.stdout[-300:], result.stderr[-350:])
    if reason:
        assert reason in (result.stdout + result.stderr), (site, result.stderr[-350:])
    return result.stdout.strip().splitlines()[-1] if expected else result.stderr.strip().splitlines()[-1]


def set_profile(root, profiles):
    target = root / "profiles/profiles.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(profiles))
    temporary.replace(target)


def check_failures(root, profiles):
    result = {}
    status_args = ["raccordement", "etat", "demo", profiles["a"]["site_id"]]
    confirmed = json.loads(manage(root, "central", *status_args).stdout)["confirmed"]
    for name, overrides, code in (
        ("identité croisée", {field: profiles["b"][field] for field in ("origin", "cert", "key")}, "identity"),
        ("version incompatible", {"engine_version": "99.0.0"}, "incompatible"),
        ("marqueur voisin", {"marker": profiles["b"]["marker"]}, "render"),
        ("certificat voisin", {"cert": profiles["b"]["cert"], "key": profiles["b"]["key"]}, "authentication"),
    ):
        set_profile(root, {**profiles, "a": {**profiles["a"], **overrides}})
        result[name] = verify(root, profiles, "a", False, code)
        state = json.loads(manage(root, "central", *status_args).stdout)
        assert state["confirmed"] == confirmed and state["status"] == code
    set_profile(root, profiles)
    verify(root, profiles, "a")
    return result


def rotate(root, profiles):
    path = root / "tls-a/readers.pem"
    first = (root / "issuer-a-first.pem").read_bytes()
    new = (root / "issuer-a-next.pem").read_bytes()

    def reload_ca(bundle):
        path.write_bytes(bundle)
        compose(root, "a", "exec", "-T", "gateway", "nginx", "-s", "reload")
        # Wait for nginx's new worker generation to begin serving.
        time.sleep(1)

    reload_ca(first + new)
    rotated = {**profiles, "a": {**profiles["a"], "cert": "/run/studio/a-next.crt", "key": "/run/studio/a-next.key"}}
    set_profile(root, rotated)
    verify(root, profiles, "a")
    reload_ca(new)
    set_profile(root, profiles)
    denied = verify(root, profiles, "a", False, "authentication")
    set_profile(root, rotated)
    verify(root, profiles, "a")
    verify(root, profiles, "b")
    return denied


def isolation(root, profiles):
    """Prove separation using same media path and distinct Wagtail editor sessions."""
    tokens = {}
    for site in SITES:
        code = f"""
from django.conf import settings
from django.contrib.auth.models import User,Group
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import connection
from reference.models import ReferencePage
assert list(ReferencePage.objects.values_list('marker',flat=True)) == [settings.ENGINE_MARKER]
u=User.objects.create_user('editor_{site}')
u.groups.add(Group.objects.get(name='Editors'))
assert u.has_perm('wagtailadmin.access_admin')
assert default_storage.save('same.txt',ContentFile(b'{site}'))=='same.txt'
session=SessionStore()
session['editor']=u.username
session.save()
with connection.cursor() as c:
    c.execute("SELECT current_database(), current_user")
    assert c.fetchone()==('site_{site}','app_{site}')
print(session.session_key)
"""
        tokens[site] = manage(root, site, "shell", "-c", code).stdout.strip().splitlines()[-1]
    for site, other in (("a", "b"), ("b", "a")):
        code = f"""
from django.core.files.storage import default_storage
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
assert not User.objects.filter(username='editor_{other}').exists()
assert not Session.objects.filter(session_key='{tokens[other]}').exists()
assert default_storage.open('same.txt','rb').read()==b'{site}'
"""
        manage(root, site, "shell", "-c", code)

    central = runtime(root, "central", "studio")[2]
    left, right = runtime(root, "a", "engine"), runtime(root, "b", "engine")
    assert left[1] == right[1]
    assert left[2].isdisjoint(right[2])
    for site in SITES:
        db = runtime(root, site, "db")
        assert central.isdisjoint(db[2])
        assert central.isdisjoint(runtime(root,site,"engine")[2])
        assert len(central & runtime(root, site, "gateway")[2]) == 1
        ref = run("docker", "inspect", "--format", "{{.Config.Image}}", runtime(root, site, "engine")[0]).stdout.strip()
        assert ref.endswith("@" + profiles[site]["image_digest"])
        effective = run("docker", "image", "inspect", "--format", "{{.Id}}", ref).stdout.strip()
        assert effective == left[1]
    return {"image_config_digest": left[1], "image_manifest_digest": profiles["a"]["image_digest"],
            "checks": ["Bases et rôles distincts", "Contenu et médias homonymes distincts",
                       "Éditeurs Wagtail et sessions isolés", "Réseaux de données privés"]}


def restore(root, site):
    """Restore the reference database and media on isolated, quiescent fixtures."""
    # This fixture has no editor traffic. Stop its only app to keep the copies consistent.
    compose(root, site, "stop", "engine")
    db_name = "site_" + site
    role = "app_" + site
    compose(root, site, "exec", "-T", "db", "pg_dump", "-U", "postgres", "-d", db_name,
            "-Fc", "-f", "/tmp/reference.dump")
    compose(root, site, "exec", "-T", "db", "createdb", "-U", "postgres", "-O", role, "restore_fixture")
    compose(root, site, "exec", "-T", "db", "pg_restore", "--exit-on-error", "-U", "postgres",
            "-d", "restore_fixture", "/tmp/reference.dump")
    restored = compose(root, site, "exec", "-T", "db", "psql", "-At", "-U", "postgres",
                       "-d", "restore_fixture", "-c", "SELECT marker FROM reference_referencepage").stdout.strip()
    assert restored == "Atelier ARCH-002 " + site.upper()
    # A one-shot utility container has the same media mount and no web listener.
    compose(root,site,"run","--rm","--no-deps","-T","engine","python","-c",
            "import tempfile,shutil; from pathlib import Path; "
            "p=Path(tempfile.mkdtemp()); archive=shutil.make_archive(str(p/'media'),'tar','/app/media'); "
            "shutil.unpack_archive(archive,p/'restore'); assert (p/'restore/same.txt').read_bytes()==b'a'")
    compose(root, site, "up", "-d", "--wait", "engine")
    compose(root, site, "exec", "-T", "gateway", "nginx", "-s", "reload")


def qualify(root, profiles):
    report = {"observed_at": datetime.now(timezone.utc).isoformat(),
              "confirmed": {s: json.loads(verify(root, profiles, s)) for s in SITES}}
    # Exercise the exposed gateway with the runtime service credential and its
    # ordinary allow-listed paths. Writes are rejected before reaching Wagtail.
    check_gateway = """
import http.client,ssl,time,json
from raccordement.profiles import load_profile
p=load_profile("a")
tls=ssl.create_default_context(cafile=p.ca)
tls.load_cert_chain(p.cert,p.key)
def request(method,path,expected):
    conn=http.client.HTTPSConnection("api-a",8443,context=tls,timeout=2)
    conn.request(method,path)
    res=conn.getresponse()
    assert res.status==expected, res.status
    res.read()
    conn.close()
request("POST","/internal/identity",405)
request("GET","/admin/",404)
start=time.monotonic()
for n in range(5):
    request("GET","/internal/render",200)
print(json.dumps({"render_mean_ms":round((time.monotonic()-start)*200,1),
                  "samples":5,"write_status":405,"outside_contract":404}))
"""
    report["gateway"] = json.loads(manage(root,"central","shell","-c",check_gateway).stdout.splitlines()[-1])
    report["isolation"] = isolation(root, profiles)
    report["refusals"] = check_failures(root, profiles)
    report["rotation_old_certificate"] = rotate(root, profiles)
    compose(root, "a", "stop", "db")
    report["unavailable_a"] = verify(root, profiles, "a", False, "unavailable")
    report["b_during_a_outage"] = json.loads(verify(root, profiles,"b"))["status"]
    compose(root, "a", "up", "-d", "--wait", "db")
    verify(root, profiles,"a")
    compose(root, "a", "stop", "gateway")
    report["unreachable_a"] = verify(root, profiles, "a", False, "communication")
    compose(root, "a", "up", "-d", "--wait", "gateway")
    restore(root, "a")
    verify(root, profiles,"a")
    report["restore"] = "Contenu publié et média restaurés et comparés sur une copie isolée."
    for site in SITES:
        manage(root,site,"migrate","--check")
        footprint = compose(root,site,"exec","-T","db","psql","-At","-U","postgres","-d","site_"+site,
                            "-c","SELECT pg_database_size(current_database())").stdout.strip()
        report[site] = {"startup_seconds":round(float((root/(site+"-duration")).read_text()),2),
                        "database_bytes":int(footprint),"stats":json.loads((root/(site+"-snapshot")).read_text())}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="studio-arch002-engine:qa", help="Image locale déjà construite")
    parser.add_argument("--output", type=Path, required=True, help="Fichier JSON des observations")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="studio-arch002-") as scratch:
        root = Path(scratch)
        profiles = prepare(root, args.image)
        try:
            compose(root,"central","up","-d","--build","--wait")
            for i, site in enumerate(SITES):
                start=time.monotonic()
                compose(root,site,"up","-d","--wait")
                (root/(site+"-duration")).write_text(str(time.monotonic()-start))
                (root/(site+"-snapshot")).write_text(json.dumps(snapshot(root,SITES[:i+1])))
            enroll(root, profiles)
            report = qualify(root,profiles)
            args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
        finally:
            for site in ("b","a","central"):
                compose(root,site,"down","--volumes",check=False)


if __name__ == "__main__":
    main()
