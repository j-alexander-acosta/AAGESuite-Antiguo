/**
 * Created by javie on 12-07-2017.
 */

const nuevaAreaInsumoFormID = '#nuevaAreaInsumoFormID';
const ID_TABLE_BODY = '#sortable';
const ID_SELECT_MULTIPLE = '#selectMultipleAreasEstrategicas';
const ID_TAB_CONFIGURACION_AREAS = '#tabsConfiguracionAreas';
const nuevaAreaEstrategicaFormID = '#nuevaAreaEstrategicaFormID';
const SelectAreas = ID_SELECT_MULTIPLE;
const modalNuevaAreaEstrategica = '#ModalAgregarAreaEstrategica';
const URL_NUEVA_AREA_INSUMO = url_prefix + '/insumos/nueva/area_insumo/';

function actualizarOpcionSeleccionadaEnTabla(){
    // opciones seleccionadas
    let opciones = [];
    let eliminarFilas = [];
    let opcionesHTML = '';
    let tabla = $(ID_TABLE_BODY);
    // largo de itemes en tabla
    let largo_itemes = 0;

    // Obtener opciones de selector multiple
    $(this).find(':selected').each(function () {
        let opcion = {
            idArea: $(this).val(),
            nombre: $(this).text()
        };
        opciones.push(opcion);
    });

    // Eliminar posibles filas no seleccionadas en tabla
    $(ID_TABLE_BODY).find('tr').each(function () {
        let idArea = $(this).find('input').val();
        let eliminarFila = true;
        $.each(opciones, function (index, opcion) {
            if(opcion.idArea === idArea){
                eliminarFila = false;
            }
        });

        if(eliminarFila){
            $(this).remove();
        }
    });

    // Determinar el largo de filas de la tabla
    largo_itemes = $(ID_TABLE_BODY).find('tr').length;

    // Generar codigo html de fila
    $.each(opciones, function (index, opcion) {
        if(!existeIdAreaTabla(ID_TABLE_BODY, opcion['idArea'])){
            // si area estrategica no ha sido agregada
            opcionesHTML += crearHtmlFila(opcion['idArea'], opcion['nombre'], largo_itemes);
            largo_itemes += 1;
        }
    });

    // Agregar filas nuevas a tabla
    tabla.append(opcionesHTML);

    // Actualizar ID de filas
    let orden_areas = $("#sortable").find("input[name*='-id_area_estrategica']");
    $.each(orden_areas, function (index, input) {
        let id_input = "#" + input['id'];
        let orden = index + 1;
        let input_orden = $(id_input);
        let parent_input = input_orden.parent();
        parent_input.find('td').html(orden);
        input_orden.val(index + 1);
    });
}

function activarTabConfiguracionAreas(posicion) {
    $(`${ID_TAB_CONFIGURACION_AREAS} a:${posicion}`).tab('show');
}

function crearHtmlFila(id_area, nombre, largo_filas){
    let opcion = `
        <tr style="cursor:pointer">
            <input type="hidden" name="id_area_estrategica" value="${id_area}">
            <input type="hidden" name="orden" value="${largo_filas + 1}">
            <td><span>${largo_filas + 1}</span></td>
            <td>${nombre}</td>
        </tr>
    `;
    return opcion
}

function existeIdAreaTabla(id_tabla, idArea) {
    let existe = false;
    $(id_tabla).find('tr').each(function () {
        if ($(this).find('input').val() === idArea){
            existe = true;
        }
    });

    return existe;
}

function actualizarOrdenOpcion(indice, opcion) {
    let input = $(opcion).find('input[name="orden"]');
    let td = $(opcion).find('td')[0];
    let orden  = indice + 1;
    $(input).val(orden);
    $(td).html(`<span>${orden}</span>`);
}


$(function() {
    //
    $('#areasTabs').on('click', function() {
        $('[id^=linkObjetivo_]').removeClass('list-group-item-secondary active');
        $('[id^=contenidoOculto_]').hide();
        $(document).find('div[id="mensaje_vacio"]').show();
    });

    // generar Nueva Estrategia
    $(document).on('submit', nuevaAreaEstrategicaFormID, function (e) {
        e.preventDefault();
        let form = $(this);

        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: form.serialize(),
            success: function(data) {
                if (!(data['success'])) {
                    if(data['form_html'] !== null){
                        form.replaceWith(data['form_html']);
                        mostrarNotificacionGrowl(data['message'], 'error');
                    }else{
                        mostrarNotificacionGrowl(data['message'], 'error');
                    }
                }
                else {
                    // hide modal
                    $(modalNuevaAreaEstrategica).modal('hide');
                    // add new area to select multiple
                    let option = `<option value="${data['id_area']}" selected>${data['area_estrategica']}</option>`;
                    $(SelectAreas).chosen('destroy');
                    $(SelectAreas).append(option);
                    $(SelectAreas).chosen({width: '100%'});
                    // Avisar de nuevo item registrado a parte de ordenamiento
                    $(SelectAreas).trigger("change");
                    // show message success
                    mostrarNotificacionGrowl(data['message'], 'success');
                }
            },
            error: function () {
                mostrarNotificacionGrowl('Ocurrio un error inesperado', 'error');
            }
        });
    });

    // Actualizar Opciones
    $(ID_SELECT_MULTIPLE).change(actualizarOpcionSeleccionadaEnTabla).change();

    $(ID_TABLE_BODY).sortable({
        update: function(event, ui) {
            // actulizar indices
            //Obtener todos los tr del tbody con id="sortable"
            let opciones = $(ID_TABLE_BODY).find('tr');
            //iterar por cada tr
            opciones.each(actualizarOrdenOpcion);
        },
    });
    $(ID_TABLE_BODY).sortable('toArray');

    // enviar Configuracion de areas al servidor
    $(document).on('submit', nuevaAreaInsumoFormID, function (e) {
        e.preventDefault();
        $(this).find('tr').each(function () {
            let id_area = $(this).find('input[name= "id_area_estrategica"]').val();
            let orden = $(this).find('input[name= "orden"]').val();
            let id_insumo = $(this).parent().find('input[name= "insumo"]').val();
            console.log(id_area + " " + id_insumo + " " + orden);
            $.post(URL_NUEVA_AREA_INSUMO, {
                id_insumo: id_insumo,
                id_area: id_area,
                orden: orden
            }).done(function (data) {
                window.parent.location.reload(true);
            });
        });
    });

});

