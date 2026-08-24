# Changelog — sf_access_review

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Campaigns with all-users or admin scope
- Auto-generated review lines with groups summary
- Keep/revoke decisions with reviewer and date
- Close gating on pending reviews
- Multi-company isolation

### Technique
- Modèles : sf.access.campaign, sf.access.review
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
