from uuid import uuid4
from django.core.exceptions import ValidationError

from composition.figma_mapping import propose, project
from composition.catalogue import installer_version
from tests.catalogue_fixture import CatalogueTestCase


class FigmaMappingTests(CatalogueTestCase):
    def setUp(self):
        self.site = uuid4()
        self.frame = {"id": "1:1", "name": "Accueil", "nodes": [
            {"id": "1:2", "parent_id": "1:1", "type": "TEXT", "name": "Titre", "text": "Nos ateliers",
             "font_size": 40, "tokens": {"ink": "#223344"}},
            {"id": "1:3", "parent_id": "1:1", "type": "VECTOR", "name": "Marque"},
        ]}
        self.obs = {"frames": [self.frame]}
        self.dest = [dict(frame_id="1:1", group="accueil", base=True, home=True, title="Accueil", slug="", format="mobile")]

    def test_no_implicit_decisions_unknown_component_and_canonical_document(self):
        rows = propose(self.site, self.obs)
        decisions = {row["id"]: {"action": "accept"} for row in rows}
        with self.assertRaises(ValidationError):
            project(self.site,self.obs,rows,decisions,self.dest,None)
        decisions["1:3"] = {"action": "exclude"}
        doc, trace = project(self.site,self.obs,rows,decisions,self.dest,None)
        page = doc["pages"][0]
        title = page["sections"][0]["blocks"][0]["children"][0]
        self.assertEqual((page["slug"], title["props"], title["appearance"]["tokens"]),
                         ("", {"text":"Nos ateliers","level":2}, {"ink":"#223344"}))
        self.assertEqual(trace["1:2"],title["id"])
        self.assertEqual(trace["1:1"],page["id"])
        self.assertNotIn("1:3",trace)
        self.assertEqual(doc["schema_version"],4)

    def test_catalogue_ambiguity_requires_explicit_choice(self):
        installer_version(None,"autre-titre",1,"Autre titre","heading")
        proposals=propose(self.site,self.obs)
        title=next(row for row in proposals if row["id"]=="1:2")
        self.assertFalse(title["suggested"])
        self.assertGreaterEqual(len(title["candidates"]),2)

    def test_alternate_format_does_not_manufacture_duplicates(self):
        alternate={"id":"2:1","name":"Mobile","gap":12,"nodes":[
            {"id":"2:2","parent_id":"2:1","type":"TEXT","name":"Titre","text":"Nos ateliers",
             "font_size":40,"tokens":{"ink":"#223344"}}]}
        obs={"frames":[self.frame,alternate]}
        rows=propose(self.site,obs)
        decisions={r["id"]:{"action":"exclude" if r["id"]=="1:3" else "accept"} for r in rows}
        dest=[dict(self.dest[0],format="desktop"),dict(self.dest[0],frame_id="2:1",base=False,format="mobile",home=False)]
        doc,trace=project(self.site,obs,rows,decisions,dest,None)
        self.assertEqual(len(doc["pages"]),1)
        self.assertEqual(trace["1:2"],trace["2:2"])
        box=doc["pages"][0]["sections"][0]["blocks"][0]
        self.assertEqual(box["props"]["layout"]["mobile"]["gap"],12)

    def test_layout_respects_excluded_or_adjusted_spacing(self):
        self.frame.update(gap=10,tokens={"gap":10})
        proposal=propose(self.site,self.obs)
        for tokens in ({},{"gap":24}):
            choices={r["id"]:{"action":"exclude" if r["type"]=="VECTOR" else "accept"} for r in proposal}
            choices["1:1"]["tokens"]=tokens
            doc,_=project(self.site,self.obs,proposal,choices,self.dest,None)
            block=doc["pages"][0]["sections"][0]["blocks"][0]
            self.assertEqual(block["props"]["layout"]["base"],tokens)
