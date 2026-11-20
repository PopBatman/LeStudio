import json
import os
from pathlib import Path
import tempfile
from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

from depots import figma


def layer(node_id, name, kind, **data):
    return dict(id=node_id, name=name, type=kind, **data)


class ReaderTests(TestCase):
    def setUp(self):
        self.profile = figma.Profile("FileA", "2:1", "g1", "fictif", {})
        self.frame = layer("2:1", "Accueil", "FRAME", children=[
            layer("2:2", "Titre", "TEXT", characters="Nos ateliers", style={"fontFamily":"DM Sans","fontSize":32},
                  fills=[{"type":"SOLID","color":{"r":1,"g":0,"b":0}}]),
            layer("2:3", "Affiche", "RECTANGLE", fills=[{"type":"IMAGE","imageRef":"fictif"}]),
        ])
        self.nodes = {"version":"v5","nodes":{"2:1":{"document":self.frame,"components":{}},
                    "8:8":{"document":layer("8:8","Autre client","FRAME")}}}

    def test_pinned_selection_ignores_unrelated_nodes_and_returns_tokens(self):
        with patch.object(figma, "_get", create=True, return_value=self.nodes) as get:
            inv = figma.inventory(self.profile)
            self.assertEqual([f["id"] for f in inv["frames"]], ["2:1"])
            read = figma.inspect_frames(self.profile, inv["version"], ["2:1"])
        frame, = read["frames"]
        heading, image = frame["nodes"]
        self.assertEqual(heading["tokens"], {"font":"dm-sans", "ink":"#FF0000"})
        self.assertEqual(heading["text"], "Nos ateliers")
        self.assertTrue(image["image"])
        self.assertNotIn("Autre client", str(read))
        self.assertEqual(get.call_args.args[-1]["version"], "v5")

    def test_null_selection_unavailable_and_stale(self):
        with patch.object(figma, "_get", return_value=self.nodes):
            with self.assertRaises(figma.FigmaError) as err:
                figma.inspect_frames(self.profile,"v4",["2:1"])
            self.assertEqual(err.exception.code, "changed")
            with self.assertRaises(figma.FigmaError):
                figma.inspect_frames(self.profile,"v5",["8:8"])
        with patch.object(figma, "_get", return_value={"version":"v5","nodes":{"2:1":None}}):
            with self.assertRaises(figma.FigmaError):
                figma.inventory(self.profile)

    def test_site_file_token_rotation_and_safe_diagnostics(self):
        site = str(uuid4())
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            secret, config = tmp/"secret", tmp/"config"
            secret.write_text("fictif-ancien")
            config.write_text(json.dumps({site:{"files":["FileA"],"token_file":str(secret),"generation":"1"}}))
            with patch.dict(os.environ, STUDIO_FIGMA_PROFILES=str(config)):
                url = "https://www.figma.com/design/FileA?node-id=2-1"
                profile = figma.load_profile(site,url)
                self.assertEqual((profile.file_key,profile.node_id),("FileA","2:1"))
                self.assertNotIn("fictif", repr(profile))
                secret.write_text("fictif-nouveau")
                self.assertNotEqual(profile.generation, figma.load_profile(site,url).generation)
                for owner, document in [(uuid4(),url),(site,url.replace("FileA","Other"))]:
                    with self.assertRaises(figma.FigmaError) as err:
                        figma.load_profile(owner,document)
                    self.assertNotIn("Other", str(err.exception))

    def test_whole_file_and_selected_instance_mapping(self):
        target = {"scope":"site","key":"entete","version":3}
        self.profile = figma.Profile("FileA", None, "g2", "fictif", {"Known": target})
        frames = [self.frame, layer("3:1","Collection","FRAME"),layer("4:1","Coordonnées","FRAME")]
        overview = {"version":"v6","document":layer("0:0","Fichier","DOCUMENT",
                    children=[layer("0:1","Écrans","CANVAS",children=frames)])}
        instance = layer("I2:1;3:4","Entête","INSTANCE", componentId="12:1",
                         componentProperties={"Contraste":{"type":"VARIANT","value":"Clair"}},
                         absoluteBoundingBox={"width":1560,"height":100},layoutMode="HORIZONTAL",itemSpacing=24)
        frames[0]["children"] = [instance,layer("2:8","Masqué","TEXT",visible=False)]
        def reader(profile, budget, route, params):
            if route == "":
                return overview
            wanted = params["ids"].split(",")
            return {"version":"v6","nodes":{p["id"]:{"document":p, "components":{"12:1":{"key":"Known"}}}
                                          for p in frames if p["id"] in wanted}}
        with patch.object(figma,"_get",side_effect=reader) as calls:
            obs = figma.inspect_frames(self.profile,"v6",[f["id"] for f in frames])
        self.assertEqual(calls.call_count,3)
        self.assertEqual(obs["frames"][0]["page"],"Écrans")
        node, = obs["frames"][0]["nodes"]
        self.assertEqual(node["mapping"], target)
        self.assertEqual((node["variant"],node["tokens"],node["width"]), ({"Contraste":"Clair"},{"gap":24},1560))
        self.assertTrue(obs["frames"][0]["gaps"])

    def test_transport_bounds_quota_and_redirect_refusal(self):
        from unittest.mock import Mock
        for status, headers, data, code, delay in [
            (429,{"Retry-After":"134"},b"","limited",134),
            (429,{},b"","limited",60),
            (302,{"Location":"https://fictif.invalid/example"},b"","incomplete",None),
            (403,{},b"","inaccessible",None), (404,{},b"","inaccessible",None),
            (200,{"Content-Type":"application/json","Content-Length":"8200"},b"","incomplete",None),
            (200,{"Content-Type":"application/json"},b"x"*1025,"incomplete",None),
            (200,{"Content-Type":"application/json","Content-Length":"20"},b"{}","incomplete",None),
        ]:
            with self.subTest(status=status,headers=headers),patch.object(figma.http.client,"HTTPSConnection") as open_conn:
                response = Mock(status=status)
                response.getheader.side_effect = headers.get
                response.read.return_value = data
                connection = open_conn.return_value
                connection.getresponse.return_value = response
                with self.assertRaises(figma.FigmaError) as err:
                    figma._get(self.profile,figma._Budget(remaining=1024),"/nodes",{"ids":"2:1"})
                self.assertEqual((err.exception.code, err.exception.retry_after),(code,delay))
                self.assertEqual(open_conn.call_args.args[0],"api.figma.com")
                connection.request.assert_called_once()
                connection.close.assert_called_once()
                self.assertNotIn("fictif",str(err.exception))

    def test_node_and_depth_limits_are_actionable(self):
        with patch.object(figma, "_get", return_value=self.nodes):
            for ids in ([],["2:1"]*9,["2:1","2:1"]):
                with self.assertRaises(figma.FigmaError) as err:
                    figma.inspect_frames(self.profile,"v5",ids)
                self.assertEqual(err.exception.code,"incomplete")
            node = self.frame
            for i in range(35):
                child = layer(f"2:{i+6}","Groupe","GROUP")
                node["children"]=[child]
                node=child
            with self.assertRaises(figma.FigmaError) as err:
                figma.inspect_frames(self.profile,"v5",["2:1"])
            self.assertEqual(err.exception.code,"incomplete")
