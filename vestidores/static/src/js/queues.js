$(document).ready(function () {
    var vestidor;
    $('.inputVestidorRadio').on('click', function () {
        vestidor = this.value;
    });

    $(".onSumitAsigarColaAle").on("click", function (e) {
        var cola_vestidor = this.value;
        console.log(vestidor, cola_vestidor);

        $.ajax({
        url: '/dressing_room_assignation',
        type: 'POST',
        data: {
            'cola_vestidor_id': cola_vestidor,
            'vestidor_id': vestidor
        },
        dataType: 'json',
        error: function(){
            swal("Ocurrio un Error");
        },
        success:function(data){
            swal("Asignación Exitosa", {
                icon: "success"
            });
            setTimeout(() => {
                location.reload();
            }, 2000);
        }
        });
    });
});

function allowDrop(ev) {
    ev.preventDefault();
}
function drag(ev) {
    var aux = ev.dataTransfer.setData("text", ev.target.id);
}
function drop(ev) {
    ev.preventDefault();
    var aux = ev.dataTransfer.getData("text").split('-');
    var cola_vestidor = aux[0]
    var cliente = aux[1]
    var vestidor = $(ev.target).closest("button")[0].id;
    var vestidor_name = $(ev.target).closest("button")[0].name;
    swal({
        title: "¿Estás seguro?",
        text: "De asignar cliente: " + cliente + " al vestidor: " + vestidor_name,
        icon: "warning",
        buttons: true,
        dangerMode: true
    }).then(willShow => {
        if (willShow) {
            $.ajax({
                url: '/dressing_room_assignation',
                type: 'POST',
                data: {
                    'cola_vestidor_id': cola_vestidor,
                    'vestidor_id': vestidor
                },
                dataType: 'json',
                error: function(){
                    swal("Ocurrio un Error");
                },
                success:function(data){
                    swal("Asignación Exitosa", {
                        icon: "success"
                    });
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                }
            });
        } else {
            swal("Asignación cancelada");
        }
    });
}