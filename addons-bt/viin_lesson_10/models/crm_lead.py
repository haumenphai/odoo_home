from odoo import models, fields


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    company_size = fields.Integer(string="Company Size")

