import os
from glob import glob
import fnmatch
import webbrowser
import time

#Set your Info here!#####
cmdr_name="CMDR FillInYourNameHere"
current_region="Inner Orion Spur"
#########################
#Set to false to only run for last body scanned#
run_continuously = True
polling_interval = 0.2 # seconds between journal checks
useOCR = True
#########################
# OCR parameters
ratio = 16/9
leftF = 0.79
topF = 0.09
bottomF = 0.21
rightF = 0.93
#########################
# recognized strings
beacon = "locations"
poiTypes = ["biological", "geological", "thargoid", "human"]
#########################

try:
	from PIL import Image
	import pytesseract
	import argparse
	import cv2
	import numpy as np
	from win32gui import GetForegroundWindow, GetWindowRect, GetWindowText
	from mss.windows import MSS as mss
	import re
except:
	useOCR = False

last_body_opened = None
last_insufficient = False

def check(first_run = False, pois = None):
	global last_body_opened
	
	#Get most recent Journal File
	newest = max(glob('Journal*.log'), key=os.path.getctime)
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
	
	if last_scan == "":
		if not run_continuously:
			print("No scan found in the last journal log.")
		return
	if last_system == "":
		if not last_insufficient:
			print("No current system information available. Please engage/disengage Supercruise to get current system info.")
			last_insufficient = True
		return #we should not be here, if there is a scan, there should necessarily be a StarSystem field
	last_insufficient = False
	
	##Time to pretty-fy!
	body_name = ""
	star_name = ""
	planet_class = ""
	
	
	last_scan = last_scan.split(",")
	last_system = last_system.split(",")
	
	for segment in last_scan:
		if "BodyName" in segment:
			body_name = segment.split('"')[3]
			#avoid opening the browser twice for the same body
			if body_name != last_body_opened:
				last_body_opened = body_name
			else:
				return
		if "PlanetClass" in segment:
			planet_class = segment.split('"')[3]
		#if '"timestamp":' in segment:
		#	time_sc = segment.split('":"')[1]
			#print(time_sc)
		if '"StarType"' in segment:
			if not (first_run and run_continuously): # don't print error messages in first run
				print("%s is a star" % body_name)
			return #we are not interested in stars
		if '"Landable"' in segment:
			landable = segment.split('":')[1]
			if landable == "false":
				if not (first_run and run_continuously): # don't print error messages in first run
					print("Planet %s is not landable." % body_name)
				return #planet is not landable and has no POIs
	
	if first_run and run_continuously:
		return # first scan is from before starting the program, just run til here to save last scan body
	
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
	if planet_class == "":
		print("Body %s is not a planet." % body_name)
		return #Invalid body
	elif planet_class in "Icy body":
		planet_class = "Ice"
	elif planet_class in "Rocky body":
		planet_class = "Rocky"
	elif planet_class in "Metal rich body":
		planet_class = "Rocky"
	elif planet_class in "High metal content body":
		planet_class = "HMC"
	elif planet_class in "Rocky ice world":
		planet_class = "Rocky Ice"
	else:
		print("Planet %s is not landable." % body_name)
		return #planet is surely not landable and has no POIs; a planet of different type cannot be submitted using the form
	
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
	
	bios = 0
	geos = 0
	thargoid = 0
	human = 0
	
	if pois:
		for k, v in pois.items():
			if k == poiTypes[0]:
				bios = v
			elif k == poiTypes[1]:
				geos = v
			elif k == poiTypes[2]:
				thargoid = v
			elif k == poiTypes[3]:
				human = v
	
	bios = str(bios)
	geos = str(geos)
	thargoid = str(thargoid)
	human = str(human)
	webbrowser.open('https://airtable.com/shrpoiulL1A3IFGeu?prefill_Region='+current_region+'&prefill_System='+star_name+'&prefill_Planet+Name='+body_name+'&prefill_Planet+Type='+planet_class+'&prefill_Planet+Materials='+material_list+'&prefill_Scouted+by='+cmdr_name+'&prefill_Bio+POI%27s='+bios+'&prefill_Geo+POI%27s='+geos+'&prefill_Thargoid+POI%27s='+thargoid+'&prefill_Human+POI%27s='+human)

def grab(sct, rect):
	left, top, right, bottom = rect
	
	height = bottom - top
	width = right - left
	
	Wleft = int(height * ratio * leftF + ((width - height * ratio) / 2))
	Wtop = int(height * topF)
	Wbottom = int(height * bottomF)
	Cwidth = int(height * ratio * (rightF - leftF))
	
	window = {"top": top + Wtop, "left": left + Wleft, "width": Cwidth, "height": Wbottom - Wtop}
	return np.array(sct.grab(window))

def OCR(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 105, 255, cv2.THRESH_TOZERO)[1]
	
	text = pytesseract.image_to_string(gray, config="--psm 11 -l eng --oem 3")
	
	print('OCR result: ' + text)
	#cv2.imshow("Cropped", image)
	#cv2.imshow("Binarized", gray)
	#cv2.waitKey(0)
	return text

def getPOIs(text):
	text = text.lower()
	ret = {}
	if beacon not in text:
		return ret
	for x in poiTypes:
		regex = x + " \(([0-9]+)\)"
		m = re.search(regex, text)
		if m:
			amt = m.group(1)
			try:
				amt = int(amt)
			except:
				continue
			if amt > 0:
				ret[x] = amt
	return ret

if not run_continuously:
	check()
else:
	if useOCR:
		with mss() as sct:
			while True:
				w = GetForegroundWindow()
				if GetWindowText(w) == 'Elite - Dangerous (CLIENT)':
					image = grab(sct, GetWindowRect(w))
					text = OCR(image)
					pois = getPOIs(text)
					print(pois)
					if pois:
						check(pois=pois)
				time.sleep(polling_interval)
	else:
		check(True)
		while True:
			time.sleep(polling_interval)
			check()
