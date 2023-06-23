from odoo import models, fields, api

class algoritma_pembelian(models.Model):
    # apa bedanya dengan menggunakan transient model???
    _inherit = 'algoritma.pembelian'

    def custom_button(self):
        # ambil buttonnya doang

        return{
            'type': 'ir.actions.act_url',
            'url': '/algoritma_pembelian/algoritma_pembelian_report_csv/%s' % (self.id),
            'target': 'new'
        }
    