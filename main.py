import time
import pandas as pd
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY

from FlightSearch import FlightSearch

DELAY = 3
DELTA_DAYS = 3

travel_plans = [
    # {'origins': ['BCN', 'MAD'], 'destinations': ['DPS', 'KUL'], 'startDate': '10/07/2023', 'returnDate': '20/08/2023'},
    {'origins': ['BCN', 'MAD'], 'destinations': ['MNL'], 'startDate': '10/07/2023', 'returnDate': '20/08/2023'},
    # {'origins': ['MNL'], 'destinations': ['DPS', 'KEF', 'CPH'], 'startDate': '01/07/2023', 'returnDate': '12/07/2023'},
]



# origin = "BCN"
# destiantions = ["BKK"]
# startDate = "10/07/2023"
# returnDate = "20/08/2023"


def get_best_deal(origin, destination, start_date, end_date):
    best_day = None
    best_price = float('inf')
    for date in rrule(DAILY, dtstart=start_date, until=end_date):
        time.sleep(DELAY)
        flights = FlightSearch(origin, destination, date)
        
        print(f"-- {date.strftime('%d/%m/%Y')}")
        flights.get_itineraries()
        if flights.array_itineraries:
            best = flights.get_best_itinerary()
            if best.get_price() < best_price:
                best_day = best
                best_price = best.get_price()
        else:
            print("ERROR: La api no ha devuelto nada")
    return best_day


def find_best_destination_day(origins, destinations, startDate, returnDate):
    itineraries = []
    # rangos de fechas
    date_object = datetime.strptime(startDate, "%d/%m/%Y")
    start_date = date_object - timedelta(days=DELTA_DAYS)
    end_date = date_object + timedelta(days=DELTA_DAYS)
    return_date_object = datetime.strptime(returnDate, "%d/%m/%Y")
    return_start_date = return_date_object - timedelta(days=DELTA_DAYS)
    return_end_date = return_date_object + timedelta(days=DELTA_DAYS)

    for origin in origins:
        for destination in destinations:
            print(f"\n{origin}-{destination}")
            best_day = get_best_deal(origin, destination, start_date, end_date)
            print(best_day)
            itineraries.append(best_day)

            # Return flights
            print(f"\n{destination}-{origin}")
            best_return_day = get_best_deal(destination, origin, return_start_date, return_end_date)
            print(best_return_day)
            itineraries.append(best_return_day)

    return itineraries



def find_best_deals(travel_plans):
    all_itineraries = []
    for plan in travel_plans:
        print("----------------\nNew travel plan")
        origins = plan['origins']
        destinations = plan['destinations']
        startDate = plan['startDate']
        returnDate = plan['returnDate']
        itineraries = find_best_destination_day(origins, destinations, startDate, returnDate)
        all_itineraries.extend(itineraries)
    return all_itineraries



def append_to_csv(file_name, new_data):
    # Add today's date as a column
    new_data['searchDay'] = datetime.today().strftime("%d-%m-%Y")

    # Read in the existing CSV file
    df = pd.read_csv(file_name)

    new_data = pd.DataFrame(data)
    # Append the new data to the DataFrame
    df = pd.concat([df, new_data], ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    df.to_csv(file_name, index=False)


if __name__ == "__main__":
    itineraries = find_best_deals(travel_plans)

    print(f"Travel plans: {len(travel_plans)}")
    print(f"Itineraries: {len(itineraries)}")
    data = {
        'origin': [i.origin for i in itineraries],
        'destination': [i.destination for i in itineraries],
        'date': [i.date.strftime("%d-%m-%Y") for i in itineraries],
        'price': [i.price for i in itineraries],
        'carrier': [i.carrier for i in itineraries],
        'link': [i.link for i in itineraries]
    }
    append_to_csv('itineraries.csv', data)