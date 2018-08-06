$(document).ready(function() {
  $(".js-example-basic-multiple").select2();
  $(".onSubmitVestidores").on("click", function(e) {
    var id_form = $(this).closest("form");
    var name = $('input[name="ticket"]', id_form).val();
    swal({
      title: "¿Estás seguro?",
      text: "De finalizar el ticket: " + name,
      icon: "warning",
      buttons: true,
      dangerMode: true
    }).then(willDelete => {
      if (willDelete) {
        id_form.submit();
        swal("El ticket " + name + " a finalizado", {
          icon: "success"
        });
        $(this)
          .closest("tr")
          .remove();
      } else {
        swal("Se cancelo la Finalización del ticket");
      }
    });
    return false;
  });

  $(".onSubmitMyRental").on("click", function(e) {
    var id_form = $(this).closest("form");
    console.log(id_form.serialize());
    swal({
      title: "¿Estás seguro?",
      text: "de tomar turno",
      icon: "warning",
      buttons: true,
      dangerMode: true
    }).then(willShow => {
      if (willShow) {
        id_form.submit();
        swal(name + " se asigno a la cola", {
          icon: "success"
        });
      } else {
        swal("Se cancelo la asignación");
      }
    });
    return false;
  });

  $(".onSubmitPartner").on("click", function(e) {
    var id_form = $(this).closest("form");
    var name = $('input[name="cliente_nombre"]', id_form).val();
    swal({
      title: "¿Estás seguro?",
      text: "de asignar turno a : " + name,
      icon: "warning",
      buttons: true,
      dangerMode: true
    }).then(willShow => {
      if (willShow) {
        swal(name + " se asigno a la cola", {
          icon: "success"
        });
      } else {
        swal("La asignación fue cancelada");
      }
    });
  });
  
  $(".onSubmitPartne").on("click", function(e) {
    var id_form = $(this).closest("form");
    var name = $('input[name="cliente_nombre"]', id_form).val();
    swal({
      title: "¿Estás seguro?",
      text: "De guardar cliente: " + name,
      icon: "warning",
      buttons: true,
      dangerMode: true
    }).then(willShow => {
      if (willShow) {
        swal("Registro Exitoso", {
          icon: "success"
        });
      } else {
        swal("Registro cancelado");
      }
    });
  });

$(".cola-draggable").draggable();

$(".vestidor-droppable").droppable({
  accept: ".cola-draggable",
  drop: function( event, ui ) {
    var iddrop = this.id;
    console.log(event, ui);
  }
});


  $(".clickColaVestidor").on("click", function(e) {
    // Dar a las imágenes la capacidad de mover las imágenes
    // var id_tr = $(this).attr("id");
    // console.log(id_tr);
    


    // Damos la capacidad al div de recibir a otros elementos, admitiendo sólo a la imagen
    // cuyo 'id' es 'arrastrar2', y con la condición de que sea soltada estando completamente dentro
    //$(".vestidor-droppable").droppable( {accept:"#arrastrar2", tolerance:"fit", drop:elementoSoltado });


    // ------------------------------
    // Al haber definido la propiedad 'accept' para que admita sólo la imagen del logo, no
    // se producirá efecto alguno si soltamos la otra imagen al no ser admitida.
    function elementoSoltado( event, ui )
    {
         var id = ui.draggable.attr("id");
         $("#log").text("La imagen con id [" + id + "] ha sido soltada y aceptada");
    }
  });

  
  
});