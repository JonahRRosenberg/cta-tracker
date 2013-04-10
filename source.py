import time
import urllib
from xml.etree import ElementTree
import client
import logger
from station import StopData

KEY = '26d8e191c10a4b8aae72a39c26841f34'

class CTASource:
  def __init__(self):
    pass
    
  def get_latest_data(self, stp_id, rt_name):
    response = urllib.urlopen(self.__api_request(KEY, stp_id, rt_name))
    client.requests_made = client.requests_made + 1
    
    stop_data_list = []
    
    tree = ElementTree.parse(response)
    root = tree.getroot()
    stops = list(root.iter('eta'))
    
    for stop in stops:
      predicted_time = time.strptime(stop.find('prdt').text, '%Y%m%d %H:%M:%S')
      arrival_time = time.strptime(stop.find('arrT').text, '%Y%m%d %H:%M:%S')
      is_app = bool(int(stop.find('isApp').text))
      is_sch = bool(int(stop.find('isSch').text))
      is_dly = bool(int(stop.find('isDly').text))
      is_flt = bool(int(stop.find('isFlt').text))
      
      data = StopData(time.mktime(predicted_time), time.mktime(arrival_time), is_app, is_sch, is_dly, is_flt)
      stop_data_list.append(data)
    
    if len(stop_data_list) <= 0:
      logger.warn('Could not find data for stp_id: ' + str(stp_id) + 
          ' and rt_name: ' + rt_name)
          
    return stop_data_list
        
  def __api_request(self, key, stp_id, rt_name):
    return 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={0}&stpid={1}&rt={2}'.format(key, stp_id, rt_name)
    