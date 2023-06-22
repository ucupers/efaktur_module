from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter

class ReportExcelAlgoritmaPembelianController(http.Controller):
    @http.route(['/algoritma_pembelian/algoritma_pembelian_report_excel/<model("algoritma.pembelian"):data>',], type="http", auth="user", csrf=False)
    def get_algoritma_pembelian_excel_report(self, data=None, **args):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                # Untuk nama filenya ditentukan di bawah ini (yg Algoritma Pembelian Report.xlsx)
                ('Content-Disposition', content_disposition('Algoritma Pembelian Report' + '.xlsx'))
            ]
        )

        # Buat object workbook dari library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Buat style untuk mengatur jenis font, ukuran font, border, dan alignment
        atas_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'align': 'left'})
        atas_isi_style = workbook.add_format({'font_name': 'Times', 'bold': False, 'align': 'left'})
        header_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'left': 1, 'bottom': 1, 'top': 1, 'right': 1, 'align': 'center'})
        text_style = workbook.add_format({'font_name': 'Times', 'bold': False, 'left': 1, 'bottom': 1, 'top': 1, 'right': 1, 'align': 'left'})

        # Looping algoritma pembelian yang dipilih
        for atas in data:
            # Buat worksheet / tab per user
            sheet = workbook.add_worksheet(atas.name)

            # Set orientation jadi landscape
            sheet.set_landscape()

            # Set ukuran kertas jadi A4 (angka 9 -> kertas A4)
            sheet.set_paper(9)

            # Set margin kertas dlm satuan inch
            sheet.set_margins(0.5, 0.5, 0.5, 0.5)

            # Set lebar kolom
            sheet.set_column('A:A', 5)
            sheet.set_column('B:B', 55)
            sheet.set_column('C:C', 40)
            sheet.set_column('D:D', 15)
            sheet.set_column('E:E', 15)
            sheet.set_column('F:F', 25)
            sheet.set_column('G:G', 25)

            # Set judul atas
            sheet.merge_range('A1:B1', 'Name', atas_style)
            sheet.merge_range('A2:B2', 'Tanggal', atas_style)

            # Set isi atas (baris ke-, kolom ke-, isinya apa, stylenya apa)
            sheet.write(0, 2, atas.name, atas_isi_style)
            sheet.write(1, 2, atas.tanggal, atas_isi_style)

            # set judul tabel
            sheet.write(3, 0, 'No', header_style)
            sheet.write(3, 1, 'Product', header_style)
            sheet.write(3, 2, 'Description', header_style)
            sheet.write(3, 3, 'Quantity', header_style)
            sheet.write(3, 4, 'Uom', header_style)
            sheet.write(3, 5, 'Price', header_style)
            sheet.write(3, 6, 'Sub Total', header_style)

            row = 4
            number = 1

            # Cari record data algoritma pembelian line yang dipilih user
            record_line = request.env['algoritma.pembelian.line'].search([('algoritma_pembelian_id', '=', atas.id)])
            for line in record_line:
                # Content / isi table
                sheet.write(row, 0, number, text_style)
                sheet.write(row, 1, line.product_id.display_name, text_style)
                sheet.write(row, 2, line.description, text_style)
                sheet.write(row, 3, line.quantity, text_style)
                sheet.write(row, 4, line.uom_id.name, text_style)
                sheet.write(row, 5, line.price, text_style)
                sheet.write(row, 6, line.sub_total, text_style)

                row += 1
                number += 1
        
        # Memasukkan file excel yang sudah digenerate ke response dan return
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response