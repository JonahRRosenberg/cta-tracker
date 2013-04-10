from bottle import route, run, SimpleTemplate, template
from source import CTASource
from client import CTAClient
import os
import logger

@route('/')
def run_app():
  now_time = client.get_current_time()
  current_time = now_time.strftime('%I:%M:%S %p')
  return template('base.tpl',
      stations=client.stations,
      trains=client.trains,
      current_time=current_time)
      
logger.initialize()

#cta_source = CTASource()
#client = CTAClient(cta_source)
  
run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
  
#try:
#except KeyboardInterrupt:
#  logger.info('^C Received. Shutting Down Server.')
#except Exception as ex:
#  logger.error('Exception occurred. ex: ' + str(ex))
#except:
#  logger.error('Unknown Exception occurred')
