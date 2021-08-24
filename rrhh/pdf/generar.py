from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

data = [
    ['titulo1','titulo2','titulo3','titulo4'],
    ['$100/10','$200/20','$300/30','$300/30'],
    ['Free','20%','50%','100%'],
    ['Oka-san','RTX GeoForce','(insert animal) Girl','One-san']
]
fileName = 'priceTable.pdf'

pdf = SimpleDocTemplate(
    fileName,
    pagesizes=letter
)
pdf.setTitle('tabla 0001')

table = Table(data)
# en corrdinada -1 es ultimo

# configura table y title
style = TableStyle([
    ('BACKGROUND', (0,0), (3,0), colors.green),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('GRID', (0,0), (-1,-1), 2, colors.black)
])
# altelna color en tbody
rowNumb = len(data)
for i in range(1, rowNumb):
    if i % 2 == 0:
        bc = colors.burlywood
    else:
        bc = colors.beige

    ts = TableStyle([
        ('BACKGROUND', (0,i), (-1,i), bc),
        
    ])
    table.setStyle(ts)


table.setStyle(style)

# borde
# ts = TableStyle([
#         ('BOX', (0,0), (-1,-1), 2, colors.black),
#         ('LINEBEFORE', (2,1), (2,-1), 2, colors.red),
#         ('LINEABOVE', (0,2), (-1,2), 2, colors.green),
#         ('GRID', (0,1), (-1,-1), 2, colors.black)
#     ])
# table.setStyle(ts)

elems = []
elems.append(table)
pdf.build(elems)