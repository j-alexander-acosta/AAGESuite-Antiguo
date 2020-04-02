/*
* Creado por Alexis 31-10-2017
*/

const URL_GUARDAR_PREPARADOS = url_prefix + "/ciclos-preparados/guardar/";

$(function() {

    $(document).find('#periodo').each(function(){
        let select = $(document).find('select[name="filtroPeriodos"]');
        let opcion = `<option value="">`;
    });

    $(document).on('click', '#seleccionarTodo', function(){
        $(document).find('input[id^="cicloPreparado"]').each(function(){
            $(this).attr("checked", true);
        });
    });

    $(document).on('click', 'button[name="guardarPreparados"]', function(){
        $(document).find('input[id^="cicloPreparado"]').each(function(){
            let cicloCalidadId = $(this).attr('id').split('_')[1];
            let preparado = false;
            if ( $(this).is(':checked') ) {
                preparado = true;
            }
            $.post( URL_GUARDAR_PREPARADOS, { ciclo_calidad_id: cicloCalidadId, preparado: preparado }).done(function(data) {
                if(data['success']){
                    alertify.success(data['message']);
                    document.location.reload();
                }else{
                    alertify.warning(data['message']);
                }
            }).fail(function () {
                alertify.warning(`Ocurrio un error inesperado..`);
            });
        });
    });

});