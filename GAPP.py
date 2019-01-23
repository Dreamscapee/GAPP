from tkinter import *
from tkinter import ttk
import requests
import re
import csv
import collections
import math
from lxml import html
from lxml import etree


'''
Track Data
Here we store all the data for all the tracks.
I was originally doing this in a .csv file, however this was causing issues with builds, so is now stored inside the program.
'''
trackData = {
	"A1-Ring": [249.22, 714.42, 676.29, 789.1, 511.89, 141.46, 0.875, 0.7829, 307.1, 0.89211, 21, 9],
	"Adelaide": [631.9, 496.9, 358.33, 549.99, 652.05, 79.46, 0.807, 0.6774, 298.6, 0.94557, 19.5, 12],
	"Ahvenisto": [993.04, 466.54, 699.74, 766.1, 240.15, 228.29, 0.8455, 0.796, 243.2, 0.9336, 11.5, 10],
	"Anderstorp": [250.72, 699.88, 769.29, 611.18, 107.05, 75.32, 0.9042, 0.785, 281.8, 0.971, 13.5, 10],
	"Austin": [521.56, 605.59, 608.9, 640.62, 786.9, 173.6, 0.8617, 0.752, 308.9, 1.00374, 17.5, 20],
	"Avus": [302.56, 636.26, 412.4, 387.41, 821.34, 103.25, 0.90563, 0, 312.3, 1.18641, 13, 4],
	"Baku City": [362.08, 615.56, 611.02, 706, 716.97, 96.71, 0.89345, 0, 306.3, 1.00055, 17, 20],
	"Barcelona": [457.87, 673.95, 503.46, 676.11, 315.93, 140.56, 0.874, 0, 307.3, 1.0933, 21, 16],
	"Brands Hatch": [475.32, 647.54, 386.69, 709.4, 641.47, 121.1, 0.8305, 0.6357, 315.5, 1.04047, 25.5, 12],
	"Brasilia": [577.88, 409.23, 697.76, 849.61, 784.06, 46.69, 0.8911, 0.6221, 301.1, 1.04035, 13.5, 12],
	"Bremgarten": [713.7, 594.03, 589.41, 697.91, 539.29, 138.55, 0.858, 0, 305.8, 1.0813, 17, 16],
	"Brno": [489.73, 515.49, 378.53, 555.53, 490.25, 73.58, 0.8324, 0.7015, 308, 0.98793, 14, 15],
	"Bucharest Ring": [269.73, 654.11, 711.39, 593.83, 744.57, 77.48, 0.9118, 0.7706, 245.7, 0.9947, 24, 14],
	"Buenos Aires": [901.29, 516.57, 272.05, 654.41, 706.34, 190.08, 0.7853, 0.572, 306.6, 0.9795, 19.5, 16],
	"Estoril": [438.52, 652.28, 302.24, 705, 575.42, 79.46, 0.8379, 0.7148, 305.2, 1.05901, 22.5, 13],
	"Fiorano": [449.29, 619.66, 301.15, 374.52, 895.1, 99.31, 0.9327, 0.872, 238.6, 0.95633, 16.5, 14],
	"Fuji": [271.38, 590.54, 633.87, 689.16, 500.84, 117.72, 0.8491, 0.6228, 305.4, 0.976, 18.5, 16],
	"Grobnik": [646.19, 384.37, 524.55, 768.66, 500.29, 128.82, 0.8224, 0, 308.4, 1.03798, 13, 15],
	"Hockenheim": [444.92, 647.63, 329.61, 789.21, 291.96	-98.2, 0.8693, 0.899, 306.4, 0.96074, 16.5, 12],
	"Hungaroring": [853.49, 439.1, 571.56, 434.45, 416.73, 62.53, 0.7657, 0.649, 305.5, 1.06388, 16.5, 14],
	"Imola": [459.77, 599.72, 672.31, 615.44, 455.84, 19.18, 0.8557, 0.6079, 305.6, 1.0555, 12, 16],
	"Indianapolis": [207.55, 706.52, 465.52, 648.5, 518.59	-35, 0.893, 0, 306.6, 1.01319, 25.5, 13],
	"Indianapolis Oval": [-58.62, 730.49, 21.69, 901.36, 304.75, 67.6, 0.9042, 0.749, 321.8, 0.9953, 45, 4],
	"Interlagos, 460.91": [578.03, 555.34, 568.26, 318.88	-26.27, 0.8492, 0.6853, 305.9, 1.04207, 18, 14],
	"Irungattukottai": [680.12, 470.29, 626.79, 620.22, 536.55, 13.95, 0.8412, 0, 293.6, 0.97159, 14, 12],
	"Istanbul": [387.85, 544.46, 700.97, 543.97, 636.53, 118.92, 0.856, 0.694, 309.4, 1.11647, 16, 14],
	"Jerez": [717.6, 608.07, 626.86, 701.3, 321.26, 143.33, 0.889, 0.6178, 306.4, 0.9, 18, 14],
	"Jyllands-Ringen": [769.66, 414.13, 556.76, 743.56, 524.72, 106.93, 0.826, 0, 184, 0.98582, 19.5, 20],
	"Kaunas": [387.37, 635.17, 515.42, 685, 362.96, 91.1, 0.8461, 0.7649, 264.1, 1.0395, 11, 10],
	"Kyalami": [777.15, 534.3, 557.47, 528.95, 749.84, 206.85, 0.8016, 0, 306.8, 1.02227, 15, 14],
	"Laguna Seca": [481.06, 401.03, 585.51, 619.45, 50.81, 54.38, 0.902, 0.751, 284.5, 1.015, 16.7, 11],
	"Magny Cours": [453.62, 564.81, 294.88, 588.24, 560.43, 147.77, 0.865, 0, 305.8, 0.94099, 18, 14],
	"Melbourne": [403.36, 619, 614.44, 757.14, 294.52, 8.04, 0.8553, 0, 307.6, 0.97952, 16.5, 17],
	"Mexico City": [632.08, 700.96, 470.54, 671.13, 323.13, 48.62, 0.8353, 0.6893, 305, 0.99074, 24, 9],
	"Monte Carlo": [1024.73, 373.43, 471.04, 374.23, 494.38, 100.89, 0.8141, 0.621, 262.8, 1.05986, 18, 19],
	"Montreal": [335.19, 677.82, 566.84, 718.1, 237.85	-98.13, 0.8553, 0.7349, 305, 1.0831, 16.5, 12],
	"Monza": [124.19, 735.83, 496, 868.17, 610.97, 24.64, 0.913, 0, 306.7, 1.0733, 25.5, 13],
	"Mugello": [517.88, 805.54, 879.84, 901.34, 590.54	-69.4, 0.8474, 0.6958, 304.3, 1.0235, 13.5, 14],
	"New Delhi": [649.99, 556.92, 556.38, 720.3, 150.9	-97.64, 0.8363, 0.768, 308.2, 1.03303, 19, 16],
	"Nurburgring": [650.81, 451.94, 626.71, 598, 149.86, 244.17, 0.799, 0, 308.7, 1.0645, 15, 16],
	"Oesterreichring": [442.09, 675.58, 496.59, 729.98, 508.34, 85.42, 0.8686, 0.6529, 308.9, 1.08664, 21, 11],
	"Paul Ricard": [362.79, 732.67, 301.68, 784.37, 575.27, 182.33, 0.8965, 0.771, 305, 1.09121, 19.5, 11],
	"Portimao": [784.36, 392.27, 486.5, 490, 295.42, 180.52, 0.8361, 0.7061, 309.7, 1.0578, 15.5, 18],
	"Poznan": [742, 546.02, 379.02, 718.46, 529.96, 182.04, 0.8239, 0, 306.2, 1.08634, 14, 14],
	"Rafaela Oval": [86.6, 645.37, 144.79, 781.23, 354.81, 67.6, 0.9058, 0.7695, 317.3, 1.06418, 10, 8],
	"Sakhir": [126.91, 406.55, 716.34, 609.56, 240.96	-21.44, 0.912, 0.7124, 308.5, 1.10363, 25.5, 14],
	"Sepang": [554, 590.12, 653.69, 746.34, 466.41, 24.6, 0.8422, 0.6161, 310.4, 0.9926, 24, 17],
	"Serres": [927.25, 414.83, 503.01, 477.94, 522.69, 177, 0.8633, 0, 254.9, 0.92879, 12, 16],
	"Shanghai": [416.43, 529.77, 641.35, 354.61, 114.21, 114.9, 0.9052, 0.6744, 305.2, 1.05878, 24, 10],
	"Silverstone": [283.41, 699.48, 590.85, 823.25, 415.1, 18.87, 0.8693, 0.681, 308.3, 1.1123, 22.5, 14],
	"Singapore": [865.61, 438.19, 578.15, 598.96, 801.2, 202.04, 0.854, 0.5521, 309.1, 1.04688, 17, 23],
	"Slovakiaring": [735.82, 439.66, 609.73, 491.45, 431.92, 184.08, 0.9069, 0.79, 313.9, 1.0652, 19.5, 14],
	"Sochi": [675.39, 588.26, 587.66, 696.24, 456.11, 137.97, 0.8404, 0, 310.1, 1.04166, 23, 19],
	"Spa": [585.64, 716.49, 446.82, 609.47, 372.54, 50.4, 0.8835, 0.4519, 306.6, 1.04803, 13.5, 22],
	"Suzuka": [413.56, 639.98, 515.88, 550.25, 531.13, 47.12, 0.857, 0.5508, 310.6, 1.0326, 15, 14],
	"Valencia": [837.83, 445.95, 657.26, 652.58, 335.82, 209.76, 0.8459, 0.56, 310.1, 0.95518, 14.5, 25],
	"Yas Marina": [730.05, 459.7, 557.69, 476.1, 419.98, 175.25, 0.8117, 0.7014, 305.5, 0.95151, 18.5, 21],
	"Yeongam": [781.67, 480.86, 719.53, 689.5, 420.63, 207.41, 0.8365, 0.7399, 309.2, 1.0452, 23.5, 18],
	"Zandvoort": [551.15, 653.24, 415.91, 779.13, 709.95, 5.57, 0.8402, 0.583, 301.8, 1.01818, 22.5, 14],
	"Zolder": [669.24, 616.83, 466.06, 628.62, 539.48, 193.3, 0.8286, 0.6365, 298.3, 0.99094, 19.5, 17]
}

