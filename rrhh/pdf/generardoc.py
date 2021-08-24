from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors

def drawMyRuler(pdf):
    pdf.drawString(100, 0, 'x100')
    pdf.drawString(200, 0, 'x200')
    pdf.drawString(300, 0, 'x300')
    pdf.drawString(400, 0, 'x400')
    pdf.drawString(500, 0, 'x500')
    pdf.drawString(600, 0, 'x600')

    pdf.drawString(0, 100, 'y100')
    pdf.drawString(0, 200, 'y200')
    pdf.drawString(0, 300, 'y300')
    pdf.drawString(0, 400, 'y400')
    pdf.drawString(0, 500, 'y500')
    pdf.drawString(0, 600, 'y600')
    pdf.drawString(0, 700, 'y700')
    pdf.drawString(0, 800, 'y800')
    pdf.drawString(0, 900, 'y900')

# /carga-academica/rrhh/pdf$ python3 ./generardoc.py
pdf = canvas.Canvas('gendoc.pdf', pagesize=A4)
drawMyRuler(pdf)

pdf.setTitle('Titulo 0001')
pdf.drawImage('/home/jorgehalty/Descargas/perrita-shiva-inu-meme-ve-768x768.jpg', 50, 775, 2*cm, 2*cm)
pdf.setFillColorRGB(0,255,0)
pdf.setFont("Times-Roman", 20)
pdf.drawCentredString(300, 800, "¡Hola, mundo!")
# test lista
text = pdf.beginText(50, 750)
text.setFont("Times-Roman", 12)
text.setFillColor(colors.blue)
testLines = [
    '¡Hola, mundo! ¡Desde ReportLab y Python!',
    'esto es un ejemplo AAGE',
    '',
    '                           Saludos'
]
for line in testLines:
    text.textLine(line)
pdf.drawText(text)
# text lista font
text = pdf.beginText(350, 750)
text.setFillColor(colors.black)
for font in pdf.getAvailableFonts():
    text.setFont(font, 10)
    text.textLines(font)
pdf.drawText(text)

pdf.setFillColorRGB(150,0,255)
pdf.setFont("Helvetica", 10)
pdf.drawString(50, 550, "Línea")
pdf.line(50, 540, 500, 500)
pdf.drawString(50, 500, "Rectángulo")
pdf.rect(120, 490, 1*cm, 1*cm)
pdf.drawString(50, 430, "Círculo")
pdf.circle(120, 430, 1*cm)
pdf.drawString(50, 380, "Elipse")
pdf.ellipse(120, 350, 300, 400)

pdf.drawString(50, 310, "Grid")
xlist = [100, 150, 200, 250]
ylist = [200, 250, 300, 350]
pdf.grid(xlist, ylist)

# pdf.showPage()
pdf.save()