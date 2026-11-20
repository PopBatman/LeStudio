# Composants de l’interface Studio

La [galerie locale](http://127.0.0.1:8000/ui/) montre les composants avec des données fictives. Les écrans peuvent réutiliser les templates de `templates/cotton/`. Chaque feature fournit ses libellés, ses valeurs et ses actions. Le serveur de la feature valide les données et les droits.

| Composant Cotton | Entrées et usage |
|---|---|
| `c-button` | Libellé dans le contenu. `variant="primary"` par défaut ou `secondary`. `type="button"` par défaut, `type="submit"` pour soumettre. `disabled` rend le contrôle indisponible. |
| `c-text-link` | Destination dans `href` et libellé dans le contenu. Utiliser une ancre ou une URL fournie par l’écran. |
| `c-field` | `id` unique, `label` visible, `type` (texte par défaut), `value`, `help`, `error`. Les attributs HTML tels que `required`, `maxlength` et `disabled` sont transmis au champ. Une erreur est reliée au contrôle et signalée par `aria-invalid`. |
| `c-alert` | `title`, explication dans le contenu et `variant="success"` ou `warning`. La galerie présente des messages statiques. Les résultats des interactions sont annoncés dans des régions `role="status"`. |
| `c-badge` | État écrit dans le contenu, variante `neutral` par défaut, `success` ou `warning`. |
| `c-table` | `caption` décrit le tableau. Le slot nommé `headings` reçoit les cellules d’en-tête et le contenu principal reçoit les lignes. L’appelant précise `scope="col"` ou `scope="row"` sur ses en-têtes. |
| `c-empty-state` | `title` explique l’absence de données. Le contenu propose une suite possible, par exemple effacer le filtre. |

```html
<c-field id="nom-site" label="Nom du site" help="Entre 2 et 80 caractères." maxlength="80" required />
<c-button type="submit">Vérifier le nom</c-button>
```

## Fondations visuelles et navigation

Les couleurs et les polices sont définies dans [la source Tailwind](../frontend/gallery.css). L’interface emploie DM Sans hébergée localement. Le spécimen de caractères utilise Georgia italique. L’encre foncée sert au texte et au bouton principal, le vermillon aux illustrations. Les variantes sémantiques associent couleur et libellé. Un contour de 3 px rend le focus clavier visible.

Le [gabarit](../templates/ui/base.html) fournit le lien de saut au contenu, la colonne latérale et les emplacements de navigation. À 800 px de large ou moins, le sommaire se déplie dans l’en-tête. À 580 px ou moins, les cartes se placent sur une colonne. Dans le sommaire ouvert, Échap le referme et rend le focus à son bouton.

Le [script de démonstration](../static/ui/gallery.js) vérifie un nom fictif et filtre les lignes par nom ou par état. Les exemples se réinitialisent au rechargement de la page.
