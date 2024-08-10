# Python_Mediatheque

- Réalisé avec Python et Django
  - Création d'une médiatheque fictive pour un projet.

# Installer Django

Dans un terminal : 

`python -m pip install Django==5.1`

# Pour lancer un serveur local

( ` python manage.py loaddata fixtures.json`) -> Pour crée des donnéés tests

`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`


Rapport de Projet
Mediathèque


 # L’étude et les correctifs du code fourni 

Explication des changements : 
- Les classes ne sont pas bien défini. L’utilisation la plus simple est celle avec une classe parent dont hérites les autres classes enfants. Par exemple Media comme parent et les enfants seront Livre, DVD, CD.
Les champs n’étaient pas bien définies également. Ici j’ai rajouter des détails pour éviter des erreurs dans la base de odnnée. Une taille maximal pour les noms de media, les createur etc.., des fonctions boolean pour la disponibilité , les date pour les emprunts .
J’ai remis les lignes sous la classe pour qu’ils soient tous alignés, ce qui ne l’étaient pas dans le code fourni. 
- Les conventions de nommage n’taient pas respecter. J’ai utiliser le CamelCase pour les classe et le snake_case pour le reste. 
- J’ai rajouter des fonctions manquantes comme le type de media pour faciliter l’ajout par les bibliothécaires.


# La mise en place des fonctionnalités demandées 

« Il y aura deux applications à déployer : 
• Une application principale qui ne sera accessible qu’aux bibliothécaires. 
• Une application de consultation accessible aux emprunteurs »

Mise en place grâce a une page d’acceuil qui permet de choisir entre un membre et un bibliothécaire, le second étant protéger par un utilisateur et un mot de passe crée par le superAdmin (ici Biblio1 avec comme mot de passe Bibliothecaire001)

« L’application membre doit permettre d’afficher tout les médias »

Implémenter en créannt une page unique « list_media » mais dont les fonctionnalité de bibliothecaire sont caché et inutilisable pour les membres.

« Mettre à jour un membre. »
Directement disponible dans la liste des membres meme si il serai plus pratique de crée une page a part et selectionner le bon membre pour plus d’ergonomie.

« Afficher la liste des médias »
la boucle « for livre » est une fonctionnalité pour les emprunt et les disponibilités que je n’ai pas étendu aux autres medias.

« Créer un emprunt pour un média disponible »

 La fonction d’emprunt a uniquement été crée pour livre, mais l’ajout pour les autres media suivrait la même logique


 # Stratégies des testes

Dans l’ordre :  
- Le premier test crée un utilisateur bibliothecaire et se connecte pour tester la sélection de rôle et le login.
Puis il crée un emprunteur pour vérifier la view de création
Et il fini par creer les media livre, dvd et cd pour tester la view correspondante

- Le second test permet de verifier le chargement de la page d’acceuil bibliothecaire après le login.

- Le troisième test permet de verifier la page des listes des membres  son chargement

- Le quatrième permet de verifier la création d’emprunt

- LE cinquième vérifie la liste des emprunteur et si delete et update sont bien afficher après la création

- Le sixième test la création d’un média

- Le septième test l’affichage de la liste des médias

- le huitième test la fonctionnalité d’emprunt d’un livre et le changement de status de disponible a emprunté.



# une base de données avec des données test 


Les données dans le test sont présent pour ajouter des emprunteurs dans la liste et des medias pour tester les emprunts. 






Pour installer et executer le programme, suivez ce qui est indiquer dans le fichier Read,me. J’ai tenter d’installer « PyInstaller »  et le configurer pour un fichier sans pré-requis, sans succès.
