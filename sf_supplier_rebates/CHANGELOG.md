# Changelog — sf_supplier_rebates

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Rebate deals: turnover bonus, retro %, per unit
- Product category scoping
- Monthly accrual computation from posted bills
- Threshold progress tracking
- Claims with credit note settlement

### Technique
- Modèles : sf.supplier.rebate.deal, sf.supplier.rebate.accrual, sf.supplier.rebate.claim
- Dépendances : base, account, purchase, product, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
