// const RESPUESTA_FORM = '#idRespuestaAutoevaluacionForm';
// const ID_CONTENIDO_RESPUESTA = 'contenidoFormularioRespuesta_';
// const URL_RESPUESTA =  url_prefix + '/autoevaluacion/respuesta/';
// const ID_QUITAR_RESPUESTA_INICIATIVA =  '#quitarRespuestaIniciativa';
// const URL_QUITAR_RESPUESTA = url_prefix + '/autoevaluacion/respuesta/quitar/';
const ID_VALIDAR_RESPUESTA_AUTOEVALUACION =  '#validarRespuestaAutoevaluacion';
const URL_VALIDAR_RESPUESTA = url_prefix + '/autoevaluacion/respuesta/validar/';

// function submitRespuestaForm(form){
//     $.ajax({
//         type: form.attr('method'),
//         url: form.attr('action'),
//         data: form.serialize(),
//         success: function(data) {
//             if (!(data['success'])) {
//                 if(data['form_html'] !== null){
//                     $(form).replaceWith(data['form_html']);
//                     console.log(data['message']);
//                     mostrarNotificacionGrowl(
//                         data['message'],
//                         'danger'
//                     );
//                 }
//             }
//             else {
//                 mostrarNotificacionGrowl(
//                     data['message'],
//                     'success'
//                 );
//                 $(form).parent().parent().parent().addClass('table-success');
//                 $(form).parent().parent().find("div.progress div.progress-bar").css(
//                     'width', `${data.porcentaje_logrado}%`).attr(
//                     'aria-valuenow', `${data.porcentaje_logrado}`).html(
//                     `${data.porcentaje_logrado}%`);
//                 $("#id_avance_autoevaluacion").find("div.progress-bar").css(
//                     'width', `${data.avance_autoevaluacion}%`).attr(
//                     'aria-valuenow', `${data.avance_autoevaluacion}`).html(
//                     `${data.avance_autoevaluacion}%`);
//             }
//         },
//         error: function () {
//             mostrarNotificacionGrowl(
//                 "Ocurrio un error inesperado..",
//                 'warning'
//             );
//         }
//     });
// }


$(function() {
    /*Validar Respuesta de Autoevaluacion*/
    $(document).on('click', ID_VALIDAR_RESPUESTA_AUTOEVALUACION, function (e) {
        let button = $(this);
        let id_ii_cc = button.find("input[name='id_iicc']").val();

        $.get(URL_VALIDAR_RESPUESTA, {'id_ii_cc': id_ii_cc}, function (data) {
            if(data['success']){
                mostrarNotificacionGrowl(
                    data['message'],
                    'success'
                );
                button.closest('tr').addClass('table-success');
                button.closest('td').find("div.progress div.progress-bar").css(
                    'width', `${data.porcentaje_logrado}%`).attr(
                    'aria-valuenow', `${data.porcentaje_logrado}%`).html(
                    `${data.porcentaje_logrado}%`);
                $("#id_avance_autoevaluacion").find("div.progress-bar").css(
                    'width', `${data.avance_autoevaluacion}%`).attr(
                    'aria-valuenow', `${data.avance_autoevaluacion}`).html(
                    `${data.avance_autoevaluacion}%`);
                button.parent().parent().remove();

            }else{
                mostrarNotificacionGrowl(
                    data['message'],
                    'error'
                );
            }
        });

    });

    // /* Escuchar submit para guardar respuesta */
    // $(document).on('submit', RESPUESTA_FORM, function (e) {
    //     e.preventDefault();
    //     submitRespuestaForm($(this));
    // });
    //
    // /* Escuchar evento para quitar respuesta */
    // $(document).on('click', ID_QUITAR_RESPUESTA_INICIATIVA, function (e) {
    //     let button = $(this);
    //     let divContenidoFormulario = button.parent().parent().parent().parent();
    //     let id_ii_cc = divContenidoFormulario.attr('id').split('_')[1];
    //
    //     alertify.confirm('Confirmar Eliminación', '¿Estás seguro que deseas eliminar tu respuesta?', function() {
    //         $.get(URL_QUITAR_RESPUESTA, {'id_ii_cc': id_ii_cc}, function (data) {
    //             if(data['success']){
    //                 mostrarNotificacionGrowl(
    //                     data['message'],
    //                     'success'
    //                 );
    //                 $(divContenidoFormulario).parent().parent().removeClass('table-success');
    //                 $(divContenidoFormulario).parent().find("div.progress div.progress-bar").css(
    //                     'width', '0%').attr(
    //                     'aria-valuenow', '0').html(
    //                     '0%');
    //                 $(divContenidoFormulario).find('#id_respuesta').val(0);
    //                 $("#id_avance_autoevaluacion").find("div.progress-bar").css(
    //                     'width', `${data.avance_autoevaluacion}%`).attr(
    //                     'aria-valuenow', `${data.avance_autoevaluacion}`).html(
    //                     `${data.avance_autoevaluacion}%`);
    //
    //             }else{
    //                 mostrarNotificacionGrowl(
    //                     data['message'],
    //                     'error'
    //                 );
    //             }
    //         });
    //     }, function(){
    //         alertify.error('Cancelado')
    //     }).set('labels', {ok:'Continuar', cancel:'Cancelar'});
    //
    // });
    //
    // /* Llenar formularios */
    // $(`div[id^=${ID_CONTENIDO_RESPUESTA}]`).each(function () {
    //     let id_ii_cc = $(this).attr('id').split('_')[1];
    //     let contenidoFormulario = $(this);
    //
    //     //generar formulario desde servidor (ajax)
    //     $.get(URL_RESPUESTA, {'id_ii_cc': id_ii_cc} , function (data) {
    //         if(data['form_html']){
    //             contenidoFormulario.html(data['form_html']);
    //         }
    //     });
    //
    // });

});
