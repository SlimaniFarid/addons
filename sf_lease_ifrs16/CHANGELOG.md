# Changelog — sf_lease_ifrs16

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Contrats de lease : lessor, catégorie d'actif, dates, terme, paiement
  (montant, fréquence mensuelle/trimestrielle/annuelle, avance/arriérés), IBR
- Composants de mesure initiale : coûts directs, incitatifs, prepaid rent,
  coûts de restauration
- Échéancier PV automatique : intérêts, principal, solde par période
  (méthode du taux d'intérêt effectif)
- ROU asset initial = liability + coûts directs + prepaid + restauration
  − incitatifs ; amortissement linéaire
- Écritures comptables en un clic : intérêts + remboursement principal
  + amortissement ROU + paiement (compte de trésorerie du journal)
- Modifications et réévaluations : re-mesure de la liability restante,
  ajustement ROU, reconstruction de l'échéancier futur, piste d'audit
- Exemptions court terme (<= 12 mois) et faible valeur : charge linéaire
- Rapport PDF échéancier complet avec statut posted par période
- Multi-sociétés (record rules), multi-devises, chatter complet
- 2 groupes de sécurité (User / Manager)
- Séquences LEASE/ et LMOD/

### Technique
- Modèles : sf.lease.contract, sf.lease.payment.line, sf.lease.modification
- Dépendances : base, account, mail
- Vues : list, form, kanban, pivot ; rapport QWeb PDF
