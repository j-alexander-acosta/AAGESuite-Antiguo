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


class DetalleContrato:

    def header(canvas,pdf):

        fecha = datetime.now().strftime("%d de %B de %Y")

        canvas.saveState()
        canvas.setFont('Times-Roman',11)
        canvas.drawCentredString(300, 750, "FUNDACIÓN EDUCACIONAL ARNALDO SALAMANCA CID")
        canvas.setFont('Times-Roman',9)
        canvas.drawCentredString(300, 740, "Con Personalidad Jurídica inscrita en el Registro Nacional de Personas Jurídicas sin Fines de Lucro,")
        canvas.drawCentredString(300, 730, "Nº de inscripción 193474 del "+fecha)

        # TODO optimizar  usuando el path del img 
        # p = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        canvas.drawImage('/code/rrhh/static/rrhh/img/EduAdvContrato.jpg', 50, 730, 2*cm, 2*cm)
        canvas.restoreState()
    
    def footer(canvas,pdf):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(50, 30, "Contrato de Trabajo")
        canvas.drawString(500, 30, "Página %d de 2" % pdf.page )
        canvas.restoreState()

    def numero_to_letras(numero):

        indicador = [("",""),("MIL","MIL"),("MILLON","MILLONES"),("MIL","MIL"),("BILLON","BILLONES")]
        entero = int(numero)
        decimal = int(round((numero - entero)*100))
        #print 'decimal : ',decimal 
        contador = 0
        numero_letras = ""
        while entero >0:
            a = entero % 1000
            if contador == 0:
                en_letras = DetalleContrato.convierte_cifra(a,1).strip()
            else :
                en_letras = DetalleContrato.convierte_cifra(a,0).strip()
            if a==0:
                numero_letras = en_letras+" "+numero_letras
            elif a==1:
                if contador in (1,3):
                    numero_letras = indicador[contador][0]+" "+numero_letras
                else:
                    numero_letras = en_letras+" "+indicador[contador][0]+" "+numero_letras
            else:
                numero_letras = en_letras+" "+indicador[contador][1]+" "+numero_letras
            numero_letras = numero_letras.strip()
            contador = contador + 1
            entero = int(entero / 1000)
        numero_letras = numero_letras #+" con " + str(decimal) +"/100"
        return numero_letras
 
    def convierte_cifra(numero,sw):

        lista_centana = ["",("CIEN","CIENTO"),"DOSCIENTOS","TRESCIENTOS","CUATROCIENTOS","QUINIENTOS","SEISCIENTOS","SETECIENTOS","OCHOCIENTOS","NOVECIENTOS"]
        lista_decena = ["",("DIEZ","ONCE","DOCE","TRECE","CATORCE","QUINCE","DIECISEIS","DIECISIETE","DIECIOCHO","DIECINUEVE"),
                        ("VEINTE","VEINTI"),("TREINTA","TREINTA Y "),("CUARENTA" , "CUARENTA Y "),
                        ("CINCUENTA" , "CINCUENTA Y "),("SESENTA" , "SESENTA Y "),
                        ("SETENTA" , "SETENTA Y "),("OCHENTA" , "OCHENTA Y "),
                        ("NOVENTA" , "NOVENTA Y ")
                    ]

        lista_unidad = ["",("UN" , "UNO"),"DOS","TRES","CUATRO","CINCO","SEIS","SIETE","OCHO","NUEVE"]
        centena = int (numero / 100)
        decena = int((numero -(centena * 100))/10)
        unidad = int(numero - (centena * 100 + decena * 10))

        #print "centena: ",centena, "decena: ",decena,'unidad: ',unidad
        texto_centena = ""
        texto_decena = ""
        texto_unidad = ""

        #Validad las centenas
        texto_centena = lista_centana[centena]
        if centena == 1:
            if (decena + unidad)!=0:
                texto_centena = texto_centena[1]
            else :
                texto_centena = texto_centena[0]
    

        #Valida las decenas
        texto_decena = lista_decena[decena]
        if decena == 1 :
            texto_decena = texto_decena[unidad]
        elif decena > 1 :
            if unidad != 0 :
                texto_decena = texto_decena[1]
            else:
                texto_decena = texto_decena[0]
        #Validar las unidades
        #print "texto_unidad: ",texto_unidad
        if decena != 1:
            texto_unidad = lista_unidad[unidad]
            if unidad == 1:
                texto_unidad = texto_unidad[sw]

        return "%s %s %s" %(texto_centena,texto_decena,texto_unidad)

    def contrato(contrato):
        pdf=BaseDocTemplate(
                'DetalleContato.pdf',
                pagesize=letter
            )
        
        frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height, id='normal')

        pdf.addPageTemplates([
            PageTemplate(id='contenido', frames=frame, onPage = DetalleContrato.header, onPageEnd = DetalleContrato.footer),
        ])

        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name = "stylesTitle", alignment=1, fontSize=20, fontName="Times-Roman", underlineProportion=1))
        styles.add(ParagraphStyle(name = "normal", alignment=0, fontSize=11, fontName="Times-Roman", leftIndent=0, rightIndent=0))
        styles.add(ParagraphStyle(name = "normal-bold", alignment=0, fontSize=11, fontName="Times-Bold", textTransform='uppercase'))

        story = []

        textTitle = 'CONTRATO DE TRABAJO DOCENTE'
        story.append(NextPageTemplate('contenido'))
        data = Paragraph(textTitle, styles['stylesTitle'])
        story.append(data)
        story.append(Spacer(0,10))

        # if contrato.tipo_contrato == 1:
            # subTitle = contrato.tipo_contrato
            # data = Paragraph('Indefinido'.upper(), styles['stylesTitle'])
            # story.append(data)

        if contrato.tipo_contrato == 2:
            subTitle = contrato.tipo_contrato
            data = Paragraph('A plazo fijo'.upper(), styles['stylesTitle'])
            story.append(data)

        if contrato.tipo_contrato == 3:
            subTitle = contrato.tipo_contrato
            data = Paragraph('Reemplazo'.upper(), styles['stylesTitle'])
            story.append(data)
    
        story.append(Spacer(0,20))


