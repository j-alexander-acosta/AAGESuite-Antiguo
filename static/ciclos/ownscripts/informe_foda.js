/*
* Creado por Alexis 11-10-2017
*/

const idModalCrear = '#crearInformeFODA';
const idFormNuevo = '#nuevoInformeFODAFormID';
const idModalEliminar = '#eliminarInformeFODA';
const idFormEliminar= '#eliminarInformeFODAFormID';
const URL_INFORMEFODA_ELIMINAR = url_prefix + '/informefoda/eliminar/';
const idFormEditar = '#editarInformeFODAFormID';
const URL_INFORMEFODA_EDITAR = url_prefix + '/informefoda/editar/';
const URL_INFORMEFODA_FINALIZAR = url_prefix + '/informefoda/finalizar/';
const URL_INFORMEFODA_HABILITAR = url_prefix + '/informefoda/habilitar/';
const URL_ANALISIS_FODA = url_prefix + '/unidades/(id_unidad)/ciclo/(id_ciclo)/foda/';

function submitInformeFODAForm(form){
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
            if (!(data['success'])) {
                if(data['form_html'] !== null){
                    form.replaceWith(data['form_html']);
                    alertify.warning(data['message']);
                }
            }
            else {
                $(document).find("div.modal.fade.show").modal('hide');
                alertify.success(data['message']);
                $(document).find("div.modal.fade.show").modal('hide');
                    let url = URL_ANALISIS_FODA.replace(
                        '(id_unidad)',
                        data['unidad']
                    ).replace(
                        '(id_ciclo)',
                        data['ciclo']
                    );
                    window.location.replace(url + `#${data.tipo}-tab`);
                    window.location.reload();
            }
        },
        error: function () {
            alertify.warning("Ocurrio un error inesperado..");
        }
    });
}

$(function () {

    let url = window.location.href;
    if ( url.indexOf("#") > -1 ) {
        let tab = url.split('#')[1].split('-')[0];
        $(document).find(`#nav-${tab}`).tab('show');
    }

    $(document).on('click', '[id^=nuevoInformeFODAButton]', function() {
        let button = $(this);
        let tipo = button.find('input[name="tipo"]').val();
        let ciclo_calidad_id = button.find('input[name="cicloCalidad"]').val();
        let modal = $(document).find(idModalCrear);
        modal.find('.modal-title').html(`Nueva ${tipo}`);
        modal.find('input[name="tipo"]').val(tipo);
        modal.find('input[name="ciclo_calidad"]').val(ciclo_calidad_id);
        modal.find('textarea[name="contenido"]').val('');
        modal.modal('show');
    });

    $(document).on('submit', idFormNuevo, function (e){
        e.preventDefault();
        submitInformeFODAForm($(this));
    });

    $(document).on('click', '[id^=eliminarInformeFODAButton]', function() {
        let button = $(this);
        let informeFODAId = button.find('input[name="informeFODA"]').val();
        let informeFODAContenido = button.find('input[name="contenido"]').val();
        let modal = $(document).find(idModalEliminar);
        modal.find('#title').html(`Eliminar ${informeFODAId}`);
        modal.find('em').html(informeFODAContenido);
        modal.find('input[name="informeFODAId"]').val(informeFODAId);
        modal.modal('show');
    });

    $(document).on('submit', idFormEliminar, function (e){
        e.preventDefault();
        let informeFODAId = $(this).find('input[name="informeFODAId"]').val();
        $.post(URL_INFORMEFODA_ELIMINAR, { id_informe_foda: informeFODAId }).done(function(data) {
                if(data['success']){
                    alertify.success(data['message']);
                    $(document).find("div.modal.fade.show").modal('hide');
                    let url = URL_ANALISIS_FODA.replace(
                        '(id_unidad)',
                        data['unidad']
                    ).replace(
                        '(id_ciclo)',
                        data['ciclo']
                    );
                    window.location.replace(url + `#${data.tipo}-tab`);
                    window.location.reload();
                }else{
                    alertify.warning(data['message']);
                }
            }).fail(function () {
                alertify.warning(`Ocurrio un error inesperado..`);
            });
    });

    $(document).on('click', '[id^=editarInformeFODAButton]', function() {
        let button = $(this);
        let informeFODAId = button.find('input[name="informeFODA"]').val();
        let modal = $(document).find(idModalCrear);
        modal.find('.modal-title').html(`Editar ${informeFODAId}`);
        $.get(URL_INFORMEFODA_EDITAR, { informe_foda_id: informeFODAId }).done(function( data ) {
            modal.find('.modal-body').html(data['form_html']);
            modal.find('form').append(`<input type="hidden" name="informeFODA" value="${informeFODAId}">`);
        });
        modal.modal('show');
    });

    $(document).on('submit', idFormEditar, function (e){
        e.preventDefault();
        let informeFODAId = $(this).find('input[name="informeFODA"]').val();
        let contenido = $(this).find('textarea[name="contenido"]').val();
        $.post(URL_INFORMEFODA_EDITAR, { id_informe_foda: informeFODAId, contenido: contenido }).done(function(data) {
                if(data['success']){
                    alertify.success(data['message']);
                    $(document).find("div.modal.fade.show").modal('hide');
                    let url = URL_ANALISIS_FODA.replace(
                        '(id_unidad)',
                        data['unidad']
                    ).replace(
                        '(id_ciclo)',
                        data['ciclo']
                    );
                    window.location.replace(url + `#${data.tipo}-tab`);
                    window.location.reload();
                }else{
                    alertify.warning(data['message']);
                }
            }).fail(function () {
                alertify.warning(`Ocurrio un error inesperado..`);
            });
    });

    $(document).on('click', '[id^=finalizarInformeFODAButton]', function (e){
        e.preventDefault();
        let tipo = $(this).find('input[name="tipo"]').val();
        console.log(tipo);
        let cicloCalidad = $(this).find('input[name="cicloCalidad"]').val();
        $.post(URL_INFORMEFODA_FINALIZAR, { ciclo_calidad: cicloCalidad, tipo: tipo }).done(function(data) {
                if(data['success']){
                    alertify.success(data['message']);
                    let url = URL_ANALISIS_FODA.replace(
                        '(id_unidad)',
                        data['unidad']
                    ).replace(
                        '(id_ciclo)',
                        data['ciclo']
                    );
                    window.location.replace(url + `#${data.tipo}-tab`);
                    window.location.reload();
                }else{
                    alertify.warning(data['message']);
                }
            }).fail(function () {
                alertify.warning(`Ocurrio un error inesperado..`);
            });
    });

    $(document).on('click', '[id^=habilitarInformeFODAButton]', function (e){
        e.preventDefault();
        let tipo = $(this).find('input[name="tipo"]').val();
        let cicloCalidad = $(this).find('input[name="cicloCalidad"]').val();
        $.post(URL_INFORMEFODA_HABILITAR, { ciclo_calidad: cicloCalidad, tipo: tipo }).done(function(data) {
                if(data['success']){
                    alertify.success(data['message']);
                    let url = URL_ANALISIS_FODA.replace(
                        '(id_unidad)',
                        data['unidad']
                    ).replace(
                        '(id_ciclo)',
                        data['ciclo']
                    );
                    window.location.replace(url + `#${data.tipo}-tab`);
                    window.location.reload();
                }else{
                    alertify.warning(data['message']);
                }
            }).fail(function () {
                alertify.warning(`Ocurrio un error inesperado..`);
            });
    });

});