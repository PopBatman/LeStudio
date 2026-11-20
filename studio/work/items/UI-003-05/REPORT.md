# UI-003-05 · Bascule du Visual Builder

- **Version et cible** — Image Studio `f7e13c3a559f`, déployée sur Studio local en mode `builder` le 20 novembre 2026.
- **Résultat vérifié** — Sur Tennis AI, **Reprendre le brouillon** ouvre la V2. Les deux routes V1 restent accessibles et les 17 révisions ont conservé leur empreinte. [Contrôle de bascule](evidence/bascule-locale.json)
- **Preuves** — 249 tests PostgreSQL réussis. Sur SQLite, 233 réussites et 16 cas ignorés. Le banc a permis de rouvrir en V1 une révision enregistrée en V2. [Index des preuves](EVIDENCE.md) · [Essai de retour arrière](evidence/retour-image.json)
- **Point ouvert** — Maintenir le repli V1 jusqu’au bilan de la première séance d’édition. [Procédure de reprise](ARCHITECTURE.md#configuration-réalisée-et-reprise-en-exploitation)
- **Décisions et suivi** — [Carte UI-003-05 dans le Kanban Studio](https://www.notion.so/41d49e23bbdb811e9acbd8b4162d3954)
