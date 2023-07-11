from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError

import xlrd, base64, os

class AccountMove(models.Model):
    # apa bedanya dengan menggunakan transient model??? -> dbnya secara perodik dihapus
    # klo bukan disini, pindahin semua aja sak class classnya soalnya ni id nempel ke data record kan?
    _inherit = 'account.move'

    test = fields.Char(string='test', default="New") # Char untuk String
    
    def export_invoice_csv(self):
        record_ids = self.ids if hasattr(self, 'ids') else [self.id]
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/efaktur/efaktur_csv?id=%s' % ','.join(str(id) for id in record_ids),
            'target': 'new'
        }