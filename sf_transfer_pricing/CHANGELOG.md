# Changelog — sf_transfer_pricing

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Pricing policies: CUP, Cost-Plus, Resale-Minus, TNMM per entity pair
- Transaction analysis with arm-length price computation and variance flags
- Review workflow with reviewer sign-off
- Master File / Local File / CbCR documentation register
- Multi-company record rules, chatter audit trail

### Technique
- Modèles : sf.tp.policy, sf.tp.transaction, sf.tp.documentation
- Dépendances : base, account, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
