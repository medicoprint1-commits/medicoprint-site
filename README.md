# Mini-site Medicoprint

Mini-site vitrine responsive, réalisé en HTML/CSS/JavaScript sans dépendance de compilation.

## Prévisualiser

Ouvrir `index.html` dans un navigateur. Les polices DM Sans et Manrope sont chargées depuis Google Fonts ; le site reste lisible avec les polices locales si la connexion n’est pas disponible.

## Contenu

- Présentation Medicoprint et positionnement autour de l’hémodialyse
- Gammes consommables, traitement de l’eau et matériel médical
- Accompagnement, conseil, assistance technique, formation et maintenance
- Liens directs vers téléphone, e-mail et WhatsApp
- Métadonnées de base pour le référencement et navigation mobile
- Brouillons de campagne pour LinkedIn, Instagram, YouTube, Facebook et TikTok dans `reseaux-sociaux.md`
- Visuels et vidéos de lancement prêts à adapter dans `assets/social/ready-to-post/`
- Maquette indépendante de page LinkedIn dans `linkedin-preview.html` (aperçu local, non publiée)
- Aperçus locaux séparés pour les cinq réseaux dans `social-pages/index.html`
- Page thématique autonome sur l’hémodialyse dans `dialyse-maroc.html` (à publier séparément)

Les visuels produits sont des illustrations CSS de maquette, pas des photos ou fiches techniques. Avant publication, remplacer/compléter avec les visuels officiels, références, caractéristiques et documents vérifiés par Medicoprint.

Les médias sociaux du dossier `assets/social/` sont une campagne séparée du mini-site. Ils utilisent des photos publiques des pages produits Medicoprint. Les détails produits et les coordonnées doivent être validés par l’entreprise avant diffusion.

## Publication séparée avec GitHub Pages

Le workflow `.github/workflows/deploy-pages.yml` prépare le mini-site, la page autonome `dialyse-maroc.html`, l’aperçu LinkedIn et les aperçus sociaux. Pour l’activer, dans GitHub ouvrir **Settings → Pages → Build and deployment → Source → GitHub Actions**. La publication apparaîtra sur le domaine GitHub Pages du dépôt ; elle ne change pas le site `medicoprint.ma`.
