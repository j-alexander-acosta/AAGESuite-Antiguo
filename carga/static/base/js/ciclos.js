
function mostrarNotificacionGrowl(mensaje, tipo){
  /* Mostrar notificacion growl */
  var tipoDefecto = 'default';
  var tiposValidos = [
    'default',
    'info',
    'success',
    'warning',
    'danger'
  ];

  if(tiposValidos.indexOf(tipo) === -1){
    //tipo no existe en tipos_validos
    if(tipo === 'error'){
      tipoDefecto = 'danger';
    }
  }else{
    tipoDefecto = tipo;
  }

  $.growl(mensaje,
    { type: tipoDefecto }
  );

}

function cargarRuta(url) {
  window.location.href = url;
}

$.wait = function(ms) {
    var defer = $.Deferred();
    setTimeout(function() { defer.resolve(); }, ms);
    return defer;
};

$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('#scroll').fadeIn();
        } else {
            $('#scroll').fadeOut();
        }
    });
    $('#scroll').click(function(){
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
});