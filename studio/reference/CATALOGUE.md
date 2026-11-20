> Référence source conservée. Les clarifications de session et conventions actuelles se trouvent dans [les décisions du projet](../project/DECISIONS.md). Le choix actuel est un seul serveur avec des services dockerisés ; les anciennes questions de topologie ne bloquent pas le travail sur Studio.

# Catalogue source — Studio / Workspace AI

Version documentaire : **0.1**. État : **inventaire à qualifier**. Source : **Texte collé(8).txt**, 609 lignes. Les numéros de ligne ci-dessous renvoient à cette source, avant toute reformulation.

## 1. Portée et règles de lecture

Ce document conserve toutes les entrées du catalogue fourni. Il recense des possibilités, des produits cités, des protocoles, des briques techniques et des pistes d’intégration. **Il ne décrit pas un catalogue de modules disponibles ou une feuille de route approuvée.**

| Repère ou champ | Signification |
| --- | --- |
| INV-FAM | Famille source ; repère documentaire créé pour cet inventaire. |
| INV-FON | Entrée fonctionnelle source ; ce n’est pas un identifiant de module validé. |
| INV-CON | Occurrence non vide d’un connecteur cité dans une famille ; une autre occurrence peut citer la même cible. |
| INV-VID | Emplacement de connecteur laissé vide ; exclu du nombre de connecteurs. |
| INV-UI / INV-EXT / INV-CLA | Inventaires annexes de composants UI, d’externalisation et de classification. |
| INV-EX | Fiche illustrative, distincte d’un module réel. |
| Statut commun | Chaque entrée d’inventaire reste à qualifier ; sa disponibilité n’est pas établie. |
| Normalisation proposée | Correction ou rapprochement proposé, à valider. Le libellé source reste conservé et aucune fusion n’est effectuée. |
| Priorité | Aucune priorité de développement attribuée. P0 apparaît uniquement comme valeur de l’exemple fourni. |

Le fichier `registres/catalogue.json` conserve également la ligne source intégrale, y compris ses espaces et sa ponctuation. Les tableaux ci-dessous conservent les libellés et descriptions d’origine ; leurs fautes éventuelles ne sont pas corrigées silencieusement. Une proposition de correction porte uniquement sur le libellé indiqué, pas sur l’ensemble de la description.

## 2. Quantités et méthode de comptage

Périmètre du catalogue détaillé : de « Sites et Contenus » (ligne 216) jusqu’avant « Structure d’une fiche métier d’un Register » (ligne 589). Chaque ligne `-->` non vide est comptée une fois comme entrée fonctionnelle ou occurrence de connecteur selon sa position dans la famille. Les deux lignes `-->` vides sont conservées séparément.

| Mesure | Quantité | Interprétation |
| --- | --- | --- |
| Familles | 15 | Familles conservées dans leur ordre source. |
| Entrées fonctionnelles | 166 | 166 descriptions textuelles distinctes ; ce ne sont pas 166 modules spécifiés. |
| Intitulés fonctionnels distincts | 163 | Notifications, Conversion et Evènements sont répétés ; le sens peut différer. |
| Occurrences non vides de connecteurs | 98 | Comptage des mentions dans les familles, avec leurs répétitions. |
| Libellés de connecteurs strictement distincts | 89 | Égalité textuelle, casse conservée, espaces de bord ignorés. |
| Libellés de connecteurs distincts sans tenir compte de la casse | 88 | API Rest / API REST constitue le rapprochement lexical supplémentaire. |
| Emplacements de connecteurs vides | 2 | Exclus des 98 occurrences. |
| Composants UI | 10 | Inventaire annexe distinct. |
| Entrées d’externalisation | 9 | Vue distincte qui chevauche le catalogue détaillé. |
| Entrées Core / Standard / Advanced | 9 | 4 Core, 3 Standard, 2 Advanced ; vue distincte et chevauchante. |
| Fiche illustrative | 1 | 17 champs ; MOD-COM-001 demeure strictement un exemple. |

Les nombres de libellés distincts résultent d’une comparaison de texte. Ils ne dénombrent pas des capacités métier indépendantes ni des intégrations prêtes à l’emploi. Les 9 entrées d’externalisation et les 9 entrées Core/Standard/Advanced ne sont pas ajoutées comme 18 modules supplémentaires. Les mentions Brevo, Mailgun et SMTP de la fiche illustrative sont exclues des 98 occurrences du catalogue.

