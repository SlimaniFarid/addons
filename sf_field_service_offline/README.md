# Field Service Offline-First Mobile

True offline-first mobile app for field technicians with background sync

Field Service Offline-First Mobile
=================================

Real offline capability for field technicians - no more paper fallback.

Features:
- SQLite local database on device (Capacitor/Ionic PWA or native wrapper)
- Full work order management offline: tasks, checklists, signatures, photos
- Background sync with conflict resolution (last-write-wins + manual merge)
- GPS location capture, barcode scanning, time tracking offline
- Equipment history, spare parts lookup, manuals cached locally
- Automatic sync when connectivity restored (Wi-Fi preferred)
- Admin dashboard: sync status, conflicts, pending uploads per technician
- Secure: encrypted local storage, token-based auth, remote wipe

Architecture:
- Odoo backend module (this) provides REST API + sync endpoints
- Mobile app built separately (Capacitor/React or Flutter) - API spec included
- Sync protocol: delta sync with vector clocks for conflict detection

Note: This module provides the Odoo backend API. Mobile app template available separately.
