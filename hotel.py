import requests

url = {
    'region' : "https://hotels-com-provider.p.rapidapi.com/v2/regions",
    'hotelSearch' : "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search",
    'hotelDetails' : "https://hotels-com-provider.p.rapidapi.com/v2/hotels/details",
}

headers = {
	"X-RapidAPI-Key": "617a4177ccmsh398027cd4dceddfp1a5f9ejsn34b6207bcb19",
	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
}

def query(place, checkin_date, checkout_date, adults, children_ages, lodging_type, price_min, price_max, rating, amenities, sort_order):
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

def query1():
    {'416454': {'name': 'Palace Hotel Tokyo', 'address': '1-1-1 Marunouchi, Chiyoda, Tokyo, Tokyo-to, 100-0005', 'coordinates': {'lat': 35.684901, 'lng': 139.761255}, 'amenities': ['Pool', 'Spa', 'Free WiFi', 'Parking available', 'Restaurant', 'Bar'], 'property_rating': 5, 'user_rating': '9.8/10 Exceptional'}, '2434355': {'name': 'Shangri-La Tokyo', 'address': 'Marunouchi Trust Tower Main, 1-8-3 Marunouchi, Chiyoda-ku, Tokyo, Tokyo-to, 100-8283', 'coordinates': {'lat': 35.681957, 'lng': 139.76956}, 'amenities': ['Pool', 'Pet friendly', 'Spa', 'Free WiFi', 'Parking available', 'Restaurant'], 'property_rating': 5, 'user_rating': '9.6/10 Exceptional'}, '44877300': {'name': 'Tokyo Bay Shiomi Prince Hotel', 'address': '2-8-16 Shiomi, Tokyo, Tokyo, 135-0052', 'coordinates': {'lat': 35.660534, 'lng': 139.8171}, 'amenities': ['Spa', 'Free WiFi', 'Parking available', 'Restaurant', 'Bar', 'Laundry facilities'], 'property_rating': 4, 'user_rating': '9.4/10 Exceptional'}, '27389865': {'name': 'ICI HOTEL Asakusabashi', 'address': '1-26-6, Asakusabashi, Taito-ku, Tokyo, Tokyo, 111-0053', 'coordinates': {'lat': 35.698326, 'lng': 139.783608}, 'amenities': ['Pet friendly', 'Free WiFi', 'Parking available', 'Restaurant', 'Laundry facilities', 'Air conditioning'], 'property_rating': 3.5, 'user_rating': '9.4/10 Exceptional'}, '36923967': {'name': 'Onyado Nono Asakusa Natural Hot Springs', 'address': '2-7-20, Asakusa, Taito, Tokyo, Tokyo, 111-0032', 'coordinates': {'lat': 35.714417, 'lng': 139.794312}, 'amenities': ['Onsen', 'Free WiFi', 'Parking available', 'Restaurant', 'Laundry facilities', 'Air conditioning'], 'property_rating': 3, 'user_rating': '9.4/10 Exceptional'}, '200300': {'name': 'Grand Nikko Tokyo Daiba', 'address': '2-6-1 Daiba, Minato-ku, Tokyo, Tokyo-to, 135-8701', 'coordinates': {'lat': 35.62506, 'lng': 139.77168}, 'amenities': ['Pool', 'Spa', 'Free WiFi', 'Parking available', 'Restaurant', 'Bar'], 'property_rating': 4.5, 'user_rating': '9.4/10 Exceptional'}, '661016': {'name': 'Cerulean Tower Tokyu Hotel', 'address': '26-1 Sakuragaoka-cho, Shibuya-ku, Tokyo, Tokyo-to, 150-8512', 'coordinates': {'lat': 35.65656, 'lng': 139.699463}, 'amenities': ['Spa', 'Free WiFi', 'Parking available', 'Restaurant', 'Bar', 'Laundry facilities'], 'property_rating': 5, 'user_rating': '9.4/10 Exceptional'}, '17563450': {'name': 'Dormy Inn Premium Kanda', 'address': '1-16 Suda-cho, Kanda, Chiyoda-ku, Tokyo, 101-0041', 'coordinates': {'lat': 35.695168, 'lng': 139.770315}, 'amenities': ['Spa', 'Free WiFi', 'Parking available', 'Restaurant', 'Laundry facilities', 'Air conditioning'], 'property_rating': 3, 'user_rating': '9.4/10 Exceptional'}, '42600519': {'name': 'Kimpton Shinjuku Tokyo, an IHG Hotel', 'address': '3 CHOME-4-7 NISHISHINJUKU, Tokyo, 160-0023', 'coordinates': {'lat': 35.685783, 'lng': 139.6923}, 'amenities': ['Pet friendly', 'Free WiFi', 'Parking available', 'Restaurant', 'Bar', 'Electric vehicle charging point'], 'property_rating': 5, 'user_rating': '9.4/10 Exceptional'}, '894625': {'name': 'Four Seasons Hotel Tokyo at Marunouchi', 'address': '1-11-1 Marunouchi, Chiyoda-ku, Tokyo, Tokyo-to, 100-6277', 'coordinates': {'lat': 35.677994, 'lng': 139.76743}, 'amenities': ['Pet friendly', 'Spa', 'Free WiFi', 'Internet access', 'Parking available', 'Restaurant'], 'property_rating': 5, 'user_rating': '9.4/10 Exceptional'}, '29660943': {'name': 'Pullman Tokyo Tamachi', 'address': '3 1 21 Shibaura, Minato, Tokyo, Tokyo, 1088566', 'coordinates': {'lat': 35.64547, 'lng': 139.74866}, 'amenities': ['Spa', 'Free WiFi', 'Parking available', 'Restaurant', 'Bar', 'Electric vehicle charging point'], 'property_rating': 4.5, 'user_rating': '9.4/10 Exceptional'}}