| Famille source | Repère | Entrées fonctionnelles | Connecteurs non vides | Emplacements vides |
| --- | --- | --- | --- | --- |
| Sites et Contenus | INV-FAM-001 | 14 | 7 | 0 |
| Communication | INV-FAM-002 | 10 | 11 | 0 |
| Authentification et sécurité | INV-FAM-003 | 12 | 8 | 0 |
| Commerce et Paiement | INV-FAM-004 | 12 | 11 | 0 |
| Industrie et B2B | INV-FAM-005 | 12 | 9 | 0 |
| Documents et données | INV-FAM-006 | 11 | 8 | 0 |
| Intelligence Artificielle | INV-FAM-007 | 12 | 7 | 0 |
| Automatisation | INV-FAM-008 | 10 | 6 | 0 |
| CRM et relation client | INV-FAM-009 | 10 | 6 | 0 |
| Statistiques et Analytics | INV-FAM-010 | 10 | 7 | 0 |
| Réservation et activité locales | INV-FAM-011 | 10 | 5 | 0 |
| Localisation et présence locale | INV-FAM-012 | 8 | 5 | 0 |
| Applications métier | INV-FAM-013 | 11 | 0 | 1 |
| Conformité et Confidentialité | INV-FAM-014 | 9 | 0 | 1 |
| Exploitation et infrastructure | INV-FAM-015 | 15 | 8 | 0 |
| TOTAL |  | 166 | 98 | 2 |

## 3. Catalogue intégral par famille

### 3.1. Sites et Contenus

Repère **INV-FAM-001** ; titre source ligne **216**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-001 | 219 | Pages : Création et Administration de pages | — |
| INV-FON-002 | 220 | Blog : Articles, catégories, auteurs | — |
| INV-FON-003 | 221 | Actualités : Publications et annonces | — |
| INV-FON-004 | 222 | Portfolio : Présentation de réalisations | — |
| INV-FON-005 | 223 | Galerie : Images, Vidéos, Album | — |
| INV-FON-006 | 224 | Catalgue : Produits et Services | Catalogue — à valider |
| INV-FON-007 | 225 | Documentation : Pages techniques, guides, notices | — |
| INV-FON-008 | 226 | Multilingue : Traduction des contenus | — |
| INV-FON-009 | 227 | Recherche : Recherche interne | — |
| INV-FON-010 | 228 | FAQ : Questions fréquentes | — |
| INV-FON-011 | 229 | Témoignages : Avis clients | — |
| INV-FON-012 | 230 | SEO : Métadonnées, sitemap, redirections | — |
| INV-FON-013 | 231 | Médias : Bibliothèque de fichiers | — |
| INV-FON-014 | 232 | Landing Pages : Pages commerciales personnalisées | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-001 | 236 | Google Search Console | — |
| INV-CON-002 | 237 | Google Analytics | — |
| INV-CON-003 | 238 | Matomo | — |
| INV-CON-004 | 239 | Cloudinary | — |
| INV-CON-005 | 240 | DeepL | — |
| INV-CON-006 | 241 | Youtube | YouTube — à valider |
| INV-CON-007 | 242 | Vimeo | — |

### 3.2. Communication

Repère **INV-FAM-002** ; titre source ligne **245**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-015 | 248 | Formulaires : Constructeur de formulaires | — |
| INV-FON-016 | 249 | Contact : Réception et suivi des messages | — |
| INV-FON-017 | 250 | Newsletter : Collecte d'abonnées | — |
| INV-FON-018 | 251 | E-mail transactionnel : Messages automatiques | — |
| INV-FON-019 | 252 | Notifications : Email, SMS, Push | — |
| INV-FON-020 | 253 | Chat : Messagerie Client | — |
| INV-FON-021 | 254 | Support : Tickets et demandes | — |
| INV-FON-022 | 255 | Campagnes : Campagnes de communication | — |
| INV-FON-023 | 256 | SMS : Messages transactionnels | — |
| INV-FON-024 | 257 | Prise de rendez-vous : Calendrier et disponibilités | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-008 | 260 | Brevo | — |
| INV-CON-009 | 261 | Mailgun | — |
| INV-CON-010 | 262 | Resend | — |
| INV-CON-011 | 263 | SendGrid | — |
| INV-CON-012 | 264 | Amazon SES | — |
| INV-CON-013 | 265 | Twilio | — |
| INV-CON-014 | 266 | Calendly | — |
| INV-CON-015 | 267 | Google Calendar | — |
| INV-CON-016 | 268 | Microsoft Outlook | — |
| INV-CON-017 | 269 | Zendesk | — |
| INV-CON-018 | 270 | Intercom | — |

