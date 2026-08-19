# PIM — Product Information Management

Central reference for all product information: families and
enriched attributes, completeness scoring, validation workflow
and publication per channel, integrated with Odoo products.

## Features

- Product families (categories) with structured attributes
- Product completeness score (0-100) with configurable threshold
- Validation workflow: draft / in_review / approved / published / archived
- Publication per channel (web, marketplace, catalogue) with
  reversible withdrawal
- Review history of validations and rejections
- Product translations by language (translatable attributes)
- Quality dashboard (graph / pivot)

## Installation

Copy the module to your addons path, update the app list and
install **PIM — Product Information Management**.

## Configuration

Assign the groups in Settings > Users:

- **PIM User**: create and enrich product sheets, submit for review.
- **PIM Manager**: validation (approve/reject), families, attributes,
  channels, publications, configuration.

Company settings (Settings > PIM):
- Minimum completeness threshold required for publication.

## Usage

1. Create PIM families and their required attributes.
2. Create publication channels (web, marketplace, catalogue).
3. Open a product and fill the PIM tab: family, attributes, media.
4. Submit for review, then approve (manager).
5. Publish the approved product on a channel.
6. The quality dashboard shows completeness by family and status.

## Permissions

- `sf_product_pim.group_pim_user` — read/write limited.
- `sf_product_pim.group_pim_manager` — full access.
- Multi-company record rules restrict users to their company.

## Dependencies

- base
- product
- mail

## Compatibility

Odoo 18.0 and 19.0 (Community and Enterprise).