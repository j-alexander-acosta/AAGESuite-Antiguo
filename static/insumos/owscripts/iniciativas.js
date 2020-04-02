
const FORM_CONTENT_ID = 'formContentID_';
const BUTTON_NEW_FORM_ID = 'buttonNewFormID_';
const ID_MODAL_EDITAR_CONTENIDO = '#modalEditarIniciativaContenido';
const ID_MODAL_EDITAR = '#modalEditarIniciativa';
const NUEVA_INICIATIVA_FORM = '#iniciativasConfigurarForm';
const URL_INICIATIVA_EDITAR = url_prefix + '/insumos/iniciativa/(id_iniciativa)/editar/';
const URL_INICIATIVA_ELIMINAR = url_prefix + '/insumos/iniciativa/eliminar/';
const URL_NUEVA_INICIATIVA = url_prefix + '/insumos/(id_insumo)/objetivo/(id_objetivo)/iniciativas/nueva/';


function iniciativaTR(data){

    // Es desafio unidad
    let es_desafio_unidad = "";
    if (data['es_desafio_unidad'] === true){
        es_desafio_unidad = `class="${data.es_desafio_unidad}"`;
    }

    let itemTR = `<tr id="iniciativa_${data.id}" ${es_desafio_unidad}>
            <td>${data.id}</td>
            <td><p class="text-primary"> ${data.iniciativa}</p>
                <p class="text-muted"> <em> Linea Base: </em> ${data.linea_base}</p>
             </td>
             <td>
                ${data.encargados_operativos} 
            </td>
            <td>
               <span class="badge badge-pill badge-warning text-white">
                ${data.porcentaje_tributado} %
               </span>
            </td>
            <td>
               <span class="badge badge-pill bgm-lightblue">
                ${data.meta_global} ${data.tipo_medida}
               </span>
            </td>
            <td>
                <div class="btn-group">
                    <input type="hidden" name="iniciativa" value="${data.id}">
                    <button class="btn btn-primary btn-sm" type="button" name="editar-iniciativa">
                        <i class="fa fa-edit"></i>
                    </button>
                    <button class="btn btn-danger btn-sm" type="button" name="eliminar-iniciativa">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>`;

    return itemTR;
}


function agregarIniciativa(data, contenedor){
    $(contenedor).append(iniciativaTR(data));
}

function reemplazarIniciativa(data, contenedor){
    let item = `<tr id="iniciativa_${data.id}">
                    <td>${data.id}</td>
                    <td>${data.iniciativa}</td>
                    <td>${data.porcentaje_tributado}</td>
                    <td>${data.meta_global}</td>
                    <td>
                        <div class="btn-group">
                            <input type="hidden" name="iniciativa" value="${data.id}">
                            <button class="btn btn-primary btn-sm" type="button" name="editar-iniciativa">
                                <i class="fa fa-edit"></i>
                            </button>
                            <button class="btn btn-danger btn-sm" type="button" name="eliminar-iniciativa">
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
                    $('.chosen').chosen();
                    mostrarNotificacionGrowl(
                        data['message'],
                        'danger'
                    );
                }
            }
            else {

                if (data['editar']) {
                    form.parents('div#modalEditarIniciativa').modal('hide');
                }

                /*
                mostrarNotificacionGrowl(
                    data['message'],
                    'success'
                );
                */
                document.location.reload();
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

function agregarFormularioIniciativa(urlNuevaIniciativa, idIndicador, idAccion) {

    const contentFormID = '#' + FORM_CONTENT_ID + idIndicador;
    $.get(urlNuevaIniciativa, function(data) {
        $(contentFormID).append(data['form_html']);
        $(contentFormID).addClass('card-body table-secondary');
        $(contentFormID).find('input[name="indicador"]').val(idIndicador);
        $(contentFormID).find('input[name="accion"]').val(idAccion);
        // activar chosen select
        $('.chosen').chosen();
    }).fail(function() {
        console.log("error");
    });
}

function quitarItem(item){
    $(item).remove();
}

function modalEditarIniciativa(data){
    let idModal = ID_MODAL_EDITAR.split("#")[1];
    let contenidoModal = `<div class="modal fade show" id="${idModal}" tabindex="-1" role="dialog" aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">Editar Iniciativa <small> ${data.iniciativa} </small></h4>
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
    $(ID_MODAL_EDITAR).modal('show');
}

$(function() {
    /* Escuchar por boton de agregar iniciativa */
    $(document).on('click', `[id*=${BUTTON_NEW_FORM_ID}]`, function () {
        const button = $(this);
        const idIndicador = button.attr('id').split('_')[1];
        const idInsumo = button.find('input[name="insumo"]').val();
        const idObjetivo = button.find('input[name="objetivo"]').val();
        const idAccion = button.find('input[name="accion"]').val();
        const urlNuevaIniciativa = URL_NUEVA_INICIATIVA.replace(
            '(id_insumo)',
            idInsumo
        ).replace(
            '(id_objetivo)',
            idObjetivo
        );
        // agregar formulario
        agregarFormularioIniciativa(
            urlNuevaIniciativa,
            idIndicador,
            idAccion
        );
    });

    /* Escuchar submit para guardar iniciativa */
    $(document).on('submit', NUEVA_INICIATIVA_FORM, function (e){
        e.preventDefault();
        submitIniciativaForm($(this));
    });

    /* Cancelar Formulario Nueva Iniciativa */
    $(document).on('click', `[id*="cancelar_iniciativa"]`, function () {
        let form = $(this).parents('form');
        form.parent().removeClass();
        quitarItem(form);
    });

    /* Editar Iniciativa */
    $(document).on('click', `button[name="editar-iniciativa"]`, function () {
        let id_iniciativa = $(this).parent().find('input[name="iniciativa"]').val();
        let urlIniciativaEditar = URL_INICIATIVA_EDITAR.replace(
            '(id_iniciativa)',
            id_iniciativa
        );

        //generar formulario desde servidor (ajax)
        $.get(urlIniciativaEditar, function (data) {
            if(data['form_html']){
                // crear modal
                modalEditarIniciativa(data);
                $('.chosen').chosen({width: '100%'});
            }
        });
    });

    /* Eliminar Iniciativa */
    $(document).on('click', `button[name="eliminar-iniciativa"]`, function () {
        let id_iniciativa = $(this).parent().find('input[name="iniciativa"]').val();
        let boton = $(this);
        alertify.confirm(
            "Confirmar Eliminación",
            `Esta seguro de querer eliminar la iniciativa <strong>${id_iniciativa}</strong>`,
            function(){
                $.post(URL_INICIATIVA_ELIMINAR, { id_iniciativa: id_iniciativa }).done(function(data) {
                    if(data['success']){
                        // actualizar
                        //alertify.success(data['message']);
                        document.location.reload();
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

});