### 3.3. Authentification et sécurité

Repère **INV-FAM-003** ; titre source ligne **273**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-025 | 276 | Login/Register : Connexion et Inscription | — |
| INV-FON-026 | 277 | MFA : Authentification multifacteur | — |
| INV-FON-027 | 278 | SSO : Connexion via fournisseur d'identité | — |
| INV-FON-028 | 279 | RBAC : Gestion des roles et permissions | — |
| INV-FON-029 | 280 | Audit Log : Historique des actions | — |
| INV-FON-030 | 281 | Sessions : Gestions des sessions | — |
| INV-FON-031 | 282 | Invitations : Invitation d'utilsateurs | — |
| INV-FON-032 | 283 | API keys : Gestion de clés d'accès | — |
| INV-FON-033 | 284 | Consentement : Gestion des consentements | — |
| INV-FON-034 | 285 | CAPTCHA : Protection des formulaires | — |
| INV-FON-035 | 286 | Rate Limiting : Limitation de requetes | — |
| INV-FON-036 | 287 | Security Dashboard : Suivi des évènements de sécurité | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-019 | 290 | Microsft Entra ID | Microsoft Entra ID — à valider |
| INV-CON-020 | 291 | Google Identity | — |
| INV-CON-021 | 292 | KeyCloak | Keycloak — à valider |
| INV-CON-022 | 293 | Auth0 | — |
| INV-CON-023 | 294 | Okta | — |
| INV-CON-024 | 295 | LDAP | — |
| INV-CON-025 | 296 | Fournisseurs OIDC | — |
| INV-CON-026 | 297 | SAML | — |

### 3.4. Commerce et Paiement

Repère **INV-FAM-004** ; titre source ligne **300**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-037 | 303 | Catalogue e-commerce : Produits et variantes | — |
| INV-FON-038 | 304 | Panier : Gestion des achats | — |
| INV-FON-039 | 305 | Commandes : Suivi des commandes | — |
| INV-FON-040 | 306 | Paiements : Paiement en ligne | — |
| INV-FON-041 | 307 | Abonnements : Paiements récurrents | — |
| INV-FON-042 | 308 | Facturation : Factures et avoirs | — |
| INV-FON-043 | 309 | Devis : Création et validation de devis | — |
| INV-FON-044 | 310 | Promotions : Codes promotionnels | — |
| INV-FON-045 | 311 | Livraison : Expédition et suivi | — |
| INV-FON-046 | 312 | Stocks : Disponibilités des produits | — |
| INV-FON-047 | 313 | Réservations : Réservations de prestations | — |
| INV-FON-048 | 314 | Cartes cadeaux : Bons et cartes cadeaux | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-027 | 317 | Stripe | — |
| INV-CON-028 | 318 | Paypal | PayPal — à valider |
| INV-CON-029 | 319 | Mollie | — |
| INV-CON-030 | 320 | Shopify | — |
| INV-CON-031 | 321 | WooCommerce | — |
| INV-CON-032 | 322 | Prestashop | PrestaShop — à valider |
| INV-CON-033 | 323 | Odoo | — |
| INV-CON-034 | 324 | Pennylane | — |
| INV-CON-035 | 325 | Colissimo | — |
| INV-CON-036 | 326 | Chronopost | — |
| INV-CON-037 | 327 | Sendcloud | — |

### 3.5. Industrie et B2B

Repère **INV-FAM-005** ; titre source ligne **330**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-049 | 333 | Catalogue industriel : Machines, équipements, capacités | — |
| INV-FON-050 | 334 | Fiches techniques : Caractéristiques et documents | — |
| INV-FON-051 | 335 | Demande de devis : Formulaires B2B | — |
| INV-FON-052 | 336 | Upload de plans : PDF, DXF, STEP et autres formats autorisés | — |
| INV-FON-053 | 337 | Suivi des commandes :  Status et historique | — |
| INV-FON-054 | 338 | Espace distributeur : Accès pro | — |
| INV-FON-055 | 339 | Gestion documentaire : Documents techniques | — |
| INV-FON-056 | 340 | Certifications : ISO, Normes, Attestations | — |
| INV-FON-057 | 341 | SAV : Demandes d'interventions | — |
| INV-FON-058 | 342 | Gestion des équipements : Référentiel de machines | — |
| INV-FON-059 | 343 | Traçabilité : Historique des opérations | — |
| INV-FON-060 | 344 | Extranet : Portail clients et partenaires | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-038 | 347 | Odoo | — |
| INV-CON-039 | 348 | SAP | — |
| INV-CON-040 | 349 | Microsoft Dynamics 365 | — |
| INV-CON-041 | 350 | Sage | — |
| INV-CON-042 | 351 | Dolibarr | — |
| INV-CON-043 | 352 | ERP internes | — |
| INV-CON-044 | 353 | SFTp | SFTP — à valider |
| INV-CON-045 | 354 | API Rest | API REST — à valider |
| INV-CON-046 | 355 | SOAP | — |

