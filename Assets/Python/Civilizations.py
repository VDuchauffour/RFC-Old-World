from Consts import *
from RFCUtils import *
from StoredData import data
import Victory as vic
from Religions import rel
from Core import *
from Events import events, handler

### Starting tech methods ###

def getScenarioTechs(iScenario, iPlayer):
	iCivilization = civ(iPlayer)
	for iScenarioType in reversed(range(iScenario+1)):
		if iCivilization in lStartingTechs[iScenarioType]:
			return lStartingTechs[iScenarioType][iCivilization]
			
def getStartingTechs(iPlayer):
	return getScenarioTechs(scenario(), iPlayer)
	
def initScenarioTechs(iScenario):
	for iPlayer in players.major():
		iCiv = civ(iPlayer)
		if dBirth[iCiv] > scenarioStartYear(): continue
	
		if iCiv in lStartingTechs[iScenario]:
			initTechs(iPlayer, lStartingTechs[iScenario][iCiv])
			
def initPlayerTechs(iPlayer):
	initTechs(iPlayer, getStartingTechs(iPlayer))
	
	if civ(iPlayer) == iChina and scenario() == i3000BC and not player(iPlayer).isHuman():
		initTech(iPlayer, iProperty)
		initTech(iPlayer, iAlloys)
				
def initTechs(iPlayer, lTechs):
	pPlayer = player(iPlayer)

	for iTech in lTechs:
		initTech(iPlayer, iTech)
	
	iCurrentEra = pPlayer.getCurrentEra()
	pPlayer.setStartingEra(iCurrentEra)
	
def initTech(iPlayer, iTech):
	team(iPlayer).setHasTech(iTech, True, iPlayer, False, False)
	
	#events.fireEvent("techAcquired", iTech, player(iPlayer).getTeam(), iPlayer)

### Tech preference functions ###

def getDictValue(dDict, key):
	if key not in dDict: return 0
	
	return dDict[key]

def getTechPreferences(iPlayer):
	dPreferences = {}
	iCivilization = civ(iPlayer)
	
	if iCivilization not in dTechPreferences:
		return dPreferences
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		dPreferences[iTech] = iValue
		
	for iTech, iValue in dTechPreferences[iCivilization].items():
		for i in range(4):
			iOrPrereq = infos.tech(iTech).getPrereqOrTechs(i)
			iAndPrereq = infos.tech(iTech).getPrereqAndTechs(i)
			
			if iOrPrereq < 0 and iAndPrereq < 0: break
			
			updatePrereqPreference(dPreferences, iOrPrereq, iValue)
			updatePrereqPreference(dPreferences, iAndPrereq, iValue)
	
	return dPreferences
	
