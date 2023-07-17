from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import float_round
from datetime import date
import io
import csv

# Header faktur
RM_HEADER_RETUR_MASUK = ["RM","NPWP","NAMA","KD_JENIS_TRANSAKSI","FG_PENGGANTI","NOMOR_FAKTUR","TANGGAL_FAKTUR","IS_CREDITABLE","NOMOR_DOKUMEN_RETUR","TANGGAL_RETUR","MASA_PAJAK_RETUR","TAHUN_PAJAK_RETUR","NILAI_RETUR_DPP","NILAI_RETUR_PPN","NILAI_RETUR_PPNBM"]

class ReportCSVEfakturKeluaranController(http.Controller):
    @http.route('/efaktur/efaktur_in_refund_csv', http='http', auth='user', csrf=False)
    def retur_masuk_report_csv(self, **kwargs):
        data_ids = kwargs.get('id')

        # handle header dari httprequest
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/csv'),
                # Untuk nama filenya ditentukan di bawah ini (yg 'efaktur') 
                ('Content-Disposition', content_disposition('retur_masuk_'+ str(date.today()).replace("-", "_") + '.csv'))
            ]
        )

        # Prepare output variable to store content
        output = io.StringIO()
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\n',quotechar = "'")

        # write header
        csv_writer.writerow(RM_HEADER_RETUR_MASUK)
        if data_ids: # check if data_ids not empty
            id_list = data_ids.split(',')  # Split the comma-separated IDs into a list
            
            for data_id in id_list:
                datarm = {}

                # Retrieve the record using the ID (in odoo, invoices and others stored in 1 table, account_move)
                move = request.env['account.move'].search([('id', '=', int(data_id))])
                datarm["RM"] = "RM"
                datarm["NPWP"] = '"' + str(move.partner_id.vat) + '"'
                datarm["NAMA"] = '"' + str(move.partner_id.name if datarm['NPWP'] == '000000000000000' else move.partner_id.l10n_id_tax_name or move.partner_id.name) + '"'
                datarm["KD_JENIS_TRANSAKSI"] = '"' + str(move.l10n_id_tax_number[0:2] or 0) + '"' # fix this part when the real taxid column added
                datarm["FG_PENGGANTI"] = '"' + str(move.l10n_id_tax_number[2:3] or 0) + '"' # fix this part when the real taxid column added
                datarm["NOMOR_FAKTUR"] = '"' + str(move.l10n_id_tax_number[3:] or 0) + '"' # fix this part when the real taxid column added
                datarm["TANGGAL_FAKTUR"] = "0" # perbaiki mintanya nanti
                datarm["IS_CREDITABLE"] = '"' + str('{0}/{1}/{2}'.format(move.invoice_date.day, move.invoice_date.month, move.invoice_date.year)) + '"'
                datarm["NOMOR_DOKUMEN_RETUR"] = "RM" #PENTING INI APA
                datarm["TANGGAL_RETUR"] = '"' + str('{0}/{1}/{2}'.format(move.date.day, move.date.month, move.date.year)) + '"'
                datarm["MASA_PAJAK_RETUR"] = '"' + str(move.date.month) + '"'
                datarm["TAHUN_PAJAK_RETUR"] = '"' + str(move.date.year) + '"'
                datarm["NILAI_RETUR_DPP"] = '"' + str(int(float_round(move.amount_untaxed, 0))) + '"'
                datarm["NILAI_RETUR_PPN"] = '"' + str(int(float_round(move.amount_tax, 0, rounding_method="DOWN"))) + '"'
                datarm["NILAI_RETUR_PPNBM"] = "0"
                csv_writer.writerow(datarm.values())

        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response