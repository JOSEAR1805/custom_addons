$(document).on("ready", function(){  
    setTimeout("location.reload();",30000);
    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    };
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
    var tickets = [];
    $('.table-tv tr').each(function() {
        var ticket = $(this).find("td span").eq(0).html();
        var vestidor = $(this).find("td span").eq(2).html();    
        if (ticket != undefined && vestidor != undefined){
            tickets.push({
                ticket: ticket,
                vestidor: vestidor
            }); 
        }
    });
    function checkCookie(cookie, tickets){
        var cookieTicket = [];
        var allTickets = [];
        cookie.map((element) => {
            cookieTicket.push(element.ticket);
        })
        tickets.map((element) => {
            var aux = cookieTicket.indexOf(element.ticket)
            if(aux < 0){
                allTickets.push(element);
            }
        })
        return allTickets;
    }
    var cookie = getCookie('Ticket');
    if(cookie){
        var checks = checkCookie(JSON.parse(cookie), tickets);
        if (checks.length > 0) {
            checks.map((element) => {
                responsiveVoice.speak("Numero " + element.ticket + " dirigirse al vestidor " + element.vestidor, "Spanish Latin American Female", {rate: 1.0});
            })
        };
    }else{
        tickets.map((element) => {
            responsiveVoice.speak("Numero " + element.ticket + " dirigirse al vestidor " + element.vestidor, "Spanish Latin American Female", {rate: 1.0});
        })
    }
    setCookie('Ticket', JSON.stringify(tickets), 15);
});
