# Changelog — sf_product_eol

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- EOL records with announcement, EOL and last-time-buy dates
- Replacement product mapping
- Remaining stock and open order detection
- One-click sale blocking on discontinuation
- Customer communication plan

### Technique
- Modèles : sf.product.eol
- Dépendances : base, product, sale, stock, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