### 3.6. Documents et données

Repère **INV-FAM-006** ; titre source ligne **358**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-061 | 361 | Import CSV : Import de données tabulaires | — |
| INV-FON-062 | 362 | Import Excel : Lecture et validation XLSX | — |
| INV-FON-063 | 363 | Import XML : Pasring et normalisation | — |
| INV-FON-064 | 364 | Import JSON : Import structuré | — |
| INV-FON-065 | 365 | Export PDF : Génération de documents | — |
| INV-FON-066 | 366 | Conversion : Transformation entre formats | — |
| INV-FON-067 | 367 | OCR : Extraction de texte | — |
| INV-FON-068 | 368 | Validation : Controles de confirmité | — |
| INV-FON-069 | 369 | Déduplication : Détection des doublons | — |
| INV-FON-070 | 370 | Synchronisation: Echanges de données | — |
| INV-FON-071 | 371 | Archivage : Conservation et historique | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-047 | 374 | Google drive | Google Drive — à valider |
| INV-CON-048 | 375 | OneDrive | — |
| INV-CON-049 | 376 | SharePoint | — |
| INV-CON-050 | 377 | Dropbox | — |
| INV-CON-051 | 378 | S3 | — |
| INV-CON-052 | 379 | Nextcloud | — |
| INV-CON-053 | 380 | SFTp | SFTP — à valider |
| INV-CON-054 | 381 | Azure Blob Storage | — |

### 3.7. Intelligence Artificielle

Repère **INV-FAM-007** ; titre source ligne **384**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-072 | 387 | Chatbot : Assistant conversationnel | — |
| INV-FON-073 | 388 | Recherche documentaire : Recherche sémantique | — |
| INV-FON-074 | 389 | RAG : Réponse fondées sur des documents | — |
| INV-FON-075 | 390 | Classification : Catégorisation automatique | — |
| INV-FON-076 | 391 | Extraction : Extraction structurée | — |
| INV-FON-077 | 392 | Résumé : Synthèse de documents | — |
| INV-FON-078 | 393 | Traduction : Traduction de contenus | — |
| INV-FON-079 | 394 | Génération de contenu : Assistance éditoriale | — |
| INV-FON-080 | 395 | Analyse documentaire : Traitements avancés | — |
| INV-FON-081 | 396 | Assistant métier : Agent spécialisé | — |
| INV-FON-082 | 397 | Modération : Controle des contenus | — |
| INV-FON-083 | 398 | Transcription | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-055 | 402 | OpenAI | — |
| INV-CON-056 | 403 | Anthropiuc | Anthropic — à valider |
| INV-CON-057 | 404 | Mistral AI | — |
| INV-CON-058 | 405 | Azure AI | — |
| INV-CON-059 | 406 | Ollama | — |
| INV-CON-060 | 407 | vLLM | — |
| INV-CON-061 | 408 | Hugging Face | — |

### 3.8. Automatisation

Repère **INV-FAM-008** ; titre source ligne **411**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-084 | 414 | Webhooks : Réception et émission d'évènements | — |
| INV-FON-085 | 415 | Worflows : Enchainements d'actions | Workflows — à valider |
| INV-FON-086 | 416 | Shcheduler : taches programmés | Scheduler — à valider |
| INV-FON-087 | 417 | Syncrhonisation : Synchronisation entre systèmes | Synchronisation — à valider |
| INV-FON-088 | 418 | Notifications évènementielles : Alertes sur les évènements | — |
| INV-FON-089 | 419 | Import automatique : Récupération périodique de données | — |
| INV-FON-090 | 420 | Export automatique : Transfert de fichiers | — |
| INV-FON-091 | 421 | Validation automatisée : Controles métier | — |
| INV-FON-092 | 422 | Approval : Circuits de validation | — |
| INV-FON-093 | 423 | Event log : Historique des évènements | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-062 | 426 | n8n | — |
| INV-CON-063 | 427 | Make | — |
| INV-CON-064 | 428 | Zapier | — |
| INV-CON-065 | 429 | API REST | — |
| INV-CON-066 | 430 | webhooks | — |
| INV-CON-067 | 431 | connecteurs dev en python | — |