# contrato.funcionario.persona.ciudad.nombre


        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        textLines = 'En '+contrato.funcionario.persona.ciudad.nombre+' a <b>'+fecha_actual+'</b>  entre la '
        upcase = ('FUNDACIÓN EDUCACIONAL '+contrato.colegio.fundacion.nombre+'').upper()
        textLines = textLines + '<u><b>"'+upcase+'"</b></u>,'
        textLines = textLines + ' R.U.T. 65.102.261-4, Persona Jurídica de Derecho privado,'
        textLines = textLines + ' concedida mediante Decreto Nº 193474 de fecha 4 de marzo de 2015 del Ministerio de Justicia, en adelante, '
        fecha_nace = contrato.funcionario.persona.fecha_nacimiento.strftime("%d de %B de %Y")
        textLines = textLines + ' “La Fundación Educacional Arnaldo Salamanca”, representada legalmente por don ERWIN ALEJANDRO JEREZ CACERES,'
        textLines = textLines + ' Profesor, C.I. y  Rut Nº 12.674.856-6, ambos con domicilio en calle 14 de febrero, Nº 2784, Antofagasta y'
        textLines = textLines + ' don (a) <b>'+contrato.funcionario.persona.get_name.upper()+'</b>, '+contrato.funcionario.persona.estado_civil+', R.U.T. '+contrato.funcionario.persona.rut+', '
        textLines = textLines +contrato.funcionario.persona.nacionalidad+', nacido el '+fecha_nace+','
        textLines = textLines + ' domiciliado en '+contrato.funcionario.persona.direccion+', '+contrato.funcionario.persona.ciudad.nombre+','
        textLines = textLines + ' en adelante, “'+contrato.funcion_principal.nombre+', se ha convenido el siguiente contrato de trabajo:'
        
        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        textLines = '<u><b>PRIMERO</b></u>: La Fundación Educacional, en su carácter de Persona Jurídica de Derecho Privado, suscribe el presente contrato representado'
        textLines = textLines + ' legalmente por este acto por el Representante Legal miembro de la Junta Directiva. Por otra parte al Docente se le'
        textLines = textLines + ' obliga a desempeñar con esmero y responsabilidad sus funciones, aportando sus conocimientos y experiencia, '
        textLines = textLines + ' procurando cumplir con máxima eficiencia los objetivos que se le asigne, dentro del marco de las políticas y '
        textLines = textLines + ' metas de la Fundación Educacional Arnaldo Salamanca.'
        
        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        textLines = '<u><b>SEGUNDO</b></u>: El profesional de la Educación antes individualizado se obliga a desempeñar las funciones de <b>'+contrato.funcion_secundaria.nombre.upper()+'</b>'
        textLines = textLines + ' del Colegio Adventista de Arica, ubicado en Aida N° 5501, Arica en conformidad con lo dispuesto en el'
        textLines = textLines + ' Artículo 6º del D.F.L Nº 1 de 1996 del Ministerio de Educación, entendiéndose dentro de aquellas la'
        textLines = textLines + ' Docencia de aula, definidas como la acción o exposición personal directa realizada en forma continua y'
        textLines = textLines + ' sistemática por el docente, inserta dentro del proceso educativo y las Actividades Curriculares no'
        textLines = textLines + ' lectivas que son aquellas labores educativas complementarias de la función docente de aula, tales como'
        textLines = textLines + ' administración de la educación; actividades anexas o adicionales a la función docente propiamente tal;'
        textLines = textLines + ' jefatura de curso; actividades coprogramáticas y culturales; reunión de apoderados; actividades extraescolares;'
        textLines = textLines + ' actividades vinculadas con organismos o acciones propias del quehacer escolar; actividades vinculadas con'
        textLines = textLines + ' organismos o instituciones del sector que incidan directa o indirectamente en la educación y las'
        textLines = textLines + ' análogas que sean establecidas por un decreto del Ministerio de Educación.'

        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))
        

        horas_total = str(contrato.horas_total)
        textLines = '<u><b>TERCERO</b></u>: El docente desempeñará sus funciones en el establecimiento educacional denominado Colegio Adventista de Arica'
        textLines = textLines + ' y tendrá una jornada ordinaria de trabajo de <b>'+horas_total+'</b> hrs. Cronológicas semanales constituidas por horas de docencia de aula'
        textLines = textLines + '  y actividades curriculares no lectivas. Las horas serán distribuidas de acuerdo a los calendarios confeccionados'
        textLines = textLines + '  en el mes de marzo de cada año y se anexarán a presente contrato debidamente firmado por las partes.'

        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        textLines = '<u><b>CUARTO</b></u>: Cuando por razones fundadas el docente deba desarrollar horas extraordinarias, éstas deberán ser  previa y expresamente'
        textLines = textLines + ' autorizadas por la Fundación Educacional. No se considerarán para ningún efecto como horas extraordinarias,'
        textLines = textLines + ' las funciones que el docente deba desarrollar con ocasión de la recuperación de horas de clases,' 
        textLines = textLines + ' cuando estas se originen por motivos que no sean imputables al empleador.'

        story.append(PageBreak())
        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        numm = 2154654
        strinng = str(numm)
        numero = strinng.replace('.','').replace(',','')
        num_letra = 'valor'
        # num_letra = DetalleContrato.numero_to_letras(numero)
        textLines = '<u><b>QUINTO</b></u>: La Fundación Educacional se compromete a remunerar al Trabajador con la suma de $'+strinng+'.- ('+num_letra+' pesos) mensuales,'
        textLines = textLines + ' como sueldo base (equivalente a la RBMN por horas de contrato), correspondientes a <b>'+horas_total+'</b> horas cronológicas semanales mensuales.'
        textLines = textLines + ' Cancelará además como parte de sus remuneraciones las siguientes asignaciones al docente:<br /><br />'
        textLines = textLines + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-    Bono Zona 40% sobre RBMN.<br />'
        textLines = textLines + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-    Ley 19410 y 19933.<br />'
        textLines = textLines + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-    Bono de Reconocimiento Profesional<br /><br />'
        textLines = textLines + 'El docente tendrá derecho a recibir una asignación de movilización que tendrá un tope de  $21.500.- (veintiún mil quinientos pesos) mensuales,'
        textLines = textLines + ' la cual será cancelada mensualmente o en los periodos que determine el empleador durante el período lectivo. Esta asignación no constituye remuneración para ningún efecto.'

        data = Paragraph(textLines, styles['normal'])
        story.append(data)
        story.append(Spacer(0,10))

        pdf.build(story)