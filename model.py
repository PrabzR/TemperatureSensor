from datetime import datetime,timedelta
import schedule
from http.client import HTTPConnection
import json

starttime=""
endtime=""
valuelst=[]
data={}
output=[]
missing_data={}
#api_url= 'http://localhost:5000/api/temperature'
#missingdata_url='http://localhost:5000/api/temperature/missing'

def convert(value):
    sensorvalue=float(value)
    sensorvalueC= sensorvalue * 3.3 / 4096 # converting into volt 12 bit resolution 2^12  is 4096
    sensorvalueC=(sensorvalueC - .5) # (subtracting offset value)
    return sensorvalueC

def gettemperature(file):
    try:

        convalue = file.readline()
        convalue=float(convalue)              # validating given value is digit and
        if (convalue>=0 and convalue<=4096):  # value ranges between -50 - +50 degree celsius
            convValue = convert(convalue)
        valuelst.append(convValue)


        if not valuelst:
            schedule.CancelJob()

    except ValueError:
        file.close()


def temperaturemeasurement(valuelst):
    try:

        endtime= datetime.now()
        starttime= endtime - timedelta(seconds=20)
        starttime=starttime.isoformat()
        endtime=endtime.isoformat()


        minv = round(min(valuelst),2)
        maxv = round(max(valuelst),2)
        avg = round(sum(valuelst) / len(valuelst),2)
        data = {"time": {
            "start": starttime,  # Start date and time in ISO8601 format for the measurement,
            "end": endtime},  # End date and time in ISO8601 format for the measurement},
            "min": minv,  # Minimum observed temperature
            "max": maxv,  # Maximum observed temperature
            "average": avg  } # Average temperature
        #output= str(starttime )+ "-" +str(endtime)+"min value: "+minv+" Max value: "+maxv+" Average: "+avg
        output.append(data)


        print("output: {} - {} min: {:.2f}, max: {:.2f}, Avg: {:.2f}".format(starttime, endtime, minv, maxv, avg))

        del valuelst[:]
        return output

    except ValueError:
        print("Need data to read")
        return schedule.CancelJob()

def postdata(output):
    httphost = "localhost"
    port = 9000
    httpmethod = "POST"
    url = "/api/temperature"
    missing_url="/api/temperature/missing"
    headers = {'Content-type': 'application/json'}

    conn = HTTPConnection(httphost, port)
    conn.connect()

    print("Connected with server in ",port)
    json_data = json.dumps(output, indent=4)

    conn.request(httpmethod, url, json_data, headers={})
    print("After: ",conn.getresponse().status)
    if (conn.getresponse().status > 500):
        missing_data.append(output)
        json_missing_data = json.dumps(missing_data, indent=4)
        conn.request(httpmethod,missing_url,json_missing_data,headers={})
        print("After: ", conn.getresponse().status)

    del output


if __name__ == '__main__':
    file = open('temperature.txt', "r")
    schedule.every(0.1).seconds.do(gettemperature, file)
    schedule.every(20).seconds.do(temperaturemeasurement, valuelst)
    schedule.every(20.1).seconds.do(postdata, output)

    while True:
        schedule.run_pending()


