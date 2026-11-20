from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404

from composition import catalogue
from composition.models import ComponentVersion, Promotion
from registre.models import Client, Site, SiteGrant
from tests.catalogue_fixture import CatalogueTestCase
from workspace.access import OPERATOR_GROUP


class CatalogueTests(CatalogueTestCase):
    def setUp(self):
        client = Client.objects.create(display_name="Ateliers", client_type="COMPANY")
        self.site = Site.objects.create(client=client, name="Premier")
        self.other = Site.objects.create(client=client, name="Second")
        group = Group.objects.create(name=OPERATOR_GROUP)
        self.author = User.objects.create_user("auteur")
        self.reviewer = User.objects.create_user("reviseur")
        for user in (self.author, self.reviewer):
            user.groups.add(group)
            SiteGrant.objects.create(site=self.site, user=user, level="manage")
        self.reviewers = Group.objects.create(name=catalogue.REVIEW_GROUP)
        self.reviewer.groups.add(self.reviewers)
        self.local = catalogue.installer_version(self.site, "signature", 1, "Encart", "signature")
        self.proposal = dict(key="encart-public", label="Encart partagé", rights="Dossier de cession 12", reason="Réemploi du dessin générique")

    def propose(self):
        return catalogue.proposer(self.author, self.site.pk, self.local.pk, **self.proposal)

    def review(self, request, actor=None, **options):
        fields = dict(fingerprint=request.fingerprint, approve=True, note="Pièce 12 et manifeste vérifiés",
                      rights_checked=True, technical_checked=True)
        fields.update(options)
        return catalogue.examiner(actor or self.reviewer, self.site.pk, request.pk, **fields)

    def test_catalogue_scope_version_media_and_revocation(self):
        self.assertSetEqual(set(ComponentVersion.objects.filter(site=None).values_list("key", flat=True)),
                            {"heading", "text", "container", "image", "button", "article"})
        with self.assertRaises(Http404):
            catalogue.bibliotheque(self.author, self.other.pk)
        self.assertIsNone(catalogue.definition(self.other.pk, "site", "signature", 1))
        catalogue.installer_version(self.other, "signature", 1, "Autre encart", "text")
        self.assertEqual(catalogue.definition(self.other.pk, "site", "signature", 1)["renderer"], "text")
        with self.assertRaises(ValidationError):
            catalogue.installer_version(self.other, "signature", 1, "Altéré", "signature")
        media = catalogue.attribuer_media(self.site)
        self.assertTrue(catalogue.reference(self.site.pk, "media", str(media.pk)))
        self.assertFalse(catalogue.reference(self.other.pk, "media", str(media.pk)))
        self.assertTrue(catalogue.media_png(self.author, self.site.pk, media.pk).startswith(b"\x89PNG"))
        catalogue.attribuer_media(self.site, actif=False)
        with self.assertRaises(Http404):
            catalogue.media_png(self.author, self.site.pk, media.pk)

    def test_separate_review_and_idempotent_publication(self):
        proposal = self.propose()
        self.author.groups.add(self.reviewers)
        with self.assertRaises(PermissionDenied):
            self.review(proposal, self.author)
        with self.assertRaises(ValidationError):
            self.review(proposal, rights_checked=False)
        self.assertIsNone(catalogue.definition(self.other.pk, "global", "encart-public", 1))
        accepted = self.review(proposal)
        self.assertEqual(self.review(proposal).result_id, accepted.result_id)
        published = catalogue.definition(self.other.pk, "global", "encart-public", 1)
        self.assertEqual(published["origin"], "promotion_revue")
        self.assertNotIn("rights", published)
        self.assertNotIn("source", published)
        self.assertTrue(ComponentVersion.objects.filter(pk=self.local.pk, site=self.site).exists())

    def test_changed_evidence_and_revoked_grant(self):
        request = self.propose()
        Promotion.objects.filter(pk=request.pk).update(rights="Autre preuve")
        with self.assertRaises(ValidationError):
            self.review(request)
        SiteGrant.objects.filter(user=self.reviewer).delete()
        with self.assertRaises(Http404):
            self.review(request)
        self.assertFalse(ComponentVersion.objects.filter(site=None, key=request.key).exists())

    def test_refusal_and_second_version_keep_old_definition(self):
        first = self.propose()
        self.assertEqual(self.review(first, approve=False).state, "rejected")
        self.assertIsNone(catalogue.definition(self.site.pk, "global", "encart-public", 1))
        accepted = self.review(self.propose())
        old = catalogue.definition(self.site.pk, "global", "encart-public", 1)
        second = catalogue.installer_version(self.site, "signature", 2, "Nouvel encart", "signature")
        newer = catalogue.proposer(self.author, self.site.pk, second.pk, **self.proposal)
        self.assertEqual(newer.version, 2)
        self.assertNotEqual(self.review(newer).result_id, accepted.result_id)
        self.assertEqual(catalogue.definition(self.site.pk, "global", "encart-public", 1), old)
