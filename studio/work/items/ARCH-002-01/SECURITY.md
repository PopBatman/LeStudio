# Habilitations de la fiche

| Acteur | Résultat au point d’entrée de la fiche |
|---|---|
| Anonyme | Parcours de connexion existant. |
| Compte authentifié hors groupe Opérateurs Studio | Refus selon le contrôle existant. Un compte désactivé ne peut pas consulter les données. |
| Opérateur sans mandat Site, mandat sur autre site ou mandat Client seul | Fiche introuvable. Même réponse qu’un identifiant inconnu. |
| Mandat Site en lecture | Nom et informations FEAT-002 déjà accessibles, résumé daté, motif métier et versions disponibles. |
| Mandat Site en gestion | Même résumé, détails de la liaison avec UUID du site et de l’instance, alias déjà confirmé et code assaini. |
| Mandat retiré | Au prochain accès, appliquer de nouveau les contrôles serveur. |

Le masquage s’applique au panneau dès la construction du contexte côté serveur, y compris aux champs dans les détails repliés. L’UUID déjà utilisé pour router une fiche autorisée n’est pas un secret d’accès. La visibilité du client conserve son mandat distinct. Les deux niveaux Site disposent de la même consultation sans action sur le moteur.

Limiter les codes techniques de gestion à une liste fermée des diagnostics connus du service (communication, timeout, authentication, unavailable, incompatible, identity, identity_mismatch, association_conflict, render, invalid_profile, profile_changed, attempt_expired). Un résultat inconnu ou un refus d’accès antérieur reçoit un libellé neutre. Ne jamais refléter une chaîne arbitraire, une exception, un alias non validé ou le contenu du JSON versions. Échapper les valeurs affichées et contrôler le format des champs. En recette injecter une valeur inconnue contenant du balisage et vérifier son absence du contexte de présentation et de la réponse. Les journaux n’enregistrent ni le snapshot brut ni les profils ou certificats. Aucun lien navigateur n’est dérivé du domaine, de l’alias, d’une origine Docker ou d’un chemin d’administration supposé.
