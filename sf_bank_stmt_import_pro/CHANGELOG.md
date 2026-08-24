# Changelog — sf_bank_stmt_import_pro

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Parsers natifs sans dépendances externes :
  - MT940 (SWIFT) : tags :20:/:25:/:28C:/:60F:/:61:/:86:/:62F:,
    soldes opening/closing, communication structurée ?20-?33
  - CAMT.053 (ISO 20022) : namespace-agnostic, Bal OPBD/CLBD,
    Ntry avec AcctSvcrRef/AddtlNtryInf
  - OFX (STMTTRN : DTPOSTED/TRNAMT/FITID/NAME/MEMO)
  - QIF (!Type:Bank, D/T/P/M/^)
  - CSV piloté par template : mapping colonnes 0-based, délimiteur,
    encodage, format de date, séparateurs décimaux/milliers,
    colonne D/C avec marqueur
- Templates par banque sauvegardés et réutilisables
- Flux guidé : upload → Parse File → aperçu → Import Lines
- Détection de doublons SHA-256 (journal+date+montant+référence)
  contre l'historique du journal et le lot courant, option force-import
- Création account.bank.statement + lignes, soldes depuis MT940/CAMT
- Multi-devises : foreign_currency_id si devise active différente
- Résolution partenaire par nom exact
- Historique des runs avec stats (parsed, duplicates, net) et lien statement
- Multi-sociétés par record rule sur la société du journal
- 2 groupes de sécurité (User / Manager), séquence BIMP/

### Technique
- Modèles : sf.bank.stmt.template, sf.bank.stmt.run,
  sf.bank.stmt.line.preview
- Parsers purs Python stdlib (re, csv, xml.etree, hashlib, datetime)
- Dépendances : base, account, mail
- Vues : list, form, kanban
- Parsers validés offline sur échantillons réels des 5 formats
