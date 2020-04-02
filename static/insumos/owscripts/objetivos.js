/**
 * Created by moltark on 26-07-17.
 */

const nuevoObjetivoEstrategicoFormID = '#nuevoObjetivoEstrategicoFormID';
const ID_CONTENIDO_MODAL = "#modalObjetivoContenidoEditarID";
const objetivoFormEditarID = "#objetivoFormEditarID";
const URL_OBJETIVO_ELIMINAR = url_prefix + "/insumos/areaestrategica/objetivo/eliminar/";
const URL_EDITAR_OBJETIVO = url_prefix + '/insumos/areaestrategica/objetivo/(id_objetivo)/editar/';
const URL_DETALLE_OBJETIVO= url_prefix + '/insumos/(id_insumo)/objetivo/(id_objetivo)/iniciativas/';
const URL_OBJETIVO_EDITAR = url_prefix + `/insumos/areaestrategica/objetivo/(id_objetivo)/editar/`;

function obtenerItemObjetivo(data, urlDetalleObjetivo, urlEditarObjetivo) {
    return `<a id="linkObjetivo_${data.id}" class="list-group-item" href="#objetivo_${data.id}">
                        ${data.objetivo_abrev}
                        <div class="btn-group pull-right p-0 m-0">
                            <button name="detalle_objetivo" class="btn btn-sm btn-warning" 
                               onclick="cargarRuta('${urlDetalleObjetivo}')">
                                <i class="fa fa-eye"></i>
                            </button>
                            <button name="editar_objetivo" class="btn btn-sm btn-info" 
                                href="${urlEditarObjetivo}">
                                <i class="fa fa-edit"></i>
                            </button>
                            <button name="eliminar_objetivo" class="btn btn-sm btn-danger">
                                <i class="fa fa-trash"></i>
                                <input type="hidden" name="objetivo_id" value="${data.id}">
                                <input type="hidden" name="mensaje_eliminacion" 
                                value="Está seguro de eliminar el objetivo estratégico: 
                                <strong> ${data.objetivo_abrev} </strong>">
                            </button>
                        </div>
                    </a>`;
}


function agregarObjetivo(modalid, data){
    let id = modalid.split('_')[1];
    let listaobetivos = '#listaObjetivos_' + id;
    let urlEditarObjetivo = URL_EDITAR_OBJETIVO.replace('(id_objetivo)', data['id']);
    let urlDetalleObjetivo = URL_DETALLE_OBJETIVO.replace(
        '(id_insumo)',
        data['id_insumo']
    ).replace(
        '(id_objetivo)',
        data['id']
    );
    let objetivo = obtenerItemObjetivo(data, urlDetalleObjetivo, urlEditarObjetivo);
    $(listaobetivos).append(objetivo);
}

function crearModalEdicion(titulo, form_html, id_modal, id_contenido_modal) {
    let id_modal_div = id_modal.split("#")[1];
    let modalHtml = `
        <div class="modal fade show" id="${id_modal_div}" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${titulo}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        ${form_html}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-dark" data-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>`;

    $(id_contenido_modal).html(modalHtml);
    $(id_modal).modal('show');
}

function editarObjetivo(data, id_lista_objetivos) {
    let item = $(id_lista_objetivos).find(`#linkObjetivo_${data.id}`);
    let urlEditarObjetivo = URL_EDITAR_OBJETIVO.replace('(id_objetivo)', data['id']);
    let urlDetalleObjetivo = URL_DETALLE_OBJETIVO.replace(
        '(id_insumo)',
        data['id_insumo']
    ).replace(
        '(id_objetivo)',
        data['id']
    );
    item.replaceWith(
        obtenerItemObjetivo(
            data,
            urlDetalleObjetivo,
            urlEditarObjetivo
        ));
}

function submitObjetivoForm(form){
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
            if (!(data['success'])) {
                if(data['form_html'] !== null){
                    if (data['editar']) {
                        form.replaceWith(data['form_html']);
                    }else{
                        form.find('#div_id_objetivo').replaceWith(data['form_html']);
                    }
                    alertify.warning(data['message']);
                }
            }
            else {
                if (data['editar']){
                    let id_tab_area = $(document).find('div[class="tab-pane active"]').attr('id');
                    let id_lista_objetivos = "#listaObjetivos_" + id_tab_area.split('_')[1];
                    editarObjetivo(data, id_lista_objetivos );
                    $('[id^=contenidoOculto_]').css('display', 'none');
                    alertify.success(data['message']);
                }else {
                    let modal = form.parent().parent().parent().attr('id');
                    agregarObjetivo(modal, data);
                    form.find('textarea').val('');
                    alertify.success(data['message']);
                }
                $(document).find("div[class='modal fade show']").modal('hide');
            }
        },
        error: function () {
            alertify.warning("Ocurrio un error inesperado..");
        }
    });
}

$(function() {

    // evento Eliminar Objetivo
    $(document).on('click', 'button[name="eliminar_objetivo"]', function () {

        let botonEliminar = $(this);
        let idObjetivo = botonEliminar.find('input[name="objetivo_id"]').val();
        let mensajeEliminacion = botonEliminar.find('input[name="mensaje_eliminacion"]').val();

        alertify.confirm("Confirmar Eliminación", mensajeEliminacion, function(){
            $.post(URL_OBJETIVO_ELIMINAR, { id_objetivo: idObjetivo }).done(function(data) {
                if(data['success']){
                    let item = botonEliminar.parent().parent();
                    item.remove();
                    $('[id^=contenidoOculto_]').css('display', 'none');
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

    // evento Editar Objetivo
    $(document).on('click', 'button[name="editar_objetivo"]', function () {
        let botonEditar = $(this);
        let idObjetivo = botonEditar.parent().find('input[name="objetivo_id"]').val();
        let urlObjetivoEditar = URL_OBJETIVO_EDITAR.replace(
            '(id_objetivo)',
            idObjetivo
        );
        // obtener formulario
        $.get(urlObjetivoEditar)
            .done(function( data ) {
                crearModalEdicion(
                    `Editar objetivo estratégico <strong>${idObjetivo}</strong>`,
                    data['form_html'],
                    `#modalID_${idObjetivo}`,
                    ID_CONTENIDO_MODAL
                );
            });
    });

    // submit formulario objetivoEditar
    $(document).on('submit', objetivoFormEditarID, function (e) {
        e.preventDefault();
        submitObjetivoForm($(this));
    });

    // submit formulario objetivoNuevo
    $(document).on('submit', nuevoObjetivoEstrategicoFormID, function (e){
        e.preventDefault();
        submitObjetivoForm($(this));
    });

    // filtrar objetivos
    $('input[name="objetivo_search"]').keyup(function () {
        let value = $(this).val();
        let listado = $(this).parent().parent().parent().find('.list-group').attr('id');
        $(`#${listado} a`).each(function () {
            if ($(this).text().toUpperCase().search(value.toUpperCase()) < 0 ) {
                $(this).css('display', 'none');
            }else{
                $(this).show();
            }
        });
    });

});
