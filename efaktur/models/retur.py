from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError, UserError

import re
import xlrd
import base64
import os

class ReturAccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    efaktur_nomor_retur = fields.Char(string="Nomor Dokumen Retur", readonly=False)
    efaktur_is_creditable = fields.Boolean(string="Is Creditable", readonly=False)

    def _prepare_default_reversal(self, move):
        # Call the original method to get the default values.

        default_values = super(ReturAccountMoveReversal, self)._prepare_default_reversal(move)

        default_values['efaktur_nomor_retur'] = self.efaktur_nomor_retur
        default_values['efaktur_is_creditable'] = self.efaktur_is_creditable
        default_values['l10n_id_tax_number'] = move.l10n_id_tax_number
        
        return default_values
    
    # def _compute_nomor_retur_default()