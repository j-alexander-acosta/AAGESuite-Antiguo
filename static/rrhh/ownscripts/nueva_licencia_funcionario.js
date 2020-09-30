/* Creado por Alexis */

$(function() {
    console.log('Funcionando!!!');
    $(document).on('click', '[name^=agregar_licencia]', function() {
        console.log('accion del boton');
        $(document).find('#div_id_tipo_licencia_descripcion').css('display', 'none');
    });
});
