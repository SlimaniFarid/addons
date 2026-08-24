# Changelog — sf_load_planning

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Load plans with carrier, vehicle and departure
- Delivery assignment with route stops
- Weight/volume/pallet capacity limits and overload flags
- Load lifecycle: draft to completed
- Multi-company isolation

### Technique
- Modèles : sf.load.plan, sf.load.line, sf.load.stop
- Dépendances : base, stock, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