def updatePrereqPreference(dPreferences, iPrereqTech, iValue):
	if iPrereqTech < 0: return
	
	iPrereqValue = getDictValue(dPreferences, iPrereqTech)
	
	if iValue > 0 and iPrereqValue >= 0:
		iPrereqValue = min(max(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	elif iValue < 0 and iPrereqValue <= 0:
		iPrereqValue = max(min(iPrereqValue, iValue), iPrereqValue + iValue / 2)
		
	dPreferences[iPrereqTech] = iPrereqValue
	
def initPlayerTechPreferences(iPlayer):
	initTechPreferences(iPlayer, getTechPreferences(iPlayer))
	
def initTechPreferences(iPlayer, dPreferences):
	for iTech, iValue in dPreferences.items():
		player(iPlayer).setTechPreference(iTech, iValue)

### Wonder preference methods ###

def initBuildingPreferences(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	if iCiv in dBuildingPreferences:
		for iBuilding, iValue in dBuildingPreferences[iCiv].iteritems():
			pPlayer.setBuildingPreference(iBuilding, iValue)
			
	if iCiv in dDefaultWonderPreferences:
		iDefaultPreference = dDefaultWonderPreferences[iCiv]
		for iWonder in range(iFirstWonder, iNumBuildings):
			if iCiv not in dBuildingPreferences or iWonder not in dBuildingPreferences[iCiv]:
				pPlayer.setBuildingPreference(iWonder, iDefaultPreference)
	
### General functions ###
		
def initBirthYear(iPlayer):
	player(iPlayer).setInitialBirthTurn(year(dBirth[iPlayer]))

@handler("GameStart")
def init():
	for iPlayer in players.major():
		initBirthYear(iPlayer)
		initPlayerTechPreferences(iPlayer)
		initBuildingPreferences(iPlayer)

### Starting technologies ###

lStartingTechs = [
{
	iNative : 		techs.of(iTanning, iMythology),
	iEgypt :		techs.of(iMining, iPottery, iAgriculture),
	iBabylonia :	techs.of(iPottery, iPastoralism, iAgriculture),
	iHarappa : 		techs.of(iMining, iPottery, iAgriculture),
	iChina :		techs.of(iTanning, iMining, iAgriculture, iPastoralism, iPottery, iMythology, iSmelting, iLeverage),
	iIndia :		techs.column(2).including(iAlloys, iWriting, iCalendar).without(iSeafaring),
	iGreece :		techs.column(2).including(iAlloys, iArithmetics, iWriting),
	iPersia :		techs.column(3).including(iBloomery, iPriesthood).without(iSeafaring, iShipbuilding),
	iCarthage :		techs.column(2).including(iAlloys, iWriting, iShipbuilding),
	iPolynesia :	techs.of(iTanning, iMythology, iSailing, iSeafaring),
	iRome : 		techs.column(3).including(iBloomery, iCement, iMathematics, iLiterature).without(iRiding, iCalendar, iShipbuilding),
	iMaya :			techs.column(1).including(iProperty, iMasonry, iSmelting, iCeremony).without(iSailing),
	iTamils :		techs.column(3).including(iBloomery, iMathematics, iContract, iPriesthood),
	iEthiopia :		techs.column(2).including(iAlloys, iWriting, iCalendar, iPriesthood),
	iKorea :		techs.column(5).without(iGeneralship, iEngineering, iCurrency),
	iByzantium :	techs.column(5).including(iArchitecture, iPolitics, iEthics),
	iJapan :		techs.column(5).including(iNobility, iSteel, iArtisanry, iPolitics),
	iVikings : 		techs.column(5).including(iNobility, iSteel, iArtisanry, iPolitics, iScholarship, iArchitecture, iGuilds),
	iTurks :		techs.column(5).including(iNobility, iSteel).column(5).without(iNavigation, iMedicine, iPhilosophy),
	iArabia :		techs.column(6).including(iAlchemy, iTheology).without(iPolitics),
	iTibet :		techs.column(5).including(iNobility, iScholarship, iEthics),
	iIndonesia :	techs.column(5).including(iEthics).without(iGeneralship),
	iMoors :		techs.column(6).including(iMachinery, iAlchemy, iTheology).without(iPolitics),
	iSpain : 		techs.column(6).including(iFeudalism, iAlchemy, iGuilds),
	iFrance :		techs.column(6).including(iFeudalism, iTheology),
	iKhmer :		techs.column(6).including(iNobility, iArchitecture, iArtisanry, iScholarship, iEthics),
	iEngland :		techs.column(6).including(iFeudalism, iTheology),
	iHolyRome :		techs.column(6).including(iFeudalism, iTheology),
	iRussia :		techs.column(6).including(iFeudalism).without(iPolitics, iScholarship, iEthics),
	iMali : 		techs.column(6).including(iTheology),
	iPoland : 		techs.column(6).including(iFeudalism, iFortification, iCivilService, iTheology),
	iPortugal :		techs.column(7).including(iPatronage),
	iInca : 		techs.column(3).including(iMathematics, iContract, iLiterature, iPriesthood).without(iSeafaring, iAlloys, iRiding, iShipbuilding),
	iMongols :		techs.column(7).including(iPaper, iCompass).without(iTheology),
	iAztecs :		techs.column(3).including(iMathematics, iContract, iLiterature, iPriesthood, iGeneralship, iAesthetics, iCurrency, iLaw).without(iSeafaring, iAlloys, iRiding, iShipbuilding),
	iItaly : 		techs.column(7).including(iCommune, iPaper, iCompass, iDoctrine),
	iMughals :		techs.column(7).including(iCommune, iCropRotation, iDoctrine, iGunpowder),
	iOttomans :		techs.column(7).including(iCommune, iCropRotation, iPaper, iDoctrine, iGunpowder),
	iCongo : 		techs.column(6).including(iMachinery, iCivilService, iTheology),
	iThailand : 	techs.column(8).without(iCompass, iDoctrine, iCommune, iPatronage),
	iIran : 		techs.column(9).including(iHeritage, iFirearms),
	iNetherlands:	techs.column(10),
	iGermany :		techs.column(11).without(iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning),
	iAmerica :		techs.column(12).including(iRepresentation, iChemistry),
	iArgentina :	techs.column(12).including(iRepresentation, iNationalism),
	iMexico :		techs.column(12).including(iRepresentation, iNationalism),
	iColombia :		techs.column(12).including(iRepresentation, iNationalism),
	iBrazil :		techs.column(12).including(iRepresentation, iNationalism, iBiology),
	iCanada :		techs.column(13).including(iBallistics, iEngine, iRailroad, iJournalism),
},
{
	iIndependent:	techs.column(5),
	iIndependent2:	techs.column(5),
	iChina :		techs.column(6).including(iMachinery, iAlchemy, iCivilService).without(iNobility),
	iKorea :		techs.column(6).including(iMachinery).without(iScholarship),
	iByzantium :	techs.column(6).including(iFortification,iMachinery, iCivilService),
	iJapan :		techs.column(6).without(iScholarship),
	iVikings :		techs.column(6).including(iGuilds),
	iTurks :		techs.column(5).including(iNobility, iSteel).without(iNavigation, iMedicine, iPhilosophy),
},
{
	iIndependent:	techs.column(10),
	iIndependent2:	techs.column(10),
	iChina :		techs.column(10).including(iHorticulture, iUrbanPlanning).without(iExploration, iOptics, iAcademia),
	iIndia : 		techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration),
	iTamils :		techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
	iIran :			techs.column(10).including(iCombinedArms, iGeography, iUrbanPlanning, iHorticulture),
	iKorea :		techs.column(10).without(iExploration, iOptics, iAcademia),
	iJapan :		techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
	iVikings :		techs.column(11).without(iEconomics, iHorticulture),
	iTurks :		techs.column(9).including(iFirearms, iLogistics, iHeritage),
	iSpain :		techs.column(10).including(iCombinedArms, iGeography, iHorticulture),
	iFrance :		techs.column(11).without(iUrbanPlanning, iEconomics),
	iEngland :		techs.column(11).without(iUrbanPlanning, iHorticulture),
	iHolyRome :		techs.column(10).including(iCombinedArms, iUrbanPlanning, iHorticulture).without(iExploration),
	iRussia : 		techs.column(10).including(iCombinedArms, iUrbanPlanning).without(iExploration, iOptics),
	iPoland :		techs.column(11).without(iEconomics, iGeography, iHorticulture, iUrbanPlanning),
	iPortugal :		techs.column(10).including(iGeography, iHorticulture),
	iOttomans :		techs.column(10).including(iUrbanPlanning, iHorticulture).without(iExploration),
	iMughals :		techs.column(10).including(iUrbanPlanning, iHorticulture).without(iExploration, iOptics),
	iThailand :		techs.column(10).without(iExploration, iOptics),
	iCongo :		techs.column(8).including(iCartography, iJudiciary),
	iNetherlands:	techs.column(11).without(iHorticulture, iScientificMethod, iUrbanPlanning),
	iGermany :		techs.column(11).without(iGeography, iCivilLiberties, iHorticulture, iUrbanPlanning),
}]

### Tech Preferences ###

dTechPreferences = {
	iEgypt : {
		iMasonry: 30,
		iDivination: 20,
		iPhilosophy: 20,
		iPriesthood: 20,
		
		iAlloys: -20,
		iBloomery: -50,
	},
	iBabylonia : {
		iWriting: 30,
		iContract: 30,
		iCalendar: 30,
		iMasonry: 20,
		iProperty: 20,
		iDivination: 20,
		iConstruction: 20,
	
		iPriesthood: -50,
		iMathematics: -30,
		iAlloys: -30,
		iBloomery: -30,
		iSteel: -30,
	},
	iHarappa : {
		iMasonry: 20,
		iPastoralism: 20,
		iPottery: 20,
		
		iMythology: -50,
		iDivination: -50,
		iCeremony: -50,
	},
	iChina : {
		iAesthetics: 40,
		iContract: 40,
		iGunpowder: 20,
		iPrinting: 20,
		iPaper: 20,
		iCompass: 20,
		iConstruction: 20,
		iCivilService: 15,
		
		iCivilLiberties: -100,
		iHumanities: -100,
		iAcademia: -100,
		iFirearms: -50,
		iCompanies: -40,
		iExploration: -40,
		iOptics: -40,
		iGeography: -40,
		iTheology: -40,
		iEducation: -40,
		iLogistics: -40,
		iCombinedArms: -40,
		iDivination: -20,
		iSailing: -20,	
	},
	iGreece : {
		iSailing: 40,
		iShipbuilding: 40,
		iNavigation: 40,
		iWriting: 30,
		iPhilosophy: 30,
		iAesthetics: 30,
		iDivination: 30,
		iPhilosophy: 30,
		iLiterature: 30,
		iMedicine: 30,
		iCement: 20,
		iArithmetics: 20,
		iMathematics: 20,
	
		iCalendar: -30,
		iMachinery: -20,
		iPaper: -20,
		iPrinting: -20,
		iTheology: -15,
	},
	iIndia : {
		iCeremony: 200,
		iPriesthood: 200,
		iPhilosophy: 50,
		
		iEngineering: -20,
		iTheology: -20,
		iCivilService: -20,
	},
	iCarthage : {
		iNavigation: 40,
		iRiding: 30,
		iCurrency: 30,
		iCompass: 20,
	},
	iPolynesia : {
		iCompass: 20,
		iDivination: 20,
		iMasonry: 20,
		
		iAlloys: -30,
		iBloomery: -30,
	},
	iPersia : {
		iFission: 15,
	
		iTheology: -40,
	},
	iRome : {
		iTheology: 30,
		iCurrency: 20,
		iLaw: 20,
		iPolitics: 20,
		iConstruction: 15,
		iEngineering: 15,
		
		iCalendar: -20,
	},
	iMaya : {
		iCalendar: 40,
		iAesthetics: 30,
	},
	iTamils : {
		iCement: 20,
		iCompass: 20,
		iCalendar: 20,
		
		iScientificMethod: -20,
		iAcademia: -20,
		iReplaceableParts: -20,
	},
	iKorea : {
		iPrinting: 30,
		iGunpowder: 30,
	
		iOptics: -40,
		iExploration: -40,
		iReplaceableParts: -40,
		iScientificMethod: -40,
	},
	iByzantium : {
		iFinance: -50,
		iOptics: -20,
		iFirearms: -20,
		iExploration: -20,
	},
	iJapan : {
		iFeudalism: 40,
		iFortification: 40,
		iRobotics: 40,
	
		iOptics: -40,
		iExploration: -40,
		iFirearms: -30,
		iMachinery: -20,
		iGuilds: -20,
		iGeography: -20,
		iReplaceableParts: -20,
		iScientificMethod: -20,
	},
	iVikings : {
		iMachinery: 30,
		iCivilService: 30,
		iCompass: 20,
		iCombinedArms: 20,
	},
	iArabia : {
		iScholarship: 30,
		iAlchemy: 30,
		
		iFinance: -50,
		iFirearms: -50,
		iCompanies: -50,
		iPaper: -20,
	},
	iTibet : {
		iPhilosophy: 30,
		iEngineering: 20,
		iPaper: 20,
		iTheology: 20,
		iDoctrine: 20,
	},
	iIndonesia : {
		iAesthetics: 30,
		iArtisanry: 30,
		iExploration: -20,
	},
	iMoors : {
		iCivilService: 20,
	
		iExploration: -40,
		iGuilds: -40,
	},
	iSpain : {
		iCartography: 100,
		iExploration: 100,
		iCompass: 100,
		iFirearms: 100,
		iPatronage: 50,
		iReplaceableParts: 30,
		iGuilds: 15,
		iGunpowder: 15,
		iChemistry: 15,
	},
	iFrance : {
		iReplaceableParts: 30,
		iFirearms: 20,
		iExploration: 20,
		iGeography: 20,
		iLogistics: 20,
		iPatronage: 20,
		iMeasurement: 20,
		iAcademia: 20,
		iEducation: 15,
		iFeudalism: 15,
		iChemistry: 15,
		iSociology: 15,
		iFission: 12,
	},
	iKhmer : {
		iPhilosophy: 30,
		iSailing: 30,
		iCalendar: 30,
		iCivilService: 30,
		iAesthetics: 20,
		
		iCurrency: -30,
		iExploration: -30,
	},
	iEngland : {
		iExploration: 40,
		iGeography: 40,
		iFirearms: 40,
		iReplaceableParts: 30,
		iLogistics: 30,
		iCivilLiberties: 20,
		iEducation: 15,
		iGuilds: 15,
		iChemistry: 15,
	},
	iHolyRome : {
		iAcademia: 50,
		iPrinting: 50,
		iFirearms: 20,
		iReplaceableParts: 20,
		iEducation: 15,
		iGuilds: 15,
		iOptics: 15,
		iFission: 12,
	},
	iRussia : {
		iMacroeconomics: 30,
		iCombinedArms: 30,
		iReplaceableParts: 30,
		iHeritage: 15,
		iPatronage: 15,
		iUrbanPlanning: 15,
		iFission: 12,
		
		iPhilosophy: -20,
		iPrinting: -20,
		iCivilLiberties: -20,
		iSocialContract: -20,
		iRepresentation: -20,
	},
	iMali : {
		iEducation: 30,
	},
	iMughals : {
		iHumanities: 30,
		iPhilosophy: 20,
		iEducation: 20,
		iPaper: 20,
		iPatronage: 20,
		iEngineering: 15,
	
		iReplaceableParts: -30,
		iScientificMethod: -30,
		iCombinedArms: -30,
		iExploration: -30,
	},
	iPoland : {
		iCombinedArms: 30,
		iCivilLiberties: 30,
		iSocialContract: 20,
		iOptics: 20,
	},
	iPortugal : {
		iCartography: 100,
		iExploration: 100,
		iGeography: 100,
		iCompass: 100,
		iFirearms: 100,
		iCompanies: 50,
		iPatronage: 50,
		iReplaceableParts: 20,
	},
	iInca : {
		iConstruction: 40,
		iCalendar: 40,
		
		iFeudalism: -40,
		iMachinery: -20,
		iGunpowder: -20,
		iGuilds: -20,
	},
	iItaly : {
		iRadio: 20,
		iPsychology: 20,
		iFinance: 20,
		iOptics: 20,
		iPatronage: 20,
		iReplaceableParts: 20,
		iHumanities: 20,
		iAcademia: 20,
		iFission: 12,
	},
	iMongols : {
		iPaper: 15,
		
		iFirearms: -40,
		iCombinedArms: -40,
	},
	iAztecs : {
		iConstruction: 40,
		iLiterature: 20,
		
		iGuilds: -40,
		iFeudalism: -20,
		iMachinery: -20,
		iGunpowder: -20,
	},
	iOttomans : {
		iGunpowder: 30,
		iFirearms: 30,
		iCombinedArms: 30,
		iJudiciary: 20,
	},
	iThailand : {
		iCartography: -50,
		iExploration: -50,
	},
	iNetherlands : {
		iExploration: 20,
		iFirearms: 20,
		iOptics: 20,
		iGeography: 20,
		iReplaceableParts: 20,
		iLogistics: 20,
		iEconomics: 20,
		iCivilLiberties: 20,
		iHumanities: 20,
		iAcademia: 20,
		iChemistry: 15,
	},
	iGermany : {
		iEngine: 20,
		iInfrastructure: 20,
		iChemistry: 20,
		iAssemblyLine: 20,
		iPsychology: 20,
		iSociology: 20,
		iSynthetics: 20,
		iFission: 12,
	},
	iAmerica : {
		iRailroad: 30,
		iRepresentation: 30,
		iEconomics: 20,
		iAssemblyLine: 20,
		iFission: 12,
	},
	iArgentina : {
		iRefrigeration: 30,
		iTelevision: 20,
		iElectricity: 20,
		iPsychology: 20,
	},
	iBrazil : {
		iRadio: 20,
		iSynthetics: 20,
		iElectricity: 20,
		iEngine: 20,
	},
}

### Building Preferences ###

dDefaultWonderPreferences = {
	iEgypt: -15,
	iBabylonia: -40,
	iGreece: -15,
	iIndia: -15,
	iRome: -20,
	iArabia: -15,
	iIndonesia: -15,
	iFrance: -12,
	iKhmer: -15,
	iEngland: -12,
	iRussia: -12,
	iThailand: -15,
	iCongo: -20,
	iNetherlands: -12,
	iAmerica: -12,
}

dBuildingPreferences = {
	iEgypt : {
		iPyramids: 100,
		iGreatLibrary: 30,
		iGreatLighthouse: 30,
		iGreatSphinx: 30,
	},
	iBabylonia : {
		iHangingGardens: 50,
		iIshtarGate: 50,
		iSpiralMinaret: 20,
		iGreatMausoleum: 15,
		
		iPyramids: 0,
		iGreatSphinx: 0,
		
		iOracle: -60,
	},
	iChina : {
		iGreatWall: 80,
		iForbiddenPalace: 40,
		iGrandCanal: 40,
		iOrientalPearlTower: 40,
		iDujiangyan: 30,
		iTerracottaArmy: 30,
		iPorcelainTower: 30,
		
		iHangingGardens: -30,
		iHimejiCastle: -30,
		iBorobudur: -30,
		iBrandenburgGate: -30,
	},
	iGreece : {
		iColossus: 30,
		iOracle: 30,
		iParthenon: 30,
		iTempleOfArtemis: 30,
		iStatueOfZeus: 30,
		iGreatMausoleum: 20,
		iMountAthos: 20,
		iHagiaSophia: 20,
		iAlKhazneh: 15,
		iGreatLibrary: 15,
		iGreatLighthouse: 15,
		
		iPyramids: -100,
		iGreatCothon: -80,
	},
	iIndia : {
		iKhajuraho: 30,
		iIronPillar: 30,
		iVijayaStambha: 30,
		iNalanda: 30,
		iLotusTemple: 30,
		iTajMahal: 20,
		iWatPreahPisnulok: 20,
		iShwedagonPaya: 20,
		iHarmandirSahib: 20,
		iJetavanaramaya: 20,
		iSalsalBuddha: 20,
		iPotalaPalace: 20,
		iBorobudur: 15,
		iPrambanan: 15,
		
		iParthenon: -30,
		iStatueOfZeus: -20,
	},
	iCarthage : {
		iGreatCothon: 30,
		iGreatLighthouse: 15,
		iColossus: 15,
		
		iPyramids: -50,
	},
	iPolynesia : {
		iMoaiStatues: 30,
	},
	iPersia : {
		iApadanaPalace: 30,
		iGreatMausoleum: 30,
		iGondeshapur: 30,
		iAlamut: 30,
		iHangingGardens: 15,
		iColossus: 15,
		iOracle: 15,
	},
	iRome : {
		iFlavianAmphitheatre: 30,
		iAquaAppia: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iAlKhazneh: 20,
		
		iGreatWall: -100,
	},
	iMaya : {
		iTempleOfKukulkan: 40,
	},
	iTamils : {
		iJetavanaramaya: 30,
		iKhajuraho: 20,
	},
	iEthiopia : {
		iMonolithicChurch: 40,
	},
	iKorea : {
		iCheomseongdae: 30,
	},
	iByzantium : {
		iHagiaSophia: 40,
		iTheodosianWalls: 30,
		iMountAthos: 30,
		
		iNotreDame: -20,
		iSistineChapel: -20,
	},
	iJapan : {
		iItsukushimaShrine: 30,
		iHimejiCastle: 30,
		iTsukijiFishMarket: 30,
		iSkytree: 30,
	
		iGreatWall: -100,
	},
	iTurks : {
		iGurEAmir: 40,
		iSalsalBuddha: 20,
		iImageOfTheWorldSquare: 20,
	},
	iVikings : {
		iNobelPrize: 30,
		iGlobalSeedVault: 30,
		iCERN: 15,
	},
	iArabia: {
		iSpiralMinaret: 40,
		iDomeOfTheRock: 40,
		iHouseOfWisdom: 40,
		iBurjKhalifa: 40,
		iAlamut: 30,
	
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iTibet : {
		iPotalaPalace: 40,
	},
	iIndonesia : {
		iBorobudur: 40,
		iPrambanan: 40,
		iGardensByTheBay: 40,
		iShwedagonPaya: 20,
		iWatPreahPisnulok: 20,
		iNalanda: 20,
	},
	iMoors : {
		iMezquita: 100,
		
		iUniversityOfSankore: -40,
		iSpiralMinaret: -40,
		iTopkapiPalace: -40,
		iBlueMosque: -40,
	},
	iSpain : {
		iEscorial: 30,
		iGuadalupeBasilica: 30,
		iChapultepecCastle: 30,
		iSagradaFamilia: 30,
		iCristoRedentor: 20,
		iWembley: 20,
		iIberianTradingCompanyBuilding: 20,
		iTorreDeBelem: 15,
		iNotreDame: 15,
		iMezquita: 15,
	},
	iFrance : {
		iTradingCompanyBuilding: 40,
		iNotreDame: 40,
		iEiffelTower: 30,
		iVersailles: 30,
		iLouvre: 30,
		iTriumphalArch: 30,
		iMetropolitain: 30,
		iCERN: 30,
		iKrakDesChevaliers: 30,
		iChannelTunnel: 30,
		iPalaceOfNations: 20,
		iBerlaymont: 20,
		iLargeHadronCollider: 20,
		iITER: 20,
	},
	iKhmer : {
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iPrambanan: 20,
		iNalanda: 20,
	},
	iEngland : {
		iTradingCompanyBuilding: 50,
		iOxfordUniversity: 30,
		iWembley: 30,
		iWestminsterPalace: 30,
		iTrafalgarSquare: 30,
		iBellRockLighthouse: 30,
		iCrystalPalace: 30,
		iChannelTunnel: 30,
		iBletchleyPark: 20,
		iAbbeyMills: 20,
		iMetropolitain: 20,
		iNationalGallery: 20,
		iKrakDesChevaliers: 20,
		iHarbourOpera: 20,
	},
	iHolyRome : {
		iSaintThomasChurch: 30,
		iKrakDesChevaliers: 20,
		iNeuschwanstein: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iRussia : {
		iKremlin: 40,
		iSaintBasilsCathedral: 40,
		iLubyanka: 40,
		iHermitage: 40,
		iMotherlandCalls: 30,
		iAmberRoom: 30,
		iSaintSophia: 30,
		iMountAthos: 20,
		iMetropolitain: 20,
	},
	iMali : {
		iUniversityOfSankore: 40,
	},
	iPoland : {
		iSaltCathedral: 30,
		iOldSynagogue: 30,
	},
	iPortugal : {
		iCristoRedentor: 40,
		iTorreDeBelem: 40,
		iIberianTradingCompanyBuilding: 40,
		iWembley: 20,
		iEscorial: 20,
		iNotreDame: 15,
	},
	iInca : {
		iMachuPicchu: 40,
		iTempleOfKukulkan: 20,
	},
	iItaly : {
		iFlavianAmphitheatre: 30,
		iSantaMariaDelFiore: 30,
		iSistineChapel: 30,
		iSanMarcoBasilica: 30,
		iMoleAntonelliana: 30,
	},
	iMongols : {
		iSilverTreeFountain: 40,
	},
	iOttomans : {
		iTopkapiPalace: 60,
		iBlueMosque: 60,
		iHagiaSophia: 20,
		iGurEAmir: 20,
		
		iTajMahal: -40,
		iRedFort: -40,
		iSaintBasilsCathedral: -40,
	},
	iAztecs : {
		iFloatingGardens: 40,
		iTempleOfKukulkan: 30,
		
		iMachuPicchu: -40,
	},
	iMughals : {
		iTajMahal: 40,
		iRedFort: 40,
		iShalimarGardens: 40,
		iHarmandirSahib: 20,
		iVijayaStambha: 20,
		
		iBlueMosque: -80,
		iTopkapiPalace: -80,
		iMezquita: -50,
	},
	iThailand : {
		iEmeraldBuddha: 40,
		iWatPreahPisnulok: 30,
		iShwedagonPaya: 30,
		iTajMahal: 20,
		iBorobudur: 20,
		iGreatCothon: 15,
	},
	iIran: {
		iImageOfTheWorldSquare: 30,
		iShalimarGardens: 20,
	},
	iNetherlands : {
		iTradingCompanyBuilding: 60,
		iBourse: 40,
		iDeltaWorks: 40,
		iAtomium: 30,
		iBerlaymont: 30,
		iNationalGallery: 20,
		iWembley: 20,
		iCERN: 20,
		iPalaceOfNations: 20,
		iNotreDame: 15,
	},
	iGermany : {
		iBrandenburgGate: 40,
		iAmberRoom: 30,
		iNeuschwanstein: 30,
		iWembley: 20,
		iCERN: 20,
		iIronworks: 15,
	},
	iAmerica : {
		iStatueOfLiberty: 30,
		iHollywood: 30,
		iPentagon: 30,
		iEmpireStateBuilding: 30,
		iBrooklynBridge: 30,
		iGoldenGateBridge: 30,
		iWorldTradeCenter: 30,
		iHubbleSpaceTelescope: 20,
		iCrystalCathedral: 20,
		iMenloPark: 20,
		iUnitedNations: 20,
		iGraceland: 20,
		iMetropolitain: 20,
	},
	iMexico : {
		iGuadalupeBasilica: 40,
		iChapultepecCastle: 40,
		iLasLajasSanctuary: 20,
	},
	iArgentina : {
		iGuadalupeBasilica: 30,
		iLasLajasSanctuary: 30,
		iWembley: 20,
	},
	iColombia : {
		iLasLajasSanctuary: 40,
		iGuadalupeBasilica: 30,
	},
	iBrazil : {
		iCristoRedentor: 30,
		iItaipuDam: 30,
		iWembley: 20,
	},
	iCanada : {
		iFrontenac: 30,
		iCNTower: 30,
	}
}