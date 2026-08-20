Safety Stock Optimizer
======================

Compute and maintain optimal safety stock and reorder points in Odoo from
real historical demand.

Features
--------
* Safety stock computed from real historical demand
* Reorder point per product and warehouse
* Suggested order quantity on reorder
* Service level selection (90%, 95%, 99%)
* Alerts for products at or below reorder point
* Demand analysis window configurable per product

Requirements
------------
* Odoo 18.0 / 19.0 with Inventory (stock) module.

Installation
------------
* Copy the module folder into your addons path.
* Install "Safety Stock Optimizer".

Usage
-----
1. Create a rule per product and warehouse under *Inventory > Safety Stock*.
2. Set the service level, demand window and lead time.
3. Safety stock, reorder point and suggested order quantity are computed
   automatically from outgoing moves.
4. Use the *Below Reorder Point* filter to find products to restock.

Support
-------
* Email: tech5262@gmail.com