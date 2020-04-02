/*
 * Creado por Alexis 29-08-2017
 */

const URL_NUEVA_INICIATIVA_PROPIA = url_prefix + '/insumos/(id_insumo)/unidad/(id_unidad)/iniciativas/nueva/';
const NUEVA_INICIATIVA_FORM = '#iniciativasPropiasConfigurarForm';
const URL_INICIATIVA_PROPIA_ELIMINAR = url_prefix + '/iniciativaPropia/eliminar/';
const URL_INICIATIVA_EDITAR = url_prefix + '/insumos/iniciativaPropia/(id_iniciativa)/editar/';
const ID_MODAL_EDITAR_CONTENIDO = '#modalEditarIniciativaPropiaContenido';
const ID_MODAL_EDITAR = '#modalEditarIniciativaPropia';

function agregarFormulario(contenedor, idIndicador, idAccion, idUnidad, idInsumo){
    let urlNuevaIniciativaPropia = URL_NUEVA_INICIATIVA_PROPIA.replace(
        '(id_insumo)',
        idInsumo
    ).replace(
        '(id_unidad)',
        idUnidad
    );
    $.get(urlNuevaIniciativaPropia, function(data) {
        $(contenedor).append(data['form_html']);
        $(contenedor).addClass('card-body table-secondary');
        $(contenedor).find('input[name="indicador"]').val(idIndicador);
        $(contenedor).find('input[name="accion"]').val(idAccion);
        $(contenedor).find('input[name="encargados_operativos"]').val(idUnidad);
        /* Ocultar encargados operativos */
        $("#div_id_encargados_operativos").hide();
    }).fail(function() {
        console.log("error");
    });
}

function agregarIniciativa(data, contenedor){
    let item = `<tr id="inicitaiva_${data.id}" class="table-info">
            <td>${data.id}</td>
            <td>${data.iniciativa}</td>
            <td>${data.unidad_medida}</td>
            <td>${data.porcentaje_tributado}</td>
            <td>0.00</td>
            <td>0.00</td>
            <td>
                <div class="btn-group">
                    <input type="hidden" name="iniciativa" value="${data.id}">
                    <button class="btn btn-sm btn-primary" name="editar-iniciativa">
                        <i class="fa fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" name="eliminar-iniciativa">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>`;
    $(contenedor).append(item);
}

function reemplazarIniciativa(data, contenedor){
    let item = `<tr id="iniciativa_${data.id}" class="table-info">
                    <td>${data.id}</td>
                    <td>${data.iniciativa}</td>
                    <td>${data.meta_global}</td>
                    <td>${data.porcentaje_tributado}</td>
                    <td>${data.respuesta_heredada}</td>
                    <td>${data.respuesta}</td>
                    <td>
                        <div class="btn-group">
                            <input type="hidden" name="iniciativa" value="${data.id}">
                            <button class="btn btn-sm btn-primary" name="editar-iniciativa">
                                <i class="fa fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" name="eliminar-iniciativa">
                                <i class="fa fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>`;
    $(contenedor).replaceWith(item);
}

function submitIniciativaForm(form){
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
            if (!(data['success'])) {
                if(data['form_html'] !== null){
                    $(form).replaceWith(data['form_html']);
                    $("#div_id_encargados_operativos").hide();
                    mostrarNotificacionGrowl(
                        data['message'],
                        'danger'
                    );
                }
            }
            else {
                mostrarNotificacionGrowl(
                    data['message'],
                    'success'
                );
                if (data['editar']) {
                    form.parents('div#modalEditarIniciativaPropia').modal('hide');
                    let iniciativa = $(document).find(`tr#iniciativa_${data.id}`);
                    reemplazarIniciativa(data, iniciativa);
                }else{
                    let contenedor = form.parent().parent().find(`tbody#indicador_${data.indicador}`);
                    agregarIniciativa(data, contenedor);
                    form.parent().removeClass();
                    form.remove();
                }
                location.reload();
            }
        },
        error: function () {
            mostrarNotificacionGrowl(
                "Ocurrio un error inesperado..",
                'warning'
            );
        }
    });
}

function modalEditarIniciativa(data){
    let idModal = ID_MODAL_EDITAR.split("#")[1];
    let contenidoModal = `<div class="modal fade show" id="${idModal}" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">Editar Iniciativa Propia<small> ${data.iniciativa} </small></h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    ${data.form_html}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
                </div>
            </div>
        </div>
    </div>`;
    $(ID_MODAL_EDITAR_CONTENIDO).html(contenidoModal);
    $("#div_id_encargados_operativos").hide();
    $(ID_MODAL_EDITAR).modal('show');
}

$(function () {

    /* Nueva Iniciativa */
    $('button[name*="nueva-iniciativa"]').on('click', function (){
        let boton = $(this);
        let idIndicador = boton.find('input[name="indicador"]').val();
        let idAccion = boton.find('input[name="accion"]').val();
        let idUnidad = boton.find('input[name="unidad"]').val();
        let idInsumo = boton.find('input[name="insumo"]').val();
        let contenedor = boton.parent().find(`div#formularioNuevaIniciativa_${idIndicador}`);
        agregarFormulario(contenedor, idIndicador, idAccion, idUnidad, idInsumo);
    });

    /* Escuchar submit para guardar iniciativa propia */
    $(document).on('submit', NUEVA_INICIATIVA_FORM, function (e){
        e.preventDefault();
        submitIniciativaForm($(this));
    });

    /* Cancelar Iniciativa */
    $(document).on('click', `[id*="cancelar_iniciativa"]`, function () {
        let form = $(this).parents('form');
        form.parent().removeClass();
        form.remove();
    });

    /* Editar Iniciativa */
    $(document).on('click', `button[name="editar-iniciativa"]`, function () {
        let id_iniciativa = $(this).parent().find('input[name="iniciativa"]').val();
        let urlIniciativaEditar = URL_INICIATIVA_EDITAR.replace(
            '(id_iniciativa)',
            id_iniciativa
        );
        /* Generar formulario desde servidor (ajax) */
        $.get(urlIniciativaEditar, function (data) {
            if(data['form_html']){
                // crear modal
                modalEditarIniciativa(data);
            }
        });
    });

    /* Eliminar Iniciativa */
    $(document).on('click', `button[name="eliminar-iniciativa"]`, function () {
        let bisabuelo = $(this).parents('tr');
        let id_iniciativa = $(this).parent().find('input[name="iniciativa"]').val();
        alertify.confirm(
            "Confirmar Eliminación",
            `Esta seguro de querer eliminar la iniciativa <strong>${id_iniciativa}</strong>`,
            function(){
                $.post(URL_INICIATIVA_PROPIA_ELIMINAR, { id_iniciativa: id_iniciativa }).done(function(data) {
                    if(data['success']){
                        bisabuelo.remove();
                        alertify.success(data['message']);
                    }else{
                        alertify.warning(data['message']);
                    }

                    document.location.reload();
                }).fail(function () {
                    alertify.warning(`Ocurrio un error inesperado..`);
                });
            }, function(){
                alertify.warning('Cancelado');
            }).set('labels', {ok:'Eliminar', cancel:'Cancelar'});
    });

    $(document).on('input', 'input[name*="meta_"]', function () {
        $("#iniciativasPropiasConfigurarForm").find("input[name='meta_global']").val($(this).val());
    });

});