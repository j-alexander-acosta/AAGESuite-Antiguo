/**
 * Created by moltark on 01-08-17.
 */

const accionInsumoFormID = '#accionInsumoFormID';
const editarAccionInsumoFormID = '#editarAccionInsumoFormID';
const nuevaEstrategiaFormID = '#nuevaEstrategiaFormID';
const nuevoIndicadorFormID = '#nuevoIndicadorFormID';
const editarAccionInsumoModal = '#editarAccionInsumo';
const urlDetalleObjetivo = url_prefix + "/insumos/(id_insumo)/objetivo/(id_objetivo)/iniciativas/";
const urlAccionInsumoFormulario = url_prefix + `/insumos/objetivo/accionInsumoFormulario/`;
const urlObjetivoEstrategiasIndicadores = url_prefix + `/insumos/areaestrategica/objetivo/(id_objetivo)/estrategias-indicadores/`;
const urlAccionInsumoEliminar = url_prefix + '/insumos/accioninsumo/eliminar/';
const urlAccionInsumoEditar = url_prefix + '/insumos/objetivo/editarAccionInsumo/';

function verDetalleObjetivo(boton) {
    let inputs = boton.find('input');
    let idObjetivo = $(inputs[0]).val();
    let idInsumo = $(inputs[1]).val();

    let ruta = urlDetalleObjetivo.replace(
        '(id_insumo)',
        idInsumo
    ).replace(
        '(id_objetivo)',
        idObjetivo
    );
    cargarRuta(ruta);
}

function listarAcciones(data, contenedor) {
    let accionesInsumo = data['accionInsumo'];
    let tabla = '';
    for (let i=0; i< data.accionInsumo_len; i++) {
        let inicio_contenido = `<tr id="accion_${accionesInsumo[i][0]}">
                            <td name="estrategia">${accionesInsumo[i][1]}</td>
                            <td name="indicador">${accionesInsumo[i][2]}</td>`;
        let botones = '';
        if (!data['es_dirplac_lectura']) {
            botones = `<td>
                        <div class="btn-group">
                            <button name="editar_accion_insumo" class="btn btn-sm btn-info">
                                <i class="fa fa-edit"></i>
                                <input type="hidden" name="accion_insumo" value="${accionesInsumo[i][0]}">
                                <input type="hidden" name="objetivo" value="${data.objetivo_id}">
                            </button>
                            <button name="eliminar_accion_insumo" class="btn btn-sm btn-danger">
                                <i class="fa fa-trash"></i>
                                <input type="hidden" name="accion_insumo" value="${accionesInsumo[i][0]}">
                                <input type="hidden" name="mensaje_eliminacion"
                                    value="Esta seguro de eliminar la relación <strong>${accionesInsumo[i][1]}</strong>
                                    - <strong>${accionesInsumo[i][2]}</strong>">
                            </button>
                        </div>
                    </td>`;
        }
        let fin_contenido = '</tr>';
        tabla += inicio_contenido + botones + fin_contenido;
    }

    $(contenedor).find('#contenido').append(tabla);
}

function agregarAccionInsumo(data) {
    let contenido = `<tr id="accion_${data.id}">
                        <td name="estrategia">${data.estrategia}</td>
                        <td name="indicador">${data.indicador}</td>
                        <td>
                        <div class="btn-group">
                            <button name="editar_accion_insumo" class="btn btn-sm btn-info">
                                <i class="fa fa-edit"></i>
                                <input type="hidden" name="accion_insumo" value="${data.id}">
                                <input type="hidden" name="objetivo" value="${data.objetivo_id}">
                            </button>
                            <button name="eliminar_accion_insumo" class="btn btn-sm btn-danger">
                                <i class="fa fa-trash"></i>
                                <input type="hidden" name="accion_insumo" value="${data.id}">
                                <input type="hidden" name="mensaje_eliminacion"
                                        value="Esta seguro de eliminar la relación <strong>${data.estrategia}</strong>
                                         - <strong>${data.indicador}</strong>">
                            </button>
                        </div></td>
                    </tr>`;
    $('tbody[id="contenido"]').append(contenido);
}

function submitAccionInsumoForm(form, id_objetivo){
    form.prepend(`<input type="hidden" name="id_objetivo" value="${id_objetivo}" id="id_objetivo">`);
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
            if (!(data['success'])) {
                if(data['form_html'] !== null){
                    form.replaceWith(data['form_html']);
                    $('.chosen').chosen();
                    alertify.error(data['message']);
                }
            }
            else {
                agregarAccionInsumo(data);
                $('[id^=nuevaAccionInsumo_]').collapse('hide');
                alertify.success(data['message']);
            }
        },
        error: function () {
            alertify.error("Ocurrio un error inesperado..");
        }
    });
}

