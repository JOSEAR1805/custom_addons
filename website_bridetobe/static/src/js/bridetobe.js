$(document).ready(function(){
//    $('input[type="date"]').datepicker({dateFormat : 'yy-mm-dd'});

    odoo.define('website_bridetobe.event_data', function (require) {
        "use strict";
        var ajax = require("web.ajax");


        if($('input#order').val() && $('input#order').val() != ''){
            alert("Su numero de orden es "+$('input#order').val()+" favor dirigirse a caja para completar su reservacion")
            $('input#order').val('')
        }

        $('.oe_cart').each(function () {
            var oe_cart = this;
            $(oe_cart).on('click', 'button.remove_item', function (ev) {
                ev.preventDefault();
                var $product_list = $('input[name="product_barcode"]').val().split(",");
                for(var $product in $product_list){
                    if($(this).val() == $product_list[$product]){
                        $product_list.splice($product, 1);
                        break;
                    }
                }
                $('input[name="product_barcode"]').val($product_list.toString());
                $(this).parent().parent().remove();
            });
        });
    });

    $('#calendar').fullCalendar({
        header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,agendaWeek,agendaDay,listWeek'
			},
			events: {
			    url: '/get_events',
			    type: 'POST',
			    data:{
			        product_id: $('input#product_id').val(),
			        csrf_token: $('input#csrf_token').val()
			    }
			},

    })
});