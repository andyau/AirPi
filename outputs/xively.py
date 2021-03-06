import output
import requests
import json
import calibration

class Xively(output.Output):
	requiredData = ["APIKey","FeedID"]
	optionalData = ["calibration"]

	def __init__(self,data):
		self.APIKey=data["APIKey"]
		self.FeedID=data["FeedID"]
		self.cal = calibration.Calibration.sharedClass
		self.docal = calibration.calCheck(data)

	def outputData(self,dataPoints):
		if self.docal == 1:
			dataPoints = self.cal.calibrate(dataPoints)
		arr = []
		for i in dataPoints:
			if i["value"] != None: #this means it has no data to upload.
				arr.append({"id":i["name"],"current_value":i["value"]})
		a = json.dumps({"version":"1.0.0","datastreams":arr})
		try:
			z = requests.put("https://api.xively.com/v2/feeds/"+self.FeedID+".json",headers={"X-ApiKey":self.APIKey},data=a)
			if z.text!="": 
				print "Xively Error: " + z.text
				return False
		except Exception:
			return False
		return True
