# Changelog — sf_purchase_price_analysis

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- PPV analysis runs per period with vendor filter
- Actual average price from posted bills
- Variance vs standard cost: amount and %
- Tolerance-based alert flagging
- Multi-company isolation

### Technique
- Modèles : sf.ppv.analysis, sf.ppv.line
- Dépendances : base, account, purchase, product, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
