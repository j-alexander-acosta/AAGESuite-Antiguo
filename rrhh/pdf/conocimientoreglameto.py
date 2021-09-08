from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, BaseDocTemplate, Frame, NextPageTemplate, PageTemplate
from sqlite3 import connect
from datetime import date, datetime
from rrhh.models.colegio import ContratoColegio
import os


class TomaConocimientoReglamentoInterno:

    def reglamento(contrato):

        pdf=BaseDocTemplate(
                'ConocimientoReglamentoInterno.pdf',
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
        data = Paragraph('Toma de conocimiento del', styles['stylesTitle'])
        story.append(data)
        story.append(Spacer(0,10))
        data = Paragraph('reglamento interno.', styles['stylesTitle'])
        story.append(data)
        story.append(Spacer(0,30))

        textLines = '&nbsp;&nbsp;Yo, <b>'+contrato.funcionario.persona.get_name+'</b>'
        textLines = textLines + ' para estos efectos domiciliado(a) en <b>'+contrato.funcionario.persona.direccion+'</b>,'
        textLines = textLines + ' R.U.T. <b>'+contrato.funcionario.persona.rut+'</b>,'
        textLines = textLines + ' Tomo conocimiento del reglamento interno del <b>'+contrato.colegio.nombre+'</b>'
        textLines = textLines + ' y declaro que el colegio facilito y/o me entrego una copia del texto del reglamento para su respectiva consulta.'

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