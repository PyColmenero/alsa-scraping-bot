from selenium import webdriver
import os
import io
import time
import json

import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

prices_json = {}


inverted = True
originName = "Sevilla"
originStationId = "90340"

destinationName = "Valencia"
destinationStationId = "94600"



if inverted:
	originName, destinationName = destinationName, originName
	originStationId, destinationStationId = destinationStationId, originStationId

stations = [destinationStationId]
print(stations)


if True:

	driver = webdriver.Chrome(ChromeDriverManager().install())
	day = 24
	month = 9
	
	
	filename = originName + " - " + destinationName + ".json"

	for station in stations:

		fail = 0
		destinationStationId = station
		print("\n===================================", destinationName, destinationStationId)

		for x in range(40):

			if (day==30):
				day=1;
				month+=1;
			else:
				day+=1;

			date = str(day) + "%2F"+str(month)+"%2F2021"
			url = "https://www.alsa.es/checkout?p_p_id=PurchasePortlet_WAR_Alsaportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_PurchasePortlet_WAR_Alsaportlet_javax.portlet.action=searchJourneysAction&p_auth=SvZ3wU4c&code=&serviceType=&accessible=0&_JourneySearchPortlet_WAR_Alsaportlet_INSTANCE_JourneySearch_21651890_originStationNameId=Sevilla%20(Todas%20las%20paradas)&originStationId="+originStationId+"&destinationStationId="+destinationStationId+"&departureDate="+date+"&_departureDate="+date+"&returnDate=&_returnDate=&locationMode=&passengerType-1=1&passengerType-4=0&passengerType-5=0&passengerType-2=0&passengerType-3=0&numPassengers=1&regionalZone=&travelType=OUTWARD&LIFERAY_SHARED_isTrainTrip=false&promoCode=&jsonAlsaPassPassenger=&jsonVoucherPassenger="
			driver.get(url)
			json_url = "https://www.alsa.es/checkout?p_p_id=PurchasePortlet_WAR_Alsaportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=JsonGetJourneysList&p_p_cacheability=cacheLevelPage&_PurchasePortlet_WAR_Alsaportlet_tabUuid=69bffc75-a3ab-41ad-bbef-a57c811385d1&_PurchasePortlet_WAR_Alsaportlet_journeyDirection=outward&p_p_lifecycle=1&_PurchasePortlet_WAR_Alsaportlet_serviceType=&_PurchasePortlet_WAR_Alsaportlet_accessible=0&_PurchasePortlet_WAR_Alsaportlet_javax.portlet.action=searchJourneysAction&_PurchasePortlet_WAR_Alsaportlet_code=&_PurchasePortlet_WAR_Alsaportlet__departureDate="+date+"&_PurchasePortlet_WAR_Alsaportlet_jsonVoucherPassenger=&_PurchasePortlet_WAR_Alsaportlet_passengerType-5=0&_PurchasePortlet_WAR_Alsaportlet_passengerType-1=1&_PurchasePortlet_WAR_Alsaportlet_destinationStationId=99085&_PurchasePortlet_WAR_Alsaportlet_passengerType-2=0&_PurchasePortlet_WAR_Alsaportlet_regionalZone=&_PurchasePortlet_WAR_Alsaportlet_passengerType-3=0&_PurchasePortlet_WAR_Alsaportlet_passengerType-4=0&_PurchasePortlet_WAR_Alsaportlet_LIFERAY_SHARED_isTrainTrip=false&_PurchasePortlet_WAR_Alsaportlet_travelType=OUTWARD&_PurchasePortlet_WAR_Alsaportlet_returnDate=&_PurchasePortlet_WAR_Alsaportlet_jsonAlsaPassPassenger=&_PurchasePortlet_WAR_Alsaportlet_numPassengers=1&_PurchasePortlet_WAR_Alsaportlet_originStationId=90340&_PurchasePortlet_WAR_Alsaportlet__JourneySearchPortlet_WAR_Alsaportlet_INSTANCE_JourneySearch_21651890_originStationNameId=Sevilla+%28Todas+las+paradas%29&_PurchasePortlet_WAR_Alsaportlet__returnDate=&_PurchasePortlet_WAR_Alsaportlet_promoCode=&_PurchasePortlet_WAR_Alsaportlet_departureDate=18%2F07%2F2021&_PurchasePortlet_WAR_Alsaportlet_locationMode=&tcontrol=1626442826949"
			driver.get(json_url)

			# print(url)



			txt_data = driver.find_element_by_xpath('/html/body/pre').get_attribute('innerHTML');
			data = json.loads(txt_data)

			journeys = data["journeys"]

			print("\t\t",date, x)
			for journy in journeys:
				fares = journy["fares"][0]
				price = str(fares["price"]);

				current_trip = {"lugarIda":journy["originName"], "lugarLlegada": journy["destinationName"], "fechaIda":journy["departureDataToFilter"], "fechaLlegada":journy["arrivalDataToFilter"], "url":url};
				if price in prices_json:
					prices_json[price].append(current_trip)
				else:
					prices_json[price] = [current_trip]

				print( journy["originName"] + " hasta "+ journy["destinationName"] )
				print( journy["departureDataToFilter"] + " - "+ journy["arrivalDataToFilter"] )
				print( str(fares["price"]) + "€ \n")

			print(len(journeys))
			if len(journeys) == 0:
				fail+=1

			if fail >= 10:
				fail = 0
				print("\t\t FAIL")
				break

			with io.open(filename,'w',encoding='utf8') as f:
			    f.write(json.dumps(prices_json));