# Data collection function
def collection(username, password, weather, sessionTemp, minimumWear):
	# Create our logon payload. 'hiddenToken' may change at a later date.
	logonData = {'textLogin':username, 'textPassword':password, 'hiddenToken':'9da482f717cf1319f10f55e35ab767a5', 'Logon':'Login', 'LogonFake':'Sign in'}
	
	# Logon to GPRO using the logon information provided and store that under our session
	session = requests.session()
	loginURL = "https://gpro.net/gb/Login.asp"
	logonResult = session.post(loginURL, data=logonData, headers=dict(referer=loginURL))
	
	# Gather the home page information and collect driver ID, track ID, team name, and manager ID
	tree = html.fromstring(logonResult.content)
	# Driver ID and check for correct login details. If login failed, then driver ID will return nothing and driverID[0] will error
	driverID = tree.xpath("//a[starts-with(@href, 'DriverProfile.asp')]/@href")
	try:
		driverURL = "https://gpro.net/gb/" + driverID[0]
	except:
		return [0, 0, 0, 0, 0, 0]
	# Team name check for verification
	teamName = tree.xpath("//a[starts-with(@href, 'TeamProfile.asp')]/text()")
	if(teamName[0] != "VIPER AUTOSPORT") and (teamName[0] != "TEAM VIPER") and (teamName[0] != "VIPER RACING"):
		return [1, 0, 0, 0, 0, 0]
	# Track ID of next race
	trackID = tree.xpath("//a[starts-with(@href, 'TrackDetails.asp')]/@href")
	trackURL = "https://gpro.net/gb/" + trackID[0]
	# URLs for car and race details, for later use
	carURL = "https://www.gpro.net/gb/UpdateCar.asp"
	raceURL = "https://www.gpro.net/gb/RaceSetup.asp"
	staffURL = "https://www.gpro.net/gb/StaffAndFacilities.asp"
	tyreURL = "https://www.gpro.net/gb/Suppliers.asp"
	# Check, while we're here, if the manager has a Technical Director and if they do, gather the TD stats
	try:
		technicalDirectorID = str(tree.xpath("//a[starts-with(@href, 'TechDProfile.asp')]/@href")[0])
		technicalDirectorValues = [0.0314707991001518, -0.0945456184596369, -0.0355383420267692, -0.00944695128810026, -0.0112688398024834]
		technicalDirectorResult = session.get(technicalDirectorURL, headers = dict(referer = technicalDirectorURL))
		technicalDirectorURL = "https://gpro.net/gb/" + technicalDirectorID
		tree = html.fromstring(technicalDirectorResult.content)
		tdExperience = int(tree.xpath("//th[contains(text(), 'Experience:')]/../td[0]/text()")[0])
		tdPitCoordination = int(tree.xpath("//th[contains(text(), 'Pit coordination:')]/../td[0]/text()")[0])
	except:
		technicalDirectorValues = [0.0355393906609645, -0.0797977676868435, 0, 0, 0]
		tdExperience = 0
		tdPitCoordination = 0


	
	
	# Request the driver information page and scrape the driver data
	driverResult = session.get(driverURL, headers=dict(referer=driverURL))
	tree = html.fromstring(driverResult.content)
	driverOverall = int(tree.xpath("normalize-space(//tr[contains(@data-step, '4')]//td/text())"))
	driverConcentration = int(tree.xpath("normalize-space(//td[contains(@id, 'Conc')]/text())"))
	driverTalent = int(tree.xpath("normalize-space(//td[contains(@id, 'Talent')]/text())"))
	driverAggressiveness = int(tree.xpath("normalize-space(//td[contains(@id, 'Aggr')]/text())"))
	driverExperience = int(tree.xpath("normalize-space(//td[contains(@id, 'Experience')]/text())"))
	driverTechnicalInsight = int(tree.xpath("normalize-space(//td[contains(@id, 'TechI')]/text())"))
	driverStamina = int(tree.xpath("normalize-space(//td[contains(@id, 'Stamina')]/text())"))
	driverCharisma = int(tree.xpath("normalize-space(//td[contains(@id, 'Charisma')]/text())"))
	driverMotivation = int(tree.xpath("normalize-space(//td[contains(@id, 'Motivation')]/text())"))
	driverReputation = int(tree.xpath("normalize-space(//tr[contains(@data-step, '13')]//td/text())"))
	driverWeight = int(tree.xpath("normalize-space(//tr[contains(@data-step, '14')]//td/text())"))
	driverAge = int(tree.xpath("normalize-space(//tr[contains(@data-step, '15')]//td/text())"))


	# Request the manager page and scrape tyre data
	tyreResult = session.get(tyreURL, headers = dict(referer = tyreURL))
	tree = html.fromstring(tyreResult.content)
	tyreSupplierName = str(tree.xpath("//div[contains(@class, 'chosen')]/h2/text()")[0])


	# Request the staff page and scrape staff data
	staffResult = session.get(staffURL, headers = dict(referer = staffURL))
	tree = html.fromstring(staffResult.content)
	staffConcentration = int(tree.xpath("//th[contains(text(), 'Concentration:')]/../td/text()")[0])
	staffStress = int(tree.xpath("//th[contains(text(), 'Stress handling:')]/../td/text()")[0])

	
	# Request the track information page and scrape the track data
	trackResult = session.get(trackURL, headers=dict(referer=trackURL))
	tree = html.fromstring(trackResult.content)
	trackName = str(tree.xpath("normalize-space(//h1[contains(@class, 'block')]/text())"))
	trackName = trackName.strip()
	trackPowerProfile = int(tree.xpath("normalize-space(//td[contains(text(), 'Power')]/following-sibling::td/@title)"))
	trackHandlingProfile = int(tree.xpath("normalize-space(//td[contains(text(), 'Handling')]/following-sibling::td/@title)"))
	trackAccelerationProfile = int(tree.xpath("normalize-space(//td[contains(text(), 'Acceleration')]/following-sibling::td/@title)"))
	trackDistanceTotal = str(tree.xpath("normalize-space(//td[contains(text(), 'Race distance')]/following-sibling::td/text())"))
	trackDistanceTotal = float((re.findall("\d+.\d+", trackDistanceTotal))[0])
	trackDistanceLap = str(tree.xpath("normalize-space(//td[contains(text(), 'Lap distance')]/following-sibling::td/text())"))
	trackDistanceLap = float((re.findall("\d+.\d+", trackDistanceLap))[0])
	trackLapsCount = int(tree.xpath("normalize-space(//td[contains(text(), 'Laps')]/following-sibling::td/text())"))
	trackPitTime = str(tree.xpath("normalize-space(//td[starts-with(text(), 'Time in')]/following-sibling::td/text())"))
	try:
		trackPitTime = float((re.findall("\d+.\d+", trackPitTime))[0])
	except:
		trackPitTime = float((re.findall("\d+", trackPitTime))[0])
	trackDownforeRating = str(tree.xpath("normalize-space(//td[contains(text(), 'Downforce')]/following-sibling::td/text())"))
	trackOvertakeRating = str(tree.xpath("normalize-space(//td[contains(text(), 'Overtaking')]/following-sibling::td/text())"))
	trackSuspensionRating = str(tree.xpath("normalize-space(//td[contains(text(), 'Suspension')]/following-sibling::td/text())"))
	trackFuelRating = str(tree.xpath("normalize-space(//td[contains(text(), 'Fuel consumption')]/following-sibling::td/text())"))
	trackTyreWearRating = str(tree.xpath("normalize-space(//td[contains(text(), 'Tyre wear')]/following-sibling::td/text())"))
	trackGripRating = str(tree.xpath("normalize-space(//td[contains(text(), 'Grip level')]/following-sibling::td/text())"))


	# Request race strategy pace and scrape the race weather data
	raceResult = session.get(raceURL, headers=dict(referer=raceURL))
	tree = html.fromstring(raceResult.content)
	rTempRangeOne = str(tree.xpath("normalize-space(//td[contains(text(), 'Temp')]/../../tr[2]/td[1]/text())"))
	rTempRangeTwo = str(tree.xpath("normalize-space(//td[contains(text(), 'Temp')]/../../tr[2]/td[2]/text())"))
	rTempRangeThree = str(tree.xpath("normalize-space(//td[contains(text(), 'Temp')]/../../tr[4]/td[1]/text())"))
	rTempRangeFour = str(tree.xpath("normalize-space(//td[contains(text(), 'Temp')]/../../tr[4]/td[2]/text())"))
	# This returns results like "Temp: 12*-17*", but we want just integers, so clean up the values
	rTempMinOne = int((re.findall("\d+", rTempRangeOne))[0])
	rTempMaxOne = int((re.findall("\d+", rTempRangeOne))[1])
	rTempMinTwo = int((re.findall("\d+", rTempRangeTwo))[0])
	rTempMaxTwo = int((re.findall("\d+", rTempRangeTwo))[1])
	rTempMinThree = int((re.findall("\d+", rTempRangeThree))[0])
	rTempMaxThree = int((re.findall("\d+", rTempRangeThree))[1])
	rTempMinFour = int((re.findall("\d+", rTempRangeFour))[0])
	rTempMaxFour = int((re.findall("\d+", rTempRangeFour))[1])
	# Find the averages of these temps for the setup
	rTemp = ((rTempMinOne + rTempMaxOne) + (rTempMinTwo + rTempMaxTwo) + (rTempMinThree + rTempMaxThree) + (rTempMinFour + rTempMaxFour)) / 8

	# Using the race strategy page requested earlier, scrape the qualifying weather data
	qOneTemp = str(tree.xpath("normalize-space(//img[contains(@name, 'WeatherQ')]/../text()[contains(., 'Temp')])"))
	qOneTemp = int((re.findall("\d+", qOneTemp))[0])
	qTwoTemp = str(tree.xpath("normalize-space(//img[contains(@name, 'WeatherR')]/../text()[contains(., 'Temp')])"))
	qTwoTemp = int((re.findall("\d+", qTwoTemp))[0])

	# Check the user selected session and assign the relevant temperature
	if(sessionTemp == "Race"):
		sessionTemp = rTemp
	elif(sessionTemp == "Q1"):
		sessionTemp = qOneTemp
	elif(sessionTemp == "Q2"):
		sessionTemp = qTwoTemp
	
	# Request the car information page and scrape the car character and part level and wear data
	carResult = session.get(carURL, headers=dict(referer=carURL))
	tree = html.fromstring(carResult.content)
	carPowerProfile = int(tree.xpath("normalize-space(//table[contains(@data-step, '1')]/tr[3]/td[1]/text())"))
	carHandlingProfile = int(tree.xpath("normalize-space(//table[contains(@data-step, '1')]/tr[3]/td[2]/text())"))
	carAccelerationProfile = int(tree.xpath("normalize-space(//table[contains(@data-step, '1')]/tr[3]/td[3]/text())"))
	# Level
	carLevelChassis = int(tree.xpath("normalize-space(//b[contains(text(), 'Chassis')]/../../td[2]/text())"))
	carLevelEngine = int(tree.xpath("normalize-space(//b[contains(text(), 'Engine')]/../../td[2]/text())"))
	carLevelFrontWing = int(tree.xpath("normalize-space(//b[contains(text(), 'Front wing')]/../../td[2]/text())"))
	carLevelReadWing = int(tree.xpath("normalize-space(//b[contains(text(), 'Rear wing')]/../../td[2]/text())"))
	carLevelUnderbody = int(tree.xpath("normalize-space(//b[contains(text(), 'Underbody')]/../../td[2]/text())"))
	carLevelSidepod = int(tree.xpath("normalize-space(//b[contains(text(), 'Sidepods')]/../../td[2]/text())"))
	carLevelCooling = int(tree.xpath("normalize-space(//b[contains(text(), 'Cooling')]/../../td[2]/text())"))
	carLevelGears = int(tree.xpath("normalize-space(//b[contains(text(), 'Gearbox')]/../../td[2]/text())"))
	carLevelBrakes = int(tree.xpath("normalize-space(//b[contains(text(), 'Brakes')]/../../td[2]/text())"))
	carLevelSuspension = int(tree.xpath("normalize-space(//b[contains(text(), 'Suspension')]/../../td[2]/text())"))
	carLevelElectronics = int(tree.xpath("normalize-space(//b[contains(text(), 'Electronics')]/../../td[2]/text())"))
	# And wear
	carWearChassis = str(tree.xpath("normalize-space(//b[contains(text(), 'Chassis')]/../../td[4]/text())"))
	if(carWearChassis == ""):
		carWearChassis = str(tree.xpath("normalize-space(//b[contains(text(), 'Chassis')]/../../td[4]/font/text())"));
	carWearChassis = int((re.findall("\d+", carWearChassis))[0])
	carWearEngine = str(tree.xpath("normalize-space(//b[contains(text(), 'Engine')]/../../td[4]/text())"))
	if(carWearEngine == ""):
		carWearEngine = str(tree.xpath("normalize-space(//b[contains(text(), 'Engine')]/../../td[4]/font/text())"));
	carWearEngine = int((re.findall("\d+", carWearEngine))[0])
	carWearFrontWing = str(tree.xpath("normalize-space(//b[contains(text(), 'Front wing')]/../../td[4]/text())"))
	if(carWearFrontWing == ""):
		carWearFrontWing = str(tree.xpath("normalize-space(//b[contains(text(), 'Front wing')]/../../td[4]/font/text())"));
	carWearFrontWing = int((re.findall("\d+", carWearFrontWing))[0])
	carWearRearWing = str(tree.xpath("normalize-space(//b[contains(text(), 'Rear wing')]/../../td[4]/text())"))
	if(carWearRearWing == ""):
		carWearRearWing = str(tree.xpath("normalize-space(//b[contains(text(), 'Rear wing')]/../../td[4]/font/text())"));
	carWearRearWing = int((re.findall("\d+", carWearRearWing))[0])
	carWearUnderbody = str(tree.xpath("normalize-space(//b[contains(text(), 'Underbody')]/../../td[4]/text())"))
	if(carWearUnderbody == ""):
		carWearUnderbody = str(tree.xpath("normalize-space(//b[contains(text(), 'Underbody')]/../../td[4]/font/text())"));
	carWearUnderbody = int((re.findall("\d+", carWearUnderbody))[0])
	carWearSidepod = str(tree.xpath("normalize-space(//b[contains(text(), 'Sidepods')]/../../td[4]/text())"))
	if(carWearSidepod == ""):
		carWearSidepod = str(tree.xpath("normalize-space(//b[contains(text(), 'Sidepods')]/../../td[4]/font/text())"));
	carWearSidepod = int((re.findall("\d+", carWearSidepod))[0])
	carWearCooling = str(tree.xpath("normalize-space(//b[contains(text(), 'Cooling')]/../../td[4]/text())"))
	if(carWearCooling == ""):
		carWearCooling = str(tree.xpath("normalize-space(//b[contains(text(), 'Cooling')]/../../td[4]/font/text())"));
	carWearCooling = int((re.findall("\d+", carWearCooling))[0])
	carWearGears = str(tree.xpath("normalize-space(//b[contains(text(), 'Gearbox')]/../../td[4]/text())"))
	if(carWearGears == ""):
		carWearGears = str(tree.xpath("normalize-space(//b[contains(text(), 'Gearbox')]/../../td[4]/font/text())"));
	carWearGears = int((re.findall("\d+", carWearGears))[0])
	carWearBrakes = str(tree.xpath("normalize-space(//b[contains(text(), 'Brakes')]/../../td[4]/text())"))
	if(carWearBrakes == ""):
		carWearBrakes = str(tree.xpath("normalize-space(//b[contains(text(), 'Brakes')]/../../td[4]/font/text())"));
	carWearBrakes = int((re.findall("\d+", carWearBrakes))[0])
	carWearSuspension = str(tree.xpath("normalize-space(//b[contains(text(), 'Suspension')]/../../td[4]/text())"))
	if(carWearSuspension == ""):
		carWearSuspension = str(tree.xpath("normalize-space(//b[contains(text(), 'Suspension')]/../../td[4]/font/text())"));
	carWearSuspension = int((re.findall("\d+", carWearSuspension))[0])
	carWearElectronics = str(tree.xpath("normalize-space(//b[contains(text(), 'Electronics')]/../../td[4]/text())"))
	if(carWearElectronics == ""):
		carWearElectronics = str(tree.xpath("normalize-space(//b[contains(text(), 'Electronics')]/../../td[4]/font/text())"));
	carWearElectronics = int((re.findall("\d+", carWearElectronics))[0])
	
	
	# Setup calculations
	# Begin by storig the track base values
	trackBaseWingsSetup = float(trackData[trackName][0]) * 2
	trackBaseEngineSetup = float(trackData[trackName][1])
	trackBaseBrakesSetup = float(trackData[trackName][2])
	trackBaseGearsSetup = float(trackData[trackName][3])
	trackBaseSuspensionSetup = float(trackData[trackName][4])
	trackBaseWingSlitSetup = float(trackData[trackName][5])

	# A collection of offset values. These always stay the same, regardless of track
	baseOffsets = {
		"wingWeatherDry": 6,
		"wingWeatherWet": 1,
		"wingWeatherOffset": 263,

		"engineWeatherDry": -3,
		"engineWeatherWet": 0.7,
		"engineWeatherOffset": -190,

		"brakesWeatherDry": 6,
		"brakesWeatherWet": 3.988375441,
		"brakesWeatherOffset": 105.5325924,

		"gearsWeatherDry": -4,
		"gearsWeatherWet": -8.0019964182,
		"gearsWeatherOffset": -4.742711704,

		"suspensionWeatherDry": -6,
		"suspensionWeatherWet": -1,
		"suspensionWeatherOffset": -257, 

		"wingDriverMultiplier": -0.001349079032746,
		"engineDriverMultiplier": 0.001655723,
		"engineDriverOffset": 0.0469416263186552
	}
	
	# Lot of info here and it's hard to see, but these offsets are used when calculating the influence of the level of a part on the setup
	carLevelOffsets = [
		[-19.74, 30.03, -15.07],
		[16.04, 4.9, 3.34],
		[6.04, -29.14, 6.11],
		[-41, 9],
		[-15.27, -10.72, 6.04, 31]
	]

	carWearOffsets = [
		[0.47, -0.59, 0.32],
		[-0.51, -0.09, -0.04],
		[-0.14, 0.71, -0.09],
		[1.09, -0.14],
		[0.34, 0.23, -0.12, -0.70]
	]
	
	# I know it seems a bit pointless to have this be an array of arrays, but it makes it easier to see which values affect each step.
	driverOffsets = [
		[0.3],
		[-0.5],
		[0.5],
		[0.75, 2]
	]


	'''
	Now, to calculate the session setup.
	There are 4 components that influence car setup for anyway given part:
		1. Weather
		2. Driver
		3. Part Level
		4. Part Wear
	We canculate these components in this order, then dump them into the equation to calculate setup.
	The reason we do them in order, is that some later components are affected by earlier ones, see driver setup on any part for an example
	'''

	# Wings
	sessionTemp = int(sessionTemp)
	weather = weather.upper()
	if(weather != "WET"):
		setupWeather = baseOffsets["wingWeatherDry"] * sessionTemp * 2;
	else:
		setupWeather = ((baseOffsets["wingWeatherWet"] * sessionTemp) + baseOffsets["wingWeatherOffset"]) * 2;
	setupDriver = driverTalent * (trackBaseWingsSetup + setupWeather) * baseOffsets["wingDriverMultiplier"]
	setupCarLevel = (carLevelOffsets[0][0] * carLevelChassis) + (carLevelOffsets[0][1] * carLevelFrontWing) + (carLevelOffsets[0][1] * carLevelReadWing) + (carLevelOffsets[0][2] * carLevelUnderbody)
	setupCarWear = ((carWearOffsets[0][0] * carWearChassis) + (carWearOffsets[0][1] * carWearFrontWing) + (carWearOffsets[0][1] * carWearRearWing) + (carWearOffsets[0][2] * carWearUnderbody))
	setupWings = (trackBaseWingsSetup + setupWeather + setupDriver + setupCarLevel + setupCarWear) / 2

	# Wing Split
	if(weather != "WET"):
		setupWingSplit = trackBaseWingSlitSetup + (driverTalent * -0.246534498671854) + (3.69107049712848 * (carLevelFrontWing + carLevelReadWing) / 2) + (setupWings * -0.189968386659174) + (sessionTemp * 0.376337780506523)
	else:
		setupWingSplit = trackBaseWingSlitSetup + (driverTalent * -0.246534498671854) + (3.69107049712848 * (carLevelFrontWing + carLevelReadWing) / 2) + (setupWings * -0.189968386659174) + (sessionTemp * 0.376337780506523) + 58.8818967363256
	setupFWi = setupWings + setupWingSplit
	setupRWi = setupWings - setupWingSplit

	# Engine
	if(weather != "WET"):
		setupWeather = baseOffsets["engineWeatherDry"] * sessionTemp;
	else:
		setupWeather = ((baseOffsets["engineWeatherWet"] * sessionTemp) + baseOffsets["engineWeatherOffset"]);
	setupDriver = (driverOffsets[0][0] * driverAggressiveness) + (driverExperience * (((trackBaseEngineSetup + setupWeather) * baseOffsets["engineDriverMultiplier"]) + baseOffsets["engineDriverOffset"]))
	setupCarLevel = ((carLevelOffsets[1][0] * carLevelEngine) + (carLevelOffsets[1][1] * carLevelCooling) + (carLevelOffsets[1][2] * carLevelElectronics))
	setupCarWear = ((carWearOffsets[1][0] * carWearEngine) + (carWearOffsets[1][1] * carWearCooling) + (carWearOffsets[1][2] * carWearElectronics))
	setupEng = (trackBaseEngineSetup + setupWeather + setupDriver + setupCarLevel + setupCarWear)

	# Brakes
	if(weather != "WET"):
		setupWeather = baseOffsets["brakesWeatherDry"] * sessionTemp;
	else:
		setupWeather = ((baseOffsets["brakesWeatherWet"] * sessionTemp) + baseOffsets["brakesWeatherOffset"]);
	setupDriver = (driverOffsets[1][0] * driverTalent)
	setupCarLevel = ((carLevelOffsets[2][0] * carLevelChassis) + (carLevelOffsets[2][1] * carLevelBrakes) + (carLevelOffsets[2][2] * carLevelElectronics))
	setupCarWear = ((carWearOffsets[2][0] * carWearChassis) + (carWearOffsets[2][1] * carWearBrakes) + (carWearOffsets[2][2] * carWearElectronics))
	setupBra = (trackBaseBrakesSetup + setupWeather + setupDriver + setupCarLevel + setupCarWear)

	# Gears
	if(weather != "WET"):
		setupWeather = baseOffsets["gearsWeatherDry"] * sessionTemp;
	else:
		setupWeather = ((baseOffsets["gearsWeatherWet"] * sessionTemp) + baseOffsets["gearsWeatherOffset"]);
	setupDriver = (driverOffsets[2][0] * driverConcentration)
	setupCarLevel = ((carLevelOffsets[3][0] * carLevelGears) + (carLevelOffsets[3][1] * carLevelElectronics))
	setupCarWear = ((carWearOffsets[3][0] * carWearGears) + (carWearOffsets[3][1] * carWearElectronics))
	setupGea = (trackBaseGearsSetup + setupWeather + setupDriver + setupCarLevel + setupCarWear)

	# Suspension
	if(weather != "WET"):
		setupWeather = baseOffsets["suspensionWeatherDry"] * sessionTemp;
	else:
		setupWeather = ((baseOffsets["suspensionWeatherWet"] * sessionTemp) + baseOffsets["suspensionWeatherOffset"]);
	if(weather != "WET"):
		setupDriver = (driverOffsets[3][0] * driverExperience) + (driverOffsets[3][1] * driverWeight)
	else:
		setupDriver = (driverOffsets[3][0] * float(driverExperience)) + (driverOffsets[3][1] * driverWeight) + (driverTechnicalInsight * 0.11)
	setupCarLevel = ((carLevelOffsets[4][0] * carLevelChassis) + (carLevelOffsets[4][1] * carLevelUnderbody) + (carLevelOffsets[4][2] * carLevelSidepod) + (carLevelOffsets[4][3] * carLevelSuspension))
	setupCarWear = ((carWearOffsets[4][0] * carWearChassis) + (carWearOffsets[4][1] * carWearUnderbody) + (carWearOffsets[4][2] * carWearSidepod) + (carWearOffsets[4][3] * carWearSuspension))
	setupSus = (trackBaseSuspensionSetup + setupWeather + setupDriver + setupCarLevel + setupCarWear)


	# Take that calculated setup and turn it into an array for easier handling
	setup = [int(setupFWi), int(setupRWi), int(setupEng), int(setupBra), int(setupGea), int(setupSus)]


	'''
	Once we have the setup calculated, we can move on to the strategy calculation.
	There are many factors that influence strategy:
		1. Tyre Supplier
		2. Track Wear on the Tyre
		3. Track Distance
	and many more, simply see the function "stopCalc" for most, and that only deals with the number of stops
	We would LIKE to also take clear track risk into account, but I don't know how risk fits into the equation, so simply cannot add it accurately.
	'''

	# We start by defining some constants. Wear factors are just static hidden values that affect tyre wear based on compound, but only slightly.
	# Without these the equation doesn't QUITE add up properly.
	tyreSupplierFactor = {"Pipirelli": 1, "Avonn": 8, "Yokomama": 3, "Dunnolop": 4, "Contimental": 8, "Badyear": 7}
	tyreCompoundSupplierFactor = {"Pipirelli": 0, "Avonn": 0.015, "Yokomama": 0.05, "Dunnolop": 0.07, "Contimental": 0.07, "Badyear": 0.09}
	trackWearLevel = {"Very low": 0, "Low": 1, "Medium": 2, "High": 3, "Very high": 4}
	wearFactors = [0.998163750229071, 0.997064844817654, 0.996380346554349, 0.995862526048112, 0.996087854384523]

	# Calcualte the number of stops for each tyre choice
	for i in range(4):
		stops[i].set(str(stopCalc(trackDistanceTotal, trackWearLevel[trackTyreWearRating], rTemp, tyreSupplierFactor[tyreSupplierName], i, carLevelSuspension, driverAggressiveness, driverExperience, driverWeight, float(trackData[trackName][9]), minimumWear, wearFactors[i])))
	stops[4].set(str(math.ceil(0.73 * stopCalc(trackDistanceTotal, trackWearLevel[trackTyreWearRating], rTemp, tyreSupplierFactor[tyreSupplierName], 5, carLevelSuspension, driverAggressiveness, driverExperience, driverWeight, float(trackData[trackName][9]), minimumWear, wearFactors[4]))))

	# Calculate the fuel load for each stint given the above number of stops
	fuelFactor = (-0.000101165467155397 * driverConcentration) + (0.0000706080613787091 * driverAggressiveness) + (-0.0000866455021527332 * driverExperience) + (-0.000163915452803369 * driverTechnicalInsight) + (-0.0126912680856842 * carLevelEngine) + (-0.0083557977071091 * carLevelElectronics)
	for i in range(4):
		fuels[i].set(str(fuelLoadCalc(trackDistanceTotal, float(trackData[trackName][6]), fuelFactor, int(stops[i].get()) + 1)))
	fuels[4].set(str(fuelLoadCalc(trackDistanceTotal, float(trackData[trackName][7]), fuelFactor, int(stops[4].get()) + 1)))

	# Calculate the pit time for each tyre choice, given the fuel load
	for i in range(5):
		pitTimes[i].set(str(pitTimeCalc(int(fuels[i].get()), technicalDirectorValues[0], technicalDirectorValues[1], staffConcentration, technicalDirectorValues[2], staffStress, technicalDirectorValues[3], tdExperience, technicalDirectorValues[4], tdPitCoordination)))

	for i in range(4):
		pitTotals[i].set(round((float(stops[i].get()) * (float(pitTimes[i].get()) + float(trackData[trackName][10]))), 2))

	for i in range(4):
		FLDs[i].set(round(fuelTimeCalc(trackDistanceTotal, float(trackData[trackName][6]), fuelFactor, int(stops[i].get()) + 1)))
	FLDs[4].set(round(fuelTimeCalc(trackDistanceTotal, trackData[trackName][7], fuelFactor, int(stops[4].get()) + 1)))

	TCDs[0].set("0")
	TCDs[1].set(round(compoundCalc(trackLapsCount, float(trackData[trackName][9]), trackDistanceLap, rTemp, tyreCompoundSupplierFactor[tyreSupplierName]), 2))
	TCDs[2].set(str(round(2 * float(TCDs[1].get()), 2)))
	TCDs[3].set(str(round(3 * float(TCDs[1].get()), 2)))
	TCDs[4].set("-")

	if(float(fuels[4].get()) < 0):
		fuels[4].set("No Data!")
		pitTimes[4].set("No Data!")
		pitTotals[4].set("No Data!")
		FLDs[4].set("No Data!")
		totals[4].set("No Data!")
		for i in range(4):
			totals[i].set(totalTimeCalc(float(pitTotals[i].get()), float(TCDs[i].get()), float(FLDs[i].get())))
	else:
		for i in range(5):
			totals[i].set(totalTimeCalc(float(pitTotals[i].get()), float(TCDs[i].get()), float(FLDs[i].get())))


	return setup

