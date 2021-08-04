//El documento, contiene las funciones de dinamismo
// del formulario de creación y edición de funcionario
let fonasa = true;
let empleado = true;

function switch_salud(){
    let div_isapre = $("#div_id_isapre");
    if(fonasa){
        div_isapre.fadeOut();
        div_isapre.find("#id_isapre").attr('disabled', true);
        fonasa = false;
    }else{
        div_isapre.fadeIn();
        div_isapre.find("#id_isapre").prop('disabled', false);
        fonasa = true;
    }
}

function switch_estado(){
    let div_tipo_misionero = $('#div_id_tipo_misionero');
    let div_puntos = $('#div_id_puntos');
    if(empleado){
        div_tipo_misionero.fadeOut();
        div_tipo_misionero.find("#id_tipo_misionero").attr('disabled', true);
        div_puntos.fadeOut();
        div_puntos.find("#id_puntos").attr('disabled', true);
        empleado = false;
    }else{
        div_tipo_misionero.fadeIn();
        div_tipo_misionero.find("#id_tipo_misionero").prop('disabled', false);
        div_puntos.fadeIn();
        div_puntos.find("#id_puntos").prop('disabled', false);
        empleado = true;
    }
}

function ready(){
    let salud = $("#id_salud").val();
    let estado = $("#id_estado").val();

    fonasa = salud === '1';
    empleado = estado === '1';

    switch_salud();
    switch_estado();
}

$(function(){
    ready();

    $("#id_salud").on('change', function(){
        switch_salud();
    });

    $("#id_estado").on('change', function(){
        switch_estado();
    });
});