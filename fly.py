import requests

from calendar import monthrange

from datetime import timedelta, date, datetime
"""
Example input:

orig = "OSL"  for Oslo
destination = "PAR" for Paris 
date = "2018-10-01"  "year-month-day"

"""


""" 

Some IATA airport codes

"""

#USA
los_angeles = "LAX"
orlando = "MCO"
san_francisco = "OAK"
fort_lauderdale = "FLL"
new_york = "JFK"

#ASIA
bangkok = "BKK"

#EUROPE
barcelona = "BCN"
paris = "PAR"
budapest = "BUD"
trondheim = "TRD"
manchester = "MAN"
milano = "MXP"
nice = "NCE"
reykjavik = "KEF"
madrid = "MAD"

#AFRICA
marrakech = "RAK"





"""
function for iterating through months and years, returns a tuple of the type (year,month)
"""

def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield y, m+1





"""
Function for getting the price calender for a specific month to and from specific destinations.
"""

def get_priskalender(orig, destination, year_month):
    year = year_month[0]
    month = year_month[1]
    norwegian_under26_url = 'https://www.norwegian.no/api/fare-calendar/calendar?adultCo' + \
                            'unt=1&destinationAirportCode=' + destination + '&includeTransit=true&originAi' + \
                            'rportCode=' + orig + '&outboundDate=' + str(year) +'-'+str(month)+'-01' + '&tripType=1&currencyCode=' + \
                            'NOK&campaignCode=under26&languageCode=nb-NO'
    kalender = requests.get(norwegian_under26_url)
    kalender.raise_for_status()  # raise exception if invalid respons
    return kalender


"""
Function for finding the cheapest flight in a month. Returns an array of tuples (price,day,month)
"""

def find_cheapest_in_month(orig, destination, year_month):
    cheapest = (10000,2,1)
    cheapest_array = [cheapest]
    kalender = get_priskalender(orig, destination, year_month)
    num_days = monthrange(year_month[0],year_month[1])
    dayees = num_days[1]
    for dag in range(0, dayees):
        pris = kalender.json()['outbound']['days'][dag]
        if pris['price'] <= cheapest[0] and pris['price'] > 0:
            cheapest = (pris['price'],dag)
            day = dag
            cheapest_array.append((pris['price'],dag,year_month[1]))
            if len(cheapest_array) > 1:
                max_ = max(cheapest_array)
                min_ = min(cheapest_array)
                if max_[0] != min_[0]:
                    cheapest_array.remove(max_)
    return cheapest_array

"""
Iterates from start date to end date and finds the cheapest price, returns an array of tuples with the price and the 
date for that price.
"""

def find_cheapest_from_date_to_date(orig, destination, start_date, end_date):
    cheapest = [(10000,2)]
    today = datetime.today()
    for year_month in month_year_iter(int(start_date[5:7]),int(start_date[0:4]),int(end_date[5:7])+1,int(end_date[0:4])):
        if year_month[1] < today.month and year_month[0] <= today.year:
            print(year_month,"er før dags dato")
            continue
        temp_cheapest = find_cheapest_in_month(orig,destination,year_month)
        if temp_cheapest[0][0] < cheapest[0][0]:
            cheapest = temp_cheapest
            cheap_month = year_month[1]
        elif temp_cheapest[0][0] == cheapest[0][0]:
            cheapest.append(temp_cheapest)
    print("Billigaste datoen til ", destination,"fra ", orig, "er: ", cheapest, ' ', cheap_month)
    return cheapest


by_liste = ["MAD","OAK","MCO"]

for by in by_liste:
    find_cheapest_from_date_to_date('TRD', by, '2018-09-01', '2019-03-01')