'''
Pit Stop Calc
trackDistanceTotal = Track Distance
tracWearLevel = Very Low, Low, Medium, High, Very High, and it's relating factor, 0, 1, 2, 3, 4 respectively
rTemp = Race Temperature
tyreSupplierFactor = Tyre Brand Factor, 1 for Pipirello, 8 for Avonn, etc.
tyreType = Tyre Compound Factor, 0.998163750229071 for Extra Soft (look at wearFactors)
carLevelSuspension = Suspension Level equipped to car
driverAggressiveness = Driver Aggressiveness
driverExperience = Driver Experience
driverWeight = Driver Weight
clearTrackRisk = Clear Track Risk used, as a percentage
trackBaseWear = Track Base Wear from trackData.csv
wearLimit = The manager chosen limit for tyre wear before pitting, so at 10%, we assume the stint will end when the tyres hit 10% wear
'''
def stopCalc(trackDistanceTotal, trackWearLevel, rTemp, tyreSupplierFactor, tyreType, carLevelSuspension, driverAggressiveness, driverExperience, driverWeight, trackBaseWear, wearLimit, tyreWearFactor):
	baseWear = 129.776458172062
	productFactors = (0.896416176238624 ** trackWearLevel) * (0.988463622 ** rTemp) * (1.048876356 ** tyreSupplierFactor) * (1.355293715 ** tyreType) * (1.009339294 ** carLevelSuspension) * (0.999670155 ** driverAggressiveness) * (1.00022936 ** driverExperience) * (0.999858329 ** driverWeight)
	stops = math.ceil((trackDistanceTotal) / ((productFactors  * baseWear * trackBaseWear) * ((100 - wearLimit) / 100))) - 1
	return stops

