# Activer la mesure d'audience

L'intégration Google Analytics est préparée mais inactive tant que l'identifiant de mesure n'est pas renseigné et que les fichiers ne sont pas publiés.

1. Dans Google Analytics, créer ou sélectionner la propriété MEDICOPRINT.
2. Dans Administration → Flux de données, créer ou ouvrir le flux Web correspondant à l'adresse publique exacte du mini-site GitHub Pages.
3. Copier l'identifiant de mesure commençant par `G-` dans `analytics-config.js`.
4. Désactiver les mesures améliorées du flux pour limiter la collecte aux pages vues configurées ici. Ne pas activer la collecte de données fournies par les utilisateurs.
5. Publier les changements via une branche et une pull request, puis vérifier le déploiement GitHub Pages.
6. Sur le site publié, accepter la mesure et vérifier l'arrivée d'une visite dans le rapport Temps réel de Google Analytics. Vérifier également qu'aucune requête Google Analytics ne part avant acceptation ou après refus.

Le code concerne les pages de ce mini-site, pas automatiquement le domaine medicoprint.ma. Les aperçus des réseaux sont comptés comme des pages du mini-site ; ils ne donnent pas les statistiques des plateformes sociales.

La mesure commence après activation et consentement. Elle ne reconstitue pas les visites antérieures. Les bloqueurs et les refus peuvent réduire les visites mesurées. Le bouton de préférences en bas des pages permet de changer le choix.

Documentation : https://developers.google.com/tag-platform/security/guides/consent?consentmode=basic
