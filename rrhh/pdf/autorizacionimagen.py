from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, BaseDocTemplate, Frame, NextPageTemplate, PageTemplate
from sqlite3 import connect
from datetime import date, datetime
from rrhh.models.entidad import Contrato
import os


class AutorizacionImagen:

    def imagen(contrato):

        pdf=BaseDocTemplate(
                'Autorizacionimagen.pdf',
                pagesize=letter
            )
        
        frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id='normal')


        pdf.addPageTemplates([
            PageTemplate(id='contenido', frames=frame),
        ])

        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name = "stylesTitle", alignment=1, fontSize=14, fontName="Times-Bold"))
        styles.add(ParagraphStyle(name = "normal", alignment=0, fontSize=11, fontName="Times-Roman", leading=20))
        styles.add(ParagraphStyle(name = "normal-bold", alignment=0, fontSize=11, fontName="Times-Bold", textTransform='uppercase'))
        
        story = []

        story.append(NextPageTemplate('contenido'))
        data = Paragraph('Autorización para el uso de imágenes', styles['stylesTitle'])
        story.append(data)
        story.append(Spacer(0,10))
        data = Paragraph('y/o testimonio.', styles['stylesTitle'])
        story.append(data)
        story.append(Spacer(0,20))

        textLines = '&nbsp;&nbsp;Yo, <b>'+contrato.funcionario.persona.get_name+'</b>'
        textLines = textLines + ' para estos efectos domiciliado(a) en <b>'+contrato.funcionario.persona.direccion+'</b>,'
        textLines = textLines + ' R.U.T. <b>'+contrato.funcionario.persona.rut+'</b>,'
        textLines = textLines + ' autorizo voluntariamente el uso de su imagen y/o testimonio.'

        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        textLines = 'En razón de lo anterior accedo a que mi representado sea entrevistado, fotografiado y/o grabado en video,'
        textLines = textLines + ' comprometiéndome a que toda la información escrita, fotografías, videos o cualquier otro material que se obtenga de él,' 
        textLines = textLines + ' en el proceso de realización de videos, documentos, afiches, gigantografías, cuadros, pendones, página web y'
        textLines = textLines + ' otros elementos en el marco de la difusión de las políticas, beneficios y programas,'
        textLines = textLines + ' serán de exclusiva propiedad del <b>'+contrato.entidad.nombre+'</b>, y no me serán devueltos, pudiendo éste utilizarlos libremente.'

        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,50))

        textLines = '&nbsp;&nbsp;'* 55
        textLines = textLines + '........................................'
        textLines = textLines + '&nbsp;&nbsp;'* 70
        textLines = textLines + '(Firma)'

        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        data = Paragraph(fecha_actual, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        pdf.build(story)