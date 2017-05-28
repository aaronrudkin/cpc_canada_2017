import os
import requests
import json
import time

try:
	os.mkdir("round_1")
except:
	pass

r_base = requests.get("https://www.intvoting.com/cpcresults/ResultsService.svc/GetAreas?lang=en").json()
with open("round_1/base.json", "w") as f:
	json.dump(r_base, f)

for i in [102, 115]: #xrange(1, 353):
	print i
	if i % 10 == 0:
		time.sleep(2)

	try:
		r_f = requests.get("https://www.intvoting.com/cpcresults/ResultsService.svc/GetAreaResult?id=" + str(i)).json()
		with open("round_1/area_" + str(i) + ".json", "w") as f:
			json.dump(r_f, f)
	except:
		print "failed"