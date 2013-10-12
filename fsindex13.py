#use Apache index file to get filesizes and estimate activity from HM camera

import os, sys
from datetime import datetime, timedelta, date
import urllib2
from bs4 import BeautifulSoup
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates




# module to download webcam file listing from the HM webserver
def getCamData (dt):

  year = dt.year
  month = dt.month
  day = dt.day
  
  imgTimeStampS1 = dt.strftime("%Y/%m/%d/")

  response = urllib2.urlopen('http://cam.hackmanhattan.com/hmmain/'+imgTimeStampS1)
  html = response.read()     # download the Apache auto-generated index file for the folder
  response.close()

  soup = BeautifulSoup(html) # parse the HTML source
  table = soup.find("table")

  scrapeddata = [] # store all of the records in this list


  for row in table.find_all('tr')[3:]:  # now iterate through the table

    if (len(row)==4):
      col = row.find_all('td')

      tsString = str(col[1].string)[0:16] # make 2 lists, one with timestamps and one with corresponding filesizes
      szString = str(col[3].string)[:3]

      timestamp = datetime(int(tsString[0:4]), int(tsString[5:7]), int(tsString[8:10]), int(tsString[11:13]), int(tsString[14:16])) 
      size = (float(szString[:3]))

      record = (timestamp, size)
      scrapeddata.append(record)

  data = np.array(scrapeddata) # put the data in a numpy array for easier manipulation
  return data



# draws a line graph of data vs time in date format
def lineGraph (timedataarray):

  datelist = timedataarray[:,0]
  datalist = timedataarray[:,1]
  datelist = dates.date2num(datelist)  # convert datetime format to float epoch for matplotlib

  hfmt = dates.DateFormatter('%m/%d %H:%M')
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(datelist, datalist)
  ax.xaxis.set_major_formatter(hfmt)
  plt.xticks(rotation='vertical')
  plt.autoscale(enable=True, axis = "x", tight = True)
  plt.ylabel("FileSize (K) / Light Level Correlate")
  plt.ion()
  plt.show()



#replaces input fileSize data with the calculated differential
def Activity(timesizearray):

  calc = np.diff(timesizearray[:,1])
  calc_add = np.insert(calc, 0, 0)      # insert an extra 0 to correct list offset
  processed = np.column_stack((timesizearray[:,0],calc_add))
  
  return processed



# returns a 24h array corrected for EST (GMT-5) and starting at 3 a.m. EST
def daySpan(dt):

  dt1 = dt
  dt2 = dt + timedelta(days = 1)

  day1 = getCamData(dt1)
  day2 = getCamData(dt2)

  if (day1.size > 300):

    day1 = day1[480:]
    day2 = day2[:480]

  else:

    day1 = day1[48:]
    day2 = day2[:48]

  spliceday = np.concatenate((day1, day2), axis = 0)
  gmtday = (spliceday[:,0] - timedelta(hours = 5))

  corrday = np.column_stack((gmtday,spliceday[:,1]))
 
  return corrday



# calculates various statistics from one day of camera data
def dayStats(timesizearray):

  tsa = timesizearray

  print str(tsa.size/2) + " data points"
  print str(np.trapz(tsa[:,1])) + ": integral over 1 day"
  print str(np.amin(tsa[:,1])) + ": minimum value"
  print str(np.amax(tsa[:,1])) + ": maximum value"

  lightson = np.extract(tsa[:,1] > 45, tsa) # max daytime lights off filesize is < 45K mid-summer
  lightson_min = len(lightson)
  lightson_hrs = lightson_min/((tsa.size/2)*0.04166667)
  usage = 100*lightson_min/(tsa.size/2)

  print str(round(lightson_hrs,1)) + ": hours of lights on"
  print str(round(usage, 2)) + " % time usage"

  return round(usage, 2)

def weekStats(dt):

  week = []
  
  for i in range(7):
    week.append(dayStats(daySpan((dt+timedelta(days = i)))))

  print week
  return week

def monthStats(dt):

  month = []
  
  for i in range(4):
    month.append(weekStats(dt+timedelta(weeks = i)))

  montharr = np.array(month)

  return montharr

  
# main loop
if __name__ == "__main__":

  print sys.argv
  d = date(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

  a = daySpan(d)

  lineGraph(a)

  b = Activity(a)
  lineGraph(b)

  dayStats(a)

#  print monthStats(d)

  raw_input("Press Enter to continue")
