# Changelog

## 1.1.0 — 18 novembre 2026

- Sépare les instructions et outils dans `workflow-ai/` du projet Django/Wagtail dans `studio/`.
- Le suivi des lots utilise `studio/work/items/`. L’installation reproduit les deux dossiers côte à côte.

## 1.0.0 — 18 novembre 2026

- Consolide le périmètre autour du Studio central et du serveur unique avec services dockerisés.
- Intègre les contrats de feature, connecteur et composant UX/UI dans les processus de travail.
- Ajoute un installateur avec simulation, manifeste d’intégrité, préservation des instructions racine et refus des conflits.
- Fournit une CLI pour créer les lots et contrôler leurs documents, mandats déclarés et preuves.
- Prépare ARCH-001, sans implémenter le produit et sans reprendre Contact comme premier lot approuvé.
- Conserve les règles et le catalogue source, avec leurs clarifications de session.
- Raccorde la documentation à Notion ; fournit une projection REST distincte et un fragment CI GitLab.
- Explicite les capacités livrées, les intégrations à configurer et les limites des contrôles locaux.

Les anciennes archives restent des éléments d’historique ; leurs tests de prototype ne valent pas validation de l’architecture présente.
