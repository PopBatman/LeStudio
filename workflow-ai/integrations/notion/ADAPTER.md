# Adaptateur de projection Notion

## État réel

| Surface | État |
|---|---|
| Connexion interactive Notion de l'assistant | Connexion confirmée par l'utilisateur pendant cette session ; publication pilotée séparément par l'assistant principal |
| Adaptateur REST de ce dossier | Implémenté ; tests hors ligne inclus, résultat de cette livraison dans le rapport |
| Écriture REST sur le compte réel | Non exécutée : jeton d'automatisation et page parente dédiée non configurés pour ce programme |
| Synchronisation bidirectionnelle / base Notion automatique | Hors périmètre de ce lot |

Cet adaptateur **publie une nouvelle page par révision d'un document** dans une page parente dédiée. Il ne remplace pas les blocs d'une page existante et ne supprime rien. Les versions antérieures et les annotations humaines restent en place. Le mot « immuable » décrit son comportement : un utilisateur disposant des droits Notion peut toujours modifier ces pages.

Le dépôt fait référence pour les contrats et les preuves techniques. La carte existante du Kanban porte la synthèse de pilotage et les décisions humaines. Sa mise à jour interactive suit les [règles de compte rendu](../../workflows/FEATURE-RAPPORT.md). Un statut, une phrase ou une case cochée dans Notion ne change aucun mandat, gate, test ou droit de déploiement.

## Utilisation hors ligne

Exécuter les commandes depuis `workflow-ai/`, avec Python 3.11 ou supérieur. Le dossier `studio/` se trouve au même niveau.

```bash
python3 integrations/notion/sync.py --dry-run
python3 integrations/notion/sync.py --dry-run --export notion-export.json
python3 -m unittest discover -s tests -p 'test_notion_sync.py' -v
```

Le dry-run n'utilise aucun compte, ne crée pas le registre SQLite et ne fait aucun appel réseau. Il affiche les documents et empreintes, sans leur contenu complet. `--export` crée exclusivement un nouveau fichier JSON contenant les documents rendus ; il refuse d'écraser un fichier existant. Le JSON exporté n'est pas le format d'import natif Notion : c'est un aperçu contrôlable destiné à l'adaptateur ou à une publication par l'assistant.

## Manifeste

Le fichier par défaut est `integrations/notion/config.example.json`. Utiliser `--manifest CHEMIN` pour une sélection propre au projet.

```json
{
  "schema_version": 1,
  "documents": [
    {
      "id": "studio-overview",
      "title": "Studio — périmètre",
      "scope": "studio",
      "path": "project/PROJECT.md"
    }
  ]
}
```

| Champ | Contrat |
|---|---|
| `id` | Identifiant stable : lettres minuscules, chiffres et tirets ; unique dans le manifeste |
| `title` | Titre lisible, non vide, au plus 160 caractères |
| `scope` | `workflow-ai` pour les règles et outils, `studio` pour les documents du projet Django/Wagtail. Les anciens manifestes qui omettent ce champ utilisent la racine de l’adaptateur. |
| `path` | Chemin relatif POSIX d'un fichier `.md`, sous la racine autorisée ; aucun segment caché ou lien symbolique |
| `source_url` | Facultatif : lien HTTPS exact vers la version GitLab source, sans identifiants dans l'URL ; ne pas inventer une URL avant création du dépôt |

Limites locales : 40 documents par lot, 128 Kio par source, 256 Kio de manifeste. Le contenu UTF-8 est rendu avec sa provenance et son SHA256. La clé de projection comprend également l'identifiant, le titre, le chemin, l'URL source, la version du rendu et celle de l'API.

Le paramètre `--root` désigne le dossier du workflow. Avec `scope: studio`, l’adaptateur lit exclusivement le chemin déclaré sous le dossier frère `studio/`. Le manifeste livré conserve les identifiants des documents. Les nouveaux chemins de provenance incluent leur dossier (`workflow-ai/…` ou `studio/…`) et donnent donc une nouvelle empreinte de projection. Un manifeste existant peut conserver son format pour les documents situés sous la racine du workflow.

Les balises XML de contrôle Notion dans la prose sont échappées ; les images Markdown deviennent des liens. Le code placé dans des blocs clôturés reste du code. Ce traitement ne remplace pas la revue des documents : l'allowlist n'est pas un système de détection de secrets.

## Activation REST

1. Créer une connexion interne Notion dédiée au Workspace. Lui donner uniquement les capacités de lecture et d'insertion nécessaires ; les capacités d'insertion de contenu et de propriétés sont requises pour créer une page Markdown.
2. Créer une page parente dédiée, la partager avec cette connexion et conserver son UUID. Ne pas passer une URL à la place de l'UUID.
3. Fournir `NOTION_API_TOKEN` et `NOTION_PARENT_PAGE_ID` depuis un gestionnaire de secrets ou des variables CI protégées. Ne pas les écrire dans ce dépôt, les documents, le manifeste ou une conversation.
4. Vérifier le dry-run puis exécuter la publication avec le registre persistant du projet.

```bash
python3 integrations/notion/sync.py --manifest integrations/notion/config.example.json --apply
```

