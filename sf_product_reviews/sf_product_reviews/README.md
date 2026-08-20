# SF Product Reviews

E-commerce Product Reviews &amp; Ratings module for Odoo 18.

## Features

- Customer reviews with rating (1-5), title, comment and optional author.
- Moderation workflow: draft, submitted, approved, rejected, archived.
- Verified purchase detection from confirmed sales orders.
- Aggregated average rating and review count per product (approved reviews only).
- Configurable moderation: when moderation is disabled, reviews above the approval threshold are auto-approved.
- Product form extension showing the rating summary and the reviews.
- Multi-company support with record rules per company.
- QWeb PDF report: Product Review Summary.

## Configuration

In Settings &gt; Product Reviews you can configure:

- Moderation required (if disabled, reviews are auto-approved when above the threshold).
- Approval threshold (rating above which auto-approval applies).

## Usage

1. Create a review for a product (rating, title, comment, optional customer).
2. Submit the review; a manager approves or rejects it.
3. Approved reviews feed the product average rating and count.
4. The verified purchase flag is set when the customer has a confirmed order containing the product.
5. Print the Review Summary report for a review.

## Permissions

- `sf_product_reviews.group_sf_product_reviews_user` - create, submit and view reviews.
- `sf_product_reviews.group_sf_product_reviews_manager` - approve, reject and archive reviews.

## Dependencies

`base`, `mail`, `product`, `sale`, `contacts`.

## Support

For questions, bug reports or feature requests, contact tech5262@gmail.com.