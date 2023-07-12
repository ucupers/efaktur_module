from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError, UserError

import xlrd, base64, os

class AccountMove(models.Model):
    # apa bedanya dengan menggunakan transient model??? -> dbnya secara perodik dihapus
    # klo bukan disini, pindahin semua aja sak class classnya soalnya ni id nempel ke data record kan?
    _inherit = 'account.move'    
    

    def export_efaktur_csv(self):
        
        # raise exception
        if self.filtered(lambda x: not x.l10n_id_tax_number):
            raise UserError(_('Some records don\'t have a Tax Number (nomor faktur)'))
        if self.filtered(lambda x: x.move_type not in ['out_invoice', 'in_invoice', 'out_refund', 'in_refund']):
            raise UserError(_('Some records are not Faktur'))
        if self.filtered(lambda x: x.move_type != self[0].move_type):
            raise UserError(_('Some records are not the same type with the others'))
        if self.filtered(lambda x: x.state != 'posted'):
            raise UserError(_('Some records is not in the posted state yet'))
        

        record_ids = self.ids if hasattr(self, 'ids') else [self.id]

        return {
            'type': 'ir.actions.act_url',
            'url': '/efaktur/efaktur_'+ str(self[0].move_type) +'_csv?id=%s' % ','.join(str(id) for id in record_ids), # + '&company_id='+str(self[0].env.company.id)
            'target': 'new'
        }