### 3.9. CRM et relation client

Repère **INV-FAM-009** ; titre source ligne **434**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-094 | 437 | Contacts : Gestion des prospects | — |
| INV-FON-095 | 438 | CRM léger : Pipeline commercial | — |
| INV-FON-096 | 439 | Leads : Qualification des prospects | — |
| INV-FON-097 | 440 | Devis commerciaux : Proposition commerciales | — |
| INV-FON-098 | 441 | Suivi client : Historique des échanges | — |
| INV-FON-099 | 442 | Segmentation : Groupes de clients | — |
| INV-FON-100 | 443 | Relances : Suivi commercial | — |
| INV-FON-101 | 444 | Satisfaction : Enquete et retours | — |
| INV-FON-102 | 445 | Fidélité : Programmes de fidélisation | — |
| INV-FON-103 | 446 | Portail client : Accès aux informations | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-068 | 449 | HubSpot | — |
| INV-CON-069 | 450 | SalesForce | Salesforce — à valider |
| INV-CON-070 | 451 | PipeDrive | Pipedrive — à valider |
| INV-CON-071 | 452 | Zoho CRM | — |
| INV-CON-072 | 453 | Odoo | — |
| INV-CON-073 | 454 | MDynamics 365 | Microsoft Dynamics 365 — à valider |

### 3.10. Statistiques et Analytics

Repère **INV-FAM-010** ; titre source ligne **457**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-104 | 460 | Analytics : Mesure d'audience | — |
| INV-FON-105 | 461 | Evènements : Suivi des interactions | — |
| INV-FON-106 | 462 | Conversion : Suivi des objectifs | — |
| INV-FON-107 | 463 | Dashboard : tableau de board | — |
| INV-FON-108 | 464 | Rapports : Rapports périodiques | — |
| INV-FON-109 | 465 | Performance : Mesures techniques | — |
| INV-FON-110 | 466 | SEO Monitoring : Suivi du référencement | — |
| INV-FON-111 | 467 | Heatmaps : Analyse des interactions | — |
| INV-FON-112 | 468 | A/B testing : Expérimentations | — |
| INV-FON-113 | 469 | Business Intelligence : Indicateurs métier | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-074 | 472 | Matomo | — |
| INV-CON-075 | 473 | Plausible | — |
| INV-CON-076 | 474 | Google Analytics | — |
| INV-CON-077 | 475 | Search Console | Google Search Console — à valider |
| INV-CON-078 | 476 | Microsoft Clarity | — |
| INV-CON-079 | 477 | MEtabase | Metabase — à valider |
| INV-CON-080 | 478 | Grafana | — |

### 3.11. Réservation et activité locales

Repère **INV-FAM-011** ; titre source ligne **481**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-114 | 484 | Rendez-vous : Réservations | — |
| INV-FON-115 | 485 | Planning : Gestion des disponibilités | — |
| INV-FON-116 | 486 | Evènements : Calendrier d'évènements | — |
| INV-FON-117 | 487 | Billetterie : Vente de places | — |
| INV-FON-118 | 488 | Restaurant : Réservation de tables | — |
| INV-FON-119 | 489 | Prestations : Réservations de services | — |
| INV-FON-120 | 490 | Gestion des ressources : Salles, Equipement | — |
| INV-FON-121 | 491 | Annulations : Politique d'annulations | — |
| INV-FON-122 | 492 | Rappels : Rappels automatiques | — |
| INV-FON-123 | 493 | Paiement d'accompte : Paieement à la réservation | Paiement d'acompte — à valider |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-081 | 496 | Google Calendar | — |
| INV-CON-082 | 497 | Outlook Calendar | — |
| INV-CON-083 | 498 | Calendly | — |
| INV-CON-084 | 499 | Stripe | — |
| INV-CON-085 | 500 | Systèmes de résa spécialisés | — |

### 3.12. Localisation et présence locale

