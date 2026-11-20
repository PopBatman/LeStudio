"""Projection des observations centrales pour la fiche Site."""
import re
from datetime import datetime
from zoneinfo import ZoneInfo


PARIS = ZoneInfo("Europe/Paris")
MOTIFS_ECHEC = {
    "communication": "Échec de communication",
    "timeout": "Délai de réponse dépassé",
    "authentication": "Authentification refusée",
    "unavailable": "Moteur indisponible lors de la tentative",
    "incompatible": "Version incompatible",
    "identity": "Identité non conforme",
    "identity_mismatch": "Identité non conforme",
    "association_conflict": "Association non conforme",
    "render": "Rendu de référence non conforme",
    "invalid_profile": "Profil de raccordement invalide",
    "profile_changed": "Profil de raccordement modifié",
}
ETATS = {
    "unlinked": ("Non raccordé", "neutral", "Aucune tentative enregistrée"),
    "connected": ("Raccordement confirmé", "success", "Réussie"),
    "checking": ("Vérification en cours", "neutral", "En cours"),
    "attempt_expired": ("Dernière vérification expirée", "warning", "Délai de la tentative écoulé"),
}
INDETERMINE = ("Résultat indéterminé", "neutral", "Résultat indisponible")


def _validated(value, pattern):
    if isinstance(value, str) and re.fullmatch(pattern, value, re.ASCII):
        return value
    return "Non renseigné"


def _version(value):
    # Accepte les numéros publiés et les suffixes usuels de préversion.
    return _validated(value, r"[0-9]{1,8}(?:\.[0-9]{1,8}){0,4}(?:(?:a|b|rc|\.post|\.dev)[0-9]{1,6})?")


def _paris(stamp):
    return datetime.fromisoformat(stamp).astimezone(PARIS) if stamp else None


def connection_panel(snapshot, site_id, manage):
    confirmed = snapshot["confirmed"] or {}
    attempt = snapshot["attempt"] or {}
    code = snapshot["status"]
    state = ETATS.get(code, INDETERMINE)
    if code in MOTIFS_ECHEC:
        state = ("Dernière vérification en échec", "warning", MOTIFS_ECHEC[code])
    elif code == "connected" and not confirmed.get("at"):
        state = INDETERMINE

    details = []
    if confirmed:
        major, minor = confirmed.get("contract_major"), confirmed.get("contract_minor")
        contract = "Non renseigné"
        if all(type(part) is int and 0 <= part <= 2147483647 for part in (major, minor)):
            contract = f"{major}.{minor}"
        details.extend([
            ("Version Wagtail", _version(confirmed.get("wagtail_version"))),
            ("Version du moteur", _version(confirmed.get("engine_version"))),
            ("Version du contrat API", contract),
        ])
    if manage:
        details.append(("Identifiant de la fiche Site", str(site_id)))
        if confirmed:
            details.extend([
                ("Instance Wagtail confirmée", confirmed.get("instance_id") or "Non renseigné"),
                ("Profil confirmé", _validated(confirmed.get("profile"), r"[A-Za-z0-9_.-]{1,80}")),
            ])
        if code in MOTIFS_ECHEC or code == "attempt_expired":
            details.append(("Code de diagnostic", code))

    status, variant, outcome = state
    return {
        "status": status, "variant": variant, "outcome": outcome,
        "confirmed_at": _paris(confirmed.get("at")),
        "attempt_at": _paris(attempt.get("finished_at") or attempt.get("started_at")),
        "finished": bool(attempt.get("finished_at")), "details": details,
    }
