# Changelog — sf_credit_insurance

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Insurance policies with coverage and premium
- Insured buyer limits with decision workflow
- Claims with computed indemnity
- Settlement states including partially paid
- Multi-company isolation

### Technique
- Modèles : sf.ci.policy, sf.ci.buyer, sf.ci.claim
- Dépendances : base, account, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
