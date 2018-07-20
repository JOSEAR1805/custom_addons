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

  $(".onSubmitRentals").on("click", function(e) {
    var id_form = $(this).closest("form");
    var name = $('input[name="cliente_nombre"]', id_form).val();
    console.log(id_form.serialize());
    swal({
      title: "¿Estás seguro?",
      text: "De asignar a: " + name + " a la cola",
      icon: "warning",
      buttons: true,
      dangerMode: true
    }).then(willshow => {
      if (willshow) {
        $.ajax({
          url: "/confeccion_queue_assignation",
          data: id_form.serialize(),
          type: "POST",
          dataType: "json",
          success: function(data) {
            console.log(data);
            id_form.closest("tr").remove();
            swal(name + " se asigno a la cola", {
              icon: "success"
            });
          },
          error: function(data) {
            console.log(data);
            swal("Hubo un error al asignar la cola", {
              icon: "warning"
            });
          }
        });
      } else {
        swal("La asignación fue cancelada");
      }
    });
    return false;
  });

  $(".onSubmitMyRental").on("click", function(e) {
    var id_form = $(this).closest("form");
    var name = $('input[name="cliente_nombre"]', id_form).val();
    console.log(id_form.serialize());
    swal({
      title: "¿Estás seguro?",
      text: "de tomar turno",
      icon: "warning",
      buttons: true,
      dangerMode: true
    }).then(willShow => {
      if (willShow) {
        $.ajax({
          url: "/confeccion_queue_assignation",
          data: id_form.serialize(),
          type: "POST",
          dataType: "json",
          success: function(data) {
            console.log(data);
            swal(name + " se asigno a la cola", {
              icon: "success"
            });
          },
          error: function(data) {
            console.log(data);
            swal("Hubo un error al asignar la cola", {
              icon: "warning"
            });
          }
        });
      } else {
        swal("La asignación fue cancelada");
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

  $('.onSubmitVoice').click(function(e){
    var id_form = $(this).closest("form").serialize();
    var vestidor = $('input[name="vestidor_name"]', id_form).val();
    var ticket = $('input[name="cola_vestidor_name"]', id_form).val();
    responsiveVoice.speak("Numero " + ticket.split('C')[1] + " dirigirse al vestidor " + vestidor.split('V-')[1], "Spanish Latin American Female", {rate: 1.0});
  })
});


