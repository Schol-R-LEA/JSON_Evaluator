from xlwt import XFStyle, Font, Workbook
import xlwt
import time

filename = "Reports/"+time.strftime("%Y%m%d-%H%M%S")+'_easlo1.xls'
wb = Workbook()
sheet1 = wb.add_sheet('Test')


global valColuna, valRow
valColuna = 0
valRow = 0

def savetoxls(jsonresponse):

    #  set the font
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True  # bold
    font.name = 'Times New Roman'  # select the font
    font.underline = False  # font underline
    font.italic = False  # italics
    font.height = 300  # the font size
    font.colour_index = 4  # the font color ::1-branco, 2-vermelho, 3-verde, 4-azul
