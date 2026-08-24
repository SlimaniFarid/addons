# Changelog — sf_sample_management

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Sample requests with purposes and lines
- Cost computation: product cost + shipping
- Approval before shipping
- Feedback records with ratings
- Conversion tracking with sale order link

### Technique
- Modèles : sf.sample.request, sf.sample.line, sf.sample.feedback
- Dépendances : base, sale_management, stock, product, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
