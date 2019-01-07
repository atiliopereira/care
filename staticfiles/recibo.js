var $ = django.jQuery;

(function($) {
    $(document).ready(function() {

        // recalcular totales al borrar un factura de un detalle no guardador (con botoncito 'x')
         $('#detallerecibo_set-group').click(function() {
            calcular_total();
         });

         $('#detallerecibo_set-group').change(function() {
            calcular_total();
         });

        // quitar coma decimal y separadores de miles antes del submit
        $('form input[type=submit]').click(function(e) {
            $('.auto').each(function (){
                $(this).val(($(this).val()!='')?unformat(document.getElementById(this.id.toString())):'');
            });
            $('#id_total').val(parseInt(total));
        });

        // al cambiar un select en el inline
        $('select').change(function(){
            vector = $(this).attr("id").split("-");

            if( (vector[0] == "id_detallerecibo_set") && (vector[2] == "venta") ){
                var optionSelected = $(this).find("option:selected");
                var valueSelected  = optionSelected.val();

                if(!valueSelected){
                    $("#id_detallerecibo_set-" + vector[1] + "-monto").val("");

                    calcular_total();
                    return
                }
                $.ajax({
                    data : {'venta_id' : valueSelected },
                    url : "/admin/cajas/getventa/",
                    type : "get",
                    success : function(data){
                        $("#id_detallerecibo_set-" + vector[1] + "-monto").val(separarMiles(parseFloat(data.saldo)));
                        calcular_total();
                    }
                });
            }

        });

    });

})(django.jQuery);

/*
    calculo de los totales
*/
function calcular_total(){
    total = 0;
    var rows = $("tr[id*='detallerecibo_set']");
    var rows_length = rows.length -1; // para evadir el empty

    for(var i=0 ; i<rows_length ; i++){
       var subtotal = document.getElementById('id_detallerecibo_set-'+i+'-monto');
       total += parseInt(subtotal.value.toString().split('.').join(''));
    }

   $('#id_monto').val(separarMiles(total));
}

function separarMiles(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}


function unformat(input){
		return input.value.replace(/\./g,'').replace(',','.');
}