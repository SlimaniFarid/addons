# Changelog — sf_policy_waivers

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Waiver requests with justification and risk
- Compensating controls requirement
- Validity windows with expiry flags
- Approve/reject workflow with sign-off
- Multi-company isolation

### Technique
- Modèles : sf.policy.waiver
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
