from odoo import models, fields, api

#class algoritma_pembelian(models.Model):
class AccountMove(models.Model):
    _inherit = 'account.move'

    test = fields.Char(string='test', default="New") # Char untuk String
    
    def export_invoice_csv(self):
        record_ids = self.ids if hasattr(self, 'ids') else [self.id]
        
        return {
            'type': 'ir.actions.act_url',
            'url': '/efaktur/efaktur_csv?id=%s' % ','.join(str(id) for id in record_ids),
            'target': 'new'
        }