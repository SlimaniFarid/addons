# Changelog — sf_backorder_priority

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Allocation runs per product with scoring weights
- Shortage detection on open deliveries
- Priority score: lateness + value + customer
- Top-down stock allocation
- Reservation application

### Technique
- Modèles : sf.bo.allocation, sf.bo.allocation.line
- Dépendances : base, sale, stock, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
