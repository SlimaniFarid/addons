# Changelog — sf_customer_onboarding

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Onboarding templates with typed steps
- Task generation per customer
- Progress % with completion gating
- First sale order link
- Multi-company isolation

### Technique
- Modèles : sf.cob.template, sf.cob.template.step, sf.customer.onboarding, sf.customer.onboarding.task
- Dépendances : base, sale, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