Repère **INV-FAM-012** ; titre source ligne **503**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-124 | 506 | Carte : Affichage géographique | — |
| INV-FON-125 | 507 | Points de vente : Localisation des établissements | — |
| INV-FON-126 | 508 | Itinéraire : Accès à un commerce | — |
| INV-FON-127 | 509 | Horaires : Horaires d'ouverture | — |
| INV-FON-128 | 510 | Géolocalisation : Recherche géographique | — |
| INV-FON-129 | 511 | Recherche de proximité : Points proches | — |
| INV-FON-130 | 512 | Zones d'intervention : Secteurs géographiques | — |
| INV-FON-131 | 513 | Avis : Affichages d'avis clients | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-086 | 516 | OpenStreetMap | — |
| INV-CON-087 | 517 | Mapbox | — |
| INV-CON-088 | 518 | Google Maps Platform | — |
| INV-CON-089 | 519 | Google Business Profile | — |
| INV-CON-090 | 520 | HERE | — |

### 3.13. Applications métier

Repère **INV-FAM-013** ; titre source ligne **523**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-132 | 526 | CRUD Builder : Gestion d'entités | — |
| INV-FON-133 | 527 | Tables : Tableaux de données | — |
| INV-FON-134 | 528 | Filtres : Recherche avancée | — |
| INV-FON-135 | 529 | Dashboard métier : Indicateurs personnalisés | — |
| INV-FON-136 | 530 | Workflows métier : Processus spécifiques | — |
| INV-FON-137 | 531 | Import/export : 2changes de données | — |
| INV-FON-138 | 532 | Permissions avancées : Accès par role | — |
| INV-FON-139 | 533 | Historique : traçabilité | — |
| INV-FON-140 | 534 | Génération documentaire : Documents métier | — |
| INV-FON-141 | 535 | Notifications : Alertes applicatives | — |
| INV-FON-142 | 536 | API métier : Exposition controlée de données | — |

**Occurrences de connecteurs**

Aucun libellé de connecteur n’est fourni dans cette famille. L’emplacement vide est conservé : **INV-VID-001**, ligne **539**. Il ne constitue pas un connecteur identifié.

### 3.14. Conformité et Confidentialité

Repère **INV-FAM-014** ; titre source ligne **542**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-143 | 545 | Politique de confidentialité : Pages et Documents | — |
| INV-FON-144 | 546 | Gestion des cookies : Consentement | — |
| INV-FON-145 | 547 | Export des données : Portabilité | — |
| INV-FON-146 | 548 | Suppression des données : Traitement des demandes | — |
| INV-FON-147 | 549 | Registre de consentement : Traçabilité | — |
| INV-FON-148 | 550 | Conservation : Polituqes de rétention | — |
| INV-FON-149 | 551 | Journal d'audit : Historique des opérations | — |
| INV-FON-150 | 552 | Gestion des accès : Droits sur les données | — |
| INV-FON-151 | 553 | Gestion des incidents : Déclaration et suivi | — |

**Occurrences de connecteurs**

Aucun libellé de connecteur n’est fourni dans cette famille. L’emplacement vide est conservé : **INV-VID-002**, ligne **556**. Il ne constitue pas un connecteur identifié.

### 3.15. Exploitation et infrastructure

Repère **INV-FAM-015** ; titre source ligne **559**. **Toutes les entrées ci-dessous sont à qualifier ; aucune disponibilité n’est établie.**

**Entrées fonctionnelles**

| Repère d’inventaire | Ligne source | Texte source | Normalisation du libellé proposée |
| --- | --- | --- | --- |
| INV-FON-152 | 562 | Deployment Manager : Gestion des déploiements | — |
| INV-FON-153 | 563 | Version Manager : Versions du moteur | — |
| INV-FON-154 | 564 | Backup Manager : Sauvegardes | — |
| INV-FON-155 | 565 | Restore Manager : Restaurations | — |
| INV-FON-156 | 566 | Monitoring : Dispo | — |
| INV-FON-157 | 567 | Log Viewer : Consultation des journaux | — |
| INV-FON-158 | 568 | Security Scanner : Conroles de sécurité | — |
| INV-FON-159 | 569 | Domain Manager : Domaines | — |
| INV-FON-160 | 570 | SSL Manager : Certificats TLS | — |
| INV-FON-161 | 571 | Resource Monitor : CPU, RAM, Stockage | — |
| INV-FON-162 | 572 | Module Manager : Installation des modules | — |
| INV-FON-163 | 573 | Concifugration Manager : Paramètrage | Configuration Manager — à valider |
| INV-FON-164 | 574 | Incident Manager : Gestion des incidents | — |
| INV-FON-165 | 575 | Updagte Managfer : MAJ | Update Manager — à valider |
| INV-FON-166 | 576 | Client Billing : Factruration de nos abonnements | — |

