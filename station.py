import time
import logger

class Station:
  def __init__(self, stp_id, rt_name, station_name, cta_source, next_station=None):
    self.stp_id = stp_id
    self.rt_name = rt_name
    self.name = station_name
    self.next_station = next_station
    self.stop_data_list = []
    self.__cta_source = cta_source    
    self.refresh()
  
  def refresh(self):
    try:
      self.stop_data_list = self.__cta_source.get_latest_data(
          self.stp_id, self.rt_name)
    except Exception as ex:
      logger.error('Failed to refresh data for station ' + self.name +
          ' exception: ' + str(ex))
    logger.info('refreshed station: ' + self.name)
  
  def get_current_times(self):
    return self.stop_data_list

class StopData:
  def __init__(self, pred_time, arr_time, is_app, is_sch, is_dly, is_flt):
    self.pred_time = pred_time
    self.arr_time = arr_time
    self.is_app = is_app
    self.is_sch = is_sch
    self.is_dly = is_dly
    
  def predicted_arrival_time(self):
    local_time = time.localtime(self.arr_time)
    return time.strftime('%I:%M:%S %p', local_time)
    
  def time_to_arrival(self):
    time_to_arrival_in_sec = self.arr_time - self.pred_time
    return int(time_to_arrival_in_sec / 60)
    
class Train:
  def __init__(self, station, initialize_time):
    self.station = station
    self.__initialize_time = initialize_time
    
  def get_initialize_time(self):
    return self.__initialize_time.strftime('%I:%M:%S %p')