Le programme ne lit pas de `.env` automatiquement. La connexion interactive de l'assistant et ce jeton REST sont deux mécanismes distincts : connecter Notion dans l'assistant ne configure pas les variables de ce script.

Transport : origine fixe `https://api.notion.com`, TLS standard, redirections désactivées, proxys issus de l'environnement désactivés, délai de 20 secondes par requête, réponses limitées à 2 Mio. Version d'API fixée à `2026-03-11`, format Markdown `v2`. Aucun endpoint de suppression ou d'édition de page n'est utilisé.

## Registre et reprise

Le registre par défaut est `.workspace/notion.sqlite3` ; le fichier a des permissions locales `0600`. Il contient les identifiants, empreintes, résultats et éventuels délais de reprise, jamais le jeton ni le contenu des documents. Un verrou exclusif empêche deux exécutions locales simultanées avec ce même registre.

| Situation | Comportement |
|---|---|
| Même cible, identifiant et contenu déjà publiés | Retour `unchanged`, aucun nouvel appel d'écriture |
| Document modifié | Création d'une nouvelle page, précédente conservée |
| Première partie du lot réussie, document suivant en échec | Les succès restent enregistrés ; la relance ne les republie pas |
| HTTP 429 / 529 | Enregistre `Retry-After` ; la relance attend sa fin, sans sommeil long ni retry automatique |
| Refus HTTP 4xx définitif | Enregistre le refus ; corriger l'accès ou la requête avant de relancer |
| Timeout, réponse invalide, HTTP 5xx ou interruption après intention | Révision `pending` ; toute nouvelle écriture de ce document vers la cible est bloquée |
| Arrêt brutal avec verrou restant | Vérifier qu'aucun processus ne tourne avant de retirer le fichier `.lock` ; ne pas supprimer le registre |

Une requête POST peut réussir côté serveur avant de perdre sa réponse. Le programme conserve donc l'intention **avant** l'appel réseau et ne prétend pas garantir une transaction distribuée ou une livraison « exactement une fois ».

Après un résultat incertain, rechercher la page sous la cible, comparer son identifiant de document et son `Projection SHA256`. Si elle existe :

```bash
python3 integrations/notion/sync.py --reconcile studio-overview --page-id UUID_DE_LA_PAGE_EXISTANTE
```

La commande vérifie par API que la page est active, dépend de la bonne page parente et contient la provenance attendue. Elle met ensuite le registre à jour sans écrire dans Notion. Il faut les mêmes variables d'environnement et, si personnalisé, le même `--state` que lors de la publication.

Si aucune page n'est retrouvée, ne pas effacer le registre pour débloquer automatiquement l'agent. Un opérateur doit établir l'absence de l'écriture avant une réparation ciblée du registre. Il n'existe volontairement pas de commande de retry forcé. Une page supprimée ou modifiée manuellement après une publication complète n'est pas resynchronisée automatiquement : cette version ne fait pas de surveillance de dérive.

Conserver un seul registre persistant et une seule identité d'écriture pour la cible. Une autre machine utilisant un registre indépendant peut produire des doublons. Une prochaine version pourra ajouter un index distant et une réconciliation multi-exécuteurs si ce besoin est confirmé.

## Vérifications et limites

Les tests utilisent un faux transport : allowlist, traversal, symlinks, tailles, dry-run sans secrets, déduplication, versions distinctes, séparation des cibles, échec partiel, résultat incertain, réconciliation, limites HTTP, absence de fuite dans les erreurs et verrou concurrent. Les résultats exécutés pour cette version sont récapitulés dans `evidence/DELIVERY-REPORT.md`. Les anciens fichiers de preuve ne sont pas repris comme preuve de cette nouvelle livraison.

Ces contrôles ne constituent pas une isolation contre un processus malveillant ayant les mêmes droits sur le filesystem. Le registre local n'est pas signé et n'autorise aucune opération de production. La qualification sur le compte réel et la comparaison du rendu Notion restent à réaliser pour cet adaptateur REST.

## Références officielles

Vérifiées le 18 novembre 2026 :

- [Créer une page, lire et modifier du Markdown](https://developers.notion.com/guides/data-apis/working-with-markdown-content) — création via `POST /v1/pages`, `markdown_version: v2`, provenance et limites de rendu.
- [Versionner les appels API](https://developers.notion.com/reference/versioning) — en-tête `Notion-Version` obligatoire.
- [Limites et reprises HTTP](https://developers.notion.com/reference/request-limits) — `Retry-After`, ambiguïté des réponses 503 et précautions de retry des écritures.
- [Connexion interactive MCP](https://developers.notion.com/guides/mcp/get-started-with-mcp) — à distinguer de l'automatisation REST.

## Pages de travail existantes

La documentation de cette session est maintenue dans les pages Notion existantes, avec conservation de leur historique. Le script REST ci-dessus a un autre comportement : il crée des pages de révision sous la page parente configurée. Il ne met pas automatiquement à jour les pages de session et ne partage pas le ZIP ni son code. Choisir une cible dédiée avant de l’activer.

Le fichier `pages.reference.json` repère les pages connues pour cette session ; il ne configure aucun accès et n’est pas lu par le script de projection.
