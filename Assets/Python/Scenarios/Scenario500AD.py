from Core import *
from Locations import *
from Resources import setupScenarioResources
from RFCUtils import *
from Scenario import *

lCivilizations = [
	Civilization(
		iEgypt,
		lCivics=[iMonarchy, iRedistribution, iDeification],
		techs=techs.of(iMining, iPottery, iAgriculture, iMythology)
	),
	# Civilization(
	# 	iNative,
	# 	iGold=300,
	# 	techs=techs.column(4)
	# ),
	# Civilization(
	# 	iIndependent2,
	# 	iGold=100,
	# 	techs=techs.column(5)
	# ),
	# Civilization(
	# 	iIndependent,
	# 	iGold=100,
	# 	techs=techs.column(5)
	# ),
]

lTribalVillages = [
	# ((54, 48), (61, 54)), # Iberia
	# ((62, 61), (69, 69)), # North Germany
	# ((52, 64), (54, 67)), # Ireland
	# ((55, 62), (59, 71)), # Britain
	# ((65, 70), (75, 78)), # Scandinavia
	# ((84, 64), (96, 70)), # Russia
	# ((96, 53), (104, 58)), # Transoxiana
	# ((103, 36), (110, 42)), # Deccan
	# ((134, 46), (136, 51)), # Kyushu
	# ((137, 59), (140, 62)), # Hokkaido
	# ((99, 65), (119, 72)), # Siberia
	# ((122, 24), (132, 32)), # Indonesia
	# ((79, 19), (84, 28)), # East Africa
	# ((75, 11), (81, 18)), # South Africa
	# ((21, 57), (30, 62)), # Great Lakes
	# ((15, 51), (21, 64)), # Great Plains
	# ((36, 29), (44, 33)), # Amazon
	# ((37, 11), (41, 20)), # Parana
	# ((25, 42), (33, 46)), # Caribbean
]


def createStartingUnits():
	if not player(iEgypt).isHuman():
		makeUnit(iEgypt, iArcher, plots.capital(iEgypt))


def setupGoals(iCiv, goals):
	if iCiv == iKhmer:
		goals[0].requirements[0].succeed()


scenario500AD = Scenario(
	iStartYear = 500,
	fileName = "RFC_500AD",
	
	lCivilizations = lCivilizations,
	lTribalVillages = lTribalVillages,
	
	iOwnerBaseCulture = 20,
	
	dGreatPeopleCreated = {
		iChina: 5,
		iIndia: 4,
		iDravidia: 2,
		iKorea: 1,
		iToltecs: 1,
	},
	dGreatGeneralsCreated = {
		iChina: 1,
		iIndia: 1,
	},
	
	lAllGoalsFailed = [iNubia, iIndia, iCelts, iDravidia, iToltecs],
	setupGoals = setupGoals,
	
	createStartingUnits = createStartingUnits,
)
		
