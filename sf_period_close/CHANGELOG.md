# Changelog — sf_period_close

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Checklist templates per department with due offsets
- Close periods with auto-generated tasks
- Task workflow: pending, in progress, done, blocked, N/A
- Blocker notes and period blocking
- Sign-offs per task and final close sign-off

### Technique
- Modèles : sf.close.template, sf.close.template.step, sf.close.period, sf.close.task
- Dépendances : base, account, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
