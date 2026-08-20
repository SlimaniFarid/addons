# SF Digital Delivery

E-commerce Digital Goods &amp; License Key Delivery module for Odoo 18.

## Features

- Digital products linked to saleable products with two delivery types: license key or download link.
- Automatic license key generation with configurable format (e.g. `XXXX-XXXX-XXXX`) and guaranteed uniqueness.
- Expirable download links with validity period and expiry tracking.
- Automatic creation of a digital delivery on sales order confirmation.
- Delivery workflow: draft, generated, delivered, failed, cancelled.
- License key lifecycle: generated, delivered, activated, revoked, expired.
- Activation tracking with a maximum number of activations per key.
- Daily cron that expires non-activated keys and flags expired download links.
- Multi-company support with record rules per company.
- QWeb PDF reports: Digital Delivery and License Key Certificate.

## Configuration

In Settings &gt; Digital Delivery you can configure:

- Default license key format.
- Default download link validity (in days).
- Default key activation delay (in days).

## Usage

1. Create a digital product and link it to a saleable product (license key or download).
2. When a sales order containing digital products is confirmed, a draft delivery is created automatically with one line per product and the ordered quantity.
3. A manager generates the license keys / download links, then delivers the digital goods (a message posts the keys or the link to the order thread).
4. Keys can be activated up to the configured maximum; revoked keys are blocked.
5. The daily cron expires keys that are never activated and raises reminders when download links expire.

## Permissions

- `sf_digital_delivery.group_sf_digital_delivery_user` - view and operate digital products, keys and deliveries.
- `sf_digital_delivery.group_sf_digital_delivery_manager` - key generation, delivery, revocation and failure handling.

## Dependencies

`base`, `mail`, `contacts`, `product`, `sale`.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.