'''
Fuel Load Calc
Here we very simply calculate how much fuel we will need across the entire race (distance * fuel per km) then divide by the stints (stops + 1)
'''
def fuelLoadCalc(trackDistanceTotal, trackFuelBase, fuelFactor, stints):
	fuelLoad = math.ceil((trackDistanceTotal * (trackFuelBase + fuelFactor)) / stints)
	return fuelLoad

'''
Pit Time Calc
or how long we'll spend during a single pit stop, which is mainly affected by the fuel load required
i.e. Longer stints mean more fuel but less stops so less overall time
'''
def pitTimeCalc(fuelLoad, tdInfluenceFuel, tdInfluenceStaffConcentration, staffConcentration, tdInfluenceStaffStress, staffStress, tdInfluenceExperience, tdExperience, tdInfluencePitCoordination, tdPitCoordination):
	return round(((fuelLoad * tdInfluenceFuel) + 24.26 + (tdInfluenceStaffConcentration * staffConcentration) + (tdInfluenceStaffStress * staffStress) + (tdInfluenceExperience * tdExperience) + (tdInfluencePitCoordination * tdPitCoordination)), 2)

'''
Compound Time Calc
Here we calculate how much time is lost from being on the compound of choice compared to the extra soft tyre, which is the fastest
The idea is to get a comparison for time lost on the tyre versus time saved in the pits from fewer stops
NOTE: Later I intend to implement some form of "wobble" calculation, which will consider how much time is
lost from being on the tyre of choice for too long.
For example, you might be able to stretch the extra soft tyre to 2 stops, over 3, by running them "bald" for a number of laps
the idea is to take into consideration that time lost, which is roughly 1-2 seconds per lap.
'''
def compoundCalc(trackLapsCount, trackCornerCount, trackDistanceLap, rTemp, tyreCompoundSupplierFactor):
	return (trackLapsCount * ((trackCornerCount * trackDistanceLap * 0.00018 * (50 - rTemp)) + tyreCompoundSupplierFactor))

