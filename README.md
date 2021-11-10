# TemperatureSensor
Temperature Measurement
Here the task is to convert temperature reading from a temperature sensor into Celsius and find the minimum ,maximum and average value and display that value in localhost:5000 for  the time period 2 minutes with start time and end time.
 The given  value has been reading with 12 bit resolution and with reference voltage 3.3v using ADC.
The gettemperature() function temperature has to be read the value in text file for every 100 ms and convert that value.
The stored minimum,maximum and average value has to send with starttime and endtime in json format to ‘http:://localhost:5000/api/temperature’ using HTTP POST request.
The starttime and endtime should be in ISO8601.
In error handling, if suppose failure occurred due to backend fail then the 10  temperature measurement values should be sent to the endpoint ‘http:://localhost:5000/api/temperature/missing’ in a json array format.
