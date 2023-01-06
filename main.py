from datetime import datetime

from Flight import Flight

origin = "BCN"
destiantions = ["MAD", "DPS", "BKK"]
date = datetime(2023, 1, 24)

for destination in destiantions:
  flight = Flight(origin, destination, date)
  # flight.save_response()
  flight.get_itineraries()
  best = flight.get_best_itinerary()
  # # barato = flight.get_cheapest_itinerary()
  print(best, best.get_link())








