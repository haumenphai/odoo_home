import collections

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'
    merge_invoice_line_ids = fields.One2many('account.move.line', 'move_id', string='Merge invoice lines')

    def merge(self):
        self.ensure_one()
        invoice_length = len(self.invoice_line_ids)
        print('self.invoice_line_ids', self.invoice_line_ids)

        invoice_lines = self.invoice_line_ids

        for i in range(0, invoice_length - 1):
            for j in range(i + 1, invoice_length):
                if (invoice_lines[i].product_id == invoice_lines[j].product_id
                        and invoice_lines[i].price_unit == invoice_lines[j].price_unit
                        and invoice_lines[i].tax_ids == invoice_lines[j].tax_ids):
                    print('aaaaaaa')

                    self.write({
                        'merge_invoice_line_ids': [
                            (1, invoice_lines[i].id, {
                            'price_unit': invoice_lines[i].price_unit + invoice_lines[j].price_unit,
                            'quantity': invoice_lines[i].quantity + invoice_lines[j].quantity
                            }),
                            (2, invoice_lines[j].id, 0)
                        ]
                    })
                    invoice_length -= 1

        print('a1', self.invoice_line_ids)
        print(self.merge_invoice_line_ids)
        # print('a2', self.merge_invoice_line_ids)


        # print(self.merge_invoice_line_ids[0].price_unit)
        # print(self.invoice_line_ids[0].price_unit)
        # self.invoice_line_ids = invoice_lines

