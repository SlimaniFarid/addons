{
    'name': 'Multi-Channel Returns & RMA Center',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Unified returns portal for eCommerce, POS, B2B, marketplaces with auto-approval rules',
    'description': """Multi-Channel Returns & RMA Center
==================================

Single hub for all return channels.

Features:
- Customer self-service portal (branded, multi-lang)
- Channel-specific rules: eCommerce (30 days), POS (14 days), B2B (contract), marketplace (policy)
- Auto-approval: amount thresholds, reason codes, customer tier, product category
- RMA workflow: receive â†’ inspect â†’ disposition (restock, repair, scrap, return-to-vendor)
- Prepaid label generation (carrier integration: UPS, FedEx, DHL, local)
- Refund/replacement/credit note automation
- Analytics: return rate by product/channel/reason, cost recovery, fraud detection
- Vendor RMA: initiate returns to suppliers from same interface
- Integration: sale.order, pos.order, marketplace connectors, helpdesk

Channels supported:
- Odoo eCommerce, Shopify, WooCommerce, Amazon, POS, manual B2B""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.25,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'stock', 'account', 'delivery'],
    'data': [
        'security/ir.model.access.csv',
        'views/rma_menus.xml',
        'data/rma_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}



