//Creado por Alexis 13/06/2019
//Funciones para el filtro de insumos pertenecientes al colegio seleccionado

const urlFiltroColegios = url_prefix + '/insumos/colegio-insumos/filtrado/';
let colegio_select = '';
let select_insumo = '';

function filtrarInsumos(id_colegio, selected){
    if (id_colegio !== '') {
        $.get(urlFiltroColegios, {id_colegio: id_colegio}).done( function( data ) {
            if(data['success']) {
                let opciones = '<option value="" selected="">---------</option>';
                let insumos = data['insumos'];
                for (let i=0; i<insumos.length; i++) {
                    let opcion = `<option value="${insumos[i].pk}">${insumos[i].nombre}</option>`;
                    opciones = opciones + opcion;
                }
                select_insumo.html(opciones);
                if(selected.length > 0){
                    for (let i = 0; i < selected.length; i++) {
                        $(`select[name='${selected[i][0]}']`).find(`option[value='']`).removeAttr('selected');
                        $(`select[name='${selected[i][0]}']`).find(`option[value='${selected[i][1]}']`).attr('selected', 'selected');
                    }
                }
            }else{
                alertify.warning(data['message']);
            }
        });
    } else {
        select_insumo.html('<option value="" selected="">---------</option>');
    }
}

$(function() {
    colegio_select = $("select[name='colegio']");
    select_insumo = $("select[name^='iteminsumo_set']");
    let selected = [];

    // filter if Colegio exist or selected
    let id_colegio = colegio_select.val();
    if (id_colegio === ''){
        select_insumo.html('<option value="" selected="">---------</option>');
    } else {
        select_insumo.each(function(){
            let insumo = [];
            insumo.push($(this).attr('name'));
            insumo.push($(this).val());
            selected.push(insumo);
        });
        filtrarInsumos(id_colegio, selected);
    }
    colegio_select.on('change', function(){
        // console.log("Dentro del if");
        filtrarInsumos($(this).val(), selected);
    });
});
