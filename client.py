from datetime import datetime
from dateutil import tz
from threading import Thread
import time
import csv
import logger

from station import Station
from station import Train

requests_made = 0

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

class CTAClient:
  def __init__(self, cta_source):
    self.__cta_source = cta_source
    self.stations = []
    
    logger.info('Initializing Stations')
    
    with open('stations.csv', 'rb') as csvfile:
      for row in csv.reader(csvfile):
        stp_id = int(row[0])
        rt_name = row[1]
        station_name = row[2]
        
        if len(self.stations) <= 0:
          station = Station(stp_id, rt_name, station_name,
            cta_source)
          self.stations.append(station)
        else:
          station = Station(stp_id, rt_name, station_name,
            cta_source, self.stations[0])
          self.stations.insert(0, station)
        
    logger.info('Initialized Stations')
    
    self.trains = dict()
    self.__starting_station = self.stations[0]
    
    #refresh_thread = Thread(target = self.__refresh_trains)
    #refresh_thread.daemon = True
    #refresh_thread.start()
    
  def get_current_time(self):
    utc = datetime.utcnow().replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)
    
  def __refresh_trains(self):
    while(True):
      try:
        station = self.__starting_station
        
        self.__refresh_stations(station)
        
        logger.info('Total requests made: ' + str(requests_made))
        
        while station:
          next_station = station.next_station
          if (next_station and
              len(next_station.stop_data_list) > 0 and
              len(station.stop_data_list) > 0):
            next_stop_data = next_station.stop_data_list[0]
            stop_data = station.stop_data_list[0]
            if (not next_stop_data.is_sch and
                next_stop_data.arr_time < stop_data.arr_time):
              if station.stp_id in self.trains:
                station = next_station
                continue
                
              time_now = self.get_current_time()
              train = Train(station, time_now)
              self.trains[station.stp_id] = train
              logger.info('Found Train: {0}, initialize_time: {1}'.format(
                  train.station.name, train.get_initialize_time()))
            elif station.stp_id in self.trains:
              train = self.trains[station.stp_id]
              logger.info('Removing train: {0}, initialize_time: {1}'.format(
                  train.station.name, train.get_initialize_time()))
              del self.trains[station.stp_id]
          
          station = next_station
        
        time.sleep(5.0)
      except Exception as e:
        logger.error('Exception occured: ' + str(e))
      except:
        logger.error('Unknown exception occured')

  def __refresh_stations(self, station):
    while station:
      station.refresh()
      station = station.next_station
      