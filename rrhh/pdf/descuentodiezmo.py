from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from sqlite3 import connect
from datetime import date, datetime
from rrhh.models.colegio import ContratoColegio

class DescuentoDiezmo:

    def diezmo(contrato):
        pdf=SimpleDocTemplate(
            'DescuentoDiezmo.pdf',
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=20,
            bottomMargin=18,
        )

        stylesTitle = ParagraphStyle(
                name='Normal',
                fontName='Times-Roman',
                fontSize=20,
                textColor= 'black',
                alignment=1, # 0 left, 1 center, 2 right
                textTransform=None,   # 'uppercase' | 'lowercase' | None
            )
        textTitle = 'Declaración Jurada<br /><br /><br /><br />'

        stylesText = ParagraphStyle(
                name='Normal',
                fontName='Times-Roman',
                fontSize=12,
                textColor= 'black',
                leading=24
            )

        dt = datetime.now().strftime("%d, %B %Y")

        textLines = ''
        textLines = textLines + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Quien suscribe, '+contrato.funcionario.persona.get_name
        textLines = textLines + ' de Nacionanlidad '+contrato.funcionario.persona.nacionalidad+', estado civil '+contrato.funcionario.persona.estado_civil+','
        textLines = textLines + ' con un a función de '+contrato.funcion_principal.nombre+', Rut '+contrato.funcionario.persona.rut+','
        textLines = textLines + ' con domicilio en '+contrato.funcionario.persona.direccion+' de la cuidad  de '+contrato.funcionario.persona.ciudad.nombre+'.'
        textLines = textLines + ' Declara que autorizo(a) a contar de esta fecha, que mi emplador la "Corporacion Iglesia Adventista"'
        textLines = textLines + ' descuenta el 10%'
        textLines = textLines + ' de mi suledo imponible, por concepto de donación de carácter religioso en calidad de diezmo,'
        textLines = textLines + ' para el sostenimiento de la obra de evanggelización que realiza la Iglesia Adventistas del Séptimo Día,'
        textLines = textLines + ' de la cual soy miembro. A su vez manifiesto que tengo pleno conocimiento de mis derechos laborales,'
        textLines = textLines + ' en especial las normas sobre descuento a las remuneración,'
        textLines = textLines + ' contenidas en artíclo 58 del código del Trabajo.'
        textLines = textLines + '<br /><br /><br />'
        textLines = textLines + dt+'<br /><br /><br /><br />'
        textLines = textLines + contrato.funcionario.persona.rut+'<br />'
        textLines = textLines + 'RUT'


        elems = []

        texto=Paragraph(textTitle, stylesTitle)
        elems.append(texto)

        texto=Paragraph(textLines, stylesText)
        elems.append(texto)
        

        pdf.build(elems)