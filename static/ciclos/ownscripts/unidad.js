//Creado por Alexis 13/06/2019
//Funciones para el filtro de insumos pertenecientes al colegio seleccionado

const urlFiltroColegios = url_prefix + '/unidad-colegio/filtrado/';
let colegio_select = '';
let select_responsable = '';
let select_superior = '';
let select_tipoinsumo = '';

function filtrarDatos(id_colegio, selected){
    select_responsable = $("select[name^='responsableunidad_set']");
    select_superior = $("select[name^='superior']");
    select_tipoinsumo = $("select[name^='tipo_insumo']");
    let opciones = '';

    if (id_colegio !== '') {

        $.get(urlFiltroColegios, {id_colegio: id_colegio}).done( function( data ) {
            if(data['success']) {
                let responsables = data['responsables'];
                let unidades = data['unidades'];
                let tiposinsumo = data['tiposinsumo'];

                opciones = '<option value="" selected="">---------</option>';
                for (let i = 0; i < responsables.length; i++) {
                    let opcion = `<option value="${responsables[i].pk}">${responsables[i].nombre}</option>`;
                    opciones = opciones + opcion;
                }
                select_responsable.html(opciones);

                opciones = '<option value="" selected="">---------</option>';
                for (let i = 0; i < unidades.length; i++) {
                    let opcion = `<option value="${unidades[i].pk}">${unidades[i].nombre}</option>`;
                    opciones = opciones + opcion;
                }
                select_superior.html(opciones);

                opciones = '<option value="" selected="">---------</option>';
                for (let i = 0; i < tiposinsumo.length; i++) {
                    let opcion = `<option value="${tiposinsumo[i].pk}">${tiposinsumo[i].nombre}</option>`;
                    opciones = opciones + opcion;
                }
                select_tipoinsumo.html(opciones);

                if(selected.length > 0){
                    // console.log(selected);
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
        select_responsable.html('<option value="" selected="">---------</option>');
        select_superior.html('<option value="" selected="">---------</option>');
        select_tipoinsumo.html('<option value="" selected="">---------</option>');
    }
}

$(function() {
    colegio_select = $("select[name='colegio']");
    select_responsable = $("select[name^='responsableunidad_set']");
    select_superior = $("select[name^='superior']");
    select_tipoinsumo = $("select[name^='tipo_insumo']");
    let selected = [];

    // filter if Colegio exist or selected
    let id_colegio = colegio_select.val();
    if (id_colegio === '') {
        select_responsable.html('<option value="" selected="">---------</option>');
        select_superior.html('<option value="" selected="">---------</option>');
        select_tipoinsumo.html('<option value="" selected="">---------</option>');
    } else {
        $("select").each(function(){
            let select = [];
            select.push($(this).attr('name'));
            select.push($(this).val());
            selected.push(select);
        });
        filtrarDatos(id_colegio, selected);
    }
    colegio_select.on('change', function(){
        // console.log("Dentro del if " + $(this).val());
        filtrarDatos($(this).val(), selected);
    });
});
