/*
* Creado por Alexis 13/11/2017
*/

const URL_ELIMINAR_EVIDENCIA = url_prefix + '/plantrabajo/seguimiento/evidencia/eliminar/';
const URL_EVIDENCIAS = url_prefix + '/plantrabajo/(id_plan_trabajo)/evidencias/';
const URL_DESCARGA_EVIDENCIA = url_prefix + '/plantrabajo/seguimiento/evidencia/(id_evidencia)/descargar/';

$(function () {

    $(document).on('click', 'button[name="eliminarEvidencia"]', function() {
        let idEvidencia = $(this).find('input[name="id"]').val();
        let evidencia = $(this).find('input[name="evidencia"]').val();
        alertify.confirm(
            "Eliminar Evidencia",
            `¿Desea eliminar la evidencia <strong>${evidencia}</strong>?`,
            function(){
                $.post(URL_ELIMINAR_EVIDENCIA, { id_evidencia: idEvidencia }).done(function(data) {
                    if(data['success']){
                        alertify.success(data['message']);
                        $(document).find(`tr[id="archivo_evidencia_${idEvidencia}"]`).remove();
                    }else{
                        alertify.warning(data['message']);
                    }
                }).fail(function () {
                    alertify.warning(`Ocurrio un error inesperado..`);
                });
            },
            function(){
                alertify.error('La operación fue cancelada');
            }).set('labels', {ok:'Eliminar', cancel:'Cancelar'});
    });

    $(document).on('click', 'button[name="evidencias"]', function () {
        let idPlanTrabajo = $(this).find('input[name="plan"]').val();
        let url = URL_EVIDENCIAS.replace(
            "(id_plan_trabajo)",
            idPlanTrabajo
        );
        $.get(url, function (data) {
            if(data['success']){
                let tabla = "";
                let evidencias = data['evidencias'];
                for (let i=0; i<evidencias.length; i++){
                    let url_descargar = URL_DESCARGA_EVIDENCIA.replace(
                        "(id_evidencia)",
                        evidencias[i].id
                    );
                    let img = '';
                    if (String(evidencias[i].evidencia).endsWith('.jpg') || String(evidencias[i].evidencia).endsWith('.jpeg') || String(evidencias[i].evidencia).endsWith('.png')){
                        img = `<img src="${evidencias[i].url_file}" width="150">`;
                    }else{
                        img = `<img src="/static/base/img/file.png" width="45">`;
                    }
                    let evidencia = `<tr id="archivo_evidencia_${evidencias[i].id}">
                        <td class="text-center" width="180">
                            ${img}
                        </td>
                        <td>
                            <p>${evidencias[i].evidencia}</p>
                        </td>
                        <td class="text-center">
                            <a class="btn btn-info" href="${url_descargar}">
                                <i class="fa fa-download"></i> Descargar
                            </a>
                            <button class="btn btn-danger" name="eliminarEvidencia">
                                <i class="fa fa-trash"></i> Eliminar
                                <input type="hidden" name="id" value="${evidencias[i].id}">
                                <input type="hidden" name="evidencia" value="${evidencias[i].evidencia}">
                            </button>
                        </td>
                    </tr>`;
                    tabla = tabla + evidencia;
                }
                $(document).find(`table#tablaEvidencia_${idPlanTrabajo}`).html(tabla);
            }else{
                console.log("no paso nada");
            }
        });

    });
});