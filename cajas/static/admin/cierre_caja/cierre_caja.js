/**
 * Created by juanber on 22/09/16.
 */
(function($) {

      $(document).ready(function () {
         $('.auto').autoNumeric('init',{mDec: 0,aSep:'.',aDec:','});
          var saldo_cierre = parseInt($('#id_ingresos').autoNumeric('get'))  - parseInt($('#id_egresos').autoNumeric('get')) + parseInt($('#id_saldo_apertura').autoNumeric('get'))

        $('#id_saldo_cierre').autoNumeric('set',saldo_cierre)

          $('#cierrecaja_form').submit(function () {
               $('.auto').each(function () {
                  $(this).val($(this).autoNumeric('get'));
               });
          });


      });



})(django.jQuery);

function get_efectivo_caja() {
    $.ajax({
            url: '/admin/get_efectivo_caja/',
            type: 'get',
            data: {'caja_id': $('#id_caja').val() },
            success: function (datos) {
                alert(JSON.stringify(datos))
                var content = `<div class="form-row field-saldo_cierre"><div><label>Efectivo:</label><p>${datos.monto}</p></div></div>`
                $('.field-saldo_cierre').html(content)
               $('#id_ingresos').val(datos.ingresos);
                $('#id_egresos').val(datos.egresos);
            },
        });
}