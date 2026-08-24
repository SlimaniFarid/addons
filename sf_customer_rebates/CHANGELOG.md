# Changelog — sf_customer_rebates

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Customer rebate deals: retro %, turnover bonus, per unit
- Product category scoping
- Monthly accruals from posted invoices
- Credit note settlement
- Multi-company isolation

### Technique
- Modèles : sf.customer.rebate.deal, sf.customer.rebate.accrual
- Dépendances : base, account, sale, product, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
