# Changelog — sf_quality_coa

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- CoA records per delivery with lot
- Test parameters with specifications and verdicts
- All-pass approval gate
- Tested/approved/issued workflow
- Multi-company isolation

### Technique
- Modèles : sf.coa, sf.coa.line
- Dépendances : base, stock, quality, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
