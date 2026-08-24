# Changelog — sf_change_requests

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Change requests with typed scopes and risk levels
- Mandatory rollback plans
- CAB votes with approval percentage
- Implemented/failed lifecycle with PIR
- Multi-company isolation

### Technique
- Modèles : sf.change.request, sf.change.vote
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
