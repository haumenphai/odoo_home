import collections

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'
    merge_invoice_line_ids = fields.One2many('account.move.line', 'move_id', string='Merge invoice lines',
                                             readonly=True)

    def merge(self):
        self.ensure_one()
        invoice_length = len(self.invoice_line_ids)
        print(self.invoice_line_ids)

        invoice_lines = list(self.invoice_line_ids)
        print(invoice_lines)

        list1 = []
        for r in self.invoice_line_ids:
            list1.append(r.read(['name']))
        print(list1)

        for i in range(0, invoice_length - 1):
            for j in range(i + 1, invoice_length):
                if (invoice_lines[i].product_id == invoice_lines[j].product_id
                        and invoice_lines[i].price_unit == invoice_lines[j].price_unit
                        and invoice_lines[i].tax_ids == invoice_lines[j].tax_ids):
                    print('a')
                    # invoice_lines[i].quantity += invoice_lines[j].quantity
                    # invoice_lines[i].price_unit += invoice_lines[j].price_unit
                    # del invoice_lines[j]
                    # invoice_length -= 1

        print(invoice_lines)

        for r in invoice_lines:
            print('ten:', r.product_id.name, 'sl:', r.quantity, 'tax:', r.tax_ids.name)
