# Changelog — sf_return_to_vendor

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- RTV orders with reasons and vendor authorization
- Line dispositions: credit, repair, replacement, scrap
- Automatic return picking with lots
- Debit note settlement workflow
- RTV value computation

### Technique
- Modèles : sf.rtv.order, sf.rtv.line
- Dépendances : base, stock, purchase, account, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
