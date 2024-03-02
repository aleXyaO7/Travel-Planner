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
    while True:
        if pointer >= len(response2['properties']): break
        hotel_id.append(response2['properties'][pointer]['id'])

    print(hotel_id)
    input()
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
            'user_rating' : response3['summary']['reviewInfo']['summary']['OverallScoreWithDescriptionA11y']['value'],
            'images' : [a['image']['url'] for a in response3['summary']['propertyGallery']['images']]
        }
    return hotels

print(query('Tokyo', '2024-03-02', '2024-03-02', '2', '', 'HOTEL', '0', '10000', '3,4,5', 'WIFI,PARKING', 'REVIEW'))