print("FINICH")


# https://timeline.google.com/maps/timeline?hl=es&authuser=0&ei=2W4BYeWuCsSWa_HUisAL%3A88&ved=1t%3A17706&pli=1&rapt=AEjHL4MsFrcLhqVIrX5IyzBqgz0Nkd_gzE1MIpaq9x4RBtsSk8qdKA-cR8F2daNH0WBYcHMPeOr3PcnCDIwV5NUZ-mMAst8nEQ&pb=!1m2!1m1!1s2021-07-23
# https://timeline.google.com/maps/timeline?hl=es&authuser=0&ei=2W4BYeWuCsSWa_HUisAL%3A88&ved=1t%3A17706&pli=1&rapt=AEjHL4MsFrcLhqVIrX5IyzBqgz0Nkd_gzE1MIpaq9x4RBtsSk8qdKA-cR8F2daNH0WBYcHMPeOr3PcnCDIwV5NUZ-mMAst8nEQ&pb=!1m2!1m1!1s2021-07-23
# https://timeline.google.com/maps/timeline?hl=es&authuser=0&ei=2W4BYeWuCsSWa_HUisAL%3A88&ved=1t%3A17706&pli=1&rapt=AEjHL4MsFrcLhqVIrX5IyzBqgz0Nkd_gzE1MIpaq9x4RBtsSk8qdKA-cR8F2daNH0WBYcHMPeOr3PcnCDIwV5NUZ-mMAst8nEQ&pb=!1m2!1m1!1s2021-07-23

'''var data;
function getdata(){

    var defaultOptions = {
        url: '../play/main',
        method: 'POST',
        data: getDataFromForm($('#form-login')),
        dataType: 'json',
        contentType: false,
        processData: false
    };

    data = $.ajax(Object.assign(defaultOptions))
    console.log(data)
    console.log(data.responseJSON.prize)
                    
}
getdata();
function login(mail){
	if (Sections.config.hasSSO) {
		goToSSO();
	} else {
		$('header').removeClass('if-big');
		Sections.goTo('#form');
	}
	$("#field_5551").val("Francisco Patera");
	$("#field_email").val(mail);
	$("#policy1").prop("checked", true); 

}
login("");


function login(mail){
	if (Sections.config.hasSSO) {
		goToSSO();
	} else {
		$('header').removeClass('if-big');
		Sections.goTo('#form');
	}
	$("#field_5551").val("Alejandro Colmenero Moreno");
	$("#field_email").val(mail);
	$("#policy1").prop("checked", true); 

}
login("selters@cbarato.vip");'''
