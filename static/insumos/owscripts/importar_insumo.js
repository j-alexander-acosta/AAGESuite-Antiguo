/*
* Creado por Alexis 12-09-2017
* Archivo javascript para enviar el archivo para importar
*/

$(function(){
    $(document).on('submit', '#archivoExcelFormID', function(e){
        e.preventDefault();
        let form = $(this);
        $(document).find('html').prepend(
            `<div id="pantallaCargando" style="
                background: url('/static/insumos/img/cargando.gif') no-repeat;
                background-size: cover;
                position: fixed;
                height: 100%;
                width: 100%;
                opacity: 0.7;
                z-index: 10000;"
            >
            </div>`
        );
        let data = new FormData(
            form.get(0)
        );
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: data,
            processData: false,
            contentType: false,
            success: function(data) {
                if (!(data['success'])) {
                    if(data['form_html'] !== null){
                        form.replaceWith(data['form_html']);
                    }
                    alertify.warning(data['message']);
                }
                else {
                    $(document).find('div#pantallaCargando').remove();
                    alertify.success(data['message']);
                    $(document).find("div[class='modal fade show']").modal('hide');
                    form.find('input[name="archivo"]').val('');
                    document.location.reload();
                }
            },
            error: function () {
                alertify.warning("Ocurrio un error inesperado..");
            }
        });
    });
});