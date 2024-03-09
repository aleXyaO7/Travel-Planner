from flask import Flask, request
from flask_cors import CORS
import requests

url = {
    'address_to_coordinates': "https://address-from-to-latitude-longitude.p.rapidapi.com/geolocationapi",
    'coordinates_to_airport': "https://aviation-reference-data.p.rapidapi.com/airports/search",
    'one_way': "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures",
    'round_trip':"https://priceline-com-provider.p.rapidapi.com/v2/flight/roundTrip",
    'region' : "https://hotels-com-provider.p.rapidapi.com/v2/regions",
    'hotelSearch' : "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search",
    'hotelDetails' : "https://hotels-com-provider.p.rapidapi.com/v2/hotels/details",
}

headers = {
    'coordinates':{
	    "X-RapidAPI-Key": "8e140a626fmsh377461c7298588ap138272jsnf7aef24a2a62",
	    "X-RapidAPI-Host": "address-from-to-latitude-longitude.p.rapidapi.com"
    },
    'airports':{
	    "X-RapidAPI-Key": "8e140a626fmsh377461c7298588ap138272jsnf7aef24a2a62",
	    "X-RapidAPI-Host": "aviation-reference-data.p.rapidapi.com"
    },
    'flights':{
	    "X-RapidAPI-Key": "8e140a626fmsh377461c7298588ap138272jsnf7aef24a2a62",
	    "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    },
    'hotels':{
	    "X-RapidAPI-Key": "617a4177ccmsh398027cd4dceddfp1a5f9ejsn34b6207bcb19",
	    "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
    }
}

def query_coordinates(address):
    query_string = {"address":address}
    response = requests.get(url['address_to_coordinates'], headers=headers['coordinates'], params=query_string)
    print(response.json())
    return {'longitude':response.json()['Results'][0]['longitude'],
            'latitude':response.json()['Results'][0]['latitude']}

def query_airports(latitude, longitude):
    query_string = {"lat":latitude,"lon":longitude,"radius":"100"}
    response = requests.get(url['coordinates_to_airport'], headers=headers['airports'], params=query_string)
    airports = []
    for i in response.json():
        airports.append({
            'code':i['iataCode'],
            'name':i['name'],
            'latitude':i['latitude'],
            'longitude':i['longitude']
        })
    return airports

def query_one_way(departure_airport, destination_airport, departure_date, adults, children, cabin_class):
    querystring = {"sid":"iSiX639",
                "adults":adults,
                "children":children,
                "departure_date":departure_date,
                "destination_airport_code":destination_airport,
                "origin_airport_code":departure_airport,
                "cabin_class":cabin_class,
                "number_of_itineraries": 10,
                "currency":"USD"}
    response = requests.get(url['one_way'], headers=headers['flights'], params=querystring).json()
    flights = []
    if response['getAirFlightDepartures']:
        for q in response['getAirFlightDepartures']['results']['result']['itinerary_data']:
            f = response['getAirFlightDepartures']['results']['result']['itinerary_data'][q]
            legs = []
            for r in f['slice_data']['slice_0']['flight_data']:
                i = f['slice_data']['slice_0']['flight_data'][r]
                legs.append({'departure_airport':i['departure']['airport']['code'],
                                'departure_date':i['departure']['datetime']['date'],
                                'departure_time':i['departure']['datetime']['time_12h'],
                                'arrival_airport':i['arrival']['airport']['code'],
                                'arrival_date':i['arrival']['datetime']['date'],
                                'arrival_time':i['arrival']['datetime']['time_12h']})
            flights.append({
                'airline':f['slice_data']['slice_0']['airline']['name'],
                'logo':f['slice_data']['slice_0']['airline']['logo'],
                'legs':legs,
                'price':f['price_details']['display_total_fare']
            })
    return flights

def query_round_trip(departure_airport, destination_airport, departure_date, return_date, adults, children, cabin_class):
    querystring = {"sid":"iSiX639",
                "adults":adults,
                "children":children,
                "departure_date":departure_date + ',' + return_date,
                "destination_airport_code":destination_airport + ',' + departure_airport,
                "origin_airport_code":departure_airport + ',' + destination_airport,
                "cabin_class":cabin_class,
                "number_of_itineraries": 10,
                "currency":"USD"}
    response = requests.get(url['round_trip'], headers=headers['flights'], params=querystring).json()
    flights = []
    for q in response['getAirFlightRoundTrip']['results']['result']['itinerary_data']:
        f = response['getAirFlightRoundTrip']['results']['result']['itinerary_data'][q]
        legs_departure, legs_return = [], []
        for r in f['slice_data']['slice_0']['flight_data']:
            i = f['slice_data']['slice_0']['flight_data'][r]
            legs_departure.append({'departure_airport':i['departure']['airport']['code'],
                         'departure_date':i['departure']['datetime']['date'],
                         'departure_time':i['departure']['datetime']['time_12h'],
                         'arrival_airport':i['arrival']['airport']['code'],
                         'arrival_date':i['arrival']['datetime']['date'],
                         'arrival_time':i['arrival']['datetime']['time_12h']})
        for r in f['slice_data']['slice_1']['flight_data']:
            i = f['slice_data']['slice_1']['flight_data'][r]
            legs_return.append({'departure_airport':i['departure']['airport']['code'],
                         'departure_date':i['departure']['datetime']['date'],
                         'departure_time':i['departure']['datetime']['time_12h'],
                         'arrival_airport':i['arrival']['airport']['code'],
                         'arrival_date':i['arrival']['datetime']['date'],
                         'arrival_time':i['arrival']['datetime']['time_12h']})
        flights.append({
            'airline':f['slice_data']['slice_0']['airline']['name'],
            'logo':f['slice_data']['slice_0']['airline']['logo'],
            'legs_departure':legs_departure,
            'legs_return':legs_return,
            'price':f['price_details']['display_total_fare']
        })
    return flights

def query_hotel(place, checkin_date, checkout_date, adults, children_ages, lodging_type, price_min, price_max, rating, amenities, sort_order):
    querystring = {"query":place,
                   "domain":"US",
                   "locale":"en_US"}
    response = requests.get(url['region'], headers=headers['hotels'], params=querystring).json()

    place_id = response['data'][0]['gaiaId']
    if children_ages:
        querystring2 = {"region_id":place_id,
                        "locale":"en_US",
                        "checkin_date":checkin_date,
                        "sort_order":sort_order,
                        "adults_number":adults,
                        "domain":"US",
                        "checkout_date":checkout_date,
                        "children_ages":children_ages,
                        "lodging_type":lodging_type,
                        "price_min":price_min,
                        "star_rating_ids":rating,
                        "page_number":"1",
                        "price_max":price_max,
                        "amenities":amenities,
                        "available_filter":"SHOW_AVAILABLE_ONLY"}
    else:
        querystring2 = {"region_id":place_id,
                        "locale":"en_US",
                        "checkin_date":checkin_date,
                        "sort_order":sort_order,
                        "adults_number":adults,
                        "domain":"US",
                        "checkout_date":checkout_date,
                        "lodging_type":lodging_type,
                        "price_min":price_min,
                        "star_rating_ids":rating,
                        "page_number":"1",
                        "price_max":price_max,
                        "amenities":amenities,
                        "available_filter":"SHOW_AVAILABLE_ONLY"}
    response2 = requests.get(url['hotelSearch'], headers=headers, params=querystring2).json()
    hotel_id = []
    pointer = 0
    while pointer <= 10:
        if pointer >= len(response2['properties']): break
        hotel_id.append(response2['properties'][pointer]['id'])
        pointer += 1
    
    hotels = {}
    for id in hotel_id:
        querystring3 = {"domain":"US","hotel_id":id,"locale":"en_US"}
        response3 = requests.get(url['hotelDetails'], headers=headers, params=querystring3).json()
        hotels[id] = {
            'name' : response3['summary']['name'],
            'address' : response3['summary']['location']['address']['addressLine'],
            'coordinates' : {'lat' : response3['summary']['location']['coordinates']['latitude'], 'lng' : response3['summary']['location']['coordinates']['longitude']},
            'amenities' : [a['text'] for a in response3['summary']['amenities']['topAmenities']['items']],
            'property_rating' : response3['summary']['overview']['propertyRating']['rating'],
            'user_rating' : response3['reviewInfo']['summary']['overallScoreWithDescriptionA11y']['value']
        }
    return hotels

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/flight', methods = ['GET'])
def flight():
    if request.method == 'GET':
        start_place = request.args.get('start_place', None)
        end_place = request.args.get('end_place', None)
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        adults = request.args.get('adults', None)
        children = request.args.get('children', None)
        cabin_class = request.args.get('cabin_class', None)
        # start_coords = query_coordinates(start_place)
        # start_airport = query_airports(start_coords['latitude'], start_coords['longitude'])[0]['code']
        # end_coords = query_coordinates(end_place)
        # end_airport = query_airports(end_coords['latitude'], end_coords['latitude'])[0]['code']
        # q = query_one_way(start_airport, end_airport, start_date, adults, children, cabin_class)
        q = [{'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '3:30pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '9:05pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-20', 'departure_time': '11:55pm', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '1:45am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '1:45pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '7:20pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-20', 'departure_time': '11:55pm', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '1:45am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '11:20am', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '4:55pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-20', 'departure_time': '11:55pm', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '1:45am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '6:50pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-21', 'arrival_time': '12:20am'}, {'departure_airport': 'IST', 'departure_date': '2024-03-21', 'departure_time': '7:35am', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '9:20am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '5:20pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '10:50pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-21', 'departure_time': '7:35am', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '9:20am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '3:30pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '9:05pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-21', 'departure_time': '7:35am', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '9:20am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '1:45pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '7:20pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-21', 'departure_time': '7:35am', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '9:20am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '6:50pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-21', 'arrival_time': '12:20am'}, {'departure_airport': 'IST', 'departure_date': '2024-03-21', 'departure_time': '1:35pm', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '3:25pm'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '11:20am', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '4:55pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-21', 'departure_time': '7:35am', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '9:20am'}], 'price': 625.53}, {'airline': 'Turkish Airlines', 'logo': 'https://secure.rezserver.com/public/media/img/air_logos2/TK.png', 'legs': [{'departure_airport': 'CDG', 'departure_date': '2024-03-20', 'departure_time': '5:20pm', 'arrival_airport': 'IST', 'arrival_date': '2024-03-20', 'arrival_time': '10:50pm'}, {'departure_airport': 'IST', 'departure_date': '2024-03-21', 'departure_time': '1:35pm', 'arrival_airport': 'TZX', 'arrival_date': '2024-03-21', 'arrival_time': '3:25pm'}], 'price': 625.53}]
        print(q)
        return q

    



if __name__ == '__main__':
    app.run()