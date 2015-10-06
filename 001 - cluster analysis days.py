__author__ = 'mirko'

import ddbscan
import json
import numpy
import datetime
from pymongo import Connection
import random

connection = Connection('localhost', 27017)

db = connection.understanding_the_attraction_dynamics_of_geolocated_hashtags

mindate=9999999999999
maxdate=0
posts=[]

for data in db.astenagusia.find():
    if data['location']!=None and 'latitude' in data['location'] and 'longitude' in data['location']:

        #print datetime.datetime.fromtimestamp(int(data['created_time'])).strftime('%Y-%m-%d %H:%M:%S')

        if mindate>float(data['created_time']):
            mindate=float(data['created_time'])

        if maxdate<float(data['created_time']):
            maxdate=float(data['created_time'])

        posts.append({  'location': [round(float(data['location']['latitude'])+random.uniform(0.0001, 0.00001),5),  #smoothing because dbscan considers two identical point like only one
                                     round(float(data['location']['longitude'])+random.uniform(0.0001, 0.00001),5)],
                        'created_time': datetime.datetime.fromtimestamp(int(data['created_time']))  })

mindate =    datetime.datetime.fromtimestamp(mindate).replace(hour=0,  minute=0, second=0, microsecond=0)
maxdate =    datetime.datetime.fromtimestamp(maxdate).replace(hour=23, minute=59,second=59,microsecond=0)
print mindate, maxdate



results_hours=[]

for day in (mindate + datetime.timedelta(days=n) for n in range((maxdate-mindate).days)):

    scan = ddbscan.DDBSCAN(eps=0.1, min_pts=1) #eps radius to look for neighbours

    for post in posts:

        if post['created_time']>= day and post['created_time'] < day + datetime.timedelta(hours=1) :
            scan.add_point(point=post['location'], count=1, desc="")

    scan.compute()

    cluster_number = 0
    clusters=[]

    for cluster in scan.clusters:

        points=[]

        for i in xrange(len(scan.points)):

            if scan.points_data[i].cluster==cluster_number:
                points.append(scan.points[i])

        cluster_number += 1

        clusters.append({
                            "points" : points,
                            "dimention" : len(points),
                            "centroid": [numpy.sum(numpy.array(points)[:, 0])/len(points),
                                         numpy.sum(numpy.array(points)[:, 1])/len(points)]
                          })

    results_hours.append({
                            'day':day.strftime('%Y-%m-%d'),
                            'date': day.strftime('%Y-%m-%d %H:%M:%S'),
                            'clusters': clusters
                        })

with open('cluster_analysis_days.json', 'w') as outfile:
    json.dump(results_hours, outfile)