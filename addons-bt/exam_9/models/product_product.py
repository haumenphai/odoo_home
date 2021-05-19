from odoo import models


class Product(models.Model):
    _inherit = 'product.product'

    def _compute_product_price_extra(self):
        for r in self:
            price_extra = 0
            product_template_attribute_value_ids = r.product_template_attribute_value_ids
            value_ids = product_template_attribute_value_ids.exclude_for.value_ids

            for product_template_attribute_value_id in product_template_attribute_value_ids:
                if product_template_attribute_value_id in value_ids:
                    price_extra = 0
                    break
                else:
                    price_extra += product_template_attribute_value_id.price_extra
            r.price_extra = price_extra
