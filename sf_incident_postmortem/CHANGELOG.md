# Changelog — sf_incident_postmortem

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Incidents with S1-S4 severity and categories
- Detection/resolution timeline with duration
- Root cause and lessons learned sections
- Corrective/preventive actions with owners
- Multi-company isolation

### Technique
- Modèles : sf.incident, sf.incident.action
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
