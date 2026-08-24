# Changelog — sf_ic_netting

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Netting sessions per period across selected entities
- Automatic scan of open IC receivables/payables via company partner mapping
- Net position per company pair with item counts
- Dispute tracking with resolution notes
- Settlement journal entries for net amounts

### Technique
- Modèles : sf.ic.netting.session, sf.ic.netting.line, sf.ic.netting.dispute
- Dépendances : base, account, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
