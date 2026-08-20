CPQ for Custom Products
========================

Configure-to-order engine for custom products in Odoo. Create attribute
groups with options, price adjustments, saved configurations and generate
quotations directly from a configuration.

Features
--------
* Attribute groups with options per product
* Price adjustments computed from selected options
* Configuration records saved and reusable
* Quote generation from a configuration
* Versioned configurations per product

Requirements
------------
* Odoo 18.0 / 19.0 with Sales (sale) and Product (product) modules.

Installation
------------
* Copy the module folder into your addons path.
* Install "CPQ for Custom Products".

Usage
-----
1. Configure attributes and their options under *CPQ > Attributes*.
2. Link a product to its attributes under *CPQ > Configurators*.
3. Create a configuration under *CPQ > Configurations*, select the options
   and the quantity; the price is computed automatically.
4. Press *Generate Quote* to create a sale order for the configured product.

Support
-------
* Email: tech5262@gmail.com