'''
Fuel Time Calc
Here we calculate how much time is lost by being on the fuel load required to run our choice of tyre.
The idea here is that running longer stints means carrying around more fuel which loses you time.
'''
def fuelTimeCalc(trackDistanceTotal, trackFuelBase, fuelFactor, stints):
	return (0.0025 * ((trackDistanceTotal * trackDistanceTotal * (trackFuelBase + fuelFactor)) / stints))

'''
TODO: Total Time Calc
Here we calculate the overall time lost and gained for that tyre strategy.
The reason is so we can compare, say 3 stops on Extra Soft versus 2 stops on Soft.
This is calculated by comparing all the other time saves and losses.
Painfully simple function
'''
def totalTimeCalc(pitTime, compoundTime, fuelTime):
	return round(pitTime + compoundTime + fuelTime, 2)

# Warning window
def warning(*args):
	frontWing.set("Login")
	rearWing.set("incorrect")

def exit():
	warning.Toplevel.destroy()

# Precheck to handle errors nicely
def calculate(*args):
	try:
		username = str(inputUsername.get())
		password = str(inputPassword.get())
		weather = str(inputWeather.get())
		session = str(inputSession.get())
		try:
			wear = float(re.findall('\d+.\d+', inputWear.get())[0])
		except:
			try:
				wear = float(re.findall('\d+', inputWear.get())[0])
			except:
				wear = 0.0
		try:
			clearTrackRisk = int(re.findall('\d+', inputCTR.get())[0])
		except:
			clearTrackRisk = 0

		setup = collection(username, password, weather, session, wear)

		if(setup[0] == 0):
			warningLabel.set("Incorect Login Details")
		elif(setup[0] == 1):
			warningLabel.set("VIPER Family Team Only")
		else:
			warningLabel.set("")
			frontWing.set(str(setup[0]))
			rearWing.set(str(setup[1]))
			engine.set(str(setup[2]))
			brakes.set(str(setup[3]))
			gear.set(str(setup[4]))
			suspension.set(str(setup[5]))
		
	except ValueError:
		pass


