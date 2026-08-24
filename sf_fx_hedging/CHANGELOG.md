# Changelog — sf_fx_hedging

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Exposure snapshots from posted FX receivables/payables
- Coverage % per currency and direction
- Forward contracts with strike, notional, value date
- Settlement at spot with realized gain/loss
- Multi-company isolation

### Technique
- Modèles : sf.fx.exposure, sf.fx.exposure.line, sf.fx.hedge
- Dépendances : base, account, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
