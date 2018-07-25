$(document).on("ready", function(){  
    setTimeout("location.reload();",10000);
    var ticket = '';
    var vestidor = '';
    $('.table-tv tr:last').each(function() {
        ticket = $(this).find("td span").eq(0).html(); 
        vestidor = $(this).find("td span").eq(2).html();    
    });

    function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for(var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    };
    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    };
    var cookie = getCookie('Ticket');
    if (cookie !== ticket) {
        setCookie('Ticket', ticket, 15);
        responsiveVoice.speak("Numero " + ticket.split('C')[1] + " dirigirse al vestidor " + vestidor.split('V-')[1], "Spanish Latin American Female", {rate: 1.0});
    };
});