from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError, UserError
import re

import xlrd, base64, os

class AccountMove(models.Model):
    # apa bedanya dengan menggunakan transient model??? -> dbnya secara perodik dihapus
    # klo bukan disini, pindahin semua aja sak class classnya soalnya ni id nempel ke data record kan?
    _inherit = 'account.move'    

    # Attributes
    efaktur_is_creditable = fields.Boolean(string="Is Creditable", store=True, readonly=False)
    efaktur_nomor_retur = fields.Char(string="Nomor Dokumen Retur", store=True, readonly=False)


    @api.constrains('efaktur_nomor_retur')
    def _constraint_nomor_retur_unique(self):
        # check if efaktur_nomor_field is empty
        for record in self:
            if not record.efaktur_nomor_retur:
                raise ValidationError('eFaktur Nomor Retur must be filled for the specific move type.')
        
        # constraint nomor retur must unique   
        for record in self.filtered('efaktur_nomor_retur'):
            if record.search_count([('efaktur_nomor_retur', '=', record.efaktur_nomor_retur)]) > 1:
                raise ValidationError('The eFaktur Nomor Retur must be unique.')
            
    # @api.constrains('efaktur_nomor_retur')
    # def _constraint_nomor_retur


    def export_efaktur_csv(self):
        
        # raise exception 
        if self.filtered(lambda x: not x.l10n_id_tax_number or not x.l10n_id_tax_number): # change what the second bool check using the name of the new attribute 
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
    
class Revisi_Efaktur(models.Model):
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