
from datetime import datetime,timedelta
import schedule
import ujson

starttime=""
endtime=""
valuelst=[]
data=0
output=[]
api_url= 'http://localhost:5000/api/temperature'
missingdata_url='http://localhost:5000/api/temperature/missing'

def convert(value):
    sensorvalue=float(value)
    sensorvalueC= sensorvalue * 3.3 / 4096 # converting into volt 12 bit resolution 2^12  is 4096
    sensorvalueC=(sensorvalueC - .5 ) # (subtracting offset value)
    return sensorvalueC

def gettemperature(file):
    try:

        convalue = file.readline()
        convValue = convert(float(convalue))
        valuelst.append(convValue)

        # print("For {} : {:.2f}".format(s,convValue))
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
        output.append(data)

        print("output: {} - {} min: {:.2f}, max: {:.2f}, Avg: {:.2f}".format(starttime, endtime, minv, maxv, avg))

        del valuelst[:]

    except ValueError:
        print("Need data to read")
        return schedule.CancelJob()

async def postdata(output):
    async with aiohttp.ClientSession(
            json_serialize=ujson.dumps) as session:
        await session.post(url, json=output)


if __name__ == '__main__':
    file = open('temperature.txt', "r")

    schedule.every(0.1).seconds.do(gettemperature, file)
    schedule.every(20).seconds.do(temperaturemeasurement, valuelst)
    #schedule.every(20.1).seconds.do(postdata, output)

    while True:
        schedule.run_pending()



