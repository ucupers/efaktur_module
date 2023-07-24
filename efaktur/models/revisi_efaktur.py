from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError, UserError
import re

class RevisiEfaktur(models.Model):
    _inherit = "l10n_id_efaktur.efaktur.range"

    @api.depends('company_id')
    def _compute_default(self):
        for record in self:
            query = """
                SELECT MAX(SUBSTRING(l10n_id_tax_number FROM 4))
                FROM account_move
                WHERE l10n_id_tax_number IS NOT NULL
                    AND company_id = %s
                    AND move_type = 'out_invoice'
            """
            self.env.cr.execute(query, [record.company_id.id])
            max_used = int(self.env.cr.fetchone()[0] or 0)
            max_available = int(self.env['l10n_id_efaktur.efaktur.range'].search([('company_id', '=', record.company_id.id)], order='max DESC', limit=1).max)
            record.min = record.max = '%013d' % (max(max_available, max_used) + 1)