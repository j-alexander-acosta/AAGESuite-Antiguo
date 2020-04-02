/*
* Creado por Alexis 05-10-2017
*/
const URL_HABILITAR_AUTOEVALUACION = url_prefix + '/unidades/autoevaluacion/habilitar/';
const URL_FINALIZAR_AUTOEVALUACION = url_prefix + '/unidades/autoevaluacion/finalizar/';
const URL_INFORMEFODA_HABILITAR = url_prefix + '/informefoda/habilitar/';

$(function(){

    $(document).on('click', 'a[name="habilitarAutoevaluacion"]', function() {
       let idCicloCalidad = $(this).find('input[name="cicloCalidad"]').val();
       alertify.confirm(
           "Habilitar Autoevaluación",
           "Al habilitar la autoevaluación, se podrán ingresar nuevas respuestas a las iniciativas",
            function(){
                $.post(URL_HABILITAR_AUTOEVALUACION, { id_ciclo_calidad: idCicloCalidad }).done(function(data) {
                    if(data['success']){
                        alertify.success(data['message']);
                        document.location.reload();
                    }else{
                        alertify.warning(data['message']);
                    }
                }).fail(function () {
                    alertify.warning(`Ocurrio un error inesperado..`);
                });
            },
            function(){
                alertify.error('La operación fue cancelada');
            }).set('labels', {ok:'Habilitar', cancel:'Cancelar'});
   });

    $(document).on('click', 'button[name="finalizarAutoEvaluacion"]', function(){
        let idUnidad = $(this).find('input[name="unidad"]').val();
        let anio = $(this).find('input[name="anio"]').val();
        alertify.confirm("Finalizar Autoevaluación", "Una vez finalizada la Autoevaluación, no podrá modificar las respuestas ingresadas",
            function(){
                $.post(URL_FINALIZAR_AUTOEVALUACION, { id_unidad: idUnidad, anio: anio }).done(function(data) {
                    if(data['success']){
                        alertify.success(data['message']);
                        document.location.reload();
                    }else{
                        alertify.warning(data['message']);
                    }
                }).fail(function () {
                    alertify.warning(`Ocurrio un error inesperado..`);
                });
            },
            function(){
                alertify.error('La operación fue cancelada');
            }).set('labels', {ok:'Finalizar', cancel:'Cancelar'});
    });

    $(document).on('click', '[id^=habilitarInformeFODALink]', function (e){
        e.preventDefault();
        let cicloCalidad = $(this).find('input[name="cicloCalidad"]').val();
        alertify.confirm(
           "Habilitar Análisis FODA",
           "Al habilitar el análisis FODA, se podrán configurar nuevamente las Fortalezas, Oportunidades, Debilidades y Amenazas",
            function(){
                $.post(URL_INFORMEFODA_HABILITAR, { ciclo_calidad: cicloCalidad }).done(function(data) {
                    if(data['success']){
                        alertify.success(data['message']);
                        document.location.reload();
                    }else{
                        alertify.warning(data['message']);
                    }
                }).fail(function () {
                    alertify.warning(`Ocurrio un error inesperado..`);
                });
            },
            function(){
                alertify.error('La operación fue cancelada');
            }).set('labels', {ok:'Habilitar', cancel:'Cancelar'});
    });

});