function agregarFormulario(id_objetivo, id_insumo, contenedor) {
    $.post(urlAccionInsumoFormulario, { id_objetivo: id_objetivo, id_insumo: id_insumo })
        .done(function( data ) {
            $(contenedor).html(data.form);
            // activar chosen
            $('.chosen').chosen();
        });
}

function nuevaEstrategia(){
    $('#nuevaEstrategia').modal('show');
}

function nuevoIndicador(){
    $('#nuevoIndicador').modal('show');
}

function agregarOpcionEstrategia(data) {
    let opcion = `<option value="${data.id}" selected>${data.estrategia}</option>`;
    let estrategia_select = $(accionInsumoFormID).find('select[name="estrategia"]');
    estrategia_select.append(opcion);
}

function agregarOpcionIndicador(data) {
    let opcion = `<option value="${data.id}" selected>${data.indicador}</option>`;
    let indicador_select = $(accionInsumoFormID).find('select[name="indicador"]');
    indicador_select.append(opcion);
}

function generarDetalleObjetivo(idObjetivo){
    let itemObjetivo = $(`#linkObjetivo_${idObjetivo}`);
    if(itemObjetivo){
        // quitar class active de los list group
        $('[id^=linkObjetivo_]').each(function () {
            $(this).removeClass('list-group-item-secondary active');
        });

        itemObjetivo.addClass('list-group-item-secondary active');
        let idArea = itemObjetivo.parent().attr('id').split('_')[1];
        let contenidoOculto = `#contenidoOculto_${idArea}`;
        let contenidoObjetivo = `#contenidoObjetivo_${idArea}`;
        let estrategiasIndicadores =urlObjetivoEstrategiasIndicadores.replace(
            '(id_objetivo)',
            idObjetivo
        );

        $.get(estrategiasIndicadores).done(function( data ) {
            $(contenidoOculto).css('display', '');
            $(contenidoObjetivo).find('#contenido').html('');
            $(contenidoObjetivo).find('h3 span').text(data.objetivo);
            $(contenidoObjetivo).find('h6').text(data.objetivo_nombre);
            $(contenidoObjetivo).find('input[name="objetivo"]').val(idObjetivo);
            $('#nuevaEstrategia').find('input[name="objetivo_estrategico"]').val(idObjetivo);
            $('[id^=nuevaAccionInsumo_]').collapse('hide');
            listarAcciones(data, contenidoObjetivo);
        });
    }
}

function reemplazarAccion(data){
    let tabla = $(document).find('.table-responsive');
    let registro = tabla.find(`#accion_${data.accion}`);
    registro.find('td[name="estrategia"]').html(data['estrategia']);
    registro.find('input[name="mensaje_eliminacion"]').val(
        `Esta seguro de eliminar la relación <strong>${data.estrategia}</strong> - <strong>${data.indicador}</strong>`
    );
    registro.find('td[name="indicador"]').html(data['indicador']);
}

