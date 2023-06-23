from odoo import models, fields, api

class algoritma_pembelian(models.Model):
    # apa bedanya dengan menggunakan transient model???
    _inherit = 'algoritma.pembelian'
    
    def custom_button(self):
        record_ids = self.ids if hasattr(self, 'ids') else [self.id]
        return {
            'type': 'ir.actions.act_url',
            'url': '/algoritma_pembelian/algoritma_pembelian_report_csv?id=%s' % ','.join(str(id) for id in record_ids),
            'target': 'new'
        }