var $ = django.jQuery;

(function($) {
    $(document).ready(function() {
        var cliente = document.getElementById('id_cliente');
        if(cliente.value == ''){
            $('#detalleventa_set-group').hide();
        }

        $('#id_cliente').change(function() {
            $('#detalleventa_set-group').show();
            var optionSelected = $(this).find("option:selected");
            var valueSelected  = optionSelected.val();
            console.log(valueSelected)
            if(!valueSelected){
                $('#detalleventa_set-group').hide();
                return
            }
            $.ajax({
                data : {'cliente_id' : valueSelected },
                url : "/admin/servicios/getdetallespendientes/",
                type : "get",
                success : function(data){
                    $('#id_puntos_acumulados').val(data[0].puntos_acumulados);
                    var rows_length = data.length;
                    for(var i=0 ; i<rows_length ; i++){
                        $("#id_detalleventa_set-" + i + "-servicio").val(data[i].id);
                        $("#id_detalleventa_set-" + i + "-servicio_descripcion").val(data[i].descripcion);
                        $("#id_detalleventa_set-" + i + "-subtotal").val(data[i].precio);
                    }
                    for(var j=rows_length; j<20 ; j++){
                        $("#detalleventa_set-" + j).hide();
                    }
                    calcular_total();
                }
            });
        });

         $('#detalleventa_set-group').click(function() {
            calcular_total();
         });

         $('#detalleventa_set-group').change(function() {
            calcular_total();
         });

         $('#pago_set-group').click(function() {
            calcular_total();
         });

         $('#pago_set-group').change(function() {
            calcular_total();
         });


        // quitar coma decimal y separadores de miles antes del submit
        $('form input[type=submit]').click(function(e) {
            $('.auto').each(function (){
                $(this).val(($(this).val()!='')?unformat(document.getElementById(this.id.toString())):'');
            });
            $('#id_total').val(parseInt(total));
        });

    });

})(django.jQuery);

/*
    calculo de los totales
*/
function calcular_total(){
    total = 0;
    var rows = $("tr[id*='detalleventa_set']");
    var rows_length = rows.length -1; // para evadir el empty

    for(var i=0 ; i<rows_length ; i++){
       var subtotal = document.getElementById('id_detalleventa_set-'+i+'-subtotal');
       if(subtotal.value != ''){
       total += parseInt(unformat(subtotal));
       }
       console.log(total)
    }
    $('#id_total').val(separarMiles(total));

    total_medios_de_pago = 0;
    total_forms = $('#id_pago_set-TOTAL_FORMS').val();
    for(var j=0; j<total_forms; j++){

        var monto = ($('#id_pago_set-' + j + '-monto').val()!='')?unformat(document.getElementById('id_pago_set-'+j+'-monto')):'0';

        if($('#id_pago_set-'+j+'-DELETE').is(':checked')==false){
            total_medios_de_pago += parseFloat(monto)
        }

    }
    $('#id_total_medios_de_pago').val(separarMiles(total_medios_de_pago));
}

function separarMiles(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}


function unformat(input){
		return input.value.replace(/\./g,'').replace(',','.');
}