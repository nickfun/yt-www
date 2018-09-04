#
# processes
#
app: python server.py
jobs: python spider.py
bean: beanstalkd -b $BEANSTALK_BINFOLDER -p $BEANSTALK_PORT
web: caddy -port $WEB_PORT
