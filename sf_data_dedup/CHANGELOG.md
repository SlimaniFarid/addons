# Changelog — sf_data_dedup

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Duplicate scans with 4 strategies
- Duplicate groups with match keys
- Review workflow: open, merged, ignored
- Company-scoped scans

### Technique
- Modèles : sf.dedup.scan, sf.dedup.group
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
