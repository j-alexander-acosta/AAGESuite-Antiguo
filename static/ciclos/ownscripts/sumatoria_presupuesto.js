/*
    Script para el calculo del presupuesto en tiempo real.
 */
let presupuesto_ciclo='';
let presupuesto_suma='';
let presupuesto_restar='';
let presupuesto_sumar='';
let diferencia_presupuesto='';

const formatter = new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    minimumFractionDigits: 0
});

$(function() {

    //Función mas elavorada
    presupuesto_ciclo = parseInt($(document).find('#presupuesto_ciclo').html().replace('$', '').replace(/\./g, ''));
    presupuesto_suma = parseInt($(document).find('#suma_presupuesto').html().replace('$', '').replace(/\./g, ''));

    $(document).find('input[id*="presupuesto_texto"]').on('click', function() {
        presupuesto_restar = parseInt($(this).val().replace('$', '').replace(/,/g, ''));
        if (isNaN(presupuesto_restar)) {
            presupuesto_restar = 0;
        }
    });

    $(document).find('input[id*="presupuesto_texto"]').on('keyup', function() {
        presupuesto_sumar = parseInt($(this).val().replace('$', '').replace(',', ''));
        if (isNaN(presupuesto_sumar)) {
            presupuesto_sumar = 0;
        }
        presupuesto_suma -= presupuesto_restar;
        presupuesto_suma += presupuesto_sumar;
        $(document).find('#suma_presupuesto').html(formatter.format(presupuesto_suma).toString().replace('CLP', ''));
        presupuesto_restar=presupuesto_sumar;

        diferencia_presupuesto = presupuesto_ciclo - presupuesto_suma;
        $(document).find('#diferencia_presupuesto').html(formatter.format(diferencia_presupuesto).toString().replace('CLP', ''));
        if(diferencia_presupuesto <= 0){
            $(document).find('#presupuesto-alert').removeClass(' bg-success');
            $(document).find('#presupuesto-alert').removeClass(' bg-warning');
            $(document).find('#presupuesto-alert').addClass(' bg-danger');
        }else if(diferencia_presupuesto <= 100000){
            $(document).find('#presupuesto-alert').removeClass(' bg-success');
            $(document).find('#presupuesto-alert').removeClass(' bg-danger');
            $(document).find('#presupuesto-alert').addClass(' bg-warning');
        }else{
            $(document).find('#presupuesto-alert').removeClass(' bg-danger');
            $(document).find('#presupuesto-alert').removeClass(' bg-warning');
            $(document).find('#presupuesto-alert').addClass(' bg-success');
        }
    });

});