**Occurrences de connecteurs**

| Repère d’inventaire | Ligne source | Libellé source | Normalisation proposée |
| --- | --- | --- | --- |
| INV-CON-091 | 579 | Gitlab | GitLab — à valider |
| INV-CON-092 | 580 | Scaleway | — |
| INV-CON-093 | 581 | DNS | — |
| INV-CON-094 | 582 | ACME | — |
| INV-CON-095 | 583 | Sentry | — |
| INV-CON-096 | 584 | Grafana | — |
| INV-CON-097 | 585 | Prometheus | — |
| INV-CON-098 | 586 | Supervisor | — |

## 4. Inventaires annexes conservés séparément

Ces listes constituent des vues complémentaires du document. Elles ne sont pas fusionnées avec les 166 entrées fonctionnelles et ne prouvent pas qu’un composant soit implémenté, validé ou installé.

### 4.1. Composants d’interface — 10 entrées

| Repère d’inventaire | Ligne source | Libellé source |
| --- | --- | --- |
| INV-UI-001 | 132 | Button |
| INV-UI-002 | 133 | Dialog |
| INV-UI-003 | 134 | Input |
| INV-UI-004 | 135 | Select |
| INV-UI-005 | 136 | Tabs |
| INV-UI-006 | 137 | Dropdown |
| INV-UI-007 | 138 | Badge |
| INV-UI-008 | 139 | Toast |
| INV-UI-009 | 140 | Card |
| INV-UI-010 | 141 | Table |

### 4.2. Modules externes — 9 entrées

L’intitulé « Modules externes » est celui de la source. Une réutilisation de composant maintenu, comme Django Auth ou une bibliothèque OIDC/SAML, ne définit pas à elle seule un service externe. Cette nature reste à qualifier.

| Repère d’inventaire | Ligne source | Texte source |
| --- | --- | --- |
| INV-EXT-001 | 178 | Serveur e-mail : Fournisseur transactionnel externe |
| INV-EXT-002 | 179 | Newsletter : Fournisseur spécialisé ou connecteur |
| INV-EXT-003 | 180 | Authentification : Django Auth et composants éprouvés |
| INV-EXT-004 | 181 | SSO : Bibilothèque OIDC/SAML maintenue |
| INV-EXT-005 | 182 | Certificat TLS : Gestion automatisée |
| INV-EXT-006 | 183 | Stockage de fichiers : Stockage S3 compatible |
| INV-EXT-007 | 184 | Paiements : Prestataire de paiement |
| INV-EXT-008 | 185 | Gestion des secrets : Gestionnaire sécurisé, séparé du code |
| INV-EXT-009 | 186 | Sauvegardes : Outils éprouvés avec restauration testée |

### 4.3. Core / Standard / Advanced — 9 entrées

Les catégories ci-dessous sont conservées comme libellés source. Elles ne valent ni découpage final des modules ni priorité de réalisation.

| Repère d’inventaire | Catégorie source | Ligne source | Libellé source |
| --- | --- | --- | --- |
| INV-CLA-001 | Core | 195 | Sécurité |
| INV-CLA-002 | Core | 196 | CMS |
| INV-CLA-003 | Core | 197 | Gestion des médias |
| INV-CLA-004 | Core | 198 | Configuration |
| INV-CLA-005 | Standard | 204 | Contact |
| INV-CLA-006 | Standard | 205 | Catalogue |
| INV-CLA-007 | Standard | 206 | Connecteurs métiers |
| INV-CLA-008 | Advanced | 212 | SSO |
| INV-CLA-009 | Advanced | 213 | Traitement documentaire |

## 5. Fiche illustrative MOD-COM-001

**EXEMPLE UNIQUEMENT — INV-EX-001.** Cette fiche reprend l’exemple du document, sans l’enregistrer comme module réel. Les valeurs **P0**, **Standard**, **IDEA**, les capacités et les connecteurs illustrent le format : elles ne constituent pas une décision de priorité, une compatibilité démontrée ou une autorisation d’implémentation.

| Ligne source | Champ source | Valeur d’exemple source |
| --- | --- | --- |
| 593 | Identifiant | `MOD-COM-001` |
| 594 | Nom | Contact Form |
| 595 | Famille | Communication |
| 596 | Description | Création de formulaires |
| 597 | Clientèle | Commerce, artisan, industrie |
| 598 | Capacités requises | Formulaires, e-mail |
| 599 | Connecteurs compatibles | Brevo, Mailgun, SMTP |
| 600 | Type | Standard |
| 601 | Exécution | Django |
| 602 | Base de données | Optionnelle selon configuration |
| 603 | Interface | Wagtail StreamField |
| 604 | Activation no-code | Oui, après installation |
| 605 | Sensibilité des données | Données personnelles |
| 606 | Criticité sécurité | Moyenne à élevée |
| 607 | Complexité | Faible à moyenne |
| 608 | Priorité | P0 |
| 609 | Statut | IDEA |

