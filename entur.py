import aiohttp
import asyncio
from enturclient import EnturPublicTransportData
from datetime import datetime, timezone, timedelta
import pytz
import pdb

API_CLIENT_ID = 'jenssen-dashboard'

async def print_stop_businfo():
    async with aiohttp.ClientSession() as client:
        stops = ['NSR:StopPlace:6059']
        quays = ['NSR:Quay:11121']

        data = EnturPublicTransportData(
            client_name=API_CLIENT_ID, # Required
            stops=stops,
            quays=quays,
            omit_non_boarding=True,
            number_of_departures=10,
            web_session=client) # recommended argument

        await data.update()

        stop_bus = data.get_stop_info('NSR:StopPlace:6059')
        n_departure = 0

        for n_departure in range(10):

            stopinfo = {
                "expected_arrival_time": stop_bus.estimated_calls[n_departure].expected_arrival_time,
                "aimed_arrival_time": stop_bus.estimated_calls[n_departure].aimed_arrival_time,
                "front_display": stop_bus.estimated_calls[n_departure].front_display
            }

            # format string to be diplayed on departure dashboard
            minutes_to_arrival = ""
            now = datetime.now(pytz.timezone('Europe/Oslo'))
            bus_arrival_time = stopinfo["expected_arrival_time"]

            if bus_arrival_time < now:
                minutes_to_arrival = "now"
            else:
                minutes_to_arrival = (bus_arrival_time-now).seconds // 60
                minutes_to_arrival = str(minutes_to_arrival) + "min"


            print(stopinfo["front_display"], ": ", minutes_to_arrival)

        #print(dir(stop_bus.estimated_calls[0]))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_stop_businfo())
