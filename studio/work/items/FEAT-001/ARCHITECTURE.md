# Architecture du parcours opérateur

Django Auth et les sessions en base prolongent ARCH-001. L’application workspace centralise le critère de groupe, les vues et la création locale du compte. La méthode de connexion aboutit à une destination interne fixe. Les primitives Cotton et les styles de UI-001 sont partagés avec les écrans du lot. Les assets nécessaires aux écrans sont disponibles même lorsque la galerie de développement est désactivée.

L’accueil répond sur `/`, la connexion sur `/connexion/` et la déconnexion sur `/deconnexion/`. Le lot introduit les migrations standard Django. La galerie et le signal de santé conservent leurs adresses et leur comportement. [Authentification Django](https://docs.djangoproject.com/en/5.2/topics/auth/default/) et [sessions Django](https://docs.djangoproject.com/en/5.2/topics/http/sessions/).
