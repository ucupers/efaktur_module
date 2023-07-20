from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import float_round
from datetime import date
import io
import csv

# Header faktur
FM_HEADER_FAKTUR_MASUK = ["FM","KD_JENIS_TRANSAKSI","FG_PENGGANTI","NOMOR_FAKTUR","MASA_PAJAK","TAHUN_PAJAK","TANGGAL_FAKTUR","NPWP","NAMA","ALAMAT_LENGKAP","JUMLAH_DPP","JUMLAH_PPN","JUMLAH_PPNBM","IS_CREDITABLE"]

class ReportCSVEfakturKeluaranController(http.Controller):
    @http.route('/efaktur/efaktur_in_invoice_csv', http='http', auth='user', csrf=False)
    def efaktur_masuk_report_csv(self, **kwargs):
        data_ids = kwargs.get('id')

        # handle header dari httprequest
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/csv'),
                # Untuk nama filenya ditentukan di bawah ini (yg 'efaktur') 
                ('Content-Disposition', content_disposition('efaktur_masuk_'+ str(date.today()).replace("-", "_") + '.csv'))
            ]
        )

        # Prepare output variable to store content
        output = io.StringIO()
        csv_writer = csv.writer(output, delimiter=',', lineterminator='\n',quotechar = "'")
        
        # write header
        csv_writer.writerow(FM_HEADER_FAKTUR_MASUK)
        if data_ids: # check if data_ids not empty
            id_list = data_ids.split(',')  # Split the comma-separated IDs into a list
            
            for data_id in id_list:
                datafm = {}

                # Retrieve the record using the ID (in odoo, invoices and others stored in 1 table, account_move)
                move = request.env['account.move'].search([('id', '=', int(data_id))])
                datafm["FM"] = "FM"
                datafm["KD_JENIS_TRANSAKSI"] = '"' + str(move.l10n_id_tax_number[0:2] or 0) + '"' # fix this part when the real taxid column added
                datafm["FG_PENGGANTI"] = '"' + str(move.l10n_id_tax_number[2:3] or 0) + '"' # fix this part when the real taxid column added
                datafm["NOMOR_FAKTUR"] = '"' + str(move.l10n_id_tax_number[3:] or 0) + '"' # fix this part when the real taxid column added
                datafm["MASA_PAJAK"] = '"' + str(move.invoice_date.month) + '"'
                datafm["TAHUN_PAJAK"] = '"' + str(move.invoice_date.year) + '"'
                datafm["TANGGAL_FAKTUR"] = '"' + str('{0}/{1}/{2}'.format(move.invoice_date.day, move.invoice_date.month, move.invoice_date.year)) + '"'
                datafm["NPWP"] = '"' + str(move.partner_id.vat) + '"'
                datafm["NAMA"] = '"' + str(move.partner_id.name if datafm['NPWP'] == '000000000000000' else move.partner_id.l10n_id_tax_name or move.partner_id.name) + '"'
                datafm["ALAMAT_LENGKAP"] = '"' + str(move.partner_id.contact_address.replace('\n', '') if datafm['NPWP'] == '000000000000000' else move.partner_id.l10n_id_tax_address or move.partner_id.street) + '"'
                datafm["JUMLAH_DPP"] = '"' + str(int(float_round(move.amount_untaxed, 0))) + '"'
                datafm["JUMLAH_PPN"] = '"' + str(int(float_round(move.amount_tax, 0, rounding_method="DOWN"))) + '"'
                datafm["JUMLAH_PPNBM"] = "0"
                datafm["IS_CREDITABLE"] = '"' + str(move.efaktur_is_creditable) + '"'
                csv_writer.writerow(datafm.values())

        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response