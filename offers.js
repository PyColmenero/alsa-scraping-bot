var offers = [];
var punto1 = "Sevilla";
var punto2 = "Lugo";

$(document).ready(function () {

    // LoadCalendar(getUrlVar("p1"), getUrlVar("p2"));
    get_offers("ida", "Sevilla", "Pontevedra");
    get_offers("vuelta", "Vigo", "Sevilla");
})

function getUrlVar(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function LoadCalendar(p1, p2) {

    get_offers("ida", p1, p2);
    get_offers("vuelta", p2, p1);
}

function get_offers(root, salida, destino) {

    $("." + root + "_month_name").each(function () {
        $(this).text($(this).text() + " " + salida + " - " + destino);
    })

    $.getJSON('./' + salida + ' - ' + destino + '.json', function (data) { // https://acolmenero.xyz/english/words.json

        offers = data;

        prices = Object.keys(offers);
        prices.sort(function (a, b) {
            return parseInt(a) - parseInt(b);
        });
        console.log(prices);

        offers[prices[0]].forEach(function (offer) {
            var total_date = offer.fechaIda
            hour = total_date.split(" ")[1]
            date = total_date.split(" ")[0]
            date = date.split("/")

            var day_div = $("#" + root + "" + date[0] + "-" + date[1])
            day_div.html(day_div.html() + "<div class='offer'><a href=" + offer.url + ">" + hour + ": <strong>" + prices[0] + "€</strong><a></div>")

        })
        if (prices.length != 1) {

            offers[prices[1]].forEach(function (offer) {
                var total_date = offer.fechaIda
                hour = total_date.split(" ")[1]
                date = total_date.split(" ")[0]
                date = date.split("/")

                var day_div = $("#" + root + "" + date[0] + "-" + date[1])
                day_div.html(day_div.html() + "<div class='offer'><a href=" + offer.url + ">" + hour + ": <strong>" + prices[1] + "€</strong><a></div>")

            })
        }

    });

}


// https://www.alsa.es/checkout?p_p_id=PurchasePortlet_WAR_Alsaportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_PurchasePortlet_WAR_Alsaportlet_javax.portlet.action=searchJourneysAction&p_auth=YFT0JB8j&code=&serviceType=&accessible=0&originStationNameId=A%20Coru%C3%B1a%2F%20La%20Coru%C3%B1a&originStationId=377&destinationStationNameId=Sevilla%20(Todas%20las%20paradas)&destinationStationId=90340&departureDate=08%2F09%2F2021&locationMode=&passengerType-1=1&passengerType-4=0&passengerType-5=0&passengerType-2=0&passengerType-3=0&numPassengers=1&regionalZone=&travelType=OUTWARD&LIFERAY_SHARED_isTrainTrip=false&promoCode=&jsonAlsaPassPassenger=&jsonVoucherPassenger=