# Create the window
root = Tk()
root.title("GAPP")


# and build the frame
frameSetup = ttk.LabelFrame(root, padding = "3 3 12 12")
frameSetup.grid(column = 0, row = 0, sticky = (N, W, E, S))
frameStrategy = ttk.LabelFrame(root, padding = "3 3 12 12")
frameStrategy.grid(column = 1, row = 0, sticky = (N, W, E))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
frameSetup.columnconfigure(0, weight = 1)
frameSetup.rowconfigure(0, weight = 1)
frameStrategy.columnconfigure(0, weight = 1)
frameStrategy.rowconfigure(0, weight = 1)


# Declare our userful variables
inputUsername = StringVar()
inputPassword = StringVar()
inputWeather = StringVar()
inputWeather.set("Dry")
inputTemp = IntVar()
inputSession = StringVar()
inputSession.set("Race")
warningLabel = StringVar()

inputWear = StringVar()
inputWear.set("20")
inputCTR = StringVar()
inputCTR.set("0")

frontWing = StringVar()
rearWing = StringVar()
engine = StringVar()
brakes = StringVar()
gear = StringVar()
suspension = StringVar()

frontWing.set("0")
rearWing.set("0")
engine.set("0")
brakes.set("0")
gear.set("0")
suspension.set("0")


# INPUT
# Build the entry boxes
entryUsername = ttk.Entry(frameSetup, width = 30, textvariable = inputUsername)
entryUsername.grid(column = 2, row = 1, sticky = (W, E))

entryPassword = ttk.Entry(frameSetup, width = 30, show = "*", textvariable = inputPassword)
entryPassword.grid(column = 2, row = 2, sticky = (W, E))

radioQ1 = ttk.Radiobutton(frameSetup, text = "Q1", variable = inputSession, value = "Q1").grid(column = 2, row = 3, sticky = (W, E))
radioQ2 = ttk.Radiobutton(frameSetup, text = "Q2", variable = inputSession, value = "Q2").grid(column = 2, row = 4, sticky = (W, E))
radioRace = ttk.Radiobutton(frameSetup, text = "Race", variable = inputSession, value = "Race").grid(column = 2, row = 5, sticky = (W, E))

radioDry = ttk.Radiobutton(frameSetup, text = "Dry", variable = inputWeather, value = "Dry")
radioDry.grid(column = 2, row = 6, sticky = (W, E))
radioWet = ttk.Radiobutton(frameSetup, text = "Wet", variable = inputWeather, value = "Wet")
radioWet.grid(column = 2, row = 7, sticky = (W, E))


# Add labels to the entry boxes
ttk.Label(frameSetup, text = "Username: ").grid(column = 1, row = 1, sticky = (W, E))
ttk.Label(frameSetup, text = "Password: ").grid(column = 1, row = 2, sticky = (W, E))
ttk.Label(frameSetup, text = "Session: ").grid(column = 1, row = 3, sticky = (W, E))
ttk.Label(frameSetup, text = "Weather: ").grid(column = 1, row = 6, sticky = (W, E))


# Add a button to calculate the setup
ttk.Button(frameSetup, text = "Calculate", command = calculate).grid(column = 1, row = 8)
ttk.Label(frameSetup, textvariable = warningLabel).grid(column = 2, row = 8)



# OUTPUT
ttk.Label(frameSetup, text = "Front Wing: ").grid(column = 1, row = 9, sticky = (W, E))
ttk.Label(frameSetup, text = "Rear Wing: ").grid(column = 1, row = 10, sticky = (W, E))
ttk.Label(frameSetup, text = "Engine: ").grid(column = 1, row = 11, sticky = (W, E))
ttk.Label(frameSetup, text = "Brakes: ").grid(column = 1, row = 12, sticky = (W, E))
ttk.Label(frameSetup, text = "Gear: ").grid(column = 1, row = 13, sticky = (W, E))
ttk.Label(frameSetup, text = "Suspension: ").grid(column = 1, row = 14, sticky = (W, E))

ttk.Label(frameSetup, textvariable = frontWing).grid(column = 2, row = 9)
ttk.Label(frameSetup, textvariable = rearWing).grid(column = 2, row = 10)
ttk.Label(frameSetup, textvariable = engine).grid(column = 2, row = 11)
ttk.Label(frameSetup, textvariable = brakes).grid(column = 2, row = 12)
ttk.Label(frameSetup, textvariable = gear).grid(column = 2, row = 13)
ttk.Label(frameSetup, textvariable = suspension).grid(column = 2, row = 14)


# Strategy
ttk.Label(frameStrategy, text = "Wear:", padding = "5 10").grid(column = 1, row = 1, sticky = (W, E))
entryWear = ttk.Entry(frameStrategy, width = 10, textvariable = inputWear).grid(column = 2, row = 1, sticky = (W, E))

ttk.Label(frameStrategy, text = "Tyre", padding = "5 10").grid(column = 1, row = 2, sticky = (W, E))
ttk.Label(frameStrategy, text = "Stops", padding = "5 10").grid(column = 2, row = 2, sticky = (W, E))
ttk.Label(frameStrategy, text = "Fuel Load (L)", padding = "5 10").grid(column = 3, row = 2, sticky = (W, E))
ttk.Label(frameStrategy, text = "Pit Time (s)", padding = "5 10").grid(column = 4, row = 2, sticky = (W, E))
ttk.Label(frameStrategy, text = "Compound Loss (s)", padding = "5 10").grid(column = 5, row = 2, sticky = (W, E))
ttk.Label(frameStrategy, text = "Fuel Loss (s)", padding = "5 10").grid(column = 6, row = 2, sticky = (W, E))
ttk.Label(frameStrategy, text = "Pit Total (s)", padding = "5 10").grid(column = 7, row = 2, sticky = (W, E))
ttk.Label(frameStrategy, text = "Total (s)", padding = "5 10").grid(column = 8, row = 2, sticky = (W, E))

ttk.Label(frameStrategy, text = "Extra Soft").grid(column = 1, sticky = (W, E))
ttk.Label(frameStrategy, text = "Soft").grid(column = 1, sticky = (W, E))
ttk.Label(frameStrategy, text = "Medium").grid(column = 1, sticky = (W, E))
ttk.Label(frameStrategy, text = "Hard").grid(column = 1, sticky = (W, E))
ttk.Label(frameStrategy, text = "Rain").grid(column = 1, sticky = (W, E))

# Strategy grid variables
extraStops = StringVar()
softStops = StringVar()
mediumStops = StringVar()
hardStops = StringVar()
rainStops = StringVar()

extraFuel = StringVar()
softFuel = StringVar()
mediumFuel = StringVar()
hardFuel = StringVar()
rainFuel = StringVar()

extraPitTime = StringVar()
softPitTime = StringVar()
mediumPitTime = StringVar()
hardPitTime = StringVar()
rainPitTime = StringVar()

extraTCD = StringVar()
softTCD = StringVar()
mediumTCD = StringVar()
hardTCD = StringVar()
rainTCD = StringVar()

extraFLD = StringVar()
softFLD = StringVar()
mediumFLD = StringVar()
hardFLD = StringVar()
rainFLD = StringVar()

extraPitTotal = StringVar()
softPitTotal = StringVar()
mediumPitTotal = StringVar()
hardPitTotal = StringVar()
rainPitTotal = StringVar()

extraTotal = StringVar()
softTotal = StringVar()
mediumTotal = StringVar()
hardTotal = StringVar()
rainTotal = StringVar()

stops = [extraStops, softStops, mediumStops, hardStops, rainStops]
fuels = [extraFuel, softFuel, mediumFuel, hardFuel, rainFuel]
pitTimes = [extraPitTime, softPitTime, mediumPitTime, hardPitTime, rainPitTime]
TCDs = [extraTCD, softTCD, mediumTCD, hardTCD, rainTCD]
FLDs = [extraFLD, softFLD, mediumFLD, hardFLD, rainFLD]
pitTotals = [extraPitTotal, softPitTotal, mediumPitTotal, hardPitTotal, rainPitTotal]
totals = [extraTotal, softTotal, mediumTotal, hardTotal, rainTotal]

grid = [stops, fuels, pitTimes, TCDs, FLDs, pitTotals, totals]

for stop in stops:
	stop.set("0")
for fuel in fuels:
	fuel.set("0")
for pitTime in pitTimes:
	pitTime.set("0")
for TCD in TCDs:
	TCD.set("0")
for FLD in FLDs:
	FLD.set("0")
for pitTotal in pitTotals:
	pitTotal.set("0")
for total in totals:
	total.set("0")

rainTCD.set("-")

x = 2
for values in grid:
	y = 3
	for value in values:
		ttk.Label(frameStrategy, textvariable = value).grid(column = x, row = y, sticky = (W))
		y = y + 1
	x = x + 1

# Automatically organize the window
for child in frameSetup.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in frameStrategy.winfo_children(): child.grid_configure(padx=5, pady=5)


# Set some QOL things, like auto focus for text entry and how to handle an "Enter" press
entryUsername.focus()
root.bind('<Return>', calculate)
root.resizable(False, False)


# Create the window
root.mainloop()