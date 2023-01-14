import time
from datetime import datetime
from dateutil.rrule import rrule, DAILY

from FlightSearch import FlightSearch

origin = "BCN"
destiantions = ["KEF","BKK","DPS"]
startDate = "10/07/2023"
endDate = "20/07/2023"


def find_best_itinerary_by_destination(origin, destiantions, startDate, endDate):
	for destination in destiantions:
		print(f"\n{origin}-{destination}")
		best_day = None
		best_price = float('inf')
		for date in rrule(DAILY, dtstart=datetime.strptime(startDate, "%d/%m/%Y"), until=datetime.strptime(endDate, "%d/%m/%Y")):
			time.sleep(3)
			flights = FlightSearch(origin, destination, date)
			print(f"-- {date.strftime('%d/%m/%Y')}")
			flights.get_itineraries()
			best = flights.get_best_itinerary()  #  Del día
			if best.get_price() < best_price:
				best_day = best
				best_price = best.get_price()
		print(best_day)
		print(best_day.get_link())


if __name__ == "__main__":
	find_best_itinerary_by_destination(origin, destiantions, startDate, endDate) 
	# flights = FlightSearch("BCN", "KUL", datetime(2023,7,10))
	# flights.get_itineraries()
	# best = flights.get_best_itinerary() 
	# print(best)



	