$(function () {

    // detalle Objetivo
    $(document).on('click', '[id^=linkObjetivo_]', function () {
        $(document).find('div[id="mensaje_vacio"]').hide();
        let idObjetivo = $(this).attr('id').split('_')[1];
        generarDetalleObjetivo(idObjetivo);
    });

    $('button[name="nuevaaccioninsumo"]').on('click', function() {
        let idContenedor = $(this).attr('data-target');
        let idObjetivo = $(this).find('input[name="objetivo"]').val();
        let idInsumo = $(this).find('input[name="insumo"]').val();
        agregarFormulario(idObjetivo, idInsumo, idContenedor);
    });

    $(document).on('click', 'button[name="eliminar_accion_insumo"]', function () {

        let botonEliminar = $(this);
        let idAccionInsumo = botonEliminar.find('input[name="accion_insumo"]').val();
        let mensajeEliminacion = botonEliminar.find('input[name="mensaje_eliminacion"]').val();

        alertify.confirm("Confirmar Eliminación", mensajeEliminacion, function(){
            $.post(urlAccionInsumoEliminar, { id_accion_insumo: idAccionInsumo }).done(function(data) {
                if(data['success']){
                    let item = botonEliminar.parents(`#accion_${idAccionInsumo}`);
                    item.remove();
                    alertify.success(data['message']);
                }else{
                    alertify.warning(data['message']);
                }
            }).fail(function () {
                alertify.warning(`Ocurrio un error inesperado..`);
            });
        }, function(){
            alertify.warning('Cancelado');
        }).set('labels', {ok:'Eliminar', cancel:'Cancelar'});
    });

    $(document).on('click', 'button[name="editar_accion_insumo"]', function () {
        let id_accion = $(this).find('input[name="accion_insumo"]').val();
        let id_objetivo = $(this).find('input[name="objetivo"]').val();
        $.get(urlAccionInsumoEditar, {id_accion: id_accion, id_objetivo: id_objetivo}).done(function( data ) {
            if(data['success']){
                $(document).find(editarAccionInsumoModal).find('.modal-body').html(data['form_html']);
                $(document).find(editarAccionInsumoModal).find('button[type="submit"]').append(
                    `<input type="hidden" name="id_objetivo" value="${id_objetivo}" id="id_objetivo">
                     <input type="hidden" name="accion" value="${id_accion}" id="accion">`
                );
                $(document).find(editarAccionInsumoModal).modal('show');
                $(document).find('.chosen').chosen({width: '100%'});
            }else{
                alertify.warning(data['message']);
            }
        });
    });

    $(document).on('submit', editarAccionInsumoFormID, function (e){
        e.preventDefault();
        let form = $(this);
        let id_accion = $(this).find('input[name="accion_insumo"]').val();
        let id_objetivo = $(this).find('input[name="objetivo"]').val();
        form.prepend(`<input type="hidden" name="id_objetivo" value="${id_objetivo}" id="id_objetivo">
            <input type="hidden" name="accion" value="${id_accion}" id="accion">`
        );
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                if (!(data['success'])) {
                    alertify.error(data['message']);
                }
                else {
                    $('div[class="modal fade show"]').modal('hide');
                    reemplazarAccion(data);
                    alertify.success(data['message']);
                }
            },
            error: function () {
                alertify.error("Ocurrio un error inesperado..");
            }
        });
    });

    $(document).on('submit', accionInsumoFormID, function (e){
        e.preventDefault();
        let id_objetivo = $(this).parent().parent().find('input[name="objetivo"]').val();
        submitAccionInsumoForm($(this), id_objetivo);
    });

    $(document).on('submit', nuevaEstrategiaFormID, function (e){
        e.preventDefault();
        let form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                if (!(data['success'])) {
                    if(data['form_html'] !== null){
                        form.find('#div_form').replaceWith(data['form_html']);
                        $('.chosen').chosen();
                        alertify.error(data['message']);
                    }
                }
                else {
                    alertify.success(data['message']);
                    $('div[class="modal fade show"]').modal('hide');
                    form.find('textarea').val('');
                    form.find('select option:selected').removeAttr("selected");
                    $(accionInsumoFormID).find('select[name="estrategia"]').chosen('destroy');
                    agregarOpcionEstrategia(data);
                    // crear chosen
                    $('.chosen').chosen();
                }
            },
            error: function () {
                alertify.error("Ocurrio un error inesperado..");
            }
        });
    });

    $(document).on('submit', nuevoIndicadorFormID, function (e){
        e.preventDefault();
        let form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data) {
                if (!(data['success'])) {
                    if(data['form_html'] !== null){
                        form.find('#div_form').replaceWith(data['form_html']);
                        alertify.error(data['message']);
                    }
                }
                else {
                    alertify.success(data['message']);
                    $('div[class="modal fade show"]').modal('hide');
                    form.find('textarea').val('');
                    $(accionInsumoFormID).find('select[name="indicador"]').chosen('destroy');
                    agregarOpcionIndicador(data);
                    // crear chosen
                    $('.chosen').chosen();
                }
            },
            error: function () {
                alertify.error("Ocurrio un error inesperado..");
            }
        });
    });

    // Actualizar detalle de objetivo por url hash
    $(window).on('load', function(e){
        // do something...
        let hash = window.location.hash;
        if(hash.indexOf("#objetivo_") !== -1){
            let idObjetivo = hash.split('_')[1];
            let idArea = hash.split('_')[3];
            // abrir tab correspondiente
            $(`#areasTabs a[href="#areaInsumo_${idArea}"]`).tab('show');
            generarDetalleObjetivo(idObjetivo);
        }
    });

});