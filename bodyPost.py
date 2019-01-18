import os
import glob
import fnmatch
import webbrowser

#Set your Info here!#####
cmdr_name="CMDR FillInYourNameHere"
current_region="Inner Orion Spur"
#########################

#Get most recent Journal File
newest = max(glob.iglob('*.log'), key=os.path.getctime)
journal = open(newest,"r")
journal_content = journal.readlines()
journal_content.reverse()
last_scan = ""
last_system = ""

#Get most recent Scan and System
for entry in journal_content:
	if fnmatch.fnmatch(entry,'*"ScanType":"Detailed"*'):
		last_scan = entry
		break

for entry in journal_content:
	if fnmatch.fnmatch(entry,'*"StarSystem":*'):
		last_system = entry
		break

##Time to pretty-fy!
body_name = ""
star_name = ""
planet_class = ""


last_scan = last_scan.split(",")
last_system = last_system.split(",")

for segment in last_scan:
	if "BodyName" in segment:
		body_name = segment.split('"')[3]

for segment in last_scan:
	if "PlanetClass" in segment:
		planet_class = segment.split('"')[3]

star_name = last_system[2].split('"')[3]


#Materials are a bit more work.
material_list = ""
check_mats = False
for segment in last_scan:
	if '"Materials":' in segment:
		last_scan = last_scan[last_scan.index(segment)-1:]
		check_mats = True
		break

if check_mats:
	findable = ["antimony","arsenic","boron","cadmium","carbon","chromium","germanium","iron","lead","manganese","mercury","molybdenum","nickel","niobium","phosphorus","polonium","rhenium","ruthenium","selenium","sulphur","technetium","tellurium","tin","tungsten","vanadium","yttrium","zinc","zirconium"]
	for segment in last_scan:
		if any(x in segment for x in findable):
			material_list += segment.split('"')[-2]
			percent = last_scan[last_scan.index(segment)+1].split(":")[-1]
			percent = percent.split("}")[0]
			material_list += ": [" + percent[:-5] + "], "

material_list = material_list[:-2]
	

#Last step - Planet types are differently named. Let's try to match them to the form!
if planet_class in "Icy body":
	planet_class = "Ice"
if planet_class in "Rocky body":
	planet_class = "Rocky"
if planet_class in "Metal rich body":
	planet_class = "Rocky"
if planet_class in "High metal content body":
	planet_class = "HMC"
if planet_class in "Rocky ice world":
	planet_class = "Rocky Ice"

star_name = star_name.lower()
star_name = star_name.swapcase()
body_name = body_name.lower()
body_name = body_name.swapcase()
material_list = material_list.title()

print(current_region)
print(star_name)
print(body_name)
print(planet_class)
print(material_list)
print(cmdr_name)

webbrowser.open('https://airtable.com/shrpoiulL1A3IFGeu?prefill_Region='+current_region+'&prefill_System='+star_name+'&prefill_Planet+Name='+body_name+'&prefill_Planet+Type='+planet_class+'&prefill_Planet+Materials='+material_list+'&prefill_Scouted+by='+cmdr_name)
