from flask import Flask
import requests

url = {
    'one_way': "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures",
    'round_trip':"https://priceline-com-provider.p.rapidapi.com/v2/flight/roundTrip",
    'region' : "https://hotels-com-provider.p.rapidapi.com/v2/regions",
    'hotelSearch' : "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search",
    'hotelDetails' : "https://hotels-com-provider.p.rapidapi.com/v2/hotels/details",
}

headers = {
    'flights':{
	    "X-RapidAPI-Key": "8e140a626fmsh377461c7298588ap138272jsnf7aef24a2a62",
	    "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    },
    'hotels':{
	    "X-RapidAPI-Key": "617a4177ccmsh398027cd4dceddfp1a5f9ejsn34b6207bcb19",
	    "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
    }
}

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
    response = requests.get(url['one_way'], headers=headers, params=querystring).json()
    flights = []
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
    response = requests.get(url['round_trip'], headers=headers, params=querystring).json()
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
    response = requests.get(url['region'], headers=headers, params=querystring).json()

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

@app.route('/info')
def info():
    return ("hello world")


if __name__ == '__main__':
    app.run()