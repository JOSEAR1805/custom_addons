$(document).ready(function () {
  $(".js-example-basic-multiple").select2();

  $(".onSubmitVestidores").on("click", function (e) {
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

  $(".onSubmitMyRental").on("click", function (e) {
    var id_form = $(this).closest("form");
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

  $(".onSubmitPartner").on("click", function (e) {
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

  $(".onSubmitPartne").on("click", function (e) {
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


});