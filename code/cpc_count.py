import json
import csv
import unidecode

f = open("../summary_results.csv", "w")
w = csv.writer(f)
w.writerow(["Area", "ID", "NumVotes", "WinRound1", "WinLastRound"])

f2 = open("../detailed_results.csv", "w")
w2 = csv.writer(f2)
w2.writerow(["Area", "ID", "Candidate", 
		"Round1", "Round2", "Round3", "Round4",
		"Round5", "Round6", "Round7", "Round8",
		"Round9", "Round10", "Round11", "Round12",
		"Win_R1", "Win_Final"])

base = json.loads(open("../raw_data/base.json", "r").read())
district_level = {}
for thing in base["d"]:
	load_file = json.loads(open("../raw_data/area_"+str(thing["id"])+".json", "r").read())

	max_1 = 0
	winner_1 = ""
	max_final = 0
	winner_final = ""
	for cand in load_file["d"]["res"]:
		if cand["rnd"][0] > max_1 and cand["nm"] != "Undervotes":
			max_1 = cand["rnd"][0]
			winner_1 = cand["nm"]
		if cand["rnd"][-1] > max_final and cand["nm"] != "Undervotes":
			max_final = cand["rnd"][-1]
			winner_final = cand["nm"]

	for cand in load_file["d"]["res"]:
		i_am_winner1 = 0
		i_am_winner_final = 0
		if winner_1 == cand["nm"]:
			i_am_winner1 = 1
		if winner_final == cand["nm"]:
			i_am_winner_final = 1
		if int(thing["id"])>=15:
			cand_row = [unidecode.unidecode(thing["nm"]), thing["id"], unidecode.unidecode(cand["nm"])] + cand["rnd"] + [i_am_winner1, i_am_winner_final]
		else:
			cand_row = [unidecode.unidecode(thing["nm"]) + " (Region)", thing["id"], unidecode.unidecode(cand["nm"])] + cand["rnd"] + [i_am_winner1, i_am_winner_final]
		w2.writerow(cand_row)

	print thing["nm"], thing["id"], load_file["d"]["bal"], winner_1, winner_final
	if int(thing["id"])>=15:
		w.writerow([unidecode.unidecode(thing["nm"]), thing["id"], load_file["d"]["bal"], winner_1, winner_final])
	else:
		w.writerow([unidecode.unidecode(thing["nm"]) + " (Region)", thing["id"], load_file["d"]["bal"], winner_1, winner_final])
