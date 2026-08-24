# Changelog — sf_facility_management

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Sites with owned/leased and lease references
- Rooms with types, capacity and floors
- Bookings with conflict detection
- Calendar view of bookings
- Multi-company isolation

### Technique
- Modèles : sf.facility.site, sf.facility.room, sf.facility.booking
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
