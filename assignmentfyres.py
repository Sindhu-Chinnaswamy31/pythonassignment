import json
import requests
import argparse
def parse(AirportCode,AirportName,TimeYear):
	for i in range(5):
		try:
			response = requests.get(url, headers=headers, verify=False)
			parser = html.fromstring(response.text)
			json_data_xpath = parser.xpath("airlines.csv")
			raw_json =json.loads(json_data_xpath[0] if json_data_xpath else '')
			flight_data = json.loads(raw_json["content"])

			flight_info  = OrderedDict() 
			lists=[]

			for i in flight_data['legs'].keys():
				total_distance =  flight_data['legs'][i].get("formattedDistance",'')
				exact_price = flight_data['legs'][i].get('price',{}).get('totalPriceAsDecimal','')

				departure_location_airport = flight_data['legs'][i].get('departureLocation',{}).get('airportLongName','')
				departure_location_city = flight_data['legs'][i].get('departureLocation',{}).get('airportCity','')
				departure_location_airport_code = flight_data['legs'][i].get('departureLocation',{}).get('airportCode','')
			    

				if no_of_stops==0:
					stop = "Nonstop"
				else:
					stop = str(no_of_stops)+' Stop'

				total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days,flight_hour,flight_minutes)
				departure = departure_location_airport+", "+departure_location_city
				arrival = arrival_location_airport+", "+arrival_location_city
				carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
				plane = carrier.get('plane','')
				plane_code = carrier.get('planeCode','')
				formatted_price = "{0:.2f}".format(exact_price)

				if not airline_name:
					airline_name = carrier.get('operatedBy','')
				
				timings = []
				for timeline in  flight_data['legs'][i].get('timeline',{}):
					if 'departureAirport' in timeline.keys():
						departure_airport = timeline['departureAirport'].get('longName','')
						departure_time = timeline['departureTime'].get('time','')
						flight_timing = {
											'departure_airport':departure_airport,
											'departure_time':departure_time,
											
						}
						timings.append(flight_timing)

				flight_info={'stops':stop,
                                        'Airport.Code':airportcode,
					'Airport.Name':Airport.Name,
					'Time.Year':Time.Year,
					'Statistics.Flights':Statistics.Flights
				}
				lists.append(flight_info)
		
		except ValueError:
			print ("Rerying...")
			
		return {"error":"failed to process the page",}

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('source',help = 'Source airport code')
	argparser.add_argument('Airport.Name',help = 'Airport.Name')
	args = argparser.parse_args()
	source = args.source
	destination = args.destination
	date = args.date
	print ("Fetching flight details")
	scraped_data = parse(source,destination,date)
	print ("Writing data to output file")
	with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
	 	json.dump(scraped_data,fp,indent = 4)
