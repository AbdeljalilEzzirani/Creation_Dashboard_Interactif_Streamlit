# Creation_Dashboard_Interactif_Streamlit
Création d'un Dashboard Interactif avec Streamlit

## Contexte du projet **
  Dans ce projet, vous allez créer un dashboard interactif en Python avec Streamlit afin de visualiser et analyser les données issues d’une base de données relationnelle dédiée aux annonces immobilières. Ce dashboard permettra aux utilisateurs de       mieux comprendre les tendances et caractéristiques du marché immobilier en exploitant les données déjà modélisées et stockées dans PostgreSQL.

* Voici les étapes détaillées que vous devrez suivre pour mener à bien ce projet :

## Étape 1 : Comprendre et S’approprier le Contexte
Objectif : Étudier la structure des données pour en extraire un maximum d'informations exploitables.

  ** Structure des tables :
      Table Annonce : Contient des champs clés comme le prix, la surface, la date de publication, etc.
      Table Ville : Relie chaque annonce à une ville donnée.
      Table Équipement : Liste les équipements disponibles (ascenseur, balcon, etc.).
      Table AnnonceEquipement : Gère la relation plusieurs-à-plusieurs entre les annonces et les équipements.
  ** Relations entre les tables :
      Annonce ↔ Ville : Une annonce est liée à une seule ville (relation plusieurs-à-un).
      Annonce ↔ Équipement : Une annonce peut avoir plusieurs équipements, et un équipement peut être associé à plusieurs annonces (relation plusieurs-à-plusieurs).
  * 💡 À faire :
      Étudiez le schéma relationnel pour bien comprendre comment les données sont interconnectées.
      Identifiez les informations à extraire, comme le nombre d'annonces par ville, les équipements les plus fréquents, ou encore l'évolution des prix.

## Étape 2 : Préparer l’Environnement
Objectif : Mettre en place un environnement de travail stable et fonctionnel.

  ** Outils nécessaires :
      Python : Langage principal pour le projet.
      Bibliothèques : streamlit, pandas, sqlalchemy, psycopg2 (pour interagir avec PostgreSQL).
  ** Base de données PostgreSQL :
      Assurez-vous qu’elle est configurée et accessible.
      Si besoin, hébergez-la via Docker pour simplifier le déploiement.
  * 💡 À faire :
      Installez les bibliothèques nécessaires via pip install.
      Testez la connexion à PostgreSQL pour vérifier l’accès aux données.

## Étape 3 : Concevoir le Dashboard
Objectif : Définir l’interface et les fonctionnalités du tableau de bord.

** Structure du dashboard :

  * Sidebar (Barre latérale) :
    Filtres interactifs :
      Gamme de prix (slider).
      Nombre de pièces et de salles de bain (sliders).
      Sélection de ville (menu déroulant).
      Équipements disponibles (multi-sélection).
      Plage de dates (sélecteur).
  * Page principale :
      Tableau des annonces filtrées.
      Graphiques interactifs et visualisations.
** Visualisations prévues :

    * Analyse des villes :
        Graphique à barres : Nombre d’annonces par ville.
        Carte interactive : Localisation des annonces par ville.
    * Analyse des prix :
        Histogramme : Répartition des prix.
        Boxplot : Comparaison des prix par ville.
    * Caractéristiques des biens :
        Camembert : Répartition des équipements (ex. : pourcentage d’annonces avec balcon).
        Graphique à barres : Moyenne de pièces/salles de bain par ville.
    * Analyse temporelle :
        Graphique linéaire : Évolution du nombre d’annonces publiées.
    * Relation surface-prix :
        Nuage de points : Corrélation entre la surface et le prix.

## Étape 4 : Implémenter le Dashboard avec Streamlit
Objectif : Construire l’application pas à pas.

  ** Connexion à la base de données :
        Configurez la connexion avec SQLAlchemy pour interagir facilement avec PostgreSQL.
  ** Extraction des données :
        Écrivez des requêtes SQL pour récupérer les données nécessaires :
        Annonces pour une ville donnée.
        Annonces filtrées par gamme de prix, nombre de pièces, etc.
        Compter le nombre d’annonces par ville.
        Statistiques sur les équipements.
  ** Visualisations interactives :
        Créez des fonctions Python pour générer chaque graphique.
        Affichez les graphiques dynamiquement selon les filtres sélectionnés.
  ** Tableau interactif :
        Ajoutez un tableau interactif (st.dataframe) pour afficher les annonces filtrées.
  ** Export des données :
        Intégrez un bouton permettant de télécharger les données filtrées au format CSV.


## Étape 5 : Déploiement (Facultatif)
Objectif : Rendre l’application accessible à d’autres utilisateurs.
    ** Hébergez le tableau de bord sur une plateforme cloud comme Streamlit Cloud, Heroku, ou sur un serveur privé.

## Conclusion
Avec ces étapes, vous serez en mesure de construire un tableau de bord complet, interactif et utile pour analyser le marché immobilier. Il vous permettra d'extraire des insights pertinents pour vos utilisateurs tout en exploitant la puissance de PostgreSQL et de Python.