## 6. Répétitions et rapprochements à examiner

### 6.1. Intitulés fonctionnels répétés

| Intitulé source | Occurrences | Repères conservés |
| --- | --- | --- |
| Notifications | 2 | INV-FON-019, INV-FON-141 |
| Conversion | 2 | INV-FON-066, INV-FON-106 |
| Evènements | 2 | INV-FON-105, INV-FON-116 |

« Conversion » désigne une transformation de formats dans Documents et données et le suivi d’objectifs dans Statistiques et Analytics. « Evènements » désigne le suivi d’interactions dans Statistiques et Analytics et un calendrier dans Réservation et activité locales. Ces exemples montrent pourquoi une égalité de libellé ne suffit pas à décider d’une fusion.

### 6.2. Libellés de connecteurs répétés exactement

| Libellé source | Occurrences | Repères conservés |
| --- | --- | --- |
| Google Analytics | 2 | INV-CON-002, INV-CON-076 |
| Matomo | 2 | INV-CON-003, INV-CON-074 |
| Calendly | 2 | INV-CON-014, INV-CON-083 |
| Google Calendar | 2 | INV-CON-015, INV-CON-081 |
| Stripe | 2 | INV-CON-027, INV-CON-084 |
| Odoo | 3 | INV-CON-033, INV-CON-038, INV-CON-072 |
| SFTp | 2 | INV-CON-044, INV-CON-053 |
| Grafana | 2 | INV-CON-080, INV-CON-096 |

Les rapprochements suggérés dans la colonne de normalisation ne changent pas ces comptes. « Search Console » / « Google Search Console » et « MDynamics 365 » / « Microsoft Dynamics 365 » restent des propositions à confirmer. « Microsoft Outlook » et « Outlook Calendar » restent séparés, car la capacité visée pourrait être différente.

### 6.3. Nature des connecteurs à préciser

| Nature à distinguer | Exemples cités | Question à résoudre |
| --- | --- | --- |
| Produit, plateforme ou service nommé | Brevo, Stripe, Odoo, GitLab, Scaleway | Quelle capacité et quelle interface utilise-t-on ? |
| Protocole, standard ou mécanisme | LDAP, Fournisseurs OIDC, SAML, SFTp, API REST, SOAP, webhooks, DNS, ACME | Quel système cible et quel contrat concret ? |
| Brique logicielle dont le déploiement reste à définir | Ollama, vLLM, Supervisor ; selon les choix, n8n, KeyCloak, Grafana, Prometheus | Où tourne-t-elle et qui en assure l’exploitation ? |
| Cible générique ou stratégie | ERP internes, Systèmes de résa spécialisés, connecteurs dev en python | Quel produit, propriétaire, format et périmètre réel ? |
| Terme ambigu à qualifier | S3 | Service spécifique ou interface compatible de stockage objet ? |

Ces catégories sont des axes d’analyse, pas des décisions de fournisseur, de licence, de gratuité ou de déploiement. La nature de la cible et son mode d’exploitation peuvent être deux champs distincts du futur registre.

## 7. Vérification de l’extraction

| Contrôle documentaire | Résultat |
| --- | --- |
| Lignes de catalogue attendues / capturées | 266 / 266 : 166 entrées fonctionnelles + 98 occurrences non vides + 2 emplacements vides. |
| Couverture des familles | 15 / 15, ordre source conservé. |
| Inventaires annexes | 10 UI, 9 externalisation, 9 classification. |
| Fiche illustrative | 17 / 17 champs source conservés. |
| Texte des lignes source dans le JSON | Comparaison exacte effectuée avec le fichier source. |
| Repères d’inventaire | Uniques ; aucune ligne de catalogue affectée deux fois. |
| Fusion sémantique | Aucune. |
| Portée de la vérification | Fidélité de l’inventaire uniquement ; aucune validation de produit ou d’architecture. |

Empreinte SHA-256 du fichier source : `3ebb5f058ba72b1bf1fa17bafce63b3e93d8cfe291a64134951473e631bfb956`.
