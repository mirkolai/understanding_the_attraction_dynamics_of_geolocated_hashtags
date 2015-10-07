__author__ = 'mirko'
# -*- coding: iso-8859-15 -*-

import json
import urllib2
import time
import traceback
import logging
import config as cgf



access_token=cgf.instagram['access_token']
client_id=cgf.instagram['client_id']
client_secret=cgf.instagram['client_secret']



tags=["anstenagusia","bbklive"]

logging.basicConfig(filename='instagram.log',level=logging.DEBUG)


for tag in tags:

    next_result="https://api.instagram.com/v1/tags/"+tag+"/media/recent?access_token="+access_token

    while(next_result):
        logging.debug(next_result)
        time.sleep(2)
        response = urllib2.urlopen(next_result)
        result = response.read()
        result = json.loads(result)

        if 'data' in result:

            deadline=False

            for media in result['data']:

                try:
                    if int(media['created_time']) < 1433116800: #Mon, 01 Jun 2015 00:00:00 GMT
                        deadline=True
                    else:
                        print media

                except Exception, err:

                    logging.warning(traceback.format_exc())

        if not deadline and result['pagination'].get('next_url'):
            next_result=result['pagination']['next_url']
        else:
            next_result=None


