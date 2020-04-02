/*
* Creado por alexis el 21-11-2017
*
*/

const RESPUESTA_FORM = '#idRespuestaSeguimientoForm';
const ID_CONTENIDO_RESPUESTA = 'contenidoFormularioRespuesta_';
const URL_RESPUESTA =  url_prefix + '/seguimiento/respuesta/';

function submitRespuestaForm(form){
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
            if (!(data['success'])) {
                if(data['form_html'] !== null){
                    $(form).replaceWith(data['form_html']);
                    console.log(data['message']);
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
                $(form).parent().parent().parent().addClass('table-success');
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

$(function() {

    /* Escuchar submit para guardar respuesta */
    $(document).on('submit', RESPUESTA_FORM, function (e) {
        e.preventDefault();
        submitRespuestaForm($(this));
    });

    /* Llenar formularios */
    $(`div[id^=${ID_CONTENIDO_RESPUESTA}]`).each(function () {
        let id_plan_trabajo = $(this).attr('id').split('_')[1];
        let contenidoFormulario = $(this);

        //generar formulario desde servidor (ajax)
        $.get(URL_RESPUESTA, {'id_plan_trabajo': id_plan_trabajo} , function (data) {
            if(data['form_html']){
                contenidoFormulario.html(data['form_html']);
                contenidoFormulario.find('input[name="plan"]').val(id_plan_trabajo);
                contenidoFormulario.find('button[name="guardar"]').attr('title', 'Guardar Respuesta');
                contenidoFormulario.find('button[name="guardar"]').attr('data-toggle', 'tooltip');
                contenidoFormulario.find('button[name="evidencias"]').attr('title', 'Ver evidencias');
                contenidoFormulario.find('button[name="evidencias"]').attr('data-toggle', 'tooltip');
                $('[data-toggle="tooltip"]').tooltip();
            }
        });

    });

    $(document).on('click', 'button[name="evidencias"]', function() {
        let id_plan_trabajo = $(this).find('input[name="plan"]').val();
        $(document).find('tr.table-warning').removeClass('table-warning');
        $(this).parents('tr').addClass('table-warning');
        $(document).find('tr[id^="evidencias"]').hide();
        $(document).find(`#evidencias_${id_plan_trabajo}`).toggle();
    });

});