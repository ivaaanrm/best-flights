import json
import requests


class Flight:
    """Calse donde se genera los datos de los vuelos dado un origen 
            y un destino y una fecha """

    def __init__(self, origin, destination, date):
        self.origin = origin
        self.destination = destination
        self.date = date
        self.KEY = "prtl6749387986743898559646983194"
        self.adults = 1
        self.cabin_class = "CABIN_CLASS_ECONOMY"
        self.response = self.search_live_flights()
        # self.response = self.read_json()
        self.array_itineraries = []


    def search_live_flights(self):
    # Formatear el cuerpo de la solicitud en formato JSON
        payload = {
            "query": {
                "market": "ES",
                "locale": "es-ES",
                "currency": "EUR",
                "query_legs": [
                    {
                            "origin_place_id": {
                                "iata": self.origin
                            },
                        "destination_place_id": {
                                "iata": self.destination
                        },
                        "date": {
                                "year": self.date.year,
                                "month": self.date.month,
                                "day": self.date.day
                        }
                    }
                ],
                "adults": self.adults,
                "cabin_class": self.cabin_class
            }
        }
        headers = {
            "x-api-key": self.KEY,
            "Content-Type": "application/json"
        }

        # Enviar solicitud POST a la API de Skyscanner
        response = requests.post(
            "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create",
            data=json.dumps(payload),
            headers=headers
        )
        # Procesar la respuesta
        return json.loads(response.text)


    def get_itineraries(self):
        try:
            itineraries = self.response["content"]["results"]["itineraries"]
            for itinerary in itineraries:
                itineraryId = itinerary
                price = float(itineraries[itinerary]["pricingOptions"][0]["price"]["amount"])/1000
                deepLink = itineraries[itinerary]["pricingOptions"][0]["items"][0]["deepLink"]        
                operatingCarrierIds = self.response["content"]["results"]["legs"][itinerary]["operatingCarrierIds"][0] # !puede ser que haya más de uno
                carrier = self.response["content"]["results"]["carriers"][operatingCarrierIds]["name"]
                new_itinerary = Itinerary(self.origin, self.destination, self.date, itineraryId, price, deepLink, carrier)
                self.array_itineraries.append(new_itinerary)

        except:
            print("Error en los datos devueltos")
            

    # Devuelve el vuelo más barato
    def get_cheapest_itinerary(self):
        bestItineraryId = self.response["content"]["sortingOptions"]["cheapest"][0]["itineraryId"]
        for iti in self.array_itineraries:
            if iti.get_id() == bestItineraryId:
                return iti


    # Devuelve el vuelo que skyscanner considera mejor
    def get_best_itinerary(self):
        bestItineraryId = self.response["content"]["sortingOptions"]["best"][0]["itineraryId"]
        for iti in self.array_itineraries:
            if iti.get_id() == bestItineraryId:
                return iti
    

    def read_json(self):
        name = f"flights/response_{self.destination}_{self.date.strftime('%d_%m')}.json"
        with open(name, 'r') as json_file:
            return json.load(json_file)
    

    def save_response(self):
        name = f"flights/response_{self.destination}_{self.date.strftime('%d_%m')}.json"
        with open(name, 'w') as f:
            # Use the json.dump function to write the data to the file with indentation
            json.dump(self.response, f, indent=4)

   


    def __str__(self):
        return f"{len(self.array_itineraries)} options to flight from {self.origin} to {self.destination} on {self.date.strftime('%m/%d/%Y')}"



class Itinerary(Flight):
    def __init__(self, origin, destination, date, id, price, deepLink, carrier):
        super().__init__(origin, destination, date)
        self.price = price
        self.id = id
        self.link = deepLink
        self.carrier = carrier

    def get_id(self):
        return self.id

    def get_link(self):
        return self.link

    def get_price(self):
        return self.price

    def __str__(self):
        return f"\n--- Itinerary: {self.carrier}\nFlight from {self.origin} to {self.destination} on {self.date.strftime('%d/%m/%Y')}\n{self.price} €"

    
