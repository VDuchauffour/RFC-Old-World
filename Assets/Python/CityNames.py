# coding: utf-8

from Core import *
from Files import *

from Events import handler


### CONSTANTS ###

iNumLanguages = 43
(iLangAmerican, iLangArabic, iLangBabylonian, iLangBurmese, iLangByzantine, 
iLangCeltic, iLangChinese, iLangCongolese, iLangDutch, iLangEgyptian, 
iLangEgyptianArabic, iLangEnglish, iLangEthiopian, iLangFrench, iLangGerman, 
iLangGreek, iLangHittite, iLangIndian, iLangIndonesian, iLangItalian, 
iLangJapanese, iLangKhmer, iLangKorean, iLangLatin, iLangMande, 
iLangMayan, iLangMongolian, iLangNahuatl, iLangNorse, iLangNubian, 
iLangPersian, iLangPhoenician, iLangPolish, iLangPolynesian, iLangPortuguese, 
iLangQuechua, iLangRussian, iLangSpanish, iLangSwedish, iLangThai, 
iLangTibetan, iLangTurkish, iLangVietnamese) = range(iNumLanguages)

dLanguages = CivDict({
	iEgypt:	[iLangEgyptian],
	iBabylonia: [iLangBabylonian],
	iHarappa: [iLangIndian],
	iAssyria: [iLangBabylonian],
	iChina: [iLangChinese],
	iHittites: [iLangHittite, iLangBabylonian],
	iNubia: [iLangNubian, iLangEgyptian],
	iGreece: [iLangGreek],
	iIndia: [iLangIndian],
	iPhoenicia: [iLangPhoenician],
	iPolynesia: [iLangPolynesian],
	iPersia: [iLangPersian],
	iRome: [iLangLatin],
	iCelts: [iLangCeltic],
	iMaya: [iLangMayan, iLangNahuatl],
	iDravidia: [iLangIndian],
	iEthiopia: [iLangEthiopian],
	iToltecs: [iLangNahuatl],
	iKushans: [iLangIndian, iLangGreek, iLangTurkish],
	iKorea: [iLangKorean, iLangChinese],
	iByzantium: [iLangByzantine],
	iMalays: [iLangIndonesian, iLangKhmer],
	iJapan: [iLangJapanese],
	iNorse: [iLangNorse],
	iTurks: [iLangTurkish, iLangPersian, iLangArabic],
	iArabia: [iLangArabic],
	iTibet: [iLangTibetan, iLangChinese],
	iKhmer: [iLangKhmer, iLangIndonesian],
	iMoors: [iLangArabic],
	iJava: [iLangIndonesian, iLangKhmer],
	iSpain: [iLangSpanish],
	iFrance: [iLangFrench],
	iEngland: [iLangEnglish],
	iHolyRome: [iLangGerman],
	iBurma: [iLangBurmese, iLangIndian],
	iVietnam: [iLangVietnamese, iLangChinese],
	iRus: [iLangRussian],
	iSwahili: [iLangArabic],
	iMali: [iLangMande],
	iPoland: [iLangPolish, iLangRussian], 
	iPortugal: [iLangPortuguese, iLangSpanish],
	iInca: [iLangQuechua],
	iItaly: [iLangItalian],
	iMongols: [iLangMongolian, iLangTurkish, iLangChinese],
	iAztecs: [iLangNahuatl],
	iMughals: [iLangPersian, iLangArabic, iLangIndian],
	iThailand: [iLangThai, iLangKhmer, iLangIndonesian],
	iSweden: [iLangSwedish, iLangNorse],
	iRussia: [iLangRussian],
	iOttomans: [iLangTurkish, iLangArabic],
	iCongo: [iLangCongolese],
	iIran: [iLangArabic, iLangPersian],
	iNetherlands: [iLangDutch],
	iGermany: [iLangGerman],
	iAmerica: [iLangAmerican, iLangEnglish],
	iArgentina: [iLangSpanish],
	iMexico: [iLangSpanish],
	iColombia: [iLangSpanish],
	iBrazil: [iLangPortuguese, iLangSpanish],
	iCanada: [iLangAmerican, iLangEnglish, iLangFrench],
}, [])


### CSV CITY NAME MAP ###

city_names = FileMap("Cities.csv")


### TRANSLATION DICTIONARIES ###

dLanguageNames = {
	iLangAmerican: "American",
	iLangArabic: "Arabic",
	iLangBabylonian: "Babylonian",
	iLangBurmese: "Burmese",
	iLangByzantine: "Byzantine",
	iLangCeltic: "Celtic",
	iLangChinese: "Chinese",
	iLangCongolese: "Congolese",
	iLangDutch: "Dutch",
	iLangEgyptian: "Egyptian",
	iLangEgyptianArabic: "EgyptianArabic",
	iLangEnglish: "English",
	iLangEthiopian: "Ethiopian",
	iLangFrench: "French",
	iLangGerman: "German",
	iLangGreek: "Greek",
	iLangHittite: "Hittite",
	iLangIndian: "Indian",
	iLangIndonesian: "Indonesian",
	iLangItalian: "Italian",
	iLangJapanese: "Japanese",
	iLangKhmer: "Khmer",
	iLangKorean: "Korean",
	iLangLatin: "Latin",
	iLangMande: "Mande",
	iLangMayan: "Mayan",
	iLangMongolian: "Mongolian",
	iLangNahuatl: "Nahuatl",
	iLangNorse: "Norse",
	iLangNubian: "Nubian",
	iLangPersian: "Persian",
	iLangPhoenician: "Phoenician",
	iLangPolish: "Polish",
	iLangPolynesian: "Polynesian",
	iLangPortuguese: "Portuguese",
	iLangQuechua: "Quechua",
	iLangRussian: "Russian",
	iLangSpanish: "Spanish",
	iLangSwedish: "Swedish",
	iLangThai: "Thai",
	iLangTibetan: "Tibetan",
	iLangTurkish: "Turkish",
	iLangVietnamese: "Vietnamese",
}

dTranslations = dict((iLanguage, FileDict("Translations/%s.csv" % dLanguageNames[iLanguage])) for iLanguage in range(iNumLanguages))


### EVENT HANDLERS ###

@handler("cityBuilt")
def onCityBuilt(city):
	updateName(city, bFound=True)


@handler("cityAcquired")
def onCityAcquired(iOwner, iNewOwner, city):
	updateName(city)
	
	# how do we handle fallback languages in case the new owner has no translation
	# and potentially keeps a non-local translation in place


@handler("birth")
def onBirth(iPlayer):
	# update some colonial to Mexican city names
	
	pass
	

@handler("periodChange")
def onPeriodChange(iCiv, iPeriod):
	# Prey Nokor becomes Saigon
	
	updateNames(iCiv)


@handler("religionSpread")
def onReligionSpread(iReligion, iPlayer, city):
	# Yogyakarta changes to Mataram with Islam
	# Budapest is renamed to Buddhapest with Buddhism
	
	updateName(city)


@handler("revolution")
def onRevolution(iPlayer):
	# civic names are handled by a different function, not persistence
	
	updateNames(iPlayer)


@handler("greatPersonBorn")
def onGreatPersonBorn(unit, iPlayer):
	# Pitic changes to Hermosillo when a great general is born
	
	updateNames(iPlayer)


### CLASSES ###

class CityName(object):
	
	def __init__(self, 
			name, 
			bRenaming=False, 
			bRelocation=False, 
			iBefore=None, 
			iAfter=None, 
			iReligion=None,
			iPeriod=None,
			iGreatGenerals=None,
			bFound=False, 
			bSmall=False, 
			bCommunist=False, 
			bOriginal=False, 
			bConquest=False, 
			bReconquest=False, 
			bAutocratic=False, 
			bCapital=False,
			bResurrected=False,
			bRepublican=False,
			bFascist=False,
		):
		self.name = name
		
		self.bRenaming = bRenaming
		self.bRelocation = bRelocation
		
		self.iBefore = iBefore
		self.iAfter = iAfter
		self.iReligion = iReligion
		self.iPeriod = iPeriod
		self.iGreatGenerals = iGreatGenerals
		
		self.bFound = bFound
		self.bSmall = bSmall
		self.bCommunist = bCommunist
		self.bOriginal = bOriginal
		self.bConquest = bConquest
		self.bReconquest = bReconquest
		self.bAutocratic = bAutocratic
		self.bCapital = bCapital
		self.bResurrected = bResurrected
		self.bRepublican = bRepublican
		self.bFascist = bFascist
	
	def isValid(self, city, bFound=False):
		if self.iBefore is not None:
			if player(city).getCurrentEra() > self.iBefore:
				return False
		
		if self.iAfter is not None:
			if player(city).getCurrentEra() < self.iAfter:
				return False
		
		if self.iReligion is not None:
			if is_minor(city):
				if not city.isHasReligion(self.iReligion):
					return False
			else:
				if player(city).getStateReligion() != self.iReligion:
					return False
		
		if self.iPeriod is not None:
			if player(city).getPeriod() != self.iPeriod:
				return False
		
		if self.iGreatGenerals is not None:
			if player(city).getGreatGeneralsCreated() < self.iGreatGenerals:
				return False
		
		if self.bFound and not bFound:
			return False
		
		if self.bSmall:
			if city.getPopulation() > player(city).getCurrentEra() + 1:
				return False
		
		if self.bCommunist:
			if not isCommunist(city.getOwner()):
				return False
		
		if self.bOriginal:
			if city.getOriginalCiv() != city.getCivilizationType():
				return False
		
		if self.bConquest:
			if city.getGameTurnAcquired() == city.getGameTurnFounded():
				return False
		
		if self.bReconquest:
			if city.getGameTurnCivLost(city.getCivilizationType()) < 0:
				return False
		
		if self.bAutocratic:
			if not isAutocratic(city.getOwner()):
				return False
		
		if self.bCapital:
			if not city.isCapital():
				return False
		
		if self.bResurrected:
			if data.civs[city.getOwner()].iResurrections == 0:
				return False
		
		if self.bRepublican:
			if not isRepublic(city.getOwner()):
				return False
		
		if self.bFascist:
			if not isFascist(city.getOwner()):
				return False
		
		return True


def translate(name, **kwargs):
	return CityName(name, **kwargs)


def rename(name, **kwargs):
	return translate(name, bRenaming=True, **kwargs)


def relocate(name, **kwargs):
	return translate(name, bRelocation=True, **kwargs)


def found(name, **kwargs):
	return relocate(name, bFound=True, **kwargs)
	

_ = object()


### MAIN FUNCTIONS ###

def updateNames(identifier):
	for city in cities.owner(identifier):
		updateName(city)


def updateName(city, bFound=False):
	if not game.isFinalInitialized():
		return
	
	if not bFound and turn() == scenarioStartTurn():
		return

	if is_minor(city):
		return

	iCiv = civ(city)
	name = determineName(iCiv, city, bFound=bFound)
	
	applyName(city, name)


def applyName(city, name):
	if not name:
		return
	
	if name.bRelocation:
		relocateCity(city, name)
	elif name.bRenaming:
		renameCity(city, name)
	
	if city.getName() != name.getName():
		city.setName(name.getName(), False)


def getName(iPlayer, tile):
	return city_names[tile]
		
		
def determineName(identifier, tile, bFound=False):
	iCiv = civ(identifier)
	
	base_name = city_names[tile]
	
	base_name = data.dRelocatedCities.get(base_name, base_name)
	base_name = data.dRenamedCities.get(base_name, base_name)
	
	for name in getCityNames(iCiv, base_name):
		if name.isValid(identifier, bFound=bFound):
			return name


def getCityNames(iCiv, name):
	if name not in dRenamings:
		return
	
	city_renamings = dRenamings[name]
	for iLanguage in getLanguages(identifier):
		if iLanguage in city_renamings:
			renaming = city_renamings[iLanguage] # we need to deal with receiving a tuple of renamings here
			
			if renaming is _:
				renaming = translate(name)
			elif isinstance(renaming, str):
				renaming = translate(renaming)
			
			yield renaming


def getLanguages(identifier):
	return getSpecialLanguages(identifier) or dLanguages[identifier]


def getSpecialLanguages(identifier):
	iCiv = civ(identifier)
	if player(identifier).getID() < 0:
		return None
	
	if iCiv == iEgypt:
		if player(identifier).getStateReligion() == iIslam:
			return [iLangEgyptianArabic, iLangArabic]
	
	elif iCiv == iInca:
		if data.civs[iCiv].iResurrections > 0:
			return [iLangSpanish]
	
	return None


def findLocations(name):
	return plots.all().land().where(lambda p: city_names[p] == name)
	
	
def getCivicRenames(iCiv):
	iPlayer = slot(iCiv)
	if iPlayer < 0:
		return {}
	
	return {}


def renameCity(city, name):
	base_name = city_names[city] # what if we rename a relocated city
	data.dRenamedCities[base_name] = newName
	
	# how do we announce when a city name has changed for someone who owns the city


def relocateCity(city, name):
	base_name = city_names[city]
	data.dRelocatedCities[base_name] = newCity
	
	# how do we announce when a city has moved for someone who owns the city


### NAME CHANGES ###

iNumLanguages = 57
lLanguages = (
	iAmerican, iArabic, iBabylonian, iBerber, iBrazilian, 
	iBurmese, iByzantine, iCeltic, iChinese, iCongolese, 
	iCoptic, iDravidian, iDutch, iEgyptian, iEgyptianArabic, 
	iEnglish, iEthiopian, iFrench, iGerman, iGreek, 
	iHarappan, iHittite, iIndian, iItalian, iJapanese, 
	iJavanese, iLangKhmer, iKiswahili, iKorean, iKushan, 
	iLatin, iLocal, iMalay, iManchu, iMande, 
	iMayan, iMexican, iModernGreek, iMongol, iNahuatl, 
	iNorse, iNubian, iPersian, iPhoenician, iPolish, 
	iPolynesian, iPortuguese, iQuechua, iUkrainian, iRussian, 
	iSomali, iSpanish, iSwedish, iThai, iTibetan, 
	iTurkish, iVietnamese,
) = range(iNumLanguages)

name_changes = {

	### A ###

	"Aachen" : {
		iArabic: "Akan",
		iChinese: "Yachen",
		iDutch: "Aken",
		iFrench: "Aix-la-Chapelle",
		iGerman: _,
		iGreek: u"Áachen",
		iItalian: "Aquisgrana",
		iJapanese: "Ahen",
		iLatin: "Aquisgranum",
		iNorse: "Takn",
		iPolish: "Akwizgran",
		iPortuguese: u"Aquisgrão",
		iRussian: u"Áhen",
		iSpanish: u"Aquisgrán",
		iThai: u"'Akhen",
		iUkrainian: u"Aáhen",
	},
	"Aalborg" : {
		iChinese: "Aobao",
		iJapanese: "Ourubou",
		iKorean: "Olboreu",
		iNorse: _,
		iSwedish: u"Ålborg",
	},
	"Aalo": {
		iEnglish: relocate("Pasighat"),
		iIndian: _,
	},
	"Aarhus" : {
		iChinese: "Aoerhusi",
		iGerman: "Aarhaus",
		iGreek: u"Órchous",
		iJapanese: "Oufusu",
		iKorean: "Oreuhuseu",
		iLatin: "Aros",
		iNorse: _,
		iRussian: "Orhus",
		iSwedish: u"Århus",
		iTurkish: "Orhus",
	},
	"Abakansk": {
		iRussian: (
			translate("Abakan", iAfter=iGlobal), 
			_,
		),
	},
	"Abakwa": {
		iFrench: "Bamenda",
		iGerman: "Bamenda",
		iLocal: _,
	},
	"Abalessa": {
		iLangArabic: (
			relocate("Tamanrasset", iAfter=iRenaissance),
			_,
		),
	},
	"Abdera": {
		iByzantine: "Polystylon",
		iGreek: _,
		iModernGreek: "Avdira",
	},
	"Abdju": {
		iArabic: (
			relocate("Sawhaj"),
			"Afud",
		),
		iCoptic: "Ebot",
		iEgyptian: _,
		iGreek: (
			relocate("Ptolemais Hermiou"),
			"Abydos",
		),
		iLatin: relocate("Ptolemais Hermiou"),
	},
	"Aborepi": {
		iArabic: "Al-Musawarat Al-Sufra",
		iEgyptian: "Jbrp",
		iEgyptianArabic: "Musawwarat Es-Sufra",
		iNubian: _,
	},
	"Abw": {
		iArabic: rename("Aswan"),
		iCoptic: "Ieb",
		iEgyptian: _,
		iGreek: "Elephantíne",
		iLatin: "Elephantine",
	},
	"Adan": {
		iArabic: _,
		iEnglish: "Aden",
		iGreek: "Eudaimon",
	},
	"Addis Abeba": {  # renamed from Barara
		iEnglish: "Addis Ababa",
		iEthiopia: _,
		iItalian: _,
	},
	"Adjabiya": {
		iArabic: _,
		iItalian: "Agedabia",
		iLatin: "Corniclanum",
		iTurkish: "Ecdebiye",
	},
	"Adma": {
		iBabylonian: found("Harran"),
		iArabic: "Ar-Ruha",
		iGreek: "Edessa",
		iHittite: found("Harran"),
		iLocal: (  # Syriac
			translate("Urhay", iAfter=iMedieval),
			_,
		),
		iTurkish: (
			translate("Sanliurfa", iAfter=iDigital),
			"Urfa",
		),
	},
	"Adramat": {
		iArabic: relocate("Al-Qayrawan"),
		iByzantine: "Justinianopolis",
		iGreek: "Adrymeton",
		iLatin: "Hadrumetum",
		iPhoenician: _,
	},
	"Adulis": {  # founded on Qohaito
		iEgyptian: "Wddt",
		iGreek: _,
	},
	"Adummatu": {
		iArabic: "Sakakah",
		iBabylonian: _,
		iLatin: "Dumatha",
		iPersian: "Duma",
		iTurkish: "Sekake",
	},
	"Adwa": {  # relocated from Aksum
		iEthiopian: _,
		iItalian: "Adua",
	},
	"Agadez": {
		iBerber: _,
		iFrench: u"Agadès",
	},
	"Agarum": {
		iBabylonian: _,
		iArabic: relocate("Al-Kuwayt", iAfter=iIndustrial),
	},
	"Agde": {  # founded on Montpellier
		iFrench: "Agde",
		iGreek: "Agathe",
	},
	"Aghmat": {
		iArabic: (
			relocate("Warzazat", iAfter=iRenaissance),
			_,
		),
	},
	"Ahikshetra": {
		iIndian: (
			translate("Ramnagar", iAfter=iRenaissance),
			_,
		),
		iPersian: relocate("Bareilly"),
		iEnglish: relocate("Bareilly"),
	},
	"Ahmednagar": {  # founded on Punawadi
		iIndian: "Ahilyanagar",
		iPersian: _,
	},
	"Ahvaz": {  # relocated from Shushan
		iPersian: (
			translate("Hormozd-Ardeshir", iBefore=iMedieval),
			_,
		),
	},
	"Aigissos": {  # founded on Galati
		iGreek: _,
		iLatin: "Aegyssus",
		iLocal: "Tulcea", # Romanian
		iRussian: "Tulcha",
		iTurkish: u"Tulça",
	},
	"Aihun": {
		iChinese: (
			rename("Heihe", iAfter=iDigital),
			rename("Saghalien Ula", iAfter=iRenaissance),
			"Ai Hun",
		),
		iManchu: (
			rename("Saghalien Ula", iAfter=iRenaissance),
			_,
		),
		iRussian: "Aigun",
	},
	u"Aïn Salah": {
		iArabic: _,
		iFrench: "In Salah",
	},
	"Ajaccio": {  # relocated from Aleria
		iChinese: "Ayakexiao",
		iFrench: _,
		iItalian: _,
		iJapanese: "Ajakushio",
		iKorean: "Ayacho",
		iLatin: "Adiacium",
		iLocal: "Aghjacciu", # Corsican
		iPortuguese: u"Ajácio",
		iRussian: "Ayachcho",
		iTurkish: u"Ayaçço",
	},
	"Ajayameru": {
		iHarappan: found("Bagor"),
		iIndian: (
			translate("Ajmer", iAfter=iRenaissance),
			_,
		),
	},
	"Ajodhan": {
		iEnglish: relocate("Montgomery"),
		iHarappan: found("Kalibangan"),
		iIndian: _,
		iPersian: "Pakpattan",
	},
	"Aketi": {  # founded on Buta
		iCongolese: _,
		iFrench: "Port-Chaltin",
	},
	"Akhsikath": {
		iTurkish: translate("Namangan", iAfter=iRenaissance),
		iPersian: _,
	},
	"Akhtuba": {
		iRussian: (
			translate("Akhtubinsk", iAfter=iGlobal),
			_,
		),
	},
	"Akjoujt": {  # relocated from Azuggi
		iBerber: _,
		iFrench: "Fort Repoux",
	},
	"Akka": {
		iArabic: _,
		iBabylonian: _,
		iEgyptian: (
			translate(u"Ptolemaïs"), # TODO: introduct Ptolemaic period for Egypt
			"Aak",
		),
		iEnglish: (
			translate("Saint John of Acre", iBefore=iMedieval),
			"Acre",
		),
		iFrench: (
			translate("Saint-Jean d'Acre", iBefore=iMedieval),
			"Acre",
		),
		iGerman: "Akkon",
		iGreek: u"Antiókheia tês en Ptolemaïdis",
		iItalian: (
			translate("San Giovanni d'Acri", iBefore=iMedieval),
			"Acri",
		),
		iLatin: "Colonia Ptolemais",
		iPhoenician: "Ak",
		iPolish: _,
		iSpanish: (
			translate("San Juan de Acre", iBefore=iMedieval),
			"Acre",
		),
		iTurkish: _,
	},
	"Ako": {
		iJapanese: _,
		iRussian: (
			translate("Alexandrovsk-Sakhalinsky", iAfter=iGlobal),
			"Alexandrovka",
		),
	},
	"Akordat": {
		iArabic: relocate("Kassala"),
		iEnglish: relocate("Keren"),
		iEthiopian: _,
		iItalian: relocate("Keren"),
		iTurkish: relocate("Kassala"),
	},
	"Akragas": {  # founded on Panormus
		iArabic: "Kirkant",
		iGreek: _,
		iItalian: "Agrigento",
		iLatin: "Agrigentum",
	},
	"Akroinon": {  # relocated or founded from Amorion
		iHittite: "Hapanuwa",
		iGreek: _,
		iByzantine: "Nikopolis",
		iTurkish: "Afyonkarahisar",
	},
	"Aksay": {
		iRussian: _,
		iTurkish: "Aqsai",
	},
	"Aksuat": {
		iRussian: _,
		iTurkish: "Aqsuat",
	},
	"Aksum": {
		iEgyptian: relocate("Yeha"),
		iEthiopian: (
			relocate("Adwa", iAfter=iIndustrial),
			relocate("Gondar", iAfter=iMedieval),
			_,
		),
		iFrench: "Aksoum",
		iItalian: "Axum",
		iLatin: "Auxume",
		iNubian: relocate("Yeha"),
		iPortuguese: "Axum",
		iSpanish: "Axum",
	},
	"Aktogay": {
		iRussian: _,
		iTurkish: "Aqtogay",
	},
	"Aktyubinsk": {
		iRussian: _,
		iTurkish: u"Aqtöbe",
	},
	"Akwa Akpa": {
		iEnglish: "Duke Town",
		iLocal: _, # Nubian
		iPortuguese: "Calabar",
	},
	"Al-Aghwat": {  # relocated from Dimd
		iArabic: _,
		iEnglish: "Laghwat",
		iFrench: "Laghouat",
		iTurkish: "Lagvat",
	},
	"Al-Aqiq": {
		iArabic: (
			"Wadi ad-Dawasir",
			_,
		),
	},
	"Al-Asnam": {
		iArabic: (
			translate("Al-Shalaf", iAfter=iDigital),
			_,
		),
		iFrench: (
			translate("Chlef", iAfter=iDigital),
			u"Orléansville",
		),
		iLatin: "Castellum Tingitanum",
		iPhoenician: found("Kartili"),
	},
	"Al-Basit": {
		iArabic: _,
		iCeltic: "Alaba",
		iFrench: u"Albacète",
		iJapanese: "Arubasete",
		iLatin: "Alba Civitas",
		iSpanish: "Albacete",
	},
	"Al-Basrah": {  # relocated from Durine
		iArabic: _,
		iChinese: "Bashila",
		iDravidian: "Pacura",
		iEnglish: "Busrah",
		iFrench: "Bassorah",
		iGerman: "Basra",
		iGreek: u"Vasóra",
		iIndian: "Basra",
		iMalay: "Basra",
		iPersian: (
			translate("Basrah", iReligion=iIslam),
			"Vaheshtabad-Ardashir",
		),
		iPortuguese: u"Baçorá",
		iRussian: "Basra",
		iSpanish: "Basora",
		iTurkish: "Basra",
	},
	"Al-Bidda": {  # relocated from Murwab
		iArabic: (
			rename("Doha", iAfter=iIndustrial),
			_,
		),
	},
	"Al-Biraq": {  # relocated from Gholaia
		iArabic: _,
		iEnglish: "Brak",
		iFrench: "Birak",
		iItalian: "Brach",
		iLatin: "Baracum",
	},
	"Al-Garnatah": {
		iArabic: _,
		iCeltic: "Ilturir",
		iDutch: "Granada",
		iEnglish: "Granada",
		iFrench: "Grenade",
		iGreek: "Elibyrge",
		iItalian: "Granada",
		iKorean: "Geuranada",
		iLatin: "Florentia Illiberitana",
		iModernGreek: "Ghranadha",
		iPhoenician: found("Tagilit"),
		iPolish: "Grenada",
		iPortuguese: "Granada",
		iSpanish: "Granada",
	},
	"Al-Hasa": {
		iArabic: (
			translate("Al-Hufuf", iAfter=iRenaissance),
			_,
		),
		iBabylonian: "Gerrha",
	},
	"Al-Jawf": {
		iArabic: _,
		iEgyptianArabic: "El-Jawf",
		iGerman: "Al-Dschauf",
		iItalian: "El-Giof",
		iPortuguese: "Jaufe",
		iSpanish: "Al Yauf",
	},
	"Al-Juhfah": {
		iArabic: (
			rename("Rabigh"),
			_,
		),
	},
	"Al-Khartum Bahri": {  # relocated from Kerri
		iArabic: _,
		iEnglish: "Khartoum North",
	},
	"Al-Kufah": {  # relocated from Dilbat
		iArabic: (
			rename("An-Najaf", iAfter=iRenaissance),
			_,
		),
		iEnglish: "Kufa",
		iFrench: "Koufa",
		iGerman: "Kufa",
		iPortuguese: "Cufa",
		iSpanish: "Kufa",
		iTurkish: "Kufe",
	},
	"Al-Kuwayt": {  # relocated from Agarum
		iArabic: _,
		iEnglish: "Kuwait",
	},
	"Al-Madinah": {
		iArabic: _,
		iCeltic: u"Meidíne",
		iDravidian: "Metina",
		iDutch: "Medina",
		iEnglish: "Medina",
		iFrench: u"Médine",
		iGerman: "Medina",
		iIndian: "Madina",
		iItalian: "Medina",
		iJapanese: "Medina",
		iJavanese: "Madinah",
		iLatin: "Medina",
		iMalay: "Madinah",
		iPersian: "Yasrib",
		iPolish: "Medyna",
		iPortuguese: "Medina",
		iRussian: "Medina",
		iSpanish: "Medina",
		iTurkish: "Medine",
	},
	"Al-Maharraqa": {  # relocated from Nekhen
		iArabic: _,
		iGreek: "Hierasykaminos",
		iLatin: "Hierasycaminus",
	},
	"Al-Mansurah": {  # relocated from Balotra
		iArabic: _,
		iPersian: (
			relocate("Amarkot", iReligion=iIslam),
			"Mansura",
		),
	},
	"Al-Mariyya": {
		iArabic: _,
		iChinese: "A'oumeiliya",
		iLatin: "Portus Magnus",
		iPhoenician: found("Bdrt"),
		iPortuguese: "Almeria",
		iRussian: "Almeriya",
		iSpanish: u"Almería",
	},
	"Al-Mawsil": {  # relocated from Ninua
		iArabic: _,
		iDutch: "Mosoel",
		iEnglish: "Mosul",
		iFrench: "Mossoul",
		iGerman: "Mossul",
		iRussian: "Mosul",
		iPolish: "Mosul",
		iPortuguese: "Mossul",
		iSpanish: "Mosul",
		iTurkish: "Musul",
	},
	"Al-Mename": {  # relocated from Dilmun, Al-Muharraq
		iArabic: _,
		iEnglish: "Manama",
	},
	"Al-Minya": {  # relocated from Henen-Nesut
		iArabic: _,
		iCoptic: "Tmone",
		iEgyptianArabic: "El-Minya",
		iEnglish: "Minya",
		iTurkish: "Al-Minye",
	},
	"Al-Muharraq": {  # founded, relocated on Dilmun
		iArabic: (
			relocate("Al-Mename", iAfter=iGlobal),
			_,
		),
		iEnglish: relocate("Al-Mename"),
		iPortuguese: u"Forte de Barém",
	},
	"Al-Qahirah": {  # relocated from Inebu-Hedj
		iArabic: _,
		iCoptic: "Tikeshromi",
		iDutch: u"Caïro",
		iEgyptianArabic: "El-Qahirah",
		iEnglish: "Cairo",
		iFrench: "Le Caire",
		iGerman: "Kairo",
		iGreek: "Kairo",
		iItalian: "Il Cairo",
		iJapanese: "Kairo",
		iNorse: "Kairo",
		iPolish: "Kair",
		iPortuguese: "Cairo",
		iRussian: "Kair",
		iSpanish: "El Cairo",
		iTurkish: "Kahire",
	},
	"Al-Qatif": {
		iArabic: (
			relocate("Dammam", iAfter=iGlobal),
			_,
		),
	},
	"Al-Qayrawan": {  # relocated from Adramat
		iArabic: _,
		iBerber: "Tikiwan",
		iEgyptianArabic: "El Qayrawan",
		iEnglish: "Cairoan",
		iFrench: "Kairouan",
		iLocal: "Qeirwan", # Tunisian Arabic
	},
	"Al-Qulzum": {
		iArabic: (
			relocate("As-Suways", iAfter=iRenaissance),
			_,
		),
		iCoptic: "Peklousma",
		iGreek: "Klysma",
		iLatin: "Clysma",
	},
	"Al-Wadi": {
		iArabic: _,
		iFrench: "El Oued",
	},
	"Al-Zuwayrat": {
		iArabic: _,
		iFrench: u"Zouérat",
	},
	"Alalakh": {  # founded on Antiokheia
		iBabylonian: "Alakhtum",
		iEgyptian: _,
		iHittite: "Alalah",
	},
	"Alba Iulia": {
		iChinese: "Aoba Youliya",
		iFrench: "Alba-Julia",
		iGerman: u"Weißenburg",
		# iHungarian: u"Gyulafehérvár",
		iLatin: "Apulum",
		iLocal: _, # Romanian
		iPortuguese: u"Alba Júlia",
		iRussian: "Balgrad",
		iTurkish: "Erdel Belgradi",
	},
	"Albany": {
		iDutch: (
			translate("Fort Nassau", bSmall=True),
			"Beverwijck",
		),
		iEnglish: _,
	},
	"Albazin": {
		iManchu: "Yaksa",
		iPolish: "Jaxa",
		iRussian: (
			translate("Albazino", iAfter=iGlobal),
			_,
		),
	},
	"Albi": {
		iCeltic: "Albiga",
		iFrench: _,
		iLatin: "Civitas Albigensium",
	},
	"Aleria": {
		iFrench: u"Aléria",
		iGreek: "Allalia",
		iItalian: (
			relocate("Ajaccio", iAfter=iMedieval),
		),
		iLatin: _,
		iLocal: "U Cateraghju", # Corsican
	},
	u"Ålesund": {  # renamed from Borgund
		iEnglish: "Aalesund",
		iNorse: _,
	},
	"Alexandria ad Issum": {  # relocated from Antiokheia
		iArabic: "Iskandiruna",
		iEnglish: "Scanderoon",
		iFrench: "Alexandrette",
		iItalian: "Alessandretta",
		iLatin: (
			translate("Alexandretta", iAfter=iMedieval),
			_,
		),
		iSpanish: "Alejandreta",
		iTurkish: "Iskenderun",
	},
	"Alexandria Eschate": {  # renamed from Kurushkatha
		iGreek: _,
		iLatin: "Alexandria Eschata",
	},
	"Alexandreia i en Ephrati": {  # founded on Barsip
		iArabic: "Iskandariyah",
		iGreek: _,
		iLatin: "Alexandria ad Euphrates",
	},
	"Alexandro-Grushevskaya": {
		iRussian: (
			translate("Shakhty", iAfter=iGlobal),
			_,
		),
	},
	"Alexandrovka": {
		iRussian: (
			translate("Stalino", bCommunist=True),
			translate("Donetsk", iAfter=iGlobal),
			translate("Yuzivka", iAfter=iIndustrial),
			_,
		),
	},
	"Alexandrovskoye": {
		iRussian: (
			translate("Kuybyshevka-Vostochnaya", bCommunist=True),
			translate("Belogorsk", iAfter=iGlobal),
			_,
		),
	},
	"Algeciras": {  # founded on Gadir
		iArabic: "Al-Jazirah al-Khadra",
		iCeltic: "Caetaria",
		iChinese: "Aohexilasi",
		iFrench: u"Algésiras",
		iLatin: "Iulia Traducta",
		iRussian: "Al'Khesiras",
		iSpanish: _,
	},
	"Alicante": {
		iArabic: "Al-Laqant",
		iChinese: "Alikante",
		iGreek: (
			found("Hemeroskopeion"),
			"Akra Leuka",
		),
		iLatin: "Lucentum",
		iLocal: "Alacant", # Catalan
		iModernGreek: "Alikante",
		iRussian: "Alikante",
	},
	"Alkalawa": {
		iFrench: relocate("Maradi"),
		iLocal: _, # Hausa
	},
	"Almaliq": {
		iChinese: "Alimali",
		iTurkish: _,
	},
	"Almeirim": {
		iDutch: translate("Adriaansz Fort", bFound=True),
		iPortuguese: _,
	},
	"Alor Setar": {  # relocated from Kedah
		iChinese: "Yaluo Shida",
		iDravidian: "Alor Cetar",
		iMalay: _,
	},
	"Amapá": {
		iPortuguese: (
			relocate(u"Calçoene", iAfter=iGlobal),
			_,
		),
		iFrench: found("Counani"),
	},
	"Amarkot": {  # relocated from Balotra
		iPersian: (
			translate("Umerkot", iAfter=iIndustrial),
			_,
		),
	},
	"Amasia": {
		iGreek: "Amaseia",
		iHittite: found("Shapinuwa"),
		iLatin: _,
		iTurkish: "Amasya"
	},
	"Amastris": {
		iGreek: _,
		iTurkish: "Amasra",
	},
	"Ambon": {
		iDutch: "Amboina",
		iLocal: _, # Ambonese
		iPortuguese: (
			translate("Nossa Senhora de Anunciada", bOriginal=True),
			"Amboim",
		),
	},
	"Amga-Sloboda": {
		iLocal: "Amma", # Yakut
		iRussian: (
			translate("Amga", iAfter=iGlobal),
			_,
		),
	},
	"Amida": {
		iArabic: "Diyar Bakr",
		iBabylonian: "Amedi",
		iGreek: _,
		iLocal: "Tigranakert", # Armenian
		# iLocal: "Amed", # Kurdish
		iTurkish: (
			translate("Diyarbakir", iAfter=iGlobal),
			"Diyarbekir",
		),
	},
	"Amisos": {
		iByzantine: "Sampsounta",
		iGreek: _,
		iItalian: "Simisso",
		iLatin: "Pompeiopolis",
		iTurkish: "Samsun",
	},
	"Amman": {
		iArabic: _,
		iGreek: "Philadelpheia",
		iIndian: "Ammana",
		iLatin: "Philadelphia",
		iPortuguese: u"Amã",
		iSpanish: u"Ammán",
	},
	"Amorion": {
		iArabic: "Ammuriya",
		iGreek: _,
		iHittite: found("Akroinon"),
		iLatin: "Amorium",
		iTurkish: (
			relocate("Akroinon", iAfter=iIndustrial),
			"Hergen Kaleh",
		),
	},
	"Amsterdam": {
		iArabic: "Amstardam",
		iCeltic: "Amstardam",
		iChinese: "Amusitedan",
		iDutch: _,
		iJapanese: "Amusuterudamu",
		iPortuguese: u"Amsterdão",
		iSpanish: u"Ámsterdam",
	},
	"Amul": {
		iPersian: (
			translate("Amol", iAfter=iMedieval),
			_,
		),
	},
	"Amunia": {
		iArabic: (
			translate("Marsa Matruh", iAfter=iIndustrial),
			"Al-Baritun",
		),
		iCoptic: "Tparatonion",
		iEgyptian: _,
		iEgyptianArabic: (
			translate("Mersa Matruh", iAfter=iIndustrial),
			"El-Baritun",
		),
		iGreek: "Paraitonion",
		iLatin: "Paraetonium",
	},
	"An-Najaf": {  # relocated from Dilbat, renamed from Al-Kufah
		iArabic: _,
		iEnglish: "Najaf",
		iFrench: "Nadjaf",
		iGerman: "Nadschaf",
		iPolish: "An-Nadzaf",
		iSpanish: u"Náyaf",
		iTurkish: "Necef",
	},
	"Anavik": {
		iLocal: "Kapisillit", # Greenlandic
		iNorse: _,
	},
	"Anchorage": {
		iEnglish: _,
		iLocal: "Dgheyay Kaq'", # Tanaina
	},
	"Andrapana": {
		iPersian: "Dera Ismail Khan",
		iHarappan: found("Hathala"),
	},
	"Angers": {
		iFrench: _,
		iLatin: "Iuliomagus",
	},
	"Angkor Borei": {
		iLangKhmer: (
			relocate("Phnom Penh", iAfter=iIndustrial),
			_,
		),
	},
	"Angmagssalik": {
		iNorse: _,
		iLocal: "Tasiilaq", # Greenlandic
	},
	"Angostura": {
		iSpanish: (
			translate(u"Ciudad Bolívar", iAfter=iIndustrial),
			translate(u"Santo Tomé de Guayana", bSmall=True),
			_,
		),
	},
	u"Angoulême": {
		iFrench: _,
		iLatin: "Iculisma",
	},
	"Angra Pequena": {
		iDutch: u"Lüderitzbaai",
		iGerman: (
			translate(u"Lüderitz", iAfter=iIndustrial),
			u"Lüderitzbucht",
		),
		iPortuguese: _,
	},
	"Angyra": {
		iArabic: "Anqarah",
		iCeltic: _,
		iChinese: "Ankala",
		iEnglish: "Angora",
		iFrench: "Angora",
		iGreek: "Ankyra",
		iHittite: "Ankuwash",
		iIndian: "Ankara",
		iItalian: "Angora",
		iJapanese: "Ankara",
		iLatin: "Ancyra",
		iPersian: "Angora",
		iPortuguese: "Ancara",
		iTurkish: (
			translate("Ankara", iAfter=iGlobal),
			u"Enkürü",
		),
	},
	"Anhan": {
		iChinese: (
			translate("Nanchong", iAfter=iMedieval),
			_,
		),
	},
	"Anhilwara": {
		iIndian: (
			translate("Patan", iAfter=iIndustrial),
			_,
		),
	},
	"Anna Regina": {
		iDutch: "Nieuw Middelburg",
		iPortuguese: _,
	},
	"Antananarivo": {
		iLocal: _, # Malagasy
		iFrench: "Tananarive",
	},
	"Antep": {  # relocated from Kyrrhus
		iArabic: "Ayintap",
		iFrench: u"Aïntab",
		iHittite: "Khantab",
		iLocal: u"Êntab", # Armenian
		iTurkish: (
			translate("Gaziantep", iAfter=iGlobal),
			_,
		),
	},
	"Antiokheia": {
		iArabic: "Antakiyah",
		iBabylonian: found("Alalakh"),
		iChinese: "Antia",
		iDutch: u"Antiochië",
		iDravidian: "Antiyoccu",
		iEgyptian: found("Alalakh"),
		iEnglish: "Antioch",
		iFrench: "Antioche",
		iGerman: "Antiochia",
		iGreek: _,
		iHittite: found("Alalakh"),
		iItalian: "Antiochia",
		iJapanese: "Antiokia",
		iKorean: "Antiok",
		iLatin: "Antiochia",
		iMalay: "Antiokia",
		iMongol: relocate("Alexandria ad Issum", bConquest=True),
		iNorse: "Antiokia",
		iPolish: "Antiochia",
		iPortuguese: u"Antióquia",
		iSpanish: "Antioquía",
		iTurkish: "Antakya",
	},
	"Antipyrgos": {
		iArabic: "Tubruq",
		iEnglish: "Tobruk",
		iFrench: "Tobrouk",
		iGerman: "Tobruk",
		iGreek: _,
		iItalian: "Tobruch",
		iLatin: "Antipyrgus",
		iTurkish: "Tobruk",
	},
	"Anuratapuram": {
		iDravidian: _,
		iDutch: relocate("Colombo"),
		iEnglish: relocate("Colombo"),
		iGreek: "Anourogrammoi",
		iIndian: "Anuradhapura", # Sinhalese
		iPortuguese: relocate("Colombo"),
	},
	"Anxi": {
		iChinese: (
			translate("Guazhou", iAfter=iMedieval),
			_,
		),
	},
	"Anyam-Godo": {
		iFrench: relocate("Matam"),
		iLocal: (
			relocate("Orefonde", iAfter=iIndustrial),
			_,
		),
	},
	"Aodu": {
		iChinese: (
			translate("Zhengzhou", iAfter=iMedieval),
			_,
		),
	},
	"Apameia": {  # founded on Hamath
		iArabic: "Afamiyah",
		iGreek: _,
		iLatin: "Apamea",
	},
	"Api-Api": {
		iChinese: "Ya Bi",
		iEnglish: "Jesselton",
		iJapanese: "Api",
		iMalay: (
			translate("Kota Kinabalu", iAfter=iIndustrial),
			_,
		),
	},
	"Apollonia": {
		iGreek: _,
		iLatin: (
			relocate("Aulona", iAfter=iMedieval),
			_,
		),
	},
	"Aquae Sulis": {  # founded on Bristol
		iCeltic: "Caerfaddon",
		iChinese: "Basi",
		iEnglish: "Bath",
		iKorean: "Baseu",
		iLatin: _,
		iRussian: "Bat",
	},
	"Aquileia": {
		iChinese: "Akuilaiya",
		iFrench: u"Aquilée",
		iGerman: "Agley",
		iGreek: "Akyliia",
		iItalian: _,
		iLatin: _,
		iPolish: "Akwileja",
		iSpanish: "Aquilea",
	},
	"Ar-Riyad": {  # renamed from Hajr
		iArabic: _,
		iChinese: "Liyade",
		iDravidian: "Riyat",
		iEnglish: "Riyadh",
		iFrench: "Riyad",
		iGerman: "Riad",
		iGreek: "Riant",
		iIndian: "Riyaz",
		iKorean: "Riyadeu",
		iJapanese: "Riyado",
		iPersian: "Riyaz",
		iPortuguese: "Riade",
		iRussian: "Er-Riyad",
		iSpanish: "Riad",
		iTurkish: "Riyad",
	},
	"Arae": {
		iArabic: "Ras Lanuf",
		iLatin: _,
	},
	"Arawan": {
		iFrench: "Araouane",
		iMande: _,
	},
	"Arbawet": {
		iBerber: _,
		iFrench: "Arbaouet",
	},
	"Ardabil": {
		# iArmenian: "Artawil",
		iDravidian: "Arutapil",
		iPersian: _,
		iRussian: "Ardebil",
		iTurkish: "Erdebil",
	},
	"Arguin": {
		iArabic: "Nouadhibou",
		iFrench: u"Port-Étienne",
		iPhoenician: found("Chernah"),
		iPortuguese: "Arguim",
		iSpanish: _,
	},
	"Ariaka": {
		iQuechua: _,
		iSpanish: "Arica",
	},
	"Ariminum": {
		iItalian: (
			relocate("Urbino", iAfter=iRenaissance),
			"Rimini",
		),
		iLatin: _,
	},
	"Ariqipaya": {
		iQuechua: _,
		iSpanish: "Arequipa",
	},
	"Aromata": {
		iEnglish: "Damo",
		iGreek: _,
		iItalian: "Damo",
		iLatin: _,
		iSomali: "Daamo",
	},
	"Aror": {
		iHarappan: found("Kot Diji"),
		iPersian: (
			relocate("Khairpur", iAfter=iRenaissance),
			translate("Rohri", iAfter=iMedieval),
			_,
		),
	},
	"Arrajan": {
		iPersian: (
			translate("Behbahan", iAfter=iMedieval),
			_,
		),
		iBabylonian: found("Hidalu"),
	},
	"Arretium": {
		iItalian: "Arezzo",
		iLatin: _,
	},
	"Arshi": {
		iChinese: "Yanqi",
		iKushan: _, # Tocharian
		iTurkish: "Qarasheher",
	},
	"Arsinoe": {
		iGreek: (
			# rename("Kleopatris", iPeriod=iPtolemaic), # TODO: Ptolemaic period
			_,
		),
	},
	"Artacoana": {
		iGreek: rename("Herat"),
		iPersian: (
			rename("Herat", iAfter=iMedieval),
			_,
		),
	},
	"Artashat": {
		iBabylonian: found("Yerevan"),
		iGreek: "Artaxata",
		iLocal: ( # Armenian
			relocate("Dvin", iAfter=iMedieval),
			_,
		),
		iPersia: (
			relocate("Yerevan", iAfter=iMedieval),
			"Artaxshas-shat",
		),
		iTurkish: relocate("Yerevan"),
	},
	"Artemita": {  # relocated from Dur-Kurigalzu
		iArabic: "Al-Daskarah",
		iGreek: _,
		iPersian: (
			translate("Khosrau-shad-Kavath", iAfter=iMedieval),
			"Dastgird",
		),
	},
	"Arusha": {
		iEnglish: "Arusha",
		iGerman: "Aruscha",
		iKiswahili: (
			translate("Arusha", iAfter=iIndustrial),
			"Engaruka",
		),
	},
	"As-Suways": {  # relocated from Al-Qulzum
		iArabic: _,
		iEnglish: "Suez",
		iFrench: "Suez",
		iTurkish: "Suveysh",
	},
	"Asaak": {
		iLatin: "Arsacia",
		iPersian: (
			translate("Quchan", iAfter=iMedieval),
			_,
		),
	},
	"Asayeta": {  # founded on Saylac
		iEthiopian: _,
		iItalian: "Asaita",
		iSomali: "Awssa",
	},
	"Ash-shur": {
		iBabylonian: _,
		iPersian: (
			translate("Ashur", iAfter=iMedieval),
			"Athur",
		),
		iGreek: rename("Hatra"),
	},
	"Ashaval": {
		iHarappan: found("Langhnaj"),
		iDravidian: "Akamatapatu",
		iIndian: (
			translate("Karnavati", iAfter=iMedieval),
			_,
		),
		iPersian: "Ahmedabad",
	},
	"Ashgabat": {  # founded on Nisa
		iArabic: "Ishq Abad",
		iDravidian: "Akkapatu",
		iDutch: "Asjchabad",
		iGerman: "Aschgabat",
		iItalian: "Ashhabad",
		iJapanese: "Ashigabaado",
		iKushan: "Konjikala",
		iPersian: "Eshqabat",
		iPolish: "Aszchabad",
		iPortuguese: "Asgabate",
		iRussian: (
			translate("Poltoratsk", bCommunist=True),
			"Ashkhabad",
		),
		iSpanish: "Asjabad",
		iTurkish: _,
	},
	"Ashir": {  # relocated from Zdif
		iArabic: _,
		iBerber: "Achir",
		iFrench: relocate("Lamdia"),
	},
	"Ashkelon": {  # founded on Gazza
		iArabic: "Asqalan",
		iBabylonian: "Isqaluna",
		iEgyptian: "Asqalanu",
		iGreek: "Askalon",
		iLatin: "Ascalon",
		iPhoenician: _,
	},
	"Ashland": {
		iEnglish: _,
		iFrench: found("La Baye"),
	},
	"Asmara": {  # relocated from Qohaito
		iArabic: _,
		iEnglish: _,
		iEthiopian: "Asmera",
		iItalian: "L'Asmara",
	},
	"Asode": {
		iBerber: _,
		iFrench: (
			relocate("Timia", iAfter=iGlobal),
			u"Assodé",
		),
	},
	"Asosa": {
		iEthiopian: _,
		iItalian: u"Asosà",
	},
	"Asrir": {
		iArabic: "Kalmim",
		iBerber: _,
		iFrench: "Guelmim"
	},
	"Assab": {  # founded on Dongolo
		iArabic: _,
		iEthiopian: "Asab",
		iGreek: u"Arsinoë Epidiris",
		iKiswahili: "Casab",
	},
	"Astorga": {  # founded on León
		iArabic: "Astariqa",
		iLatin: "Asturica Augusta",
		iSpanish: _,
	},
	"Astrakhan": {
		iCeltic: u"An Astracáin", # Irish
		iDutch: "Astrachan",
		iFrench: _,
		iGerman: "Astrachan",
		iGreek: "Astrachan",
		iItalian: _,
		iJapanese: "Asutorahan",
		iKorean: "Aseuteurahan",
		iLatin: "Astracanum",
		iMongol: "Hajji Tarkhan",
		iPersian: "Hajitarkhan",
		iPolish: "Astrachan",
		iPortuguese: u"Astracã",
		iRussian: _,
		iSpanish: u"Astraján",
		iTurkish: "Xacitarxan",
	},
	u"Asunción": {
		iPortuguese: u"Assuncão",
		iSpanish: _,
	},
	"Aswan": {  # relocated from Abw
		iArabic: _,
		iCoptic: "Souan",
		iEgyptian: "Swenett",
		iEnglish: "Assuan",
		iFrench: "Assouan",
		iGreek: "Syene",
		iNubian: "Dib",
	},
	"Atbara": {
		iArabic: "Atbarah",
		iEthiopian: _,
		iNubian: _,
	},
	"Atemar": {
		iRussian: (
			translate("Atemar", bSmall=True),
			"Saransk",
		),
	},
	"Athenai": {
		iArabic: "Atina",
		iCeltic: u"An Àithne",
		iChinese: "Yadian",
		iDutch: "Athene",
		iEnglish: "Athens",
		iFrench: u"Athènes",
		iGerman: "Athen",
		iGreek: _,
		iItalian: "Atene",
		iJapanese: "Atene",
		iKorean: "Atene",
		iLatin: "Athenae",
		iModernGreek: u"Athína",
		iNorse: "Athena",
		iPolish: "Ateny",
		iPortuguese: "Atenas",
		iRussian: "Afiny",
		iSpanish: "Atenas",
		iTurkish: "Atina",
		iUkrainian: "Ateny",
	},
	"Atlantic City": {
		iDutch: found("Zwaanendael"),
		iEnglish: _,
		iSwedish: found(u"Älfsborg"),
	},
	"Atlin": {
		iEnglish: _,
		iLocal: u"Wéinaa", # Tlingit
	},
	"Attaleia": {
		iGreek: _,
		iItalian: "Adalia",
		iLatin: "Attalia",
		iPersian: relocate("Phaselis"),
		iTurkish: (
			translate("Antalya", iAfter=iIndustrial),
			"Adalia",
		),
	},
	"Augsburg": {
		iChinese: "Aogesibao",
		iDutch: _,
		iFrench: "Augsbourg",
		iGerman: _,
		iGreek: u"Avgústa",
		iItalian: "Augusta",
		iJapanese: "Aukusuburuku",
		iLatin: "Augusta Vindelicorum",
		iNorse: u"Ágsborg",
		iPolish: _,
		iRussian: _,
		iTurkish: _,
	},
	"Augusta": {
		iEnglish: _,
		iFrench: found(u"Fort Pentaguët"),
		iLocal: "Cushnoc", # Abenaki
	},
	"Augusta Taurinorum": {
		iCeltic: "Taurasia",
		iDutch: "Turijn",
		iEnglish: "Turin",
		iFrench: "Turin",
		iGerman: "Turin",
		iGreek: u"Touríno",
		iItalian: "Torino",
		iJapanese: "Torino",
		iKorean: "Torino",
		iLatin: (
			translate("Taurinum", iAfter=iMedieval),
			_,
		),
		iPolish: "Turyn",
		iPortuguese: "Turim",
		iSpanish: u"Turín",
		iSwedish: "Turin",
		iTurkish: "Torino",
	},
	"Aulona": {
		iEnglish: "Avlona",
		iGreek: "Avlonas",
		iItalian: "Valona",
		iLatin: _,
		iLocal: u"Vlorë", # Albanian
		iTurkish: "Avlonya",
	},
	"Aurangabad": {  # relocated from Devagiri
		iIndian: "Chhatrapati Sambhaji Nagar",
		iPersian: _,
	},
	"Austin": {
		iEnglish: _,
		iSpanish: translate("San Marcos", bFound=True),
	},
	"Automala": {
		iArabic: "Al-Uqaylah",
		iEgyptianArabic: "El Agheila",
		iGreek: _,
		iLatin: "Anabucis",
	},
	"Avarua": {
		iFrench: found("Tupua'i"),
		iPolynesian: _,
	},
	"Avignon": {
		iChinese: "Aweiniweng",
		iFrench: _,
		iGreek: "Auenion",
		iItalian: "Avignone",
		iKorean: "Abinyon",
		iLatin: "Avenio",
		iLocal: "Avinhon", # Provencal
		iPolish: "Awinion",
		iPortuguese: u"Avinhão",
		iRussian: "Avin'on",
		iSpanish: u"Aviñón",
	},
	"Awa": {
		iBurmese: (
			translate("Inwa", iAfter=iGlobal),
			_,
		),
		iIndian: "Ratanapura",
		iPortuguese: "Ava",
	},
	"Awarna": {  # founded on Halikarnassos
		iGreek: "Xanthos",
		iHittite: _,
		iLatin: "Xanthus",
		iLocal: translate(u"Arñna", iBefore=iClassical), # Lycian
		iPersian: "Arna",
		iTurkish: "Kinik",
	},
	"Awbari": {  # relocated from Garama
		iArabic: _,
		iItalian: "Ubari",
	},
	"Awdaghost": {
		iArabic: rename("Kiffa"),
		iBerber: _,
		iFrench: "Aoudaghost",
	},
	"Awjila": {
		iArabic: _,
		iGerman: "Audschila",
		iItalian: "Augila",
		iPolish: "Audzila",
		iPortuguese: "Aujila",
	},
	"Axim": {  # founded on Krindjabo
		iDutch: "Fort Sint Anthony",
		iEnglish: "Fort Saint Anthony",
		iLocal: _,
		iPortuguese: u"Forte de Santo António",
	},
	"Ayapir": {
		iArabic: "Idhaj",
		iPersian: (
			translate("Izeh", iAfter=iMedieval),
			_,
		),
	},
	"Ayutthaya": {
		iIndian: "Ayodhya",
		iLangKhmer: "Preah Nakhon",
		iThai: (
			relocate("Bangkok", iAfter=iIndustrial),
			_,
		),
	},
	"Az-Zallah": {
		iArabic: _,
		iItalian: "Zella",
	},
	"Azov": {
		iGreek: "Tanais",
		iRussian: _,
		iTurkish: "Azaq",
	},
	"Azuggi": {
		iBerber: (
			relocate("Akjoujt", iAfter=iIndustrial),
			_,
		),
		iFrench: (
			relocate("Akjoujt", iAfter=iIndustrial),
			"Azougui",
		),
		iMande: "Quqadam", # Soninke
	},
	
	### B ###
	
	u"Babilû": {
		iArabic: (
			relocate("Baghdad"),
			"Babil",
		),
		iBabylonian: _,
		iEnglish: "Babylon",
		iFrench: "Babylone",
		iGerman: "Babylon",
		iGreek: (
			relocate("Seleukeia"),
			"Babylon",
		),
		iIndian: "Baveru",
		iPersian: "Babirush",
		iPortuguese: u"Babilónia",
		iSpanish: "Babilonia",
		# iSumerian: "Kandigirak",
	},
	"Bagaw": {  # renamed from Hongsawatoi
		iBurmese: _,
		iEnglish: "Pegu",
	},
	"Baktra": {
		iArabic: "Balkh",
		# iArmenian: "Bahl",
		iGreek: _,
		iIndian: "Bahlika",
		iLatin: "Bactra",
		iLocal: "Bakhlo", # Bactrian
		iPersian: (
			translate("Zariaspa", iBefore=iClassical),
			"Bakhl",
		),
	},
	"Badamsha": {
		iRussian: _,
		iTurkish: "Badamshy",
	},
	"Badi": {
		iArabic: (
			relocate("Hayya", iAfter=iRenaissance),
			_,
		),
		iGreek: "Ptolemais Theron",
	},
	"Baghdad": {  # relocated from Babilû
		iArabic: _,
		iBabylonian: "Bagdadu",
		iChinese: "Baoda",
		iDravidian: "Pakutatu",
		iDutch: "Bagdad",
		iEnglish: _,
		iGerman: "Bagdad",
		iGreek: u"Vagdáti",
		iIndian: "Bagadad",
		iItalian: "Baldacco",
		iJapanese: "Bagudaddo",
		iKorean: "Bageudadeu",
		iLatin: "Bagdatum",
		iNorse: "Bagdad",
		iPolish: "Bagdad",
		iPortuguese: u"Bagdá",
		iRussian: "Bagdad",
		iSomali: "Baqdaad",
		iSpanish: "Bagdad",
		iThai: u"Bækdæt",
		iTurkish: "Bagdat",
		iVietnamese: "Bat-da",
	},
	"Baguio": {  # renamed from Kafagway
		iEnglish: _,
		iLocal: "Bagiw", # Ibaloi
		iSpanish: _,
	},
	"Bahir Giyorgis": {
		iEthiopian: (
			translate("Bahir Dar", iAfter=iIndustrial),
			_,
		),
	},
	u"Bahía Blanca": {
		iGerman: found("Tornquist"),
		iSpanish: _,
	},
	"Baie-Comeau": {
		iEnglish: "Comeau Bay",
		iFrench: _,
	},
	"Baigong": {
		iChinese: (
			translate("Shaoyang", iAfter=iGlobal),
			translate("Baoqing", iAfter=iMedieval),
			_,
		),
	},
	"Bailundu": {
		iLocal: _, # Ovimbundu
		iPortuguese: "Ambaca",
	},
	"Bakanas": {  # relocated from Gorguz
		iRussian: _,
		iTurkish: "Baqanas",
	},
	"Bakel": {
		iLocal: _,
		iFrench: found(u"Sénoudébou"),
	},
	"Baker Lake": {
		iEnglish: _,
		iLocal: "Qamani'tuaq", # Inuktitut
	},
	"Baku": {
		iArabic: "Bakuyah",
		iDutch: "Bakoe",
		iDravidian: "Paku",
		iFrench: "Bakou",
		iGreek: u"Bakoú",
		iLocal: "Baki", # Azerbaijani
		iPersian: (
			translate("Bad-kube", iBefore=iClassical),
			_,
		),
		iPortuguese: "Bacu",
		iRussian: _,
		iSpanish: u"Bakú",
		iTurkish: u"Bakü",
	},
	"Bakwanga": {
		iCongolese: (
			translate("Mbuji-Mayi", iAfter=iGlobal),
			_,
		),
	},
	"Balagi": {
		iArabic: "Al-Masaqit",
		iFrench: "Massaguet",
		iLocal: _, # Kanuri
	},
	"Balasagun": {
		iMongol: "Gobalik",
		iRussian: relocate("Bishkek"),
		iTurkish: (
			relocate("Bishkek", iAfter=iIndustrial),
			_,
		),
	},
	"Balotra": {
		iArabic: relocate("Al-Mansurah"),
		iHarappan: found("Loteshwar"),
		iIndian: _,
		iPersian: relocate("Amarkot"),
	},
	"Balkanabat": {
		iRussian: "Neftedag",
		iTurkish: (
			translate("Nebit-dag", iBefore=iGlobal),
			_,
		),
	},
	"Ballaarat": {
		iEnglish: "Ballarat",
		iLocal: _, # Aboriginal Wathawurrung
	},
	"Balovale": {
		iLocal: (
			translate("Zambezi", iAfter=iDigital),
			_,
		),
	},
	"Balwantnagar": {
		iIndian: _,
		iPersian: "Jhansi",
	},
	"Bambusi": {
		iEnglish: "Victoria Falls",
		iLocal: _,
	},
	"Bamiyan": {
		iArabic: "Bamyan",
		iKushan: _,
		iPersian: "Bamikan",
	},
	"Banda Aceh": {  # renamed from Kutaraja
		iArabic: "Banda Atshih",
		iChinese: "Bandayaqi",
		iDravidian: "Panta Acce",
		iDutch: "Banda Atjeh",
		iIndian: _,
		iJavanese: "Banda Acèh",
		iKorean: "Bandaache",
		iMalay: _,
		iPersian: "Banda Achah",
		iThai: "Banda'ache",
	},
	"Bandar Lampung": {  # relocated from Menggala
		iDutch: "Oosthaven",
		iMalay: _,
	},
	"Bandar Qasim": { # renamed from Boosaaso
		iArabic: _,
		iItalian: "Bender Cassim",
	},
	"Bandiagara": {
		iArabic: "Hamdullahi",
		iFrench: "Mopti",
		iMande: _,
	},
	"Bandundu": {  # relocated from Okango
		iCongolese: _,
		iDutch: "Banningstad",
		iFrench: "Banningville",
	},
	u"Bängâsu": {
		iFrench: "Bangassou",
		iLocal: _,
	},
	"Banger": {
		iJavanese: (
			rename("Probolinggo", iAfter=iIndustrial),
			_,
		),
	},
	"Bangi": {
		iFrench: "Bangui",
		iGerman: found("M'Baiki"),
		iLocal: _,
	},
	"Bangkok": {  # relocated from Ayutthaya
		iCeltic: u"Bancác",
		iChinese: "Mangu",
		iDravidian: "Pankakku",
		iGreek: u"Bangóg",
		iIndian: "Byankak",
		iLangKhmer: "Bang Makok",
		iKorean: "Bangkog",
		iPortuguese: "Banguecoque",
		iThai: _,
		iVietnamese: "Bang Coc",
	},
	"Banjar Masih": {
		iDutch: "Bandjermasin",
		iMalay: (
			translate("Banjarmasin", iAfter=iIndustrial),
			_,
		),
	},
	"Banten": {
		iMalay: (
			translate("Serang", iAfter=iIndustrial),
			_,
		),
	},
	"Banyo": {
		iGerman: "Banjo",
		iLocal: _,
	},
	"Baranavichi": {
		iEnglish: "Baranavichy",
		iGerman: "Baranawitschy",
		iPolish: "Baranowicze",
		iRussian: _,
	},
	"Barara": {
		iEthiopian: (
			rename("Addis Abeba", iAfter=iIndustrial),
			_,
		),
	},
	"Barbara": {
		iArabic: _,
		iChinese: "Bobali",
		iEnglish: "Berbera",
		iGreek: "Malao",
		iSomali: _,
	},
	"Barcelona": {
		iArabic: "Barshiluna",
		iCeltic: u"Bárkeno", # Iberian
		iChinese: "Basailuona",
		iFrench: "Barcelone",
		iGreek: (
			found("Kallipolis"),
			"Barkinon",
		),
		iItalian: "Barcellona",
		iJapanese: "Baruserona",
		iKorean: "Bareusellona",
		iLatin: "Barcino",
		iModernGreek: u"Varkelóni",
		iPhoenician: "Barkenon",
		iRussian: "Barselona",
		iSpanish: _,
		iTurkish: "Barselona",
	},
	"Bardhere": {
		iArabic: "Bardir",
		iEnglish: "Bardere",
		iItalian: "Bardera",
		iSomali: _,
	},
	"Barion": {
		iGreek: _,
		iItalian: "Bari",
		iLatin: "Barium",
	},
	"Barquisimeto": {
		iDutch: found("Oranjestad"),
		iLocal: "Watkisimeeta", # Wayuu
		iSpanish: _,
	},
	"Barrobo": {
		iEnglish: (
			found("Harper"),
			"Cape Palmas",
		),
		iLocal: _,
		iPortuguese: "Cabo das Palmas",
	},
	"Barsip": {
		iArabic: (
			relocate("Karbala"),
			"Birs",
		),
		iBabylonian: _,
		iGreek: (
			found("Alexandreia i en Ephrati"),
			"Borsippa",
		),
	},
	"Bartica": {
		iDutch: found("Fort Zeelandia"),
		iEnglish: found("Fort Island"),
	},
	"Barus": {
		iArabic: "Fansur",
		iChinese: "Binsu",
		iIndian: "Warusaka",
		iMalay: (
			relocate("Padangsidempuan", iAfter=iIndustrial),
			_,
		),
		iPersian: "Balus",
	},
	"Bashar": {
		iArabic: _,
		iBerber: "Beccar",
		iFrench: u"Béchar",
	},
	"Bassam": {  # founded on Krindjabo
		iFrench: (
			translate("Abidjan", iAfter=iIndustrial),
			"Grand-Bassam",
		),
		iLocal: _,
	},
	"Basse-Terre": {
		iEnglish: found("St. John's"),
		iFrench: _,
		iSwedish: found("Gustavia"),
	},
	"Bassein": {  # renamed from Thinsawanargara
		iBurmese: "Pathein",
		iEnglish: _,
	},
	"Bassonsdrif": {
		iDutch: _,
		iGerman: found("Warmbad"),
		iLocal: "Kakamas",
	},
	"Batalyaws": {
		iArabic: _,
		iCeltic: found("Nertobriga"),
		iEnglish: "Badajos",
		iLatin: found("Emerita Augusta"),
		iSpanish: "Badajoz",
	},
	"Batdambang": {  # founded on Chanthaburi
		iFrench: "Battambang",
		iLangKhmer: _,
	},
	"Bathurst": {  # founded on Siggcoor
		iEnglish: _,
		iFrench: "Sante Marie de Bathurs",
		iMande: "Banjul",
	},
	"Bathurst Inlet": {
		iEnglish: _,
		iLocal: "Qingaut", # Innuinnaqtun
	},
	"Baton Rouge": {
		iEnglish: _,
		iFrench: u"Bâton-Rouge",
	},
	"Baubau": {  # relocated from Unaaha
		iMalay: (
			relocate("Kendari", iAfter=iIndustrial),
			_,
		),
	},
	"Bay Chimo": {
		iEnglish: _,
		iLocal: "Umingmaktuuq", # Innuinnaqtun
	},
	"Bay-Shapur": {
		iPersian: (
			relocate("Kazerun", bReconquest=True),
			translate("Bishapur", iAfter=iRenaissance),
			_,
		),
	},
	u"Bayan Tümen": {
		iMongol: (
			translate("Choibalsan", bCommunist=True),
			_,
		),
	},
	"Bayanhot": {
		iMongol: _,
		iChinese: "Dingyuanying",
	},
	"Bayannaghur": {
		iChinese: "Bayanno'er",
		iMongol: _,
	},
	"Bayonne": {
		iFrench: _,
		iLatin: "Lapurdum",
	},
	"Bayrut": {  # founded or relocated on Gebal
		iArabic: _,
		iChinese: "Beilute",
		iDravidian: "Peyruttu",
		iDutch: "Beiroet",
		iEnglish: "Beirut",
		iFrench: "Beyrouth",
		iGerman: "Beirut",
		iGreek: u"Virytós",
		iIndian: "Beyarut",
		iItalian: "Beirut",
		iJapanese: "Beiruuto",
		iKorean: "Beiruteu",
		iLatin: "Beritus",
		iPersian: _,
		iNorse: "Beirut",
		iPolish: "Bejrut",
		iPortuguese: "Beirute",
		iRussian: "Bejrut",
		iSpanish: "Beirut",
		iTurkish: "Beyrut",
	},
	"Baytabaw": {
		iArabic: _,
		iEnglish: "Baidoa",
		iEthiopian: found("Gode"),
		iItalian: "Iscia Baidoa",
		iSomali: "Baydhabo",
	},
	"Bayyu": {
		iArabic: "Daim az-Zubayr",
		iEnglish: "Deim Zubeir",
		iLocal: _,
	},
	"Bazi": {
		iChinese: (
			translate("Bazhong", iAfter=iGlobal),
			translate("Bazhou", iAfter=iMedieval),
			_,
		),
	},
	"Bdrt": {  # relocated from Al-Mariyya
		iArabic: "Adra",
		iGreek: "Abdera",
		iPhoenician: _,
		iSpanish: "Adra",
	},
	u"Béal Feirste": {
		iCeltic: _,
		iEnglish: "Belfast",
		iNorse: found(u"Kerlingfjördr"),
	},
	"Beaubassin": {  # founded on Moncton
		iEnglish: relocate("Moncton"),
		iFrench: _,
	},
	"Beaumont": {
		iEnglish: _,
		iSpanish: "Santa Anna",
	},
	"Bedulu": {
		iDutch: relocate("Singaraja"),
		iLocal: (
			translate("Denpasar", iAfter=iIndustrial),
			translate("Gelgel", iAfter=iRenaissance),
			translate("Samprangan", iAfter=iMedieval),
			_,
		),
	},
	"Beizimiao": {
		iChinese: _,
		iMongol: "Xilinhot",
	},
	"Bejjamwada": {  # relocated from Dhanyakataka
		iIndian: (
			translate("Vijayawada", iAfter=iGlobal),
			_,
		),
		iEnglish: "Bezwada",
	},
	"Bela": {
		iArabic: "Armabil",
		iGreek: "Rhambakia",
		iHarappan: found("Sokhta Koh"),
		iIndian: "Armapilla",
		iPersian: _,
	},
	"Bela-Bela": {
		iDutch: "Warmbad",
		iEnglish: "Warmbaths",
		iLocal: _,
	},
	"Belize City": {  # founded on Lam'an'ain
		iEnglish: _,
		iMayan: "Holzuz",
		iSpanish: "Puerto Valiz",
	},
	"Belleville": {
		iEnglish: _,
		iFrench: found("Fort de Chartres"),
	},
	"Bellin": {
		iEnglish: _,
		iLocal: "Kangirsuk", # Inuktitut
	},
	"Beloozero": {
		iRussian: (
			translate("Belozersk", iAfter=iIndustrial),
			_,
		),
	},
	"Belotsarsk": {
		iRussian: _,
		iTurkish: "Kyzyl",
	},
	u"Belém": {
		iPortuguese: _,
		iLocal: "Mairi", # Tupinamba
	},
	"Beneventum": {
		iGerman: "Benevent",
		iGreek: found("Barion"),
		iItalian: "Benevento",
		iLatin: _,
	},
	"Bengkulu": {
		iDravidian: "Pankulu",
		iDutch: "Benkoelen",
		iEnglish: "Bencoolen",
		iIndian: "Benkulu",
		iJapanese: "Benkuru",
		iMalay: (
			translate("Bangka Hulu", iBefore=iMedieval),
			_,
		),
	},
	"Benin": {
		iDutch: "Benin-Stad",
		iEnglish: "Benin City",
		iGerman: "Benin-Stadt",
		iLocal: _, # Edo
		iPortuguese: "Cidade do Benim",
		iSpanish: u"Ciudad de Benín",
	},
	"Beograd": {
		iArabic: "Bilgrad",
		iCeltic: "Singidun",
		iChinese: "Bei'ergelaide",
		iDutch: "Belgrado",
		iFrench: "Belgrade",
		iGerman: "Belgrad",
		iGreek: "Singidunon",
		iItalian: "Belgrado",
		iJapanese: "Beogurado",
		iKorean: "Beogeuradeu",
		iLatin: "Singidunum",
		iLocal: _, # Serbian
		iModernGreek: u"Veligrádhi",
		iNorse: "Beograd",
		iPolish: "Belgrad",
		iPortuguese: "Belgrado",
		iRussian: "Belgrad",
		iSpanish: "Belgrado",
		iTurkish: "Belgrad",
	},
	"Bergen": {  # renamed from Bjørgvin
		iChinese: "Bei'ergen",
		iDutch: _,
		iGerman: _,
		iLatin: "Berga",
		iNorse: _,
		iSwedish: _,
		iPortuguese: "Berga",
		iTurkish: _,
	},
	"Berlin": {  # relocated from Brandenburg
		iArabic: "Barlin",
		iCeltic: u"Beirlín",
		iChinese: "Bolin",
		iDutch: "Berlijn",
		iEnglish: _,
		iFrench: _,
		iGerman: _,
		iGreek: u"Verolíno",
		iItalian: "Berlino",
		iJapanese: "Berurin",
		iKorean: "Bereullin",
		iLatin: "Berolinum",
		iNorse: _,
		iPortuguese: "Berlim",
		iSpanish: u"Berlín",
		iTurkish: _,
	},
	"Bern": {
		iChinese: "Bo'en",
		iDutch: _,
		iEnglish: _,
		iFrench: "Berne",
		iGerman: _,
		iGreek: u"Vérni",
		iItalian: "Berna",
		iJapanese: "Berun",
		iKorean: "Bereun",
		iLatin: "Berna",
		iNorse: _,
		iPersian: _,
		iPolish: "Berno",
		iPortuguese: "Berna",
		iSpanish: "Berna",
		iTurkish: _,
	},
	"Bertua": {
		iFrench: "Bertoua",
		iGerman: _,
		iLocal: _,
	},
	"Beruas": {
		iMalay: (
			relocate("Melaka", iAfter=iMedieval),
			_,
		),
	},
	"Beruniy": {  # renamed from Kath
		iArabic: "Biruni",
		iRussian: _,
	},
	u"Besançon": {
		iChinese: "Beisangsong",
		iFrench: _,
		iGerman: translate("Bisanz", iBefore=iRenaissance),
		iItalian: "Besanzone",
		iLatin: "Vesontio",
	},
	"Beshbalik": {
		iTurkish: (
			translate("Jimsar", iAfter=iRenaissance),
			_,
		),
		iChinese: (
			translate("Fuyuan", iAfter=iRenaissance),
			translate("Tingzhou", iAfter=iMedieval),
			"Beiting",
		),
	},
	"Bethel": {
		iEnglish: _,
		iLocal: "Mamterilleq", # Yupik
	},
	"Beyin": {  # founded on Krindjabo
		iDutch: "Fort Willem III",
		iEnglish: "Fort Apollonia",
		iLocal: _,
		iPortuguese: u"Forte Apolónia",
		iSwedish: "Fort Apollonia",
	},
	"Bharuch": {
		iArabic: _,
		iChinese: "Polukachepo",
		iEnglish: "Broach",
		iGreek: "Barygaza",
		iHarappan: found("Bhagatray"),
		iIndian: "Bharutkachha",
		iLatin: "Barigaza",
		iPersian: (
			relocate("Surat", iAfter=iRenaissance),
			_,
		),
		iPortuguese: relocate("Daman"),
	},
	"Bhatia": {
		iGreek: "Alexandreia i en Indos",
		iHarappan: found("Ganweriwala"),
		iPersian: (
			translate("Uch", iAfter=iMedieval),
			_,
		),
	},
	"Bhir": {  # founded on Kalyani
		iArabic: "Bir",
		iEnglish: "Beed",
		iIndian: "Bidar",
		iPersian: _,
	},
	"Bhuj": {
		iIndian: _,
		iPersian: translate("Suleiman Nagar", iReligion=iIslam),
	},
	"Bibracte": {  # founded on Nevers
		iCeltic: _,
		iFrench: "Autun",
		iLatin: "Augustodunum",
	},
	"Bida": {
		iFrench: found("Fort Arenberg"),
		iLocal: ( # Nupe
			relocate("Abuja", iAfter=iGlobal),
			_,
		),
	},
	"Bidderi": {
		iFrench: found("Massakory"),
		iLocal: _,
	},
	"Bihe": {
		iLocal: _,
		iPortuguese: (
			rename("Cuito", iAfter=iGlobal),
			"Silva Porto",
		),
	},
	"Bikrampur": {
		iEnglish: "Dacca",
		iIndian: _,
		iPersian: (
			translate("Jahangirabad", iBefore=iRenaissance),
			"Dhaka",
		),
	},
	"Bilbao": {
		iCeltic: found("Tullo"),
		iChinese: "Bi'erba'e",
		iJapanese: "Birubao",
		iLatin: (
			found("Flaviobriga"),
			"Bilbaum",
		),
		iLocal: "Bilbo", # Basque
		iPortuguese: "Bilbau",
		iSpanish: _,
	},
	"Bingzhou": {
		iChinese: (
			translate("Jining", iAfter=iMedieval),
			_,
		),
		iMongol: (
			translate("Ulanqab", bCommunist=True),
			"Chaborte",
		),
	},
	u"Bir Moghreïn": {
		iArabic: _,
		iFrench: found("Fort-Trinquet"),
	},
	"Biram": {
		iEnglish: found("Damaturu"),
		iLocal: ( # Hausa
			translate("Hadeja", iAfter=iGlobal),
			_,
		),
	},
	"Birka": {
		iNorse: (
			rename("Stockholm", iAfter=iRenaissance),
			_,
		),
		iSwedish: (
			rename("Stockholm", iAfter=iRenaissance),
			_,
		),
	},
	"Birmingham": {  # relocated from Derby
		iChinese: "Bominghan",
		iEnglish: _,
		iJapanese: "Bamingamu",
		iRussian: "Birmingem",
	},
	"Birnin Kebbi": {
		iLocal: (
			relocate("Sakkwato", iReligion=iIslam),
			_,
		),
	},
	"Bishkek": {
		iChinese: "Bishikaike",
		iDutch: "Bisjkek",
		iDravidian: "Pitkekku",
		iFrench: "Bichkek",
		iGerman: "Bischkek",
		iIndian: "Biskek",
		iJapanese: "Bishukeku",
		iPolish: "Biszkek",
		iRussian: (
			translate("Frunze", bCommunist=True),
			_,
		),
		iTurkish: _,
	},
	"Bishnupur": {
		iIndian: _,
		iNorse: found("Dannemarksnagore"),
		iPersian: found("Qazimbazar"),
	},
	u"Bjørgvin": {
		iNorse: (
			rename("Bergen", iAfter=iRenaissance),
			_,
		),
	},
	u"Bjørnsted": {
		iLocal: "Nanortalik", # Greenlandic
		iNorse: (
			found(u"Herjolfsnæs", iBefore=iMedieval),
			_,
		),
	},
	"Black River": {
		iEnglish: _,
		iSpanish: found("Puerto Lempira"),
	},
	"Blagoveshchensk": {
		iLocal: "Aytyun",
		iRussian: _,
	},
	"Bloomington": {
		iEnglish: _,
		iFrench: found("Fort Ouiatenon"),
	},
	"Bluefields": {
		iDutch: "Blauvelt",
		iEnglish: _,
		iLocal: "Kukra",
		iSpanish: found("San Carlos"),
	},
	"Boduna": {
		iChinese: (
			translate("Songyuan", iAfter=iDigital),
			_,
		),
		iEnglish: "Petuna",
		iKorean: found("Buyeo"),
		iRussian: "Bodune",
	},
	u"Bogotá": {
		iLocal: u"Muyquytá",
		iSpanish: (
			translate(u"Bogotá", iAfter=iIndustrial),
			u"Santafé",
		),
	},
	"Bogu": {
		iChinese: (
			translate("Binzhou", iAfter=iDigital),
			"Putai",
		),
		iLocal: _,
	},
	"Bokuda": {
		iDutch: relocate("Gemena"),
		iFrench: relocate("Gemena"),
		iLocal: _,
	},
	"Boma": {
		iEnglish: rename("Lundazi"),
		iLocal: _,
		iKiswahili: _,
	},
	"Bomani": {
		iArabic: rename("Baraka"),
		iDutch: rename("Baraka"),
		iFrench: rename("Baraka"),
		iKiswahili: rename("Baraka"),
	},
	"Bononia": {
		iChinese: "Boluoniya",
		iDutch: "Bologna",
		iEnglish: "Bologna",
		iFrench: "Bologne",
		iGerman: "Bologna",
		iGreek: u"Volonía",
		iItalian: "Bologna",
		iJapanese: "Boronya",
		iKorean: "Bollonya",
		iLatin: _,
		iLocal: (
			translate(u"Bulåggna", iAfter=iMedieval), # Bolognese
			"Felsina", # Etruscan
		),
		iPolish: "Bolonia",
		iPortuguese: "Bolonha",
		iSpanish: "Bolonia",
		iTurkish: "Bolonya",
	},
	"Boosaaso": {
		iArabic: rename("Bandar Qasim"),
		iEnglish: "Bosaso",
		iGreek: "Mosylon",
		iItalian: "Bosaso",
		iLatin: "Mosyllum",
		iLocal: _, # Somali
	},
	"Bordeaux": {
		iArabic: "Burdu",
		iCeltic: (
			translate(u"Bordaíl", iAfter=iMedieval),
			"Burdigala",
		),
		iChinese: "Bo'erduo",
		iDutch: _,
		iEnglish: _,
		iFrench: _,
		iGerman: _,
		iGreek: u"Vordhígala",
		iJapanese: "Borudo",
		iKorean: "Boreudo",
		iLatin: "Burdigala",
		iLocal: translate(u"Bordèu", iAfter=iMedieval), # Occitan
		iPortuguese: u"Bordéus",
		iSpanish: "Burdeos",
		iSwedish: _,
	},
	"Bordj Badji Mokhtar": {
		iBerber: _,
		iFrench: "Bordj Le Prieur",
	},
	"Bordj Omar Driss": {
		iBerber: _,
		iFrench: "Fort Flatters",
	},
	"Borg": {
		iNorse: (
			translate("Sarpsborg", iAfter=iRenaissance),
			_,
		),
	},
	"Borgund": {
		iNorse: (
			rename(u"Ålesund", iAfter=iIndustrial),
			_,
		),
	},
	u"Borgå": {
		iLatin: "Borgoa",
		iLocal: "Porvoo", # Finnish
		iSwedish: _,
	},
	"Borroloola": {
		iDutch: found("Kaap van der Lyn"),
		iEnglish: _,
		iLocal: "Burrulula", # Aboriginal Garrwa
	},
	"Bosra": {
		iArabic: "Busra",
		iGreek: (
			found("Kanatha"),
			"Bostra",
		),
		iLatin: "Nova Trajana Bostra",
		iLocal: _, # Nabataean
		iTurkish: "Nafs Busra",
	},
	"Bost": {
		iLatin: "Bestia Desolata",
		iPersian: (
			rename("Lashkargah", iAfter=iMedieval),
			_,
		),
	},
	"Boston": {
		iEnglish: _,
		iFrench: "Tremontaine",
		iLocal: "Shawmut", # Massachusett
	},
	"Bouar": {
		iFrench: found("Carnot"),
		iLocal: _,
	},
	"Bourges": {
		iCeltic: "Avaricon",
		iFrench: _,
		iLatin: "Avaricum",
	},
	"Bozhou": {
		iChinese: (
			translate("Zunyi", iAfter=iRenaissance),
			_,
		),
	},
	"Bozok": {
		iTurkish: (
			translate("Nur-Sultan", iAfter=iDigital, bAutocratic=True, bCapital=True),
			translate("Astana", iAfter=iGlobal, bCapital=True),
			translate("Akmola", iAfter=iIndustrial),
			_,
		),
		iRussian: (
			translate("Tselinograd", bCommunist=True),
			"Akmolinsk",
		),
	},
	"Braganza": {  # founded on Orense
		iEnglish: _,
		iFrench: "Bragance",
		iGerman: _,
		iPortuguese: u"Bragança",
		iSpanish: _,
	},
	"Bragman's Bluff": {
		iEnglish: _,
		iLocal: "Bilwi",
		iSpanish: "Puerto Cabezas",
	},
	"Brandenburg": {
		iGerman: (
			relocate("Berlin", iAfter=iRenaissance, bCapital=True),
			_,
		),
		iPolish: "Brenna", # Polabian
	},
	"Brandon": {
		iEnglish: _,
		iFrench: found("Fort Qu'Apelle"),
	},
	u"Brattahlið": {
		iEnglish: "Brattahlid",
		iLocal: "Narsarsuaq",
		iNorse: _,
	},
	"Bremen": {
		iChinese: "Bulaimei",
		iDutch: _,
		iFrench: u"Brême",
		iGerman: _,
		iGreek: u"Vrémi",
		iItalian: "Brema",
		iJapanese: "Buremen",
		iKorean: "Beuremen",
		iLatin: "Brema",
		iNorse: (
			translate("Brimarborg", iBefore=iMedieval),
			_,
		),
		iPolish: "Brema",
		iPortuguese: "Brema",
		iSpanish: "Brema",
		iSwedish: _,
		iTurkish: _,
	},
	"Bremersdorp": {  # founded on KaMpfumu
		iDutch: _,
		iEnglish: relocate("Mbabane", iAfter=iGlobal),
		iLocal: "Manzini",
	},
	"Brest": {
		iArabic: "Brist",
		iCeltic: "Bresta",
		iEnglish: _,
		iFrench: _,
		iLatin: "Gesoscribate",
	},
	"Brest-Litovsk": {
		iGerman: "Brest-Litowsk",
		iLatin: "Berestia",
		iPolish: (
			translate("Brzesc nad Bugiem", iAfter=iGlobal),
			"Brzesc Litewski",
		),
		iRussian: _,
		iUkrainian: "Berestia",
	},
	"Bristol": {
		iCeltic: (
			found("Aquae Sulis"),
			translate("Bryste", iAfter=iIndustrial),
			"Caerodor",
		),
		iChinese: "Bulisituo'er",
		iEnglish: _,
		iLatin: (
			found("Aquae Sulis"),
			"Bristolium",
		),
	},
	"Brixia": {
		iItalian: "Brescia",
		iLatin: _,
		iLocal: translate(u"Brèsa", iAfter=iMedieval), # Lombard
	},
	"Brno": {
		iGerman: u"Brünn",
		iItalian: "Bruna",
		iLatin: "Bruna",
		iLocal: _, # Czech
		iPolish: "Berno",
		iPortuguese: "Bruno",
		iRussian: "Brno",
	},
	"Broughton Island": {
		iEnglish: _,
		iLocal: "Qikiqtarjuaq", # Inuktitut
	},
	"Bruxelles": {
		iArabic: "Bruksel",
		iCeltic: u"An Bhruiséil",
		iChinese: "Bulusai'er",
		iDutch: "Brussel",
		iEnglish: "Brussels",
		iFrench: _,
		iGerman: (
			translate(u"Brüssel", iAfter=iRenaissance),
			"Bruchsal",
		),
		iGreek: u"Vrixélles",
		iItalian: "Borsella",
		iJapanese: "Buryusseru",
		iKorean: "Beurwisel",
		iLocal: "Brussele", # Walloon
		iNorse: "Bryssel",
		iPolish: "Bruksela",
		iPortuguese: "Bruxelas",
		iRussian: "Bryussel",
		iSpanish: "Bruselas",
		iSwedish: "Bryssel",
		iTurkish: u"Brüksel",
	},
	"Bu'ri": {
		iChinese: (
			translate("Simao", bCommunist=True),
			translate("Pu'er", iAfter=iRenaissance),
			translate("Pu'ri", iAfter=iMedieval),
			_,
		),
	},
	"Buchanan": {  # founded on Nzerekore
		iAmerican: _,
		iEnglish: "Grand Bassa",
		iLocal: "Gbezohn", # Bassa
	},
	"Buckland": {
		iEnglish: _,
		iLocal: "Nunatchiaq", # Inupiaq
	},
	"Bucuresti": {
		iArabic: "Buqarist",
		iCeltic: u"Búcairist",
		iChinese: "Bujialesite",
		iDutch: "Boekarest",
		iEnglish: "Bucharest",
		iFrench: "Bucarest",
		iGerman: "Bukarest",
		iGreek: u"Voukourésti",
		iItalian: "Bucarest",
		iJapanese: "Bukaresuto",
		iKorean: "Bukuresyuti",
		iLatin: "Bucaresta",
		iLocal: (
			translate("Herastrau", iBefore=iClassical), # Dacian
			_, # Romanian
		),
		iMalay: "Bucares",
		iNorse: "Bukarest",
		iPolish: "Bukareszt",
		iPortuguese: "Bucareste",
		iRussian: "Bukharest",
		iSpanish: "Bucarest",
		iSwedish: "Bukarest",
		iTurkish: "Bükresh",
	},
	"Buda": {
		iDutch: "Boeda",
		iGerman: (
			rename("Budapest", iAfter=iIndustrial),
			"Ofen",
		),
		iLatin: "Aquincum",
		iLocal: ( # Hungarian
			rename("Budapest", iAfter=iIndustrial),
			_,
		),
		iTurkish: "Budin",
	},
	"Budapest": {  # renamed from Buda
		iCeltic: u"Búdaipeist",
		iChinese: "Budapeisi",
		iDutch: "Boedapest",
		iGerman: _,
		iGreek: u"Voudhapésti",
		iItalian: _,
		iJapanese: "Budapesuto",
		iLatin: "Budapestinum",
		iLocal: _, # Hungarian
		iPolish: "Budapeszt",
		iPortuguese: "Budapeste",
		iRussian: "Budapesht",
		iSpanish: _,
		iSwedish: _,
		iTurkish: "Budapeshte",
	},
	"Buenos Aires": {
		iEnglish: found("Hurlingham"),
		iSpanish: _,
	},
	"Bugulma": {
		iMongol: "Begelma",
		iRussian: _,
		iTurkish: u"Bögelma",
	},
	"Bukhara": {
		iArabic: _,
		iChinese: (
			translate("Buhala", iAfter=iGlobal),
			"Buhe",
		),
		iDravidian: "Pukkara",
		iDutch: "Boechara",
		iEnglish: "Bokhara",
		iFrench: "Boukhara",
		iGreek: u"Poukhára",
		iItalian: "Buchara",
		iLocal: translate("Buxarak", iBefore=iMedieval), # Sogdian
		iPersian: "Boxara",
		iPolish: "Buchara",
		iPortuguese: "Bucara",
		iRussian: _,
		iSpanish: u"Bujará",
		iTurkish: "Bukhara",
	},
	"Bukui": {
		iChinese: _,
		iManchu: "Qiqihar",
	},
	"Bulawayo": {
		iDutch: found("Vryheid"),
		iEnglish: found("Newcastle, kwaZulu-Natal"),
		iLocal: _, # Ndebele
	},
	"Buna": {  # relocated from Kong
		iFrench: "Bouna",
		iLocal: _,
	},
	"Bunbun": {
		iEnglish: "Brooke's Point",
		iLocal: _, # Palawan
	},
	"Bunbury": {
		iDutch: found("Landt van de Leeuwin"),
		iEnglish: _,
		iLocal: "Goomburrup", # Aboriginal Nyungar
	},
	"Bundi": {
		iIndian: _,
		iPersian: relocate("Kotah"),
	},
	"Bunkeya": {
		iCongolese: relocate("Likasi"),
		iDutch: relocate("Likasi"),
		iFrench: relocate("Likasi"),
		iLocal: _,
	},
	"Burco": {  # relocated from Maduuna
		iArabic: "Burao",
		iEnglish: "Burao",
		iSomali: _,
	},
	"Burekiwe": {
		iDutch: rename("Yambio"),
		iEnglish: rename("Yambio"),
		iFrench: rename("Yambio"),
		iLocal: _,
	},
	"Burgos": {
		iArabic: "Burghush",
		iCeltic: found("Cluniaco"),
		iLatin: (
			found("Cluniaco"),
			"Caput Castellae",
		),
		iSpanish: _,
	},
	"Burketown": {
		iDutch: found("Van Diemens Kaap"),
		iEnglish: _,
	},
	"Burlington": {
		iEnglish: _,
		iFrench: found("Fort Carillon"),
	},
	"Burnie": {
		iDutch: found("Van Diemens Landt"),
		iEnglish: _,
	},
	"Bursa": {  # relocated from Pergamon
		iDutch: "Boersa",
		iDravidian: "Purca",
		iFrench: "Brousse",
		iGreek: "Prousa",
		iJapanese: "Burusa",
		iLatin: "Prusa",
		iPersian: "Borsa",
		iTurkish: _,
	},
	"Buta": {
		iCongolese: _,
		iFrench: found("Aketi"),
	},
	"Butha": {
		iChinese: (
			rename("Zhalantun", iAfter=iGlobal),
			"Buteha",
		),
		iMongol: (
			rename("Zhalantun", iAfter=iGlobal),
			_,
		),
	},
	"Butre": {  # founded on Krindjabo
		iDutch: "Fort Batenstein",
		iLocal: _,
	},
	"Buur Gabo": {  # founded on Kismaayo
		iEnglish: "Port Dunford",
		iGerman: "Hohenzollernhafen",
		iGreek: "Nikon",
		iItalian: "Bur Gavo",
		iLatin: "Nicon",
		iSomali: _,
	},
	"Buyeo": {  # founded on Boduna
		iChinese: "Nong'an",
		iKorean: _,
	},
	"Buzanjird": {
		iPersian: (
			translate("Bojnord", iAfter=iMedieval),
			_,
		),
	},
	"Buzulukskaya": {
		iRussian: (
			translate("Buzuluk", iAfter=iIndustrial),
			_,
		),
	},
	"Bwake": {
		iFrench: u"Bouaké",
		iLocal: _,
	},
	"Bwali": {
		iCongolese: _,
		iFrench: found("Pointe-Noire"),
		iPortuguese: rename("Loango"),
	},
	"Bwhen": {
		iArabic: "Buhen",
		iEgyptian: _,
		iGreek: "Boon",
		iLatin: "Buma",
	},
	"Bydgoszcz": {
		iGerman: "Bromberg",
		iLatin: "Bidgostia",
		iPolish: _,
		iUkrainian: "Bydhoshch",
	},
	"Bytown": {
		iEnglish: (
			translate("Ottawa", iAfter=iIndustrial),
			_,
		),
		iLocal: u"Odàwàg", # Algonquian
	},
	"Byzantion": {
		iArabic: "Bizantiya",
		iChinese: "Baizhanting",
		iDutch: _,
		iEnglish: "Byzantium",
		iFrench: "Byzance",
		iGerman: "Byzanz",
		iItalian: "Bisanzio",
		iGreek: _,
		iLatin: (
			rename("Constantinopolis", iReligion=iOrthodoxy),
			"Byzantium",
		),
		iLocal: "Lygos", # Thracian
		iPolish: "Bizancjum",
		iPortuguese: u"Bizâncio",
		iRussian: "Visantiy",
		iSpanish: "Bizancio",
		iSwedish: "Bysans",
	},
	
	### C ###
	
	"Cacheu": {  # founded on Koldaa
		iLocal: "Caticheu", # Banyun
		iPortuguese: _,
	},
	"Cadota": {
		iChinese: "Jingjue",
		iKushan: _,
		iLocal: "Niya",
	},
	"Caen": {
		iFrench: _,
		iLatin: "Catumagos",
	},
	"Caernarfon": {
		iCeltic: _,
		iEnglish: "Carnarvon",
		iLatin: (
			found("Canovium"),
			"Seguntium",
		),
	},
	"Cahors": {
		iCelts: "Divona",
		iFrench: _,
		iLatin: "Divona Cadurcorum",
	},
	"Calagurris": {  # Logroño
		iArabic: "Qalat Horra",
		iLatin: _,
		iLocal: "Calagorra", # Aragonese
		iSpanish: "Calahorra",
	},
	"Calatayud": {
		iArabic: "Qalat Ayyub",
		iCeltic: found("Nouantikum"),
		iLatin: "Augusta Bilbilis",
		iSpanish: (
			found("Soria"),
			_,
		),	
	},
	"Calixtlahuaca": {
		iNahuatl: _,
		iSpanish: "Toluca",
	},
	"Cambridge": {
		iCeltic: "Caergrawnt",
		iChinese: "Jianqiao",
		iEnglish: _,
		iGreek: u"Kantavrigía",
		iJapanese: "Kemburijji",
		iKorean: "Keimbeuriji",
		iLatin: (
			translate("Duroliponte", bFound=True),
			"Cantabrigia",
		),
		iPortuguese: u"Cambrígia",
	},
	"Cambridge Bay": {
		iEnglish: _,
		iLocal: "Iqaluktuuttiaq", # Innuinnaqtun
	},
	"Can Tho": {  # relocated from O Keo
		iEnglish: "Cantho",
		iFrench: _,
		iVietnamese: _,
	},
	"Canosium": {
		iItalian: "Canosa",
		iLatin: _,
	},
	"Canovium": {  # founded on Caernarfon
		iEnglish: "Conwy",
		iLatin: _,
	},
	u"Cap-Français": {
		iFrench: _,
		iLocal: rename(u"Cap-Haïtien"),
		iSpanish: u"Cabo Francés",
	},
	u"Cap-Haïtien": {
		iEnglish: "Cape Haitien",
		iFrench: _,
		iLocal: "Kap Ayisyen",
		iPortuguese: "Cabo Haitiano",
		iSpanish: "Cabo Haitiano",
	},
	"Cape Dorset": {
		iEnglish: _,
		iLocal: "Kinngait", # Inuktitut
	},
	"Cape Girardeau": {
		iEnglish: _,
		iFrench: "Cap-Girardeau",
	},
	"Capsa": {
		iArabic: "Gafsah",
		iFrench: "Gafsa",
		iLatin: _,
	},
	"Caracas": {
		iDutch: found("Kralendijk"),
		iSpanish: _,
	},
	"Caralis": {
		iFrench: "Caglier",
		iGreek: "Karalis",
		iItalian: "Cagliari",
		iLatin: _,
		iLocal: "Casteddu",
		iPhoenician: "Karaly",
		iSpanish: u"Cáller",
	},
	"Cardiff": {
		iCeltic: "Caerdydd",
		iEnglish: _,
		iNorse: found("Swansea"),
	},
	"Carnarvon": {
		iDutch: found("Dirck Hartogs Ree Cap"),
		iEnglish: _,
		iFrench: found("Havre Hamelin"),
		iLocal: "Kuwinywardu",
	},
	"Carolusborg": {  # founded on Ougaa
		iEnglish: "Cape Coast Castle",
		iSwedish: _,
	},
	"Carnot": {  # founded on Bouar
		iFrench: _,
		iLocal: "Tendira",
	},
	"Cartagena": {  # founded on Mursiyya
		iArabic: "Al-Qartajanna",
		iByzantine: "Carthago Spartaria",
		iCeltic: "Mastia",
		iChinese: "Xin Jiataiji",
		iFrench: u"Carthagène",
		iLatin: "Carthago Nova",
		iModernGreek: u"Karthayéni",
		iPhoenician: "Qart-Hadasht",
		iPolish: "Kartagina",
		iPortuguese: _,
		iSpanish: _,
	},
	"Cartago": {
		iSpanish: (
			relocate(u"San José", iAfter=iIndustrial),
			_,
		),
	},
	"Castelo Branco": {
		iArabic: "Bur Al-Agrah",
		iCeltic: "Kataleukos",
		iLatin: "Castra Leuca",
		iPortuguese: _,
	},
	"Castra Madensia": {
		iArabic: (
			found("Mizda"),
			"Gheriat el-Garbia",
		),
		iLatin: _,
	},
	"Castro": {
		iDutch: "Castrolanda",
		iPortuguese: (
			relocate("Londrina", iAfter=iGlobal),
			_,
		),
	},
	"Catamarca": {
		iQuechua: found("Shincal"),
		iSpanish: _,
	},
	"Catanzaro": {  # relocate from Crotona
		iArabic: "Qatansar",
		iGreek: u"Katantzárion",
		iItalian: _,
		iLatin: "Chatacium",
	},
	"Cayenne": {
		iFrench: _,
		iPortuguese: "Caiena",
		iSpanish: "Cayena",
	},
	u"Cañadón León": {
		iSpanish: (
			translate("Gobernador Gregores", iAfter=iGlobal),
			_,
		),
	},
	"Cedar Rapids": {
		iEnglish: _,
		iGerman: found("Neu-Ulm"),
	},
	"Cempoalatl": {
		iNahuatl: _,
		iSpanish: relocate("Veracruz"),
	},
	"Cervantes": {
		iDutch: found("I. de Edels Landt"),
		iEnglish: _,
		iSpanish: _,
	},
	u"Ceské Budejovice": {
		iGerman: "Budweis",
		iKorean: "Cheseuki Budeyobiche",
		iLatin: "Budovicium",
		iLocal: _,
		iPolish: "Czeskie Budziejowice",
		iUkrainian: "Ches'ke-Budejovyce",
	},
	"Chach": {
		iArabic: "Ash-Shash",
		iChinese: "Zheshi",
		iPersian: (
			translate("Tashkand", iAfter=iMedieval),
			_,
		),
		iRussian: "Tashkent",
		iTurkish: "Toshkent",
	},
	"Chaiya": {
		iMalay: _,
		iThai: (
			found("Surat Thani"),
			"Talat Chaiya",
		),
	},
	"Chakanputun": {
		iMayan: _,
		iSpanish: (
			found("Villahermosa"),
			u"Champotón",
		),
	},
	"Chalchihuites": {
		iNahuatl: _,
		iSpanish: found("Durango"),
	},
	u"Chalon-sur-Saône": {
		iCeltic: "Cabillonum",
		iFrench: _,
		iLatin: "Cavillonum",
	},
	"Chamdo": {
		iChinese: "Changdu",
		iTibetan: _,
	},
	"Champa": {
		iIndian: (
			translate("Bhagalpur", iAfter=iMedieval),
			_,
		),
	},
	"Champassak": {
		iFrench: rename("Pakse"),
		iLangKhmer: (
			rename("Pakse", iAfter=iIndustrial),
			_,
		),
	},
	"Chan Chan": {
		iLocal: _,
		iQuechua: _,
		iSpanish: relocate("Trujillo"),
	},
	"Chandanavati": {
		iEnglish: "Baroda",
		iHarappan: found("Lothal"),
		iIndian: (
			translate("Vadodara", iAfter=iMedieval),
			_,
		),
		iPersian: "Muhammadpur",
	},
	"Chandax": {  # renamed from Heraklion and Knossos
		iArabic: "Rabd al-Handaq",
		iByzantine: _,
		iEnglish: "Candy",
		iFrench: "Candie",
		iItalian: "Candia",
		iSpanish: "Candia",
		iTurkish: "Kandiye",
	},
	"Chandka": {
		iHarappa: found("Mohenjo-Daro"),
		iIndian: (
			translate("Larkana", iAfter=iMedieval),
			_,
		),
	},
	"Chandraketugarh": {
		iDutch: found("Pipli"),
		iIndian: (
			translate("Khulna", iAfter=iMedieval),
			_,
		),
		iNorse: found("Pipli"),
	},
	"Chandrapura": {
		iArabic: found("Karwar"),
		iDutch: found("Vengurla"),
		iEnglish: found("Karwar"),
		iIndia: (
			relocate("Govapuri", iAfter=iMedieval),
			_,
		),
		iPortuguese: relocate("Govapuri"),
	},
	"Chandradwip": {
		iArabic: "Tshandra Dip",
		iIndian: (
			translate("Barishal", iAfter=iMedieval),
			_,
		),
		iPersian: (
			translate("Ismailpur", iReligion=iIslam),
			"Gird-e-Bandar",
		),
		iPortuguese: "Bacola",
	},
	"Chang'an": {
		iChinese: (
			translate("Xi'an", bResurrected=True),
			_,
		),
		iKorean: "Jang'an",
		iMongol: "Fengyuan",
	},
	"Changchun": {
		iChinese: _,
		iJapanese: "Hsinking",
		iKorean: "Jangchun",
	},
	"Changnan": {
		iChinese: (
			translate("Jingdezhen", iAfter=iMedieval),
			_,
		),
	},
	"Chania": {  # renamed from Kydonia
		iArabic: "Al-Kan",
		iFrench: u"La Canée",
		iGreek: "Chania",
		iItalian: "La Canea",
		iSpanish: "La Canea",
		iTurkish: "Hanya",
	},
	"Chanthaburi": {
		iLangKhmer: found("Batdambang"),
		iThai: _,
	},
	"Chaozhou": {
		iChinese: (
			translate("Shantou", iAfter=iRenaissance),
			_,
		),
	},
	u"Chapecó": {
		iGerman: found("Dreizehnlinden"),
		iPortuguese: _,
	},
	"Charklik": {
		iChinese: "Ruoqiang",
		iTurkish: _,
	},
	"Charleston": {
		iAmerican: _,
		iEnglish: "Charles Town",
	},
	"Charlottesville": {
		iEnglish: _,
		iGerman: "Germanna",
	},
	"Charlottetown": {
		iEnglish: _,
		iFrench: found("Port-LaJoye"),
	},
	"Chartres": {
		iFrench: _,
		iLatin: "Autricum",
	},
	"Chattogram": {
		iArabic: (
			translate("Jatjam", iAfter=iIndustrial),
			"Sadkawan",
		),
		iBurmese: "Tsi-ta-gung",
		iDravidian: "Conkin",
		iDutch: "Xatigan",
		iEnglish: "Chittagong",
		iIndian: _,
		iJapanese: "Juukei",
		iKorean: "Chunggyeong",
		iLocal: "Chatigaon",
		iPersian: (
			translate("Islamabad", iReligion=iIslam, iBefore=iIndustrial),
			"Chatgam",
		),
		iPortuguese: u"Chatigão",
		iTibetan: "Jvalan'dhdra",
		iTurkish: "Chungching",
		iVietnamese: "Trung Khanh",
	},
	"Cheboksary": {
		iItalian: "Cibocar",
		iLocal: "Shupashkar",
		iRussian: _,
		iTurkish: "Chabaqsar",
	},
	"Chedzugwe": {
		iEnglish: found("Kariba"),
		iItalian: found("Sinoia"),
		iLocal: _,
		iPortuguese: found("Ongoe"),
	},
	"Chelkar": {
		iRussian: _,
		iTurkish: "Shalqar",
	},
	"Chelyabinsk": {
		iArabic: "Tshiliabinsk",
		iChinese: "Cheliyabinsike",
		iDutch: "Tsjeljabinsk",
		iFrench: "Tcheliabinsk",
		iGerman: "Tscheljabinsk",
		iJapanese: "Cheryabinsuku",
		iMongol: u"Çiläbe",
		iPolish: "Czelabinsk",
		iRussian: _,
		iSpanish: u"Cheliábinsk",
		iTurkish: u"Çelyabi",
	},
	"Chengdu": {
		iChinese: _,
		iDravidian: "Cenkutu",
		iJapanese: "Seito",
		iKorean: "Seongdo",
		iPersian: "Changdo",
		iTurkish: "Chingdu",
		iVietnamese: "Thanh Do",
	},
	"Chengsijiazi": {
		iChinese: (
			translate("Baicheng", iAfter=iMedieval),
			_,
		),
		iMongol: "Chaghanhot",
	},
	"Chengxiang": {
		iChinese: (
			translate("Meizhou", iAfter=iGlobal),
			translate("Jiaying", iAfter=iRenaissance),
			translate("Meizhou", iAfter=iMedieval),
			_,
		),
	},
	"Cherbourg": {
		iCeltic: (
			found("Duron"),
			"Coriallo",
		),
		iEnglish: "Kerburgh",
		iFrench: _,
		iLatin: (
			found("Duron"),
			"Coriallum",
		),
		iNorse: "Kjarrborg",
	},
	"Cherkassk": {
		iRussian: (
			relocate("Rostov-na-Donu", iAfter=iIndustrial),
			_,
		),
	},
	"Chernah": {  # founded on Arguin
		iLatin: "Cerne",
		iPhoenician: _,
	},
	"Chernihiv": {
		iGerman: "Tschernigow",
		iPolish: u"Czernihów",
		iRussian: "Chernigov",
		iUkrainian: _,
	},
	"Chernivtsi": {
		iGerman: "Tschernowitz",
		# iHungarian: "Csernyivci",
		iNorse: "Tsjernivtsi",
		iPolish: "Czerniowce",
		# iRomanian: "Cernauti",
		iRussian: "Chernovtsy",
		iUkrainian: _,
	},
	"Chesterfield Inlet": {
		iEnglish: _,
		iLocal: "Igluligaarjuk", # Inuktitut
	},
	"Chiang Mai": {
		iChinese: "Qingmai",
		iEnglish: _,
		iFrench: _,
		iJapanese: "Chenmai",
		iPortuguese: _,
		iSpanish: _,
		iThai: "Cheiynghim",
	},
	"Chibyu": {
		iLocal: "Ukva", # Komi
		iRussian: (
			translate("Ukhta", iAfter=iGlobal),
			_,
		),
	},
	"Chicoutimi": {
		iFrench: "Saguenay",
		iLocal: _,
	},
	"Chifeng": {
		iChinese: (
			translate("Linhuang", bCapital=True),
			_,
		),
		iMongol: "Ulanhad",
	},
	"Chilia": {
		iGreek: _,
		iItalian: "Licostomo",
		iRussian: "Kiliya",
		iTurkish: "Kiliya",
		iUkrainian: "Kiliia",
	},
	"Chimoio": {
		iEnglish: found("Umtali"),
		iLocal: _,
		iPortuguese: "Vila Pery",
	},
	"Chishinau": {
		iArabic: "Kishinaw",
		iDutch: "Chisinau",
		iGerman: "Kischinau",
		iGreek: u"Kisnóvio",
		iJapanese: "Kishinau",
		iLocal: _, # Romanian
		iPolish: u"Kiszyniów",
		iPortuguese: "Quixinau",
		iRussian: "Kishinyov",
		iSpanish: "Chisinau",
		iTurkish: "Kishinev",
		iUkrainian: "Kyshyniv",
	},
	"Chita": {
		iMongol: "Cyty",
		iRussian: _,
	},
	"Chittor": {
		iHarappan: found("Langhnaj"),
		iIndian: (
			translate("Chitrakuta", iBefore=iClassical),
			translate("Chittorgarh", iAfter=iRenaissance),
			_,
		),
	},
	"Chipata": {
		iEnglish: "Fort Jameson",
		iLocal: _,
		iPortuguese: relocate("Zumbo"),
	},
	"Chortitza": {  # founded on Oleksandrivsk
		iDutch: _,
		iRussian: "Khortytsya",
	},
	"Chouragarh": {
		iIndian: (
			translate("Narsinghpur", iAfter=iRenaissance),
			_,
		),
	},
	"Christchurch": {  # relocated from Te Kai-a-te-Karoro
		iEnglish: _,
		iPolynesian: "Otautahi",
	},
	"Christianburg": {
		iEnglish: (
			translate("Linden", iAfter=iGlobal),
			_,
		),
	},
	"Christianshaab": {
		iLocal: "Qasigiannguit", # Greenlandic
		iNorse: _,
	},
	"Chunju": {
		iKorean: (
			translate("Chuncheon", iAfter=iRenaissance),
			_,
		),
	},
	"Churchill": {
		iEnglish: (
			translate("Prince of Wales Fort", bSmall=True),
			_,
		),
	},
	"Circesium": {  # founded on Mari
		iArabic: "Al-Qarqisiya",
		iLatin: _,
	},
	u"Ciudad de Panamá": {
		iDutch: "Panama-Stad",
		iEnglish: (
			found("New Edinburgh"),
			"Panama City",
		),
		iFrench: "Panama",
		iGerman: "Panama-Stadt",
		iPortuguese: u"Cidade do Panamá",
		iSpanish: _,
	},
	"Ciudad del Este": {
		iSpanish: (
			translate("Puerto Flor de Lis", bAutocratic=True),
			_,
		),
	},
	"Ciudad Real": {  # relocated from Pa' Chan
		iMayan: "Jovel",
		iSpanish: (
			translate(u"San Cristóbal de las Casas", iAfter=iIndustrial),
			_,
		),
	},
	"Claudiopolis": {  # founded on Herakleia
		iByzantine: "Hadrianopolis",
		iGreek: "Bithynion",
		iLatin: _,
		iTurkish: "Bolu",
	},
	"Clermont": {
		iCeltic: "Nemessos",
		iFrench: (
			translate("Clermont-Ferrant", iAfter=iRenaissance),
			_,
		),
		iLatin: "Augustonemetum",
	},
	"Clinton Creek": {
		iEnglish: _,
		iLocal: u"Dätl'äkayy juu", # Hän
	},
	"Cluj": {
		iGerman: "Klausenburg",
		# iHungarian: u"Kaloszvár",
		iKorean: "Keullujinapoka",
		iLatin: (
			translate("Claudiopolis", iAfter=iMedieval),
			"Napoca",
		),
		iLocal: _, # Romanian
		iPolish: "Kluz",
	},
	"Cluniaco": {  # founded on Burgos
		iCeltic: _,
		iLatin: "Colonia Clunia Sulpicia",
		iSpanish: "Clunia",
	},
	"Clyde River": {
		iEnglish: _,
		iLocal: "Kangiqtugaapik", # Inuktitut
	},
	"Cohors Breucorum": {  # founded on Muaskar
		iArabic: "Takhemaret",
		iLatin: _,
	},
	"Coimbra": {
		iArabic: "Qulumriyah",
		iCeltic: "Conimbriga",
		iLatin: "Aeminium",
		iPhoenician: "Habis",
		iPortuguese: _,
		iSpanish: u"Coímbra",
	},
	"Colchester": {
		iCeltic: "Camulodunon",
		iEnglish: _,
		iLatin: "Camulodunum",
	},
	"Colhuacan": {
		iNahuatl: _,
		iSpanish: u"Culiacán",
	},
	"Colombo": {  # relocated from Anuratapuram
		iArabic: "Kalanpu",
		iDravidian: "Kolumpu",
		iDutch: _,
		iEnglish: _,
		iIndian: "Kolamba",
		iPortuguese: _,
	},
	"Colonia del Sacramento": {
		iBrazilian: u"Colônia do Sacramento",
		iPortuguese: u"Colónia do Sacramento",
		iSpanish: _,
	},
	"Columbia": {
		iAmerican: _,
		iEnglish: "Brunswick Town",
	},
	"Concord": {
		iEnglish: _,
		iFrench: found("Fort Sainte-Anne"),
	},
	"Confluencia": {
		iLocal: "Nehuenken", # Mapundugun
		iSpanish: (
			translate(u"Neuquén", iAfter=iIndustrial),
			_,
		),
	},
	"Constanta": {
		iGerman: "Konstanza",
		iGreek: "Tomis",
		iLocal: _, # Romanian
		iPolish: "Konstanca",
		iPortuguese: u"Constança",
		iRussian: "Konstanca",
		iTurkish: u"Köstence",
	},
	"Constantina": {  # renamed from Kirthan
		iArabic: "Qusantinah",
		iByzantine: "Konstantina",
		iFrench: "Constantine",
		iItalian: _,
		iLatin: _,
		iPortuguese: _,
		iSpanish: _,
		iTurkish: "Konstantin",
	},
	"Constantinopolis": {  # renamed from Byzantion
		iArabic: "Qustantiniyya",
		iChinese: "Junshitandingbao",
		iDutch: "Constantinopel",
		iEnglish: "Constantinople",
		iFrench: "Constantinople",
		iGerman: "Konstantinopel",
		iGreek: "Konstantinoupolis",
		iItalian: "Constantinopoli",
		iJapanese: "Konsutantinopuru",
		iKorean: "Konseutantinopolliseu",
		iLatin: _,
		iNorse: u"Miklagarðr",
		iPersian: (
			translate("Takht-e Rum", iBefore=iClassical),
			"Qostantiniye",
		),
		iPolish: u"Carogród",
		iPortuguese: "Constantinopla",
		iRussian: "Tsargrad",
		iSpanish: "Constantinopla",
		iSwedish: u"Miklagård",
		iTurkish: (
			rename("Istanbul", iAfter=iGlobal),
			"Kostantiniyye",
		),
	},
	"Consuegra": {  # founded and relocated from Qal'at Rabah
		iCeltic: "Consabura",
		iLatin: "Consaburum",
		iSpanish: _,
	},
	"Cooktown": {
		iDutch: found("'t Landt Van Carpentarie"),
		iEnglish: _,
		iLocal: "Gangaar",
	},
	"Coppermine": {
		iEnglish: _,
		iLocal: "Qurluqtuq", # Inuktitut
	},
	"Coral Bay": {
		iDutch: found("Dorre Eijlanden"),
		iEnglish: _,
		iFrench: found("Havre Freycinet"),
	},
	"Coral Harbour": {
		iEnglish: _,
		iLocal: "Salliit", # Inuktitut
	},
	"Corcaigh": {
		iCeltic: _,
		iChinese: "Kuo'erkaihe",
		iEnglish: "Cork",
		iKorean: "Koreukeu",
		iLatin: "Corcagia",
		iNorse: found("Waterford"),
	},
	"Corfinium": {
		iGerman: relocate("L'Aquila", iBefore=iRenaissance),
		iItalian: "Valva",
		iLatin: _,
	},
	"Corinium": {  # founded on Oxford
		iCeltic: "Corinion",
		iEnglish: "Cirencester",
		iGreek: "Korinion",
		iLatin: _,
	},
	"Coro": {
		iDutch: found("Willemstad"),
		iGerman: "Neu-Augsburg",
		iSpanish: _,
	},
	"Counani": {  # founded on Amapá
		iFrench: _,
		iPortuguese: "Cunani", 
	},
	"Crotona": {
		iGreek: (
			relocate("Catanzaro", iAfter=iMedieval),
			"Kroton",
		),
		iItalian: (
			translate("Crotone", iAfter=iGlobal),
			"Cotrone",
		),
		iLatin: _,
	},
	"Cua Han": {  # relocated from Indrapura
		iChinese: "Xiangang",
		iDravidian: "Tananku",
		iFrench: "Tourane",
		iJapanese: "Danan",
		iLocal: "Daknan", # Cham
		iPersian: "Da Naang",
		iVietnamese: (
			translate("Da Nang", iAfter=iIndustrial),
			_,
		),
	},
	"Cuauhnahuac": {
		iLocal: u"Ñu'iza",
		iNahuatl: _,
		iSpanish: (
			found("Puebla"),
			"Cuernavaca",
		),
	},
	"Cuenca": {
		iArabic: "Qunqa",
		iCeltic: found("Segobriga"),
		iLatin: found("Segobriga"),
		iSpanish: _,
	},
	"Cuito": {
		iLocal: "Kuito",
		iPortuguese: _,
	},
	"Cumuda": {
		iChinese: (
			translate("Hami", iAfter=iRenaissance),
			translate("Zhongyun", iAfter=iMedieval),
			"Kunmo",
		),
		iKushan: _,
		iMongol: "Qamil",
		iTurkish: "Qumul",
	},
	"Curitiba": {
		iGerman: found("Pomerode"),
		iLocal: "Kuri'yty", # Tupi
		iPortuguese: _,
	},
	
	### D ###
	
	"Dabaw": {
		iLocal: _, # Tagalog
		iSpanish: "Davao",
	},
	"Dadun": {
		iChinese: _,
		iJapanese: rename("Taichung"),
		iLocal: "Toatun",
	},
	u"Däkkär": {
		iArabic: "Dakkar",
		iEnglish: relocate("Hargeysa"),
		iEthiopian: (
			relocate("Jijiga"),
			_,
		),
		iSomali: "Doggor",
	},
	"Dagon": {
		iBurmese: (
			translate("Yangon", iAfter=iRenaissance),
			_,
		),
		iEnglish: "Rangoon",
		iFrench: "Rangoun",
		iGerman: "Rangun",
		iJapanese: "Yangun",
		iPortuguese: "Rangum",
		iSpanish: u"Rangún",
	},
	"Dahanapura": {
		iJavanese: (
			translate("Kediri", iAfter=iRenaissance),
			_,
		),
	},
	"Daire": {
		iCeltic: _,
		iEnglish: "Londonderry",
	},
	"Dala": {
		iLocal: ( # Hausa
			translate("Kano", iAfter=iRenaissance),
			_,
		),
	},
	"Daliang": {
		iChinese: (
			translate("Bianliang", iAfter=iMedieval, iBefore=iMedieval),
			translate("Kaifeng", iAfter=iClassical),
			_,
		),
		iKorean: "Kaebong",
	},
	"Dallas": {
		iEnglish: _,
		iFrench: found("Fort le Dout"),
	},
	"Daman": {
		iIndian: _,
		iPersian: _,
		iPortuguese: u"Damão",
	},
	"Dampier": {
		iDutch: found("'t Landt Van d'Eendracht"),
		iEnglish: _,
	},
	"Damxung": {
		iChinese: _,
		iTibetan: "Dangquka",
	},
	"Danangombe": {
		iEnglish: found("Gweru"),
		iLocal: _,
		iPortuguese: found("Maramuca"),
	},
	"Dangqu": {
		iChinese: (
			translate("Quxian", iAfter=iMedieval),
			_,
		),
	},
	"Danjiangkou": {
		iChinese: (
			translate("Shiyan", iAfter=iMedieval),
			_,
		),
	},
	"Dannemarksnagore": {  # founded on Bishnupur
		iIndian: "Gondalpara",
		iNorse: _,
	},
	"Dani Baa": {  # relocated from Huaxyacac
		iLocal: _,
		iNahuatl: relocate("Huaxyacac"),
		iSpanish: u"Monte Albán",
	},
	"Dantewada": {
		iDutch: found("Nagula Vancha"),
		iIndian: _,
	},
	"Danzig": {
		iCeltic: "Gydanysg",
		iDutch: "Danswijk",
		iEnglish: translate("Dantsic", iBefore=iRenaissance),
		iGerman: _,
		iGreek: "Ghdhansk",
		iItalian: "Danzica",
		iJapanese: "Gudanisuku",
		iKorean: "Geudanseukeu",
		iLatin: "Gedania",
		iPolish: "Gdansk",
		iPortuguese: "Danzigue",
		iRussian: "Gdansk",
		iSpanish: _,
		iUkrainian: "Hdansk",
	},
	"Dar es Salaam": {  # relocated from Mzizima
		iArabic: "Dar as-Salam",
		iEnglish: _,
		iGerman: "Daressalam",
		iKiswahili: _,
		iTurkish: "Darusselam",
	},
	"Darabgerd": {
		iPersian: (
			translate("Darab", iAfter=iMedieval),
			_,
		),
	},
	"Darrtsemdo": {
		iChinese: (
			translate("Kangding", iAfter=iIndustrial),
			"Dajianlu",
		),
		iTibetan: _,
	},
	"Dawei": {
		iBurmese: _,
		iEnglish: "Tavoy",
		iThai: (
			found("Ratchaburi"),
			"Thawai",
		),
	},
	"Dayong": {
		iChinese: (
			translate("Zhangjiajie", iAfter=iDigital),
			_,
		),
	},
	"Dayr az-Zawr": {  # founded on Mari
		iArabic: _,
		iTurkish: "Deir ez-Zor",
	},
	"Debal": {
		iArabic: "Daybul",
		iGreek: "Barbarikon",
		iHarappan: found("Balakot"),
		iLatin: "Barbaricum",
		iPersian: (
			translate("Karachi", iAfter=iIndustrial),
			translate("Kolachi", iAfter=iRenaissance),
			_,
		),
	},
	"Debba": {
		iArabic: "Al Dabbah",
		iEgyptianArabic: "El Debbah",
		iNubian: _,
	},
	"Debrecen": {
		iGerman: "Debrezin",
		iGreek: u"Débretsen",
		iKorean: "Debeurechen",
		iLocal: _, # Hungarian
		iPolish: "Debreczyn",
		iRussian: "Debretsin",
	},
	"Deception Bay": {
		iEnglish: _,
		iLocal: "Salluit", # Inuktitut
	},
	"Degehabur": {
		iEthiopian: _,
		iItalian: "Dagabur",
		iSomali: "Dhagaxbuur",
	},
	"Delhi": {  # renamed from Indraprastha
		iEnglish: "New Delhi",
		iIndian: "Dilli",
		iPersian: (
			translate("Shahjahanabad", iAfter=iRenaissance, iBefore=iRenaissance, bCapital=True),
			_,
		),
		iPortuguese: "Deli",
	},
	"Der": {
		iArabic: "Al-Kut",
		iBabylonian: _,
		iPersian: translate("Madharaya", iReligion=iZoroastrianism),
	},
	"Deraheib": {
		iArabic: "Jebel Alaqi",
		iGreek: "Berenike Panchrysos",
		iLatin: "Berenice Panchrysos",
		iNubian: _,
	},
	"Derawar": {
		iPersian: (
			translate("Bahawalpur", iAfter=iIndustrial),
			_,
		),
	},
	"Derbent": {
		iArabic: "Bab al-Abwab",
		iPersian: (
			translate("Darband", iAfter=iRenaissance),
			translate("Weroy-pahr", iAfter=iMedieval),
			"Albana",
		),
		iRussian: _,
		iTurkish: "Demirkapi",
	},
	"Derventio": {
		iCeltic: found("Uiroconion"),
		iEnglish: (
			found("Coventry"),
			relocate("Birmingham", iAfter=iIndustrial),
			"Derby",
		),
		iLatin: _,
		iNorse: u"Djúrabý"
	},
	"Desinganadu": {
		iDutch: "Quilon",
		iDravidian: (
			translate("Kollam", iAfter=iRenaissance),
			_,
		),
		iEnglish: (
			relocate("Kochi"),
			"Quilon",
		),
		iPortuguese: "Coulam",
	},
	"Desterro": {
		iFrench: found("Joinville"),
		iGerman: found("Blumenau"),
		iPortuguese: (
			translate(u"Florianópolis", iAfter=iIndustrial),
			_,
		),
	},
	"Detroit": {
		iEnglish: _,
		iFrench: u"Fort Détroit",
	},
	"Devagiri": {
		iIndian: _,
		iPersian: (
			relocate("Aurangabad", iAfter=iRenaissance),
			"Daulataband",
		),
		iPortuguese: found(u"Paço de Arcos"),
	},
	"Devikota": {
		iEnglish: "Darjeeling",
		iIndian: (
			relocate("Siliguri", iAfter=iGlobal),
			relocate("Koch Behar", iAfter=iRenaissance),
			_,
		),
		iPersian: relocate("Dinajpur"),
	},
	"Dewaim": {
		iArabic: "Ad-Duwaym",
		iEgyptianArabic: "Ed Dueim",
		iEnglish: (
			relocate("Kosti", iAfter=iIndustrial),
			_,
		),
		iGreek: relocate("Kosti"),
	},
	"Dhanyakataka": {
		iEnglish: relocate("Bejjamwada"),
		iIndian: _,
	},
	"Dhanyawadi": {
		iBurmese: (
			relocate("Waithali", iAfter=iMedieval),
			_,
		),
		iIndian: "Dhannavati",
	},
	"Dhar": {
		iEnglish: relocate("Indore"),
		iIndian: (
			relocate("Indore", iAfter=iIndustrial),
			_,
		),
		iPersian: "Mandu",
	},
	"Dharmasraya": {
		iDutch: relocate("Pekanbaru"),
		iMalay: _,
	},
	"Diakaba": {
		iFrench: relocate("Kayes"),
		iMande: _,
	},
	"Diakha": {
		iArabic: "Zagha",
		iFrench: "Dia",
		iMande: _,
	},
	"Dianjiang": {
		iChinese: (
			translate("Hechuan", iAfter=iGlobal),
			_,
		),
	},
	"Diara": {
		iArabic: "Zara",
		iMande: (
			translate("Nioro", iAfter=iIndustrial),
			_,
		),
	},
	"Diego-Suarez": {
		iArabic: "Al-Ilharana",
		iFrench: _,
		iLocal: "Antsiranana", # Malagasy
		iPortuguese: "Ilharana",
		iSpanish: _,
	},
	"Dijon": {
		iCeltic: "Diviodunon",
		iFrench: _,
		iItalian: "Digione",
		iKorean: "Dijong",
		iLatin: "Diviodunum",
	},
	"Dikwa": {
		iEnglish: found("Gombe"),
		iFrench: "Dikoa",
		iLocal: _,
	},
	"Dilbat": {
		iArabic: (
			relocate("An-Najaf", iAfter=iRenaissance),
			relocate("Al-Kufah"),
		),
		iBabylonian: _,
	},
	"Dili": {  # founded on Kupang
		iMalay: _,
		iPortuguese: u"Díli",
	},
	"Dillingham": {
		iEnglish: _,
		iLocal: "Curyung", # Yupik
	},
	"Dilmun": {
		iArabic: relocate("Al-Muharraq"),
		iBabylonian: _,
		iEnglish: relocate("Al-Mename"),
		iPortuguese: relocate("Al-Muharraq"),
	},
	"Dimashq": {
		iArabic: _,
		iBabylonian: u"Imerishú",
		iCeltic: "Damaisc",
		iChinese: "Damashige",
		iDravidian: "Tamasuka",
		iDutch: "Damascus",
		iEgyptian: "Tmsq",
		iFrench: "Damas",
		iGerman: "Damaskus",
		iGreek: "Damaskos",
		iIndian: "Damishk",
		iItalian: "Damasco",
		iJapanese: "Damasukasu",
		iKiswahili: "Dameski",
		iKorean: "Damaseukuseu",
		iLatin: "Damascus",
		iMalay: "Damsyik",
		iNorse: "Damaskus",
		iPersian: "Damishq",
		iPortuguese: "Damasco",
		iRussian: "Damask",
		iSomali: "Dimshek",
		iSpanish: "Damasco",
		iTurkish: "Sham",
	},
	"Dimd": {
		iArabic: (
			relocate("Al-Aghwat", iAfter=iIndustrial),
			"Messaad",
		),
		iFrench: "Messaâd",
		iLatin: "Castellum Dimmidi",
		iPhoenician: _,
	},
	"Dire Dawa": {  # relocated from Harar
		iArabic: "Diri Dawa",
		iEthiopian: _,
		iItalian: "Diredaua",
		iLocal: "Dirree Dhawaa", # Oromo
		iSomali: "Diridhaba",
	},
	"Dirkou": {
		iArabic: _,
		iFrench: found("Madama"),
	},
	"Djedet": {
		iEgyptian: _,
		iGreek: relocate("Dumyat"),
	},
	"Djibouti": {  # founded on Saylac
		iArabic: "Ghibuti",
		iFrench: _,
		iGerman: "Dschibuti",
		iItalian: "Gibuti",
		iSomali: "Jabuuti",
		iSpanish: "Yibuti",
	},
	"Djoboro": {
		iFrench: u"Djenné",
		iMande: _,
		iPortuguese: u"Jené",
	},
	"Dkarmdzes": {
		iChinese: "Ganzi",
		iTibetan: _,
	},
	"Docker River": {
		iEnglish: _,
		iLocal: "Kaltukatjara",
	},
	"Dodoma": {  # relocated from Mpwapwa
		iEnglish: _,
		iGerman: _,
		iKiswahili: "Idodomya",
	},
	"Domboshaba": {
		iEnglish: found("Francistown"),
		iLocal: (
			translate("Luswingo", iAfter=iIndustrial),
			_,
		),
	},
	"Dompo": {
		iMalay: (
			translate("Bima", iAfter=iRenaissance),
			_,
		),
	},
	"Dong'ou": {
		iChinese: (
			translate("Wenzhou", iAfter=iGlobal),
			translate("Yongjia", iAfter=iIndustrial),
			_,
		),
		iEnglish: "Yungkia",
	},
	"Dongolo": {
		iArabic: found("Assab"),
		iEthiopian: (
			translate("Wuqro", iAfter=iIndustrial),
			_,
		),
		iGreek: found("Assab"),
		iItalian: u"Ugorò",
	},
	"Dori": {
		iArabic: "Winde",
		iLocal: _,
	},
	"Doura-Europos": {  # founded on Mari
		iGreek: _,
		iLatin: "Dura-Europos",
	},
	"Dorylaion": {
		iGreek: _,
		iLatin: "Dorylaeum",
		iTurkish: "Eskishehir",
	},
	"Drakchi": {
		iChinese: "Lanzhi",
		iTibetan: (
			translate("Nying Khri", iAfter=iRenaissance),
			_,
		),
	},
	"Dreizehnlinden": {  # founded on Chapecó
		iGerman: _,
		iPortuguese: u"Treze Tílias",
	},
	"Dresden": {
		iChinese: "Deleisidun",
		iDutch: _,
		iFrench: "Dresde",
		iGerman: _,
		iGreek: u"Drésdi",
		iItalian: "Dresda",
		iJapanese: "Doresuden",
		iKorean: "Deureseuden",
		iNorse: _,
		iPolish: "Drezno",
		iPortuguese: "Dresda",
		iRussian: "Drezden",
		iSpanish: "Dresde",
		iTurkish: _,
	},
	"Drohiczyn": {
		iPolish: _,
		iUkrainian: "Dorohochyn",
	},
	"Dryden": {
		iEnglish: _,
		iLocal: "Paawidigong", # Ojibwe
	},
	"Duala": {
		iEnglish: "Cameroons Town",
		iFrench: "Douala",
		iGerman: "Kamerunstadt",
		iLocal: _,
		iPortuguese: u"Rio dos Camarões",
	},
	"Dubasari": {
		iGreek: found("Nikonion"),
		iLocal: _, # Romanian
		iRussian: "Dubossary",
	},
	"Dubrovnik": {
		iEnglish: "Ragusa",
		iFrench: "Raguse",
		iGerman: "Ragusa",
		iGreek: "Ragousa",
		iItalian: "Ragusa",
		iKorean: "Dubeurobeunikeu",
		iLatin: "Rhagusium",
		iLocal: _,
		iPolish: "Dubrownik",
		iRussian: _,
		iTurkish: "Raguza",
	},
	"Duibhlinn": {
		iArabic: "Dablin",
		iCeltic: (
			translate(u"Átha Cliath", iAfter=iIndustrial),
			_,
		),
		iEnglish: "Dublin",
		iGreek: u"Duvlíno",
		iItalian: "Dublino",
		iJapanese: "Daburin",
		iKorea: "Deobeullin",
		iNorse: "Dyflin",
		iPortuguese: "Dublim",
		iSpanish: u"Dublín",
	},
	"Dumyat": {  # relocated from Djedet
		iArabic: _,
		iCoptic: "Tamiati",
		iEnglish: "Damietta",
		iFrench: "Damiette",
		iGreek: "Tamiathis",
		iTurkish: "Dimyat",
	},
	"Dunedin": {  # relocated from Karitane and Pukekura
		iEnglish: _,
		iPolynesian: "Otepoti",
	},
	"Dunhuang": {
		iChinese: _,
		iTurkish: "Dukhan",
	},
	"Dur-Kurigalzu": {
		iArabic: relocate("Baqubah"),
		iBabylonian: _,
		iGreek: relocate("Artemita"),
		iPersian: relocate("Artemita"),
	},
	"Durban": {
		iDutch: found("Pietermaritzburg"),
		iEnglish: _,
		iLocal: "eThekwini", # Zulu
	},
	"Durine": {
		iArabic: relocate("Al-Basrah"),
		iChinese: "Ganluo",
		iGreek: "Antiokheia tes Sousianes",
		iLatin: "Antiochia in Susiana",
		iPersian: (
			translate("Astarabad-Ardashir", iAfter=iMedieval),
			_,
		),
	},
	"Duron": {  # founded on Cherbourg
		iCeltic: _,
		iFrench: "Bayeux",
		iLatin: "Augustodurum",
	},
	"Durovernum": {  # founded on Portsmouth
		iCeltic: "Durouernon",
		iChinese: "Kantebeilei",
		iDutch: "Kantelberg",
		iEnglish: "Canterbury",
		iFrench: u"Cantorbéry",
		iKorean: "Kaenteoberi",
		iLatin: _,
		iNorse: "Kantaraborg",
		iPortuguese: u"Cantuária",
	},
	"Dvaraka": {
		iHarappan: found("Rojdi"),
		iIndian: (
			translate("Dwarka", iAfter=iMedieval),
			_,
		),
		iPortuguese: relocate("Diu"),
	},
	"Dvin": {  # relocated from Artashat
		iArabic: "Dabil",
		iGreek: "Tibion",
		iLocal: _, # Armenian
	},
	"Dvinsk": {
		iFrench: "Dunebourg",
		iGerman: u"Dünaburg",
		iLocal: "Daugavpils", # Estonian
		iPolish: "Dzwinsk",
		iRussian: _,
		iSwedish: "Dynaburg",
	},
	u"Dùn Breatann": {
		iCeltic: _,
		iEnglish: (
			relocate("Glasgow", iAfter=iRenaissance),
			"Dumbarton",
		),
		iNorse: found("Iona"),
	},
	u"Dùn Èideann": {
		iArabic: "Idinburah",
		iCeltic: _,
		iChinese: "Aidingbao",
		iDravidian: "Etinparo",
		iFrench: u"Édimbourg",
		iGerman: "Edinburg",
		iGreek: u"Edimvoúrgo",
		iIndian: "Edinbara",
		iItalian: "Edimburgo",
		iJapanese: "Ejimbara",
		iKorean: "Edeunbeoreo",
		iLatin: (
			found("Trimontium"),
			"Edimburgum",
		),
		iLocal: "Embra", # Scots
		iPolish: "Edynburg",
		iPortuguese: "Edimburgo",
		iRussian: "Edinburg",
		iSpanish: "Edimburgo",
		iThai: "Edinbara",
		iUkrainian: "Edynburh",
	},
	"Dyl": {  # founded on Lidir
		iBabylonian: "Edidal",
		iGreek: "Idalion",
		iLatin: "Idalium",
		iPhoenician: _,
	},
	
	### E ###
	
	"East London": {
		iDutch: "Oos-Londen",
		iEnglish: _,
		iLocal: "eMonti",
	},
	"Eau Claire": {
		iEnglish: _,
		iFrench: found("Fort Bon Secours"),
	},
	"Eburodunum": {  # founded on Grenoble
		iCeltic: _,
		iFrench: "Embrun",
		iGreek: "Ebrodounon",
		iLocal: translate("Ambrun", iAfter=iMedieval), # Occitan
		iLatin: _,
	},
	"Echizen": {
		iJapanese: (
			translate("Fukui", iAfter=iIndustrial),
			_,
		),
	},
	"Edmonton": {
		iEnglish: _,
		iLocal: "Amiskwaciy Waskahikan", # Cree
	},
	"Edo": {
		iChinese: "Jianghu",
		iEnglish: "Yedo",
		iJapanese: (
			rename("Toukyou", iAfter=iIndustrial),
			_,
		),
	},
	"Egedesminde": {
		iLocal: "Aasiaat", # Greenlandic
		iNorse: _,
	},
	"El Picacho": {
		iSpanish: (
			translate(u"Puerto Carreño", iAfter=iGlobal),
			_,
		),
	},
	"El-Obeid": {
		iArabic: "Al-Ubayyid",
		iEgyptianArabic: _,
	},
	"Elath": {
		iArabic: "Al-Aqabah",
		iGreek: (
			translate("Aila", iAfter=iMedieval),
			"Berenike",
		),
		iLatin: "Aela",
		iLocal: _,
		iTurkish: "Aqaba",
	},
	"Elbing": {
		iGerman: _,
		iLocal: "Truso", # Old Prussian
		iNorse: "Ilfing",
		iPolish: "Elblag",
		iRussian: "Elblong",
	},
	"Elfoqhat": {
		iArabic: "Al-Fuqaha",
		iBerber: _,
		iEgyptianArabic: "El-Foqaha",
		iItalian: u"Fógaha",
	},
	"Elimberris": {  # founded on Pau
		iCeltic: _,
		iEnglish: "Auch",
		iLatin: "Augusta Ausciorum",
		iLocal: "Aush", # Gascon
	},
	"Elmina": {  # founded on Oguaa
		iDutch: _,
		iPortuguese: u"São Jorge da Mina",
	},
	"Elusa": {  # founded on Pau
		iCeltic: _,
		iFrench: u"Éauze",
		iLatin: _,
		iLocal: "Euso", # Gascon
	},
	"Emerita Augusta": {  # founded on Batalyaws
		iArabic: "Marida",
		iLatin: _,
		iSpanish: u"Mérida",
	},
	"Enda Meseqel": {
		iEthiopian: (
			translate("Mekelle", iAfter=iIndustrial),
			_,
		),
	},
	"English Bazar": {  # relocated from Lakshmanavati
		iEnglish: _,
		iIndian: "Malda",
		iPersian: "Angrezabad",
	},
	"Ensenada": {
		iLocal: "Pa-tai", # Kumeyaay 
		iSpanish: _,
	},
	"Epako": {
		iDutch: found("Witvlei"),
		iGerman: "Gobabis",
		iLocal: _,
	},
	"Ephesos": {
		iGreek: (
			relocate("Smyrna", iAfter=iMedieval),
			_,
		),
		iHittite: "Apasha",
		iLatin: "Ephesos",
		iTurkish: relocate("Smyrna"),
	},
	"Epidamnos": {
		iFrench: "Duras",
		iGreek: (
			translate("Dyrrhachion", iAfter=iMedieval),
			_,
		),
		iItalian: "Durazzo",
		iLatin: "Dyrrhachium",
		iLocal: u"Durrës",
		iModernGreek: u"Dirráchio",
		iPortuguese: "Durazo",
		iTurkish: u"Diraç",
	},
	"Er-Roseires": {
		iArabic: "Al-Rusayris",
		iEgyptianArabic: _,
	},
	"Erie": {
		iEnglish: _,
		iFrench: found(u"Fort de la Presqu'île"),
	},
	"Eshnunna": {
		iArabic: relocate("Baqubah"),
		iBabylonian: _,
		iGreek: relocate("Artemita"),
		iPersian: relocate("Artemita"),
	},
	"Eskimo Point": {
		iEnglish: _,
		iLocal: "Arviat",
	},
	"Esperance": {
		iDutch: found("'t Landt van de Leeuwin"),
		iEnglish: _,
	},
	"Esutoru": {
		iJapanese: _,
		iRussian: "Uglegorsk",
	},
	"Euesperides": {
		iArabic: "Banghazi",
		iEnglish: "Benghazi",
		iFrench: "Benghazi",
		iGerman: "Bengasi",
		iGreek: (
			translate("Hesperides", iAfter=iMedieval),
			_,
		),
		iItalian: "Bengasi",
		iLatin: "Berenice",
		iSpanish: "Bengasi",
		iTurkish: "Bingazi",
	},
	"Eupatoria": {
		iGreek: _,
		iMongol: (
			found("Simferopol"),
			"Kezlev",
		),
		iRussian: (
			found("Simferopol"),
			translate("Yevpatoriya", iAfter=iIndustrial),
			"Kozlov",
		),
		iPolish: u"Kozlów",
		iTurkish: u"Gözleve",
		iUkrainian: "Yevpatoriia",
	},
	"Evansville": {
		iEnglish: _,
		iFrench: found("Vincennes"),
		iGerman: found("Harmonie"),
	},
	"Eyl": {
		iArabic: "Illig",
		iItalian: "Eil",
		iSomali: _,
	},
	"Ezorongondo": {
		iDutch: "Walvisbaai",
		iEnglish: "Walvis Bay",
		iGerman: (
			found("Swakopmund"),
			"Walfischbucht",
		),
		iLocal: _, # Herero
		iPortuguese: u"Santa Maria da Conceição",
	},
	
	### F ###
	
	"Fachi": {
		iBerber: _,
		iLocal: "Agram", # Kanuri
	},
	"Farab": {
		iArabic: _,
		iPersian: "Parab",
		iTurkish: (
			relocate(u"Türkistan", iAfter=iRenaissance),
			"Otrar",
		),
	},
	"Farah": {
		iArabic: _,
		iGreek: "Alexandreia Prophthasia",
		iPersian: "Phrada",
	},
	"Fashoda": {
		iArabic: _,
		iEnglish: translate("Kodok", iAfter=iIndustrial),
	},
	"Faya": {
		iArabic: _,
		iFrench: "Largeau",
	},
	"Finke": {
		iEnglish: _,
		iLocal: "Apatula",
	},
	"Fizaz": {
		iArabic: "Fas",
		iBerber: _,
		iEnglish: "Fes",
		iFrench: u"Fès",
		iLatin: found("Walilt"),
		iTurkish: "Fes",
	},
	"Flat": {
		iEnglish: _,
		iRussian: "Pokrovskaya",
	},
	"Flaviobriga": {  # founded on Bilbao
		iCeltic: "Portus Amanum",
		iLatin: _,
		iSpanish: "Castro Urdial",
	},
	"Flinders": {
		iDutch: found("Eijland St. Pieter"),
		iEnglish: (
			translate("Streaky Bay", iAfter=iGlobal),
			_,
		),
	},
	"Florentia": {
		iCeltic: u"Flórans",
		iChinese: "Foluolunsi",
		iDutch: u"Florentië",
		iEnglish: "Florence",
		iFrench: "Florence",
		iGerman: "Florenz",
		iGreek: "Florentia",
		iItalian: (
			translate("Firenze", iAfter=iIndustrial),
			"Fiorenza",
		),
		iJapanese: "Firenshe",
		iKorean: "Pirenche",
		iLatin: _,
		iNorse: "Florens",
		iPolish: "Florencja",
		iPortuguese: u"Florença",
		iRussian: "Florentsiya",
		iTurkish: "Floransa",
	},
	"Fort Albany": {
		iEnglish: _,
		iFrench: found("Fort Sainte-Anne"),
	},
	"Fort Arenberg": {
		iFrench: _,
		iLocal: "Badjibo", # Nupe
	},
	"Fort Carillon": {  # founded on Burlington
		iEnglish: "Fort Ticonderoga",
		iFrench: _,
		iLocal: u"Tekontaró:ken", # Iroquois
	},
	"Fort Charles": {
		iEnglish: (
			translate("Waskaganish", iAfter=iGlobal),
			_,
		),
		iFrench: "Fort Saint-Jacques",
		iLocal: u"Wâskâhîkanish", # Cree
	},
	"Fort Chimo": {
		iEnglish: _,
		iLocal: "Kuujjuaq", # Inuktitut
	},
	"Fort Cormantin": {  # founded on Oguaa
		iDutch: "Fort Amsterdam",
		iEnglish: _,
	},
	"Fort de Goede Hoop": {  # founded on Hartford
		iDutch: _,
		iEnglish: "Fort Good Hope",
	},
	"Fort Frances": {
		iEnglish: _,
		iFrench: "Fort Saint-Pierre",
	},
	"Fort Franklin": {
		iEnglish: _,
		iLocal: u"Déline", # North Slavey
	},
	"Fort George": {
		iEnglish: (
			translate("Chisasibi", iAfter=iGlobal),
			_,
		),
		iLocal: u"Cisâsîpî", # Cree
	},
	"Fort Jakob": {  # founded on Ndakaaru
		iEnglish: "Fort James",
		iGerman: _,
	},
	"Fort Liard": {
		iEnglish: _,
		iLocal: "Echaot'l Koe", # Slavey
	},
	"Fort Maurepas": {
		iEnglish: found("Fort Alexander"),
		iFrench: _,
	},
	"Fort McMurray": {
		iEnglish: _,
		iFrench: "Fort la Biche",
	},
	"Fort Nassau": {
		iDutch: (
			translate(_, bSmall=True),
			rename("Nieuw Amsterdam"),
		),
	},
	"Fort Norman": {
		iEnglish: _,
		iLocal: "Tulita", # Slavey
	},
	"Fort Orléans": {
		iEnglish: "Columbia",
		iFrench: found(_),
		iGerman: found("Dutzow"),
	},
	"Fort Ouiatenon": {
		iEnglish: "Lafayette",
		iFrench: _,
		iLocal: "Waayaahtanonki", # Wea
	},
	u"Fort Pentaguët": {
		iFrench: _,
		iLocal: "Majabagaduce", # Abenaki
	},
	"Fort Providence": {
		iEnglish: _,
		iLocal: "Zhahti Koe", # Slavey
	},
	"Fort Rae": {
		iEnglish: _,
		iLocal: (
			translate(u"Behchokò", iAfter=iDigital),
			"Rae-Edzo",
		),
	},
	"Fort Resolution": {
		iEnglish: _,
		iLocal: u"Denı́nu Kúé",
	},
	"Fort Severight": {
		iEnglish: _,
		iFrench: u"Port-Nouveau-Québec",
		iLocal: "Kangiqsualujjuaq", # Inuktitut
	},
	"Fort Simpson": {
		iEnglish: _,
		iLocal: u"Líídlii Kúé", # Slavey
	},
	"Fort Wayne": {
		iEnglish: _,
		iFrench: found("Fort Miami"),
	},
	"Fort William": {
		iEnglish: (
			translate("Thunder Bay", iAfter=iGlobal),
			_,
		),
		iFrench: "Fort Camanistigoyan",
	},
	"Fort Yukon": {
		iEnglish: _,
		iLocal: "Gwichyaa Zheh", # Gwich'in
	},
	"Fort Zeelandia": {
		iDutch: _,
		iEnglish: "Fort Willoughby",
		iFrench: found("Sinnamary"),
		iLocal: "Paramaribo", # Tupi-Guarani
		iPortuguese: found("Torarica"),
	},
	"Fort-Aleksandrovskiy": {
		iRussian: (
			translate("Fort-Shevchenko", iAfter=iGlobal),
			_,
		),
	},
	"Fort-Dauphin": {
		iFrench: _,
		iLocal: "Tolagnaro", # Malagasy
		iPortuguese: found("Matatana"),
	},
	"Fort-Rousset": {  # founded on Monsol
		iFrench: _,
		iLocal: "Owando",
	},
	u"Forte Príncipe da Beira": {
		iPortuguese: (
			translate(_, bSmall=True),
			"Costa Marques",
		),
	},
	u"Forte São Joaquim": {
		iPortuguese: (
			translate(_, bSmall=True),
			"Boa Vista",
		),
	},
	u"Forte São Sebastião": {
		iDutch: "Fort Schoonenborch",
		iPortuguese: (
			translate(_, bSmall=True),
			"Fortaleza",
		),
	},
	u"Fortín López de Filippis": {
		iPortuguese: (
			translate("Mariscal Estigarribia", iAfter=iGlobal),
			_,
		),
	},
	"Frankfurt": {
		iChinese: "Falankefu",
		iDutch: "Frankfort",
		iEnglish: _,
		iFrench: "Francfort",
		iGerman: _,
		iGreek: u"Frankfoúrti",
		iItalian: "Francoforte",
		iJapanese: "Furankufuruto",
		iKorean: "Peurangkeupureuteu",
		iPolish: _,
		iPortuguese: "Francoforte",
		iRussian: _,
		iSpanish: u"Fráncfort",
		iTurkish: _,
	},
	"Fredericton": {
		iEnglish: _,
		iFrench: "Pointe-Sainte-Anne",
	},
	"Frederiksstad": {  # founded on Haithabu
		iDutch: "Frederikstad",
		iGerman: "Friedrichstadt",
		iNorse: _,
	},
	"Frederikstad": {  # founded on Natal
		iDutch: _,
		iPortuguese: u"João Pessoa",
	},
	"Freiburg": {
		iFrench: "Fribourg",
		iGerman: _,
		iItalian: "Friburgo",
		iJapanese: "Furaiburuku",
		iPolish: "Fryburg",
		iPortuguese: "Friburgo",
		iSpanish: "Friburgo",
	},
	"Freising": {
		iFrench: "Frisingue",
		iGerman: (
			relocate(u"München", iAfter=iRenaissance),
			_,
		),
		iItalian: "Frisinga",
		iPolish: "Fryzynga",
		iSpanish: "Fresinga",
	},
	"Frobisher Bay": {
		iEnglish: _,
		iLocal: "Iqaluit", # Inuktitut
	},
	u"Fuerte Boquerón": {
		iPolish: "Filadelfia",
		iRussian: "Filadelfia",
		iSpanish: _,
	},
	u"Fuerte Borbón": {
		iSpanish: (
			rename("Fuerte Olimpo", bRepublican=True),
			_,
		),
	},
	"Fuerte El Petroso": {
		iSpanish: (
			translate(u"Junín", iAfter=iIndustrial),
			_,
		),
	},
	"Fuerte Recabarren": {
		iSpanish: (
			translate(_, bSmall=True),
			"Temuco",
		),
	},
	"Fulu": {
		iChinese: (
			translate("Jiuquan", iAfter=iMedieval),
			_,
		),
	},
	"Fumm Tittawin": {
		iBerber: _,
		iFrench: "Tataouine",
	},
	"Fuping": {
		iArabic: "Yantashwan",
		iChinese: (
			translate("Yinchuan", iAfter=iRenaissance),
			translate("Huaiyuan", iAfter=iMedieval),
			_,
		),
		iJapanese: "Ginkawa",
		iKorean: "Inchwan",
		iMongol: "Iryai",
		iVietnamese: "Ngan Xuyen",
	},
	"Fushun": {
		iChinese: (
			translate("Fuxi", iBefore=iClassical),
			_,
		),
		iFrench: "Fouchouen",
		iKorean: found("Musun"),
		iVietnamese: "Phu Thuan",
	},
	
	### G ###
	
	"Gaalkacyo": {
		iArabic: "Galkayo",
		iEnglish: "Galkayo",
		iEthiopian: relocate("Werder"),
		iFrench: "Gaal Kacyo",
		iItalian: "Gallacaio",
		iPortuguese: "Galcaio",
		iSomali: _,
		iSpanish: "Galcaio",
	},
	"Gaarissa": {
		iEnglish: "Garissa",
		iSomali: _,
	},
	"Gadir": {
		iArabic: "Al-Qadis",
		iCeltic: found("Algeciras"),
		iChinese: "Jiadesi",
		iEnglish: (
			found("Gibraltar"),
			"Cales",
		),
		iFrench: "Cadix",
		iGerman: "Cadiz",
		iGreek: "Gadeira",
		iItalian: u"Càdice",
		iJapanese: "Kadisu",
		iKorean: "Kadiseu",
		iLatin: (
			found("Algeciras"),
			"Gades",
		),
		iPolish: "Kadyks",
		iPortuguese: u"Cádis",
		iRussian: "Kadis",
		iSpanish: u"Cádiz",
		iPhoenician: _,
	},
	"Gaillimh": {
		iCelts: _,
		iEnglish: "Galway",
		iGreek: "Rhaeba",
		iKorean: "Golwei",
		iLatin: "Galvia",
	},
	"Galati": {
		iGerman: "Galatz",
		iGreek: (
			found("Aigissos"),
			u"Galátsi",
		),
		iLatin: found("Aigissos"),
		iLocal: _, # Romanian
		iPolish: "Galacz",
		iRussian: "Galac",
		iTurkish: "Kalas",
		iUkrainian: "Halac",
	},
	"Galena": {
		iEnglish: _,
		iLocal: "Notaale Denh", # Koyukon
	},
	"Gallabat": {  # founded on Gorgora
		iArabic: _,
		iEnglish: "Hor-Cacamoot",
	},
	"Galuuta Nuur": {
		iLocal: _, # Buryat
		iMongol: "Galuutnuur",
		iRussian: (
			translate("Shakhty", bCommunist=True),
			"Gusinoozersk",
		),
	},
	"Gamtila": {
		iArabic: (
			translate("N'Djamena", iAfter=iGlobal),
			"Nighamina",
		),
		iFrench: "Fort-Lamy",
		iLocal: _,
	},
	"Ganda": {  # founded on Kalukembe
		iCongolese: _,
		iPortuguese: "Vila Mariano Machado",
	},
	"Ganja": {  # relocated from Qabala
		iArabic: "Janza",
		iPersian: _,
		iRussian: (
			translate("Kirovabad", bCommunist=True),
			"Yelizatevpol",
		),
		iTurkish: "Gence",
	},
	"Ganyushkino": {
		iMongol: u"Sarai Jük",
		iRussian: _,
		iTurkish: "Qurmanghazy",
	},
	"Ganzhou": {
		iChinese: (
			translate("Zhangye", iAfter=iMedieval),
			_,
		),
	},
	"Gaoyao": {
		iChinese: (
			translate("Zhaoqing", iAfter=iMedieval),
			_,
		),
	},
	"Gaozhou": {
		iChinese: (
			translate("Maoming", iAfter=iMedieval),
			_,
		),
	},
	"Garama": {
		iArabic: relocate("Awbari"),
		iBerber: _,
		iLatin: _,
	},
	"Gardez": {
		iHarappan: found("Rana Ghundai"),
		iPersian: _,
	},
	"Garoowe": {
		iEthiopian: "Garowe",
		iItalian: "Garoe",
		iSomali: _,
	},
	"Garwa": {
		iCongolese: "Garua",
		iFrench: "Garoua",
		iGerman: (
			found("Mora"),
			"Garua",
		),
		iLocal: _, # Hausa
	},
	"Gasegonyane": {
		iDutch: "Die Oog",
		iEnglish: "Kuruman",
		iLocal: _,
	},
	"Gatiga": {
		iLocal: (
			translate("N'Guigmi", iAfter=iIndustrial),
			_,
		),
	},
	"Gawgaw": {
		iEnglish: "Gao",
		iFrench: "Gao",
		iMande: _,
	},
	"Gawulun": {
		iAmerican: relocate("Monrovia"),
		iEnglish: "Cape Mensurado",
		iLocal: _,
		iPortuguese: "Cabo Mensurado",
	},
	"Gaya": {  # renamed from Uruvela
		iIndian: (
			translate("Bodh Gaya", iReligion=iBuddhism, iAfter=iRenaissance),
			translate("Vajrasana", iReligion=iBuddhism, iAfter=iMedieval),
			translate("Sambodhi", iReligion=iBuddhism),
			_,
		),
	},
	"Gazaka": {
		iArabic: "Jazna",
		iBabylonian: found("Izirtu"),
		iGreek: _,
		iLatin: "Gazaca",
		iLocal: "Gandzak", # Armenian
		iPersian: (
			found("Phraaspa"),
			relocate("Tabriz", iAfter=iMedieval),
			"Ganzak",
		),
	},
	"Gazza": {
		iArabic: _,
		iBabylonian: "Hazat",
		iEgyptian: "Gadatw",
		iEnglish: "Gaza",
		iGreek: "Seleukeia",
		iPhoenician: found("Ashkelon"),
		iTurkish: "Gazze",
	},
	u"Gbogré-Djigbi": {
		iEnglish: "Sassandra",
		iFrench: "Sasssandra",
		iLocal: _,
		iPortuguese: u"Santo André",
	},
	"Gdynia": {
		iGerman: (
			translate("Gotenhafen", bFascist=True),
			"Gdingen",
		),
		iPolish: _,
	},
	"Gebal": {
		iArabic: (
			found("Bayrut"),
			relocate("Bayrut", iAfter=iRenaissance),
			"Jubayl",
		),
		iBabylonian: "Gubla",
		iEgyptian: "Kebny",
		iEnglish: "Byblos",
		iGreek: "Byblos",
		iItalian: "Biblo",
		iLatin: "Byblus",
		iPhoenician: _,
		iPortuguese: "Biblos",
		iSpanish: "Biblos",
		iTurkish: (
			found("Bayrut"),
			relocate("Bayrut", iAfter=iRenaissance),
			"Biblos",
		),
	},
	"Gelfa": {
		iArabic: "Al-Jilfa",
		iBerber: _,
		iFrench: "Djelfa",
		iLatin: "Fallaba",
		iTurkish: "Celfa",
	},
	"Geneina": {
		iArabic: "Al-Junaynah",
		iEgyptianArabic: "El Geneina",
		iEnglish: _,
	},
	"Genhe": {
		iChinese: _,
		iMongol: "Gegengol",
	},
	"Genua": {
		iBrazilian: u"Gênova",
		iDutch: _,
		iEnglish: "Genoa",
		iFrench: u"Gênes",
		iGerman: _,
		iGreek: u"Yénova",
		iItalian: "Genova",
		iJapanese: "Jenoba",
		iKorean: "Chenoba",
		iLatin: _,
		iLocal: "Zena", # Ligurian
		iNorse: _,
		iPolish: _,
		iPortuguese: u"Génova",
		iSpanish: u"Génova",
		iTurkish: "Cenova",
	},
	u"Genève": {
		iArabic: "Jinif",
		iCeltic: u"An Ghinéiv",
		iChinese: "Rineiwa",
		iEnglish: "Geneva",
		iFrench: _,
		iGerman: "Genf",
		iGreek: u"Yenévi",
		iItalian: "Ginevra",
		iJapanese: "Juneebu",
		iKorean: "Cheneba",
		iMalay: "Jenewa",
		iPolish: "Genewa",
		iPortuguese: "Genebra",
		iRussian: "Zheneva",
		iSpanish: "Ginebra",
		iSwedish: "Geneve",
		iTurkish: "Cenevre",
	},
	"Gent": {
		iDutch: _,
		iEnglish: (
			translate("Gaunt", iBefore=iMedieval),
			"Ghent",
		),
		iFrench: "Gand",
		iGerman: _,
		iGreek: u"Ghándhi",
		iItalian: "Guanto",
		iKorean: "Genteu",
		iMalay: _,
		iPortuguese: "Gand",
		iRussian: _,
		iSpanish: "Gante",
		iSwedish: _,
	},
	"George Town": {  # relocated from Kedah
		iChinese: "Qiaozhi",
		iDravidian: "Jarj Idavun",
		iEnglish: _,
		iMalay: "Tanjong Penaga",
		iThai: "Chogethao",
	},
	"Georgetown": {
		iDutch: "Stabroek",
		iEnglish: _,
		iFrench: "Longchamps",
	},
	"Ger": {
		iChinese: (
			relocate("Shiquanhe", iAfter=iGlobal),
			"Ga'er",
		),
		iEnglish: "Ngari",
		iTibetan: _,
	},
	"Geraldton": {
		iDutch: found("Houtmans Abrolhos"),
		iEnglish: _,
		iLocal: "Jambinu", # Wajarri
	},
	"Gerasa": {
		iArabic: "Gharash",
		iEnglish: "Jerash",
		iGreek: "Antiokheia Hippos",
		iLatin: _,
		iTurkish: "Jaras",
	},
	"Getembe": {
		iGerman: found("Musoma"),
		iLocal: (
			translate("Kisii", iAfter=iGlobal),
			translate("Bosongo", iAfter=iIndustrial),
			_,
		),
	},
	"Gezzam": {
		iArabic: "In Guezzam",
		iBerber: _,
		iFrench: "In Guezzam",
	},
	"Ghanzi": {
		iDutch: "Kamp",
		iLocal: _,
	},
	"Ghat": {
		iArabic: _,
		iBerber: _,
		iItalian: _,
		iLatin: "Rapsa",
	},
	"Ghazni": {
		iArabic: (
			translate("Ghazna", iBefore=iMedieval),
			_,
		),
		iGreek: "Alexandreia Opiane",
		iPersian: translate("Jaguda", iBefore=iClassical),
	},
	"Gholaia": {
		iArabic: relocate("Al-Biraq"),
		iBerber: _,
		iLatin: _,
	},
	"Ghulja": {
		iChinese: "Yining",
		iTurkish: _,
	},
	"Gibraltar": {  # founded on Gadir
		iArabic: "Jabal Tariq",
		iCeltic: u"Giobráltar",
		iChinese: "Zhibuluotuo",
		iEnglish: _,
		iGreek: u"Ghivraltár",
		iItalian: "Gibilterra",
		iJapanese: "Jiburarutaru",
		iKorean: "Jibeurolteo",
		iPortuguese: _,
		iSpanish: _,
		iTurkish: "Cebelitarik",
	},
	u"Gijón": {  # relocated from Oviedo
		iLocal: u"Xixón", # Asturian
		iSpanish: _,
	},
	"Gilgit": {
		iHarappan: found("Gufkral"),
		iPersian: (
			translate("Sargin", iBefore=iClassical),
			_,
		),
	},
	"Gimhathitha": {
		iArabic: "Qali",
		iDravidian: (
			translate("Kali", iAfter=iRenaissance),
			_,
		),
		iEnglish: "Galle",
		iFrench: "Point de Galle",
		iLocal: ( # Sinhala
			translate("Galla", iAfter=iRenaissance),
			_,
		),
		iPortuguese: "Galle",
	},
	"Giyamusi": {
		iManchu: _,
		iChinese: "Jiamusi",
	},
	"Gjoa Haven": {
		iEnglish: _,
		iLocal: "Uqsuqtuuq", # Inuktitut
	},
	"Glasgow": {  # relocated from Dùn Breatann
		iCeltic: "Glaschu",
		iEnglish: _,
		iGreek: "Glaskove",
		iJapanese: "Gurasugou",
		iKorean: "Geullaeseugo",
		iLocal: "Glesga", # Scots
		iPortuguese: u"Glásgua",
	},
	"Gleden": {
		iRussian: (
			translate("Veliky Ustyug", iAfter=iRenaissance),
			_,
		),
	},
	"Glennallen": {
		iEnglish: _,
		iLocal: "Ciisik'e Na'", # Ahtna
	},
	u"Glexwé": {
		iDutch: "Fida",
		iEnglish: "Whydah",
		iFrench: (
			relocate("Kutonou", iAfter=iIndustrial),
			"Ouidah",
		),
		iGerman: "Hweda",
		iLocal: _,
		iPortuguese: (
			found("Porto-Novo"),
			u"Ajudá",
		),
	},
	"Gode": {  # founded on Baytabaw
		iEthiopian: _,
		iSomali: "Godey",
	},
	"Godhavn": {
		iLocal: "Qeqertarsuaq", # Greenlandic
		iNorse: _,
	},
	"Goeree": {  # founded on Ndakaaru
		iDutch: _,
		iFrench: u"Gorée",
		iPortuguese: "Bezeguiche",
	},
	"Golkonda": {
		iDravidian: _,
		iIndian: _,
		iPersian: "Hyderabad",
	},
	"Golshan": {
		iPersian: (
			translate("Tabas", iAfter=iMedieval),
			_,
		),
	},
	"Gomel": {
		iRussian: _,
		iUkrainian: "Homel",
	},
	"Gondokoro": {
		iEnglish: relocate("Juba"),
		iLocal: _,
	},
	"Gordion": {
		iGreek: _,
		iLatin: "Gordium",
		iLocal: "Gordum",
	},
	"Gorgora": {
		iArabic: found("Gallabat"),
		iEthiopian: (
			relocate("Metemma", iAfter=iIndustrial),
			_,
		),
	},
	"Gorguz": {
		iPersian: _,
		iRussian: relocate("Bakanas"),
		iTurkish: (
			relocate("Bakanas", iAfter=iIndustrial),
			"Karamergen",
		),
	},
	"Gorodets": {
		iRussian: (
			translate("Kasimov", iAfter=iRenaissance),
			_,
		),
	},
	"Goslar": {
		iGerman: (
			relocate("Hannover", iAfter=iRenaissance),
			_,
		),
	},
	u"Göteborg": {  # renamed from Lödöse
		iChinese: "Gedebao",
		iDutch: "Gotenburg",
		iEnglish: "Gothenburg",
		iFrench: "Gothembourg",
		iGerman: "Gotenburg",
		iItalian: "Gotemburgo",
		iJapanese: "Youtebori",
		iKorean: "Yetebori",
		iNorse: u"Gøteborg",
		iPolish: "Gotenburg",
		iPortuguese: "Gotemburgo",
		iSpanish: "Gotemburgo",
		iSwedish: _,
		iTurkish: u"Göteburg",
	},
	"Govapuri": {  # relocated from Chandrapura
		iDravidian: "Gove",
		iIndian: _,
		iLocal: "Goy",
		iPortuguese: (
			relocate("Panaji", iAfter=iIndustrial),
			"Goa",
		),
	},
	"Grahamstown": {
		iEnglish: _,
		iLocal: "Makhanda", # isiXhosa
	},
	"Grand Forks": {
		iEnglish: _,
		iFrench: "Les Grandes Fourches",
	},
	"Grand Rapids": {
		iDutch: found("Zeeland"),
		iEnglish: _,
		iFrench: found("Fort Saint-Joseph"),
		iLocal: "Baawiting", # Odawa
	},
	"Graz": {
		iChinese: "Gelaci",
		iDutch: _,
		iEnglish: _,
		iFrench: "Gratz",
		iGerman: _,
		iGreek: "Grats",
		iItalian: _,
		iJapanese: "Guraatsu",
		iKorean: "Geuracheu",
		iLatin: "Graecium",
		iPersian: "Gerats",
		iPolish: "Grodziec",
		iRussian: "Grats",
		iSwedish: _,
		iTurkish: _,
		iUkrainian: "Hrats",
	},
	"Green Bay": {
		iDutch: found("Hollandstad"),
		iEnglish: _,
		iFrench: "La Baie",
	},
	"Grenoble": {
		iCeltic: (
			found("Eburodunum"),
			"Cularo",
		),
		iEnglish: _,
		iFrench: _,
		iLatin: "Gratianopolis",
		iLocal: translate(u"Graçanòbol", iAfter=iMedieval), # Occitan
		iPortuguese: "Grenobla",
	},
	"Greymouth": {  # relocated from Karamea
		iEnglish: _,
		iPolynesian: "Mawhera",
	},
	"Griekwastad": {
		iDutch: _,
		iEnglish: "Griquatown",
	},
	"Grodno": {
		iGerman: "Garten",
		iLatin: "Grodna",
		iLocal: "Gardinas", # Lithuanian
		iRussian: _,
		iUkrainian: "Hrodna",
	},
	"Groningen": {
		iDutch: _,
		iEnglish: _,
		iFrench: "Groningue",
		iGerman: _,
		iItalian: "Groninga",
		iPortuguese: "Groninga",
		iSpanish: "Groninga",
	},
	"Groznaya": {
		iEnglish: "Grozny",
		iJapanese: "Gurozunui",
		iKorean: "Geurojeuni",
		iLocal: u"Sölza-Gala", # Chechen
		iMongol: relocate("Majar"),
		iPolish: "Grozny",
		iRussian: (
			translate("Groznyy", iAfter=iIndustrial),
			_,
		),
		iTurkish: "Caharkale",
		iUkrainian: "Hroznyy",
	},
	"Gterlenkha": {
		iChinese: "Delingha",
		iMongol: "Delhi",
		iTibetan: _,
	},
	"Guangzhouwan": {
		iChinese: (
			translate("Zhanjiang", iAfter=iGlobal),
			_,
		),
		iFrench: "Fort-Bayard",
	},
	"Guarapuava": {
		iLocal: u"Agûarápuaba",
		iPolish: found("Morska Wola"),
		iPortuguese: _,
	},
	"Gucheng": {
		iChinese: _,
		iTurkish: "Qitai",
	},
	"Guet Ndar": {
		iFrench: u"Saint-Louis-du-Sénégal",
		iLocal: _, # Wolof
	},
	"Guihua": {
		iChinese: (
			rename(u"Höh Hot", bCommunist=True),
			translate("Guisui", iAfter=iGlobal),
			_,
		),
		iJapanese: rename(u"Höh Hot"),
		iMongol: (
			rename(u"Höh Hot", iAfter=iGlobal),
			"Kokegota",
		),
	},
	"Guizhou": {
		iChinese: (
			translate("Guilin", iAfter=iMedieval),
			_,
		),
	},
	"Gulashkird": {
		iGreek: "Alexandreia i en Karmania",
		iPersian: (
			translate("Jiroft", iAfter=iMedieval),
			_,
		),
	},
	"Gulbarga": {  # relocated from Manyakheta
		iEnglish: relocate("Solapur"),
		iIndian: "Kalaburagi",
		iPersian: (
			translate("Hasanabad", iBefore=iRenaissance, iReligion=iIslam),
			_,
		),
	},
	"Gulu": {
		iEnglish: found("Wadelai"),
		iLocal: _,
	},
	"Gure": {
		iFrench: u"Gouré",
		iLocal: _,
	},
	"Gurgan": {
		iPersian: (
			translate("Gorgan", iAfter=iMedieval),
			_,
		),
		iTurkish: "Astarabad",
	},
	"Guryev": {
		iRussian: _,
		iTurkish: "Atyrau",
	},
	"Gustavia": {  # founded on Basse-Terre
		iFrench: u"Le Carénage",
		iSwedish: _,
	},
	"Gvaliyar": {
		iIndian: (
			translate("Gwalior", iAfter=iMedieval),
			_,
		),
		iPersian: "Lashkar",
	},
	"Gwadar": {
		iGreek: relocate("Oraea"),
		iLatin: relocate("Oraea"),
		iPersian: _,
	},
	"Gwadar": {
		iArabic: "Qundar",
		iEnglish: "Gondar",
		iEthiopian: (
			translate(u"Gondär", iAfter=iIndustrial),
			_,
		),
	},
	"Gwandu": {
		iEnglish: "Gando",
		iLocal: _,
	},
	"Gweru": {  # founded on Danangombe
		iEnglish: _,
		iLocal: "iKwelo",
	},
	"Gwosh": {
		iArabic: "Jasad",
		iEnglish: "Jos",
		iLocal: _, # Izere
	},
	"Gyeongseong": {
		iChinese: "Chongjin",
		iJapanese: "Seishin",
		iKorean: (
			translate("Cheongjin", iAfter=iGlobal),
			_,
		),
	},
	u"Gyêgumdo": {
		iChinese: "Jiegu",
		iTibetan: _,
	},
	
	### H ###
	
	"Hacibey": {  # founded on Odesa
		iRussian: "Khadjibey",
		iTurkish: _,
	},
	"Hadrianopolis": {  # renamed from Orestias
		iGreek: "Adrianoupolis",
		iLatin: _,
		iTurkish: "Edirne",
	},
	u"Hagåtña": {
		iEnglish: "Agana",
		iGerman: found("Saipan"),
		iJapanese: (
			found("Saipan"),
			"Akashi",
		),
		iLocal: _,
		iSpanish: u"Agaña",
	},
	"Hailar": {  # founded on Hulunbuir
		iChinese: _,
		iMongol: "Qayilar",
	},
	"Haines": {
		iEnglish: _,
		iLocal: u"Deishú", # Tlingit
		iRussian: found("Slavorossiya"),
		iSpanish: found(u"Puerto Córdova"),
	},
	"Haithabu": {
		iDutch: found("Frederiksstad"),
		iGerman: (
			found("Kiel", iAfter=iRenaissance),
			_,
		),
		iNorse: (
			translate("Heithabyr", iBefore=iMedieval),
			"Hedeby",
		),
	},
	"Hajr": {
		iArabic: (
			rename("Ar-Riyad", iAfter=iRenaissance),
			_,
		),
	},
	"Hakata": {
		iDutch: found("Hirado"),
		iJapanese: (
			translate("Fukuoka", iAfter=iIndustrial),
			_,
		),
		iPortuguese: found("Hirado"),
	},
	"Hakodate": {
		iJapanese: _,
		iLocal: "Hak-Casi", # Ainu
		iRussian: "Khakodate",
	},
	"Halab": {
		iArabic: _,
		iBabylonian: _,
		iChinese: "Alepo",
		iDravidian: "Aleppo",
		iDutch: "Aleppo",
		iEgyptian: "Hereb",
		iEnglish: "Aleppo",
		iFrench: "Alep",
		iGerman: "Aleppo",
		iGreek: "Beroia",
		iHittite: "Halpu",
		iIndian: _,
		iJapanese: "Areppo",
		iKorean: "Allepo",
		iLatin: "Beroea",
		iModernGreek: u"Chelépion",
		iNorse: "Aleppo",
		iPersian: _,
		iPolish: "Aleppo",
		iPortuguese: "Alepo",
		iRussian: "Khaleb",
		iSpanish: "Alepo",
		iTurkish: "Halep",
	},
	"Halifax": {
		iEnglish: _,
		iFrench: found("Port-Royal"),
		iLocal: "Kjipuktuk", # Mi'kmaq
	},
	"Halikarnassos": {
		iGreek: _,
		iHittite: found("Awarna"),
		iLatin: (
			translate("Petronium", iAfter=iMedieval),
			"Halicarnassus",
		),
		iLocal: translate("Alos Karnos", iBefore=iClassical), # Carian
		iTurkish: "Bodrum",
	},
	"Halin": {
		iBurmese: (
			translate("Shwebo", iAfter=iGlobal),
			translate("Konbaung", iAfter=iRenaissance),
			_,
		),
		iThai: "Chawebo",
	},
	"Hall Beach": {
		iEnglish: _,
		iLocal: "Sanirajak", # Inuktitut
	},
	"Hamath": {
		iArabic: "Hama",
		iByzantine: u"Emathoùs",
		iBabylonian: "Amat",
		iGreek: (
			found("Apameia"),
			"Epiphaneia",
		),
		iHittite: "Amatuwana",
		iLatin: (
			found("Apameia"),
			"Hama",
		),
		iLocal: translate(_, iBefore=iClassical), # Aramean
		iPhoenician: found("Sopute"),
	},
	"Hamburg": {
		iArabic: _,
		iChinese: "Hanbao",
		iEnglish: _,
		iFrench: "Hambourg",
		iGerman: _,
		iGreek: u"Amvúrgho",
		iItalian: "Amburgo",
		iJapanese: "Hamburuku",
		iKorean: "Hambureukeu",
		iLatin: (
			translate("Treva", bFound=True),
			"Hammaburgum",
		),
		iNorse: "Hamborg",
		iPolish: _,
		iPortuguese: "Hamburgo",
		iRussian: "Gamburg",
		iSpanish: "Hamburgo",
		iSwedish: _,
		iTurkish: _,
	},
	"Hamju": {
		iJapanese: "Kankou",
		iKorean: (
			translate("Hamheung", iAfter=iMedieval),
			_,
		),
	},
	"Hanga Roa": {
		iPolynesian: _,
		iSpanish: u"Bahía Larga",
	},
	"Hagmatana": {
		iGreek: "Ecbatana",
		iPersian: (
			translate("Hamada", iAfter=iMedieval),
			_,
		),
	},
	"Hancheng": {
		iChinese: (
			translate("Yangzhou", iAfter=iRenaissance),
			translate("Jiangdu", iAfter=iMedieval),
			translate("Guangling", iAfter=iClassical),
			_,
		),
	},
	"Hangzhou": {
		iChinese: (
			translate("Lin'an", bCapital=True),
			_,
		),
		iKorean: "Hangju",
	},
	"Hannover": {  # relocated from Goslar
		iCeltic: u"Hanòbhar",
		iChinese: "Hannuowei",
		iDutch: _,
		iEnglish: "Hanover",
		iFrench: "Hanovre",
		iGerman: _,
		iGreek: u"Anóvero",
		iItalian: _,
		iJapanese: "Hanoubaa",
		iKorean: "Hanobeo",
		iPolish: "Hanower",
		iPortuguese: u"Hanôver",
		iRussian: "Ganover",
		iSpanish: u"Hanóver",
		iSwedish: _,
		iTurkish: _,
	},
	"Hanyang": {
		iChinese: (
			translate("Wuhan", iAfter=iGlobal),
			_,
		),
	},
	"Harar": {
		iArabic: _,
		iEthiopian: (
			relocate("Dire Dawa", iAfter=iGlobal),
			_,
		),
		iItalian: relocate("Dire Dawa"),
		iLocal: "Adare Biyyo", # Oromo
		iSomali: "Herer",
	},
	"Harda": {  # relocated from Mahishmati
		iEnglish: _,
		iIndian: _,
		iPersian: "Hardah",
	},
	"Haresse Lil": {
		iArabic: (
			translate("Bani Abbas", iAfter=iRenaissance),
			_,
		),
		iFrench: u"Béni Abbès",
	},
	"Hargeysa": {  # relocated from Däkkär
		iEnglish: "Hargeisa",
		iSomali: _,
	},
	"Hariharalaya": {
		iLangKhmer: (
			translate("Roluos", iAfter=iIndustrial),
			_,
		),
	},
	"Harmonie": {  # founded on Evansville
		iEnglish: "New Harmony",
		iGerman: _,
	},
	"Harmozeia": {
		iGreek: _,
		iPersian: (
			translate("Minab", iAfter=iMedieval),
			"Armuzia",
		),
	},
	"Harran": {  # founded on Adma
		iArabic: _,
		iBabylonian: "Huzirina",
		iGreek: (
			translate("Hellenopolis", iAfter=iMedieval),
			"Karrhai",
		),
		iLatin: "Carrhae",
		iHittite: "Harranu",
		iPersian: "Karrai",
		iTurkish: _,
	},
	"Hartford": {
		iDutch: found("Fort de Goede Hoop"),
		iEnglish: _,
	},
	"Hastinapura": {
		iHarappan: found("Bargaon"),
		iIndian: (
			translate("Hastinapur", iAfter=iMedieval),
			_,
		),
		iPersian: relocate("Bijnor"),
	},
	"Hatra": {  # renamed from Ash-shur
		iArabic: "Al-Hadr",
		iGreek: "Atra",
		iLatin: "Hatra",
		iPersian: "Hatra",
	},
	"Hatunqulla": {
		iQuechua: _,
		iSpanish: rename("Puno"),
	},
	"Hebet": {
		iArabic: "Al-Harigha",
		iCoptic: "Hib",
		iEgyptian: _,
		iEgyptianArabic: "El-Harigha",
		iEnglish: "Kharga",
		iGreek: "Hibis",
		iLatin: "Oasis Magna",
		iTurkish: "Harga",
	},
	"Hegra": {
		iLocal: _, # Nabataean
		iArabic: (
			relocate("Al-Ula", iAfter=iMedieval),
			"Al-Hijr",
		),
	},
	"Heian-kyou": {
		iChinese: "Jingdu",
		iDravidian: "Kiyotto",
		iDutch: "Kioto",
		iEnglish: "Kyoto",
		iFrench: "Kyoto",
		iGerman: "Kyoto",
		iJapanese: (
			translate("Kyouto", iAfter=iRenaissance),
			_,
		),
		iKorean: "Gyeongdo",
		iPersian: "Kiyoto",
		iPolish: "Kioto",
		iPortuguese: "Quioto",
		iRussian: "Kioto",
		iSpanish: "Kioto",
	},
	"Helike": {  # founded on Mursiyya
		iGreek: _,
		iLatin: "Illice",
		iLocal: "Elx", # Valencian
		iSpanish: "Elche",
	},
	"Helsingfors": {
		iArabic: "Hilsinki",
		iBrazilian: "Helsinque",
		iCeltic: u"Heilsincí",
		iChinese: "He'erxinji",
		iDutch: "Elsenfors",
		iGerman: _,
		iGreek: u"Elsínki",
		iIndian: "Helsinki",
		iJapanese: "Herushinki",
		iKorean: "Helsingki",
		iLatin: "Helsingia",
		iLocal: "Helsinki", # Finnish
		iNorse: _,
		iPortuguese: u"Helsínquia",
		iRussian: (
			translate("Khel'sinki", iAfter=iGlobal),
			"Gel'singfors",
		),
		iSwedish: _,
		iTibetan: "Harshanca",
	},
	"Hemeroskopeion": {  # founded on Alicante
		iArabic: "Daniyya",
		iGreek: _,
		iLatin: "Dianium",
		iLocal: u"Dénia", # Valencian
		iSpanish: "Denia",
	},
	"Henen-Nesut": {
		iArabic: relocate("Al-Minya"),
		iEgyptian: _,
		iGreek: (
			found("Per-Medjed"),
			"Herakleopolis",
		),
		iLatin: (
			found("Per-Medjed"),
			"Heracleopolis Magna",
		),
	},
	"Hengzhou": {
		iChinese: (
			translate("Hengyang", iAfter=iIndustrial),
			_,
		),
	},
	"Herakleia": {
		iByzantine: "Pontoherakleia",
		iGreek: _,
		iItalian: "Pontarachia",
		iLatin: (
			found("Claudiopolis"),
			"Heraclea",
		),
		iTurkish: "Eregli",
	},
	"Heraklion": {  # renamed from Knossos
		iArabic: rename("Chandax"),
		iByzantine: "Megale Kastron",
		iGreek: _,
		iLatin: "Heracleum",
		iModernGreek: "Iraklion",
	},
	"Herat": {  # renamed from Artacoana
		iGreek: "Alexandreia Areion",
		iPersian: (
			translate("Haraiva", iBefore=iClassical),
			_,
		),
	},
	"Hervey Bay": {
		iDutch: found("'t Landt Van Quiri"),
		iEnglish: _,
	},
	"Himologan": {
		iLocal: _,
		iSpanish: u"Cagayán de Oro",
	},
	"Hirmata": {
		iEthiopian: (
			rename("Jimma", iAfter=iIndustrial),
			_,
		),
		iLocal: "Jiren", # Oromo
	},
	"Hirado": {  # founded on Hakata
		iDutch: "Firando",
		iJapanese: _,
		iPortuguese: "Firando",
	},
	"Hiroshima": {
		iChinese: "Guangdao",
		iDravidian: "Irocima",
		iJapanese: _,
		iKorean: "Gwangdo",
		iRussian: "Khirosima",
	},
	"Hisar": {  # renamed from Isukara
		iEnglish: "Hissar",
		iPersian: _,
	},
	"Hoa Lu": {
		iChinese: "Hua Lu",
		iVietnamese: (
			relocate("Thanh Hoa", iAfter=iRenaissance),
			_,
		),
	},
	"Hobarton": {
		iDutch: found("Boreels-eiland"),
		iEnglish: (
			translate("Hobart", iAfter=iIndustrial),
			_,
		),
		iLocal: "Nipaluna",
	},
	"Hobe": {
		iDutch: "Fort Antonio",
		iChinese: (
			rename("Taipei", iAfter=iGlobal),
			"Tamsui",
		),
		iJapanese: rename("Taipei"),
		iLocal: _,
		iPortuguese: "Fort Santo Domingo",
	},
	"Hobyo": {
		iArabic: "Hobyaa",
		iItalian: "Obbia",
		iPortuguese: u"Óbia",
		iSomali: _,
	},
	u"Höh Hot": {  # renamed from Guihua
		iEnglish: "Hohhot",
		iChinese: "Huhehaote",
		iMongol: _,
		iRussian: "Huh-Hoto"
	},
	"Holman": {
		iEnglish: _,
		iLocal: "Ulukhaktok", # Kangiryuarmiutun
	},
	"Holsteinsborg": {
		iLocal: "Sisimiut", # Greenlandic
		iNorse: _,
	},
	u"Hölzel": {  # founded on La Plata
		iGerman: _,
		iSpanish: "Colonia Nievas",
	},
	"Homirzad": {
		iArabic: "Jarun",
		iDutch: "Gameroon",
		iEnglish: "Gombroon",
		iPersian: (
			translate("Bandar-e Abbas", iAfter=iRenaissance),
			translate("Gamerun", iAfter=iMedieval),
			_,
		),
		iPortuguese: u"Comorão",
	},
	"Homs": {  # relocated from Kadesh
		iArabic: _,
		iByzantine: "Khemps",
		iFrench: "La Chamelle",
		iGreek: "Emesa",
		iLatin: "Emesus",
	},
	"Hong Kong": {  # relocated from Nantou
		iChinese: "Xianggang",
		iEnglish: _,
		iRussian: "Sjangan",
	},
	"Hongsawatoi": {
		iBurmese: (
			rename("Bagaw", iAfter=iIndustrial),
			_,
		),
		iEnglish: "Hanthawaddy",
		iIndian: "Hamsavati",
		iPortuguese: relocate("Syriam"),
	},
	"Hooper Bay": {
		iEnglish: _,
		iLocal: "Naparyaarmiut", # Yupiq
	},
	"Houcheng": {
		iChinese: (
			translate("Shengjing", bCapital=True),
			translate("Shenyang", iAfter=iMedieval),
			_,
		),
		iJapanese: "Shinyou",
		iKorean: "Gaemo",
		iManchu: "Mukden",
	},
	"Houston": {
		iEnglish: _,
		iFrench: found("Fort St. Louis"),
	},
	"Huangchuan": {
		iChinese: (
			translate("Xinyang", iAfter=iGlobal),
			_,
		),
	},
	"Huaxyacac": {
		iLocal: "Ndua", # Zapotec
		iNahuatl: _,
		iSpanish: "Oaxaca",
	},
	"Huesca": {
		iCeltic: "Bolskan",
		iGreek: "Ileoskan",
		iLatin: "Osca",
		iLocal: "Uesca", # Aragonese
		iSpanish: _,
	},
	"Huipu": {
		iChinese: (
			translate("Taizhou", iAfter=iMedieval),
			_,
		),
	},
	"Hulagan": {
		iFrench: "Grand-Popo",
		iGerman: found("Lome"),
		iLocal: _,
		iPortuguese: (
			found("Porto Seguro"),
			u"Grande Popô",
		),
	},
	"Hulbuk": {
		iArabic: "Dushanbah",
		iChinese: (
			translate("Shidalinnabade", bCommunist=True),
			"Dushangbie",
		),
		iDutch: "Doesjanbe",
		iDravidian: "Tucanpe",
		iEnglish: (
			translate("Stalinabad", bCommunist=True),
			"Dyushambe",
		),
		iFrench: u"Douchanbé",
		iGerman: "Duschanbe",
		iIndian: "Dusambai",
		iJapanese: "Dushanbe",
		iKorean: "Dusyanbe",
		iModernGreek: "Tosambe",
		iNorse: "Dusjanbe",
		iPersian: _,
		iPortuguese: u"Duchambé",
		iRussian: (
			translate("Stalinabad", bCommunist=True),
			"Dushanbe",
		),
		iSpanish: u"Dusambé",
		iThai: "Duchanbe",
		iTurkish: (
			translate("Stalinobod", bCommunist=True),
			u"Düshenbe",
		),
	},
	"Hulunbuir": {
		iChinese: (
			found("Hailar"),
			"Hulunbu'er",
		),
		iMongol: _,
	},
	"Hvalsey": {
		iLocal: "Qaqortoq",
		iNorse: (
			translate(u"Julianehåb", iAfter=iRenaissance),
			_,
		),
	},
	
	### I ###
	
	"Iader": {  # founded on Pula
		iFrench: "Jadres",
		iGreek: "Idassa",
		iItalian: "Zara",
		iKorean: "Jadareu",
		iLatin: _,
		iLocal: (
			translate("Zadar", iAfter=iMedieval), # Croatian
			_, # Liburnian
		),
		iPolish: "Zadar",
		iPortuguese: "Zara",
	},
	"Iashi": {
		iChinese: "Yaxi",
		iEnglish: "Jassy",
		iFrench: "Iassy",
		iGerman: "Jassenmarkt",
		iGreek: u"Iásio",
		iItalian: "Jassi",
		iKorean: "Iasi",
		iLatin: "Iassium",
		iLocal: _, # Romanian
		iPolish: "Jassy",
		iRussian: "Jassy",
		iTurkish: "Yash",
	},
	"Ibo": {
		iPortuguese: found("Pemba"),
		iKiswahili: _,
	},
	"Ibon": {
		iLocal: _,
		iSpanish: (
			translate("Cabanatuan", iAfter=iIndustrial),
			_,
		),
	},
	"Idaho Falls": {
		iEnglish: _,
		iLocal: "Moson Kahni",
	},
	"Igbo-Ukwu": {
		iEnglish: "Enugu",
		iLocal: (
			translate("Enugwu", iAfter=iIndustrial),
			_,
		),
	},
	"Iguatemi": {
		iPortuguese: (
			relocate(u"Naviraí", iAfter=iGlobal),
			_,
		),
	},
	"Ika": {
		iQuechua: _,
		iSpanish: "Ica",
	},
	u"Ikh Khüree": {
		iCeltic: translate(u"Ulánbátar", bCommunist=True),
		iChinese: (
			translate("Wulanbatuo", bCommunist=True),
			"Da Kulun",
		),
		iDravidian: translate("Ulanpattar", bCommunist=True),
		iEnglish: "Kuren",
		iFrench: (
			translate("Oulan-Bator", bCommunist=True),
			"Ourga",
		),
		iItalian: translate("Ulan Bator", bCommunist=True),
		iJapanese: (
			translate("Uranbaatoru", bCommunist=True),
			"Uruga",
		),
		iKorean: translate("Ullanbatareu", bCommunist=True),
		iMalay: translate("Ulan Bator", bCommunist=True),
		iMongol: (
			translate("Ulaanbaatar", bCommunist=True),
			_,
		),
		iPolish: translate("Ulan Bator", bCommunist=True),
		iPortuguese: translate(u"Ulán Bator", bCommunist=True),
		iRussian: (
			translate("Ulan-Bator", bCommunist=True),
			"Bogdo-Kuren'",
		),
		iSpanish: translate(u"Ulán Bator", bCommunist=True),
		iThai: translate("Ulanbato", bCommunist=True),
		iTurkish: (
			translate("Ulan-Batur", bCommunist=True),
			u"Ürgöö",
		),
	},
	"Iki-Oguz": {
		iRussian: (
			rename("Taldyqorghan", iAfter=iGlobal),
			"Gavrilovka",
		),
		iTurkish: _,
	},
	"Ikonion": {
		iArabic: "Quniya",
		iGreek: _,
		iHittite: "Ikkuwaniya",
		iLatin: "Iconium",
		iTurkish: "Konya",
	},
	"Ilanbaliq": {
		iChinese: "Zhaerkente",
		iTurkish: (
			translate("Jarkent", iAfter=iIndustrial),
			_,
		),
		iRussian: (
			translate("Panfilov", bCommunist=True),
			_,
		),
	},
	u"Ilé-Ifè": {
		iLocal: (
			relocate("Oyo-Ile", iAfter=iRenaissance),
			_,
		),
	},
	"Ilebo": {
		iCongolese: _,
		iDutch: (
			found("Luebo"),
			"Francquihaven",
		),
		iFrance: "Port-Francqui",
	},
	"Iletsk": {
		iRussian: (
			translate("Sol-Iletsk", iAfter=iGlobal),
			_,
		),
	},
	"Ilimsk": {
		iRussian: (
			translate("Ust-Ilimsk", iAfter=iDigital),
			_,
		),
	},
	"Illizi": {
		iBerber: _,
		iFrench: found("Fort-Polignac"),
	},
	"Ilperrelhelame": {
		iEnglish: "Lake Nash",
		iLocal: _, # Aboriginal Alyawarre
	},
	"Imi": {
		iEthiopian: _,
		iSomali: "Iimeey",
	},
	"Imperatorskaya Gavan": {
		iRussian: (
			translate("Sovetskaya Gavan", bCommunist=True),
			_,
		),
	},
	"Impfondo": {
		iCongolese: _,
		iFrench: "Besbordesville",
	},
	"Inbhir Nis": {
		iCeltic: _,
		iChinese: "Yinfuneisi",
		iEnglish: "Inverness",
		iKorean: "Inbeoneseu",
		iNorse: found("Kirkwall"),
	},
	"Inderborskiy": {
		iRussian: _,
		iTurkish: "Inderbor",
	},
	"Indore": {  # relocated from Dhar
		iEnglish: _,
		iIndian: "Indaura",
	},
	"Indraprastha": {
		iHarappan: found("Rakhigarhi"),
		iIndian: _,
		iPersian: rename("Delhi", iReligion=iIslam),
	},
	"Indrapura": {
		iChinese: "Foshicheng",
		iIndian: _,
		iVietnamese: relocate("Cua Han"),
	},
	"Induru": {
		iIndian: (
			translate("Indhrapuri", iAfter=iMedieval),
			_,
		),
		iPersian: "Nizamabad",
	},
	"Inebu-Hedj": {
		iArabic: relocate("Al-Qahirah"),
		iCoptic: "Memfi",
		iEgyptian: (
			translate("Men-nefer", iAfter=iClassical),
			_,
		),
		iEgyptianArabic: relocate("Al-Qahirah"),
		iGreek: "Memphis",
	},
	"Ing'ombe Ilede": {
		iEnglish: relocate("Lusaka"),
		iLocal: (
			relocate("Lusaka", iAfter=iMedieval),
			_,
		),
	},
	"Inkapirka": {
		iLocal: u"Hatun Cañar",
		iQuechua: _,
		iSpanish: "Guayaquil",
	},
	"Inhambane": {
		iArabic: "Iana'ana",
		iKiswahili: _,
		iPortuguese: "Terra de Boa Gente",
	},
	"Inkawasi": {
		iQuechua: _,
		iSpanish: relocate("Pisco"),
	},
	"Inshindi": {
		iLocal: _,
		iPortuguese: "Cazombo",
	},
	"Inukjuak": {
		iEnglish: "Port Harrison",
		iLocal: _, # Inuktitut
	},
	"Invercargill": {  # relocated from Piopiotahi
		iEnglish: _,
		iPolynesian: "Waihopai",
	},
	"Iona": {  # founded on Dùn Breatann
		iCeltic: "Eilean Idhe",
		iEnglish: "Icolmkill",
		iLatin: _,
		iNorse: "Hy",
	},
	"Iritu": {
		iArabic: relocate("Nasiriyah"),
		iBabylonian: _,
		iLocal: "Eridug",
		iPersian: "Amghishiya",
	},
	"Irkutsk": {
		iChinese: "Yierkucike",
		iDravidian: "Irukkuttacukku",
		iFrench: "Irkoutsk",
		iJapanese: "Irukuutsuku",
		iMongol: u"Erhüü",
		iPersian: "Arkotask",
		iPolish: "Irkuck",
		iRussian: _,
	},
	"Isamu Pati": {
		iEnglish: "Livingstone",
		iLocal: (
			translate("Senkobo", iAfter=iMedieval),
			_,
		),
	},
	"Isca": {  # founded on Plymouth
		iCeltic: _,
		iEnglish: "Exeter",
		iLatin: "Isca Dumnoniorum",
		iLocal: "Karesk", # Cornish
	},
	"Ishbiliya": {
		iArabic: _,
		iCeltic: "Sevilla",
		iEnglish: "Seville",
		iFrench: u"Séville",
		iGerman: "Sevilla",
		iItalian: "Siviglia",
		iJapanese: "Sebiriya",
		iKorean: "Sebiya",
		iLatin: "Hispalis",
		iModernGreek: u"Sevílli",
		iNorse: "Sevilla",
		iPhoenician: "Hisbaal",
		iPolish: "Sewilla",
		iPortuguese: "Sevilha",
		iSpanish: "Sevilla",
		iTurkish: "Sevilya",
	},
	"Ishim": {
		iRussian: (
			translate("Korkina Sloboda", iBefore=iRenaissance),
			_,
		),
	},
	"Isiro": {
		iCongolese: _,
		iDutch: "Paulis",
	},
	"Istanbul": {  # renamed from Byzantion
		iArabic: _,
		iCeltic: u"Iostanbúl",
		iChinese: "Yisitanbao",
		iDutch: "Istanboel",
		iEnglish: _,
		iFrench: "Stamboul",
		iGerman: _,
		iItalian: _,
		iJapanese: "Isutamburu",
		iKorean: "Iseutanbul",
		iPolish: "Istambul",
		iPortuguese: "Istambul",
		iRussian: "Stambul",
		iSpanish: "Estambul",
		iTurkish: _,
	},
	"Isukara": {
		iHarappan: found("Banawali"),
		iIndian: _,
		iPersian: rename("Hisar"),
	},
	"Itchyma": {
		iQuechua: _,
		iSpanish: "Lima",
	},
	"Iuliobriga": {  # founded on Orense
		iLatin: _,
		iSpanish: u"Júliobriga",
	},
	"Iwnw": {
		iArabic: relocate("Al-Qahirah"),
		iEgyptian: _,
		iEgyptianArabic: relocate("Al-Qahirah"),
		iCoptic: "On",
		iGreek: "Helioupolis",
		iLatin: "Heliopolis",
	},
	
	### J ###
	
	"Jagdalpur": {
		iEnglish: "Jagdalpore",
		iIndian: _,
	},
	"Jaisana": {
		iHarappan: found("Chapowala"),
		iIndian: (
			translate("Jaisalmer", iAfter=iMedieval),
			_,
		),
		iPersian: "Jaisalmer",
	},
	"Jakobshavn": {
		iLocal: "Ilulissat", # Greenlandic
		iNorse: _,
	},
	"Jalu": {
		iArabic: _,
		iEnglish: "Jallow",
		iItalian: "Gialo",
	},
	"Jamestown, Saint Helena": {
		iDutch: "Sint-Helena",
		iEnglish: "Jamestown",
		iPortuguese: "Santa Helena",
	},
	"Jampur": {
		iHarappan: found("Dabar Kot"),
		iIndian: "Jampura",
		iPersian: _,
	},
	"Janit": {
		iArabic: "Djanet",
		iBerber: _,
		iFrench: found("Fort Charlet"),
	},
	"Jaunde": {  # relocated from Jaunde
		iEnglish: "Yaunde Station",
		iFrench: u"Yaoundé",
		iGerman: _,
		iPortuguese: u"Iaundé",
	},
	"Jayapura": {
		iDutch: "Hollandia",
		iMalay: (
			translate("Sukarnopura", bAutocratic=True),
			_,
		),
	},
	"Jean Marie River": {
		iEnglish: _,
		iLocal: "Tthek'edeli", # Slavey
	},
	"Jelgava": {
		iGerman: "Mitau",
		iLocal: (
			translate("Mintauja", iBefore=iMedieval), # Lithuanian
			_,
		),
		iPolish: "Mitawa",
		iRussian: "Mitava",
	},
	"Jepara": {
		iDutch: relocate("Semarang"),
		iJavanese: (
			relocate("Semarang", iAfter=iRenaissance),
			_,
		),
	},
	"Jhelum": {
		iGreek: "Boukephala",
		iHarappan: found("Sarai Kola"),
		iIndian: "Paurava",
		iPersian: _,
	},
	"Jhunjhunu": {
		iHarappan: found("Karanpura"),
		iPersian: _,
	},
	"Ji'an": {
		iChinese: (
			translate("Tonghua", iAfter=iGlobal),
			_,
		),
		iKorean: "Gungnae",
	},
	"Jiading": {
		iChinese: (
			translate("Leshan", iAfter=iGlobal),
			_,
		),
	},
	"Jiancheng": {
		iChinese: (
			translate("Gao'an", iAfter=iMedieval),
			_,
		),
	},
	"Jiandu": {
		iChinese: (
			translate("Xichang", iAfter=iGlobal),
			_,
		),
	},
	"Jiangzhou": {
		iChinese: (
			translate("Chongqing", iAfter=iMedieval),
			translate("Yuzhong", iAfter=iClassical),
			_,
		),
		iDravidian: "Conkin",
		iDutch: "Chungqing",
		iJapanese: "Juukei",
		iKorean: "Chunggyeong",
		iPersian: "Chungching",
		iVietnamese: "Trung Khanh",
	},
	"Jianyang": {
		iChinese: (
			translate("Nanping", iAfter=iRenaissance),
			_,
		),
	},
	"Jiao'ao": {
		iChinese: (
			translate("Qingdao", iAfter=iIndustrial),
			_,
		),
		iEnglish: "Tsingtao",
		iGerman: "Tsingtau",
		iJapanese: "Chintao",
		iKorean: "Cheongdo",
		iVietnamese: "Thanh Dao",
	},
	"Jicheng": {
		iCeltic: u"Béising",
		iChinese: (
			translate("Beijing", iAfter=iIndustrial),
			translate("Shuntian", iAfter=iRenaissance),
			translate("Beiping", bReconquest=True),
			translate("Yuzhou", iAfter=iMedieval),
			_,
		),
		iDutch: "Peking",
		iDravidian: "Peycinku",
		iEnglish: "Peking",
		iFrench: u"Pékin",
		iGerman: "Peking",
		iGreek: u"Pekíno",
		iIndian: "Bijing",
		iItalian: "Pechino",
		iJapanese: "Pekin",
		iKorean: "Bukgyeong",
		iMongol: (
			translate("Bejzhin", iAfter=iIndustrial),
			"Khanbaliq",
		),
		iNorse: "Peking",
		iPersian: "Biyijang",
		iPolish: "Pekin",
		iPortuguese: "Pequim",
		iRussian: "Pekin",
		iSpanish: u"Pekín",
		iThai: "Pakking",
		iTibetan: "Bejing",
		iTurkish: (
			translate("Pekin", iAfter=iIndustrial),
			"Hanbalik",
		),
		iVietnamese: "Bac Kinh",
	},
	"Jijiga": {  # relocated from Däkkär
		iEthiopian: _,
		iItalian: "Giggiga",
		iSomali: "Jigjiga",
	},
	"Jilin": {
		iChinese: _,
		iKorean: "Seogyeong",
	},
	"Jimma": {  # renamed from Hirmata
		iEthiopian: _,
		iItalian: "Gimma",
		iLocal: "Jimmaa", # Oromo
		iPortuguese: "Jima",
		iSpanish: "Jima",
	},
	"Jincheng": {
		iChinese: (
			translate("Lanzhou", iAfter=iMedieval),
			_,
		),
		iKorean: "Ryangju",
	},
	"Jinyang": {
		iChinese: (
			translate("Taiyuan", iAfter=iMedieval),
			_,
		),
	},
	"Jiuyuan": {
		iChinese: (
			translate("Lucheng", iAfter=iIndustrial),
			_,
		),
		iMongol: translate("Baotou", iAfter=iIndustrial),
	},
	"Jixi": {
		iChinese: _,
		iKorean: "Donggyeong",
	},
	"Jocay": {
		iLocal: _,
		iSpanish: "Manta",
	},
	"Johannesburg": {  # relocated from Kweneng
		iDutch: _,
		iEnglish: _,
		iLocal: "eGoli",
	},
	"Jolo": {
		iArabic: _,
		iChinese: "Ho Lo",
		iLocal: "Tiyanggi", # Tausug
		iSpanish: u"Joló",
	},
	"Jonesboro": {
		iEnglish: _,
		iFrench: found("Poste de Arkansea"),
		iSpanish: found("Poste de Arkansea"),
	},
	u"Jonquière": {
		iFrench: (
			translate("Saguenay", iAfter=iDigital),
			_,
		),
	},
	"Jugu": {
		iFrench: "Djougou",
		iLocal: _,
	},
	"Juiz de Fora": {
		iGerman: found("Neufreiburg"),
		iPortuguese: _,
	},
	"Juketau": {
		iMongol: _,
		iRussian: (
			found("Naberezhnye Chelny"),
			"Zhukotin",
		),
		iTurkish: u"Cükätäw",
	},
	"Julfar": {
		iArabic: (
			translate("Dubai", iAfter=iRenaissance),
			_,
		),
		iFrench: u"Dubaï",
		iPolish: "Dubaj",
		iSpanish: u"Dubái",
	},
	"Juneau": {
		iEnglish: _,
		iLocal: u"Dzánti K'ihéeni",
		iRussian: found("Sitka"),
	},
	"Juzhou": {
		iChinese: (
			translate("Guiyang", iAfter=iRenaissance),
			_,
		),
		iKorean: "Gwiyang",
		iMongol: translate("Shunyuan", iBefore=iRenaissance),
	},
	
	### K ###
	
	"Ka-ba": {
		iMande: (
			translate("Kangaba", iAfter=iRenaissance),
			_,
		),
		iFrench: relocate("Bamako"),
	},
	"Kaapstad": {
		iDutch: _,
		iEnglish: "Cape Town",
		iFrench: "Le Cap",
		iGerman: "Kapstadt",
		iItalian: u"Città del Capo",
		iLocal: "iKapa",
		iPortuguese: "Cidade do Cabo",
		iSpanish: "Ciudad del Cabo",
	},
	"Kabaw": {
		iArabic: _,
		iItalian: "Cabao",
	},
	"Kadapa": {
		iDravidian: _,
		iEnglish: "Cuddapah",
		iPersian: "Neknamabad",
	},
	"Kadesh": {
		iArabic: relocate("Homs"),
		iBabylonian: (
			found("Qatanim"),
			"Kidsha",
		),
		iEgyptian: "Qadeshu",
		iGreek: relocate("Homs"),
		iHittite: _,
	},
	"Kaditshwene": {
		iDutch: "Zeerust",
		iLocal: (
			relocate("Mahikeng", iAfter=iIndustrial),
			_,
		),
	},
	u"Kaédi": {
		iArabic: _,
		iMande: found("Silla"),
	},
	"Kafagway": {
		iChinese: relocate("Vigan"),
		iEnglish: rename("Baguio"),
		iLocal: _, # Ibaloi
		iSpanish: relocate("Vigan"),
	},
	"Kaffa": {  # founded on Khersonesos
		iByzantine: "Theodhosia",
		iChinese: "Xi'aoduoxiya",
		iEnglish: "Caffa",
		iFrench: u"Théodosie",
		iGerman: "Feodossija",
		iGreek: "Kaphas",
		iLatin: "Theodosia",
		iItalian: _,
		iPolish: "Teodozja",
		iRussian: "Feodosiya",
		iTurkish: "Kefe",
	},
	"Kagoshima": {
		iChinese: "Luerdao",
		iJapanese: _,
		iKorean: "Gagosima",
		iRussian: "Kagosima",
	},
	"Kahu-jo-darro": {
		iHarappan: found("Nuhato"),
		iIndian: _,
		iPersian: (
			relocate("Hyderabad", iAfter=iRenaissance),
			"Mirpur Khas",
		),
	},
	"Kahuripan": {
		iDutch: relocate("Surabaya"),
		iJavanese: (
			relocate("Trowulan", iAfter=iMedieval),
			_,
		),
	},
	"Kainsk": {
		iRussian: (
			translate("Kuybyshev", bCommunist=True),
			_,
		),
	},
	"Kaiping": {
		iChinese: _,
		iMongol: rename("Shangdu"),
	},
	"Kajiado": {
		iEnglish: relocate("Nairobi"),
		iLocal: _,
	},
	"Kakhovka": {  # founded on Kryvyi Rih
		iMongol: "Islam Kermen",
		iRussian: _,
	},
	"Kakisa": {
		iEnglish: _,
		iLocal: "K'agee", # Slavey
	},
	"Kakongo": {
		iCongolese: _,
		iPortuguese: "Cacongo",
	},
	"Kalandula": {
		iLocal: _,
		iPortuguese: u"Duque do Bragança",
	},
	"Kalaymyo": {
		iBurmese: (
			translate("Kalay", iAfter=iRenaissance),
			_,
		),
		iEnglish: "Kale",
	},
	"Kalenga": {
		iGerman: "Neu-Iringa",
		iLocal: (
			translate("Iringa", bReconquest=True),
			_,
		),
	},
	"Kalispell": {
		iEnglish: _,
		iLocal: u"Qlispé", # Salish
	},
	"Kalisz": {
		iGerman: "Kalisch",
		iPolish: _,
		iRussian: "Kalish",
	},
	"Kalhu": {
		iArabic: relocate("Karkuk"),
		iBabylonian: _,
		iEnglish: "Nimrod",
		iGreek: relocate("Karkuk"),
		iHittite: found("Karkuk"),
		iPersian: relocate("Newkart"),
	},
	"Kallikkottai": {
		iArabic: "Qaliqut",
		iChinese: "Kulifo",
		iDravidian: _,
		iEnglish: "Calicut",
		iGerman: "Kalikut",
		iIndian: "Koyil-kota",
		iLocal: "Kozhikode",
	},
	"Kalo": {
		iArabic: relocate("Musuru"),
		iFrench: relocate("Musuru"),
		iLocal: _,
	},
	"Kalukembe": {
		iCongolese: _,
		iPortuguese: (
			found("Ganda"),
			"Caluquembe",
		),
	},
	"Kalyani": {
		iIndian: (
			translate("Basavakalyan", iAfter=iGlobal),
			_,
		),
		iPersian: found("Bhir"),
	},
	"Kamen": {
		iRussian: (
			translate("Kamen-na-Obi", iAfter=iGlobal),
			_,
		),
	},
	"Kamensky Zavod": {
		iRussian: (
			translate("Kamensk-Uralsky", iAfter=iGlobal),
			_,
		),
	},
	"Kamianets": {
		iPolish: "Kamieniec",
		iRussian: "Kamenets",
		iTurkish: u"Kamaniçe",
		iUkrainian: _,
	},
	"Kaminaljuyu": {
		iMayan: _,
		iNahuatl: found("Xoconochco"),
		iSpanish: "Ciudad de Guatemala",
	},
	"KaMpfumu": {
		iDutch: (
			found("Bremersdorp"),
			"Fort Lydsaamheid",
		),
		iLocal: (
			translate("Maputo", iAfter=iRenaissance),
			_,
		),
		iPortuguese: u"Lourenço Marques",
	},
	"Kana": {
		iLocal: (
			translate("Abomey", iAfter=iRenaissance),
			_,
		),
	},
	"Kananga": {  # relocated from Nsheng
		iCongolese: _,
		iDutch: "Luluaburg",
		iFrench: "Luluabourg",
	},
	"Kanannay": {
		iLocal: _,
		iSpanish: (
			found("Ovalle"),
			"Canela",
		),
	},
	"Kanatha": {  # founded on Bosra
		iArabic: "Qanawat",
		iGreek: _,
		iLatin: "Canatha",
	},
	"Kanazawa": {
		iChinese: "Jinze",
		iJapanese: _,
		iKorean: "Ganajawa",
	},
	"Kanchipuram": {
		iDravidian: _,
		iEnglish: "Conjeevaram",
		iFrench: relocate("Puducherry"),
		iNorse: relocate("Tharangamba"),
	},
	"Kandahar": {
		iArabic: "Qandahar",
		iGreek: "Alexandria Arachosias",
		iHarappan: found("Mundigak"),
		iPersian: _,
	},
	"Kandarpapura": {
		iChinese: "Shunhua",
		iIndian: _,
		iVietnamese: "Hue",
	},
	"Kandyagash": {
		iRussian: _,
		iTurkish: "Qandyaghash",
	},
	"Kanesh": {  # founded on Mazaka
		iBabylonian: _,
		iHittite: "Nesha",
	},
	"Kangla": {
		iIndian: (
			translate("Imphal", iAfter=iIndustrial),
			_,
		),
	},
	"Kangra": {
		iEnglish: relocate("Shimla"),
		iHarappan: found("Jognakhera"),
		iIndian: _,
		iPersian: relocate("Muzaffarnagar"),
	},
	"Kankabatok": {
		iLocal: _,
		iSpanish: "Tacloban",
	},
	"Kannur": {  # founded on Mangalapuram
		iDravidian: _,
		iEnglish: "Cannanore",
		iGreek: "Naura",
	},
	"Kanpur": {
		iEnglish: "Cawnpore",
		iIndian: _,
	},
	"Kansala": {
		iFrench: "Gabu",
		iLocal: _,
		iPortuguese: (
			found("Bissau"),
			"Nova Lamego",
		),
	},
	"Kansas City": {
		iEnglish: _,
		iFrench: found("Fort de Cavagnial"),
	},
	"Kantipur": {
		iChinese: "Yambu",
		iIndian: (
			translate("Kathmandu", iAfter=iRenaissance),
			_,
		),
		iLocal: "Yen",
	},
	"Kanyakubja": {
		iEnglish: "Cannodge",
		iIndian: (
			translate("Kannauj", iAfter=iMedieval),
			_,
		),
		iPersian: relocate("Lakhnau", iAfter=iRenaissance),
	},
	"Kanyembo": {
		iLocal: (
			translate("Mporokoso", iAfter=iIndustrial),
			_,
		),
	},
	"Kap Dan": {
		iLocal: "Kulusuk",
		iNorse: _,
	},
	"Kapingamarangi": {
		iEnglish: found("Weno"),
		iPolynesian: _,
	},
	"Kapisa": {  # founded on Kubha
		iChinese: "Jiapishi",
		iGreek: "Kapisi",
		iKushan: _,
		iPersian: relocate("Bagram", iReligion=iIslam),
	},
	"Karamea": {
		iEnglish: relocate("Greymouth"),
		iPolynesian: _,
	},
	"Karaulny Mys": {
		iRussian: (
			translate("Pokrovsk", iAfter=iGlobal),
			translate("Pokrovskoye", iAfter=iIndustrial),
			_,
		),
	},
	"Karbala": {  # relocated from Barsip
		iArabic: _,
		iTurkish: "Kerbela",
	},
	"Karitane": {
		iDutch: found("Staten Landt"),
		iEnglish: relocate("Dunedin"),
		iPolynesian: _,
	},
	"Karkuk": {  # relocated and founded on Kalhu
		iArabic: _,
		iBabylonian: "Arrapka",
		iDutch: "Kirkuk",
		iEnglish: "Kirkuk",
		iFrench: "Kirkouk",
		iGerman: "Kirkuk",
		iGreek: "Korkyra",
		iHittite: "Arrapha",
		iLatin: "Corcyra",
		iLocal: u"Kerkûk", # Kurdish
		iPolish: "Kirkuk",
		iPortuguese: "Quircuque",
		iRussian: "Kirkuk",
		iSpanish: "Kirkuk",
		iTurkish: u"Kerkük",
	},
	"Kartili": {  # founded on Al-Asnam
		iArabic: "Damous",
		iFrench: "Dupleix",
		iLatin: "Carcome",
		iPhoenician: _,
	},
	"Karumba": {
		iDutch: found("Van Diemens Baai"),
		iEnglish: _,
	},
	"Karwar": {  # founded on Chandrapura
		iArabic: "Bait-e-Kol",
		iEnglish: "Carwar",
		iIndian: _,
		iLocal: "Kadwad",
	},
	"Kasanje": {
		iCongolese: _,
		iPortuguese: "Cassange",
	},
	"Kashamarka": {
		iQuechua: _,
		iSpanish: "Cajamarca",
	},
	"Kashi": {
		iEnglish: "Benares",
		iFrench: u"Bénarès",
		iIndian: (
			translate("Varanasi", iAfter=iMedieval),
			_,
		),
		iPolish: "Waranasi",
		iPersian: "Banaras",
		iSpanish: u"Benarés",
	},
	"Kashyapapura": {
		iIndian: _,
		iPersian: (
			rename("Multan", iAfter=iMedieval),
			"Kashtpur",
		),
	},
	"Kasimov": {  # relocated from Murom
		iMongol: "Qasim",
		iRussian: _,
	},
	"Kasongo": {
		iCongolese: (
			translate("Kalemie", iAfter=iGlobal),
			_,
		),
		iDutch: "Albertstad",
		iFrench: "Albertville",
	},
	"Kassel": {
		iFrench: "Cassel",
		iGerman: (
			translate("Cassel", iBefore=iIndustrial),
			_,
		),
	},
	"Kasuela": {
		iDutch: "Kasjoe Eiland",
		iEnglish: "Cashew Island",
		iLocal: _,
	},
	"Katende": {
		iCongolese: (
			translate("Kongolo", bReconquest=True),
			_,
		),
	},
	"Katete": {
		iLocal: (
			translate("Luangwa", bReconquest=True),
			_,
		),
		iPortuguese: "Feira",
	},
	"Kath": {
		iPersian: (
			translate("Shobboz", iAfter=iRenaissance),
			_,
		),
		iTurkish: (
			translate("Fil", iAfter=iRenaissance),
			"Kos",
		),
		iRussian: rename("Beruniy", iAfter=iGlobal),
	},
	"Katowice": {
		iGerman: "Kattowitz",
		iPolish: (
			translate(u"Stalinogród", bCommunist=True),
			_,
		),
		iTurkish: u"Katoviçe",
	},
	"Kaunas": {
		iChinese: "Kaonasi",
		iGerman: "Kauen",
		iKorean: "Kaunaseu",
		iLocal: _,
		iPolish: "Kowno",
		iPortuguese: "Caunas",
		iRussian: _,
	},
	"Kaupanger": {
		iNorse: (
			relocate(u"Florø", iAfter=iIndustrial),
			_,
		),
	},
	"Kaushambi": {
		iIndian: (
			translate("Koshambi", iAfter=iMedieval),
			_,
		),
	},
	"Kauthara": {
		iIndian: _,
		iVietnamese: "Nha Trang",
	},
	"Kayes": {  # relocated from Diakaba
		iFrench: _,
		iMande: "Kayi",
		# iSonghai: "Xaayi",
	},
	"Kazan": {
		iArabic: "Qazan",
		iChinese: "Kashan",
		iGerman: "Kasan",
		iJapanese: _,
		iMongol: "Qashan",
		iPolish: _,
		iPortuguese: u"Cazã",
		iRussian: _,
		iTurkish: "Qazan",
	},
	"Kazembe": {  # renamed from Mwansabombwe
		iEnglish: _,
		iPortuguese: "Cazembe",
	},
	"Kazerun": {
		iArabic: "Balad al-Atigh",
		iPersian: _,
	},
	"Kaztalovka": {
		iRussian: _,
		iTurkish: "Kaztal",
	},
	"Ke Van": {
		iVietnamese: (
			translate("Vinh", iAfter=iIndustrial),
			_,
		),
	},
	"Kedah": {
		iArabic: "Qalahbar",
		iChinese: "Jida",
		iDravidian: "Kadaram",
		iEnglish: relocate("George Town"),
		iIndian: "Kataha-Nagara",
		iMalay: (
			relocate("Alor Setar", iAfter=iRenaissance),
			_,
		),
		iThai: "Sai Buri",
	},
	"Kelem": {
		iEthiopian: (
			translate("Omorate", iAfter=iIndustrial),
			_,
		),
		iKiswahili: (
			found("Lodwar", iAfter=iIndustrial),
			found("Namoratunga"),
		),
	},
	"Kem": {
		iLocal: "Kemi", # Finnish
		iRussian: _,
	},
	"Kenai": {
		iEnglish: _,
		iLocal: "Shk'ituk't", # Dena'ina
		iRussian: (
			found("Nikolaevsk"),
			"Kenay",
		),
	},
	"Kenora": {
		iEnglish: (
			translate("Rat Portage", iBefore=iIndustrial),
			_,
		),
		iFrench: (
			found("Fort Saint-Charles"),
			"Portage-aux-Rats",
		),
		iLocal: "Wazhashk-Onigam", # Ojibwe
	},
	"Kerder": {
		iPersian: "Nukas",
		iRussian: "Nukus",
		iTurkish: _,
	},
	"Keren": {  # relocated from Akordat
		iEnglish: _,
		iEthiopian: "Sanhit",
		iItalian: "Cheren",
	},
	u"Kerlingfjördr": {  # founded on Béal Feirste
		iCeltic: "Cairlinn",
		iEnglish: "Carlingford",
		iNorse: _,
	},
	"Kerma": {
		iArabic: (
			relocate("Wadi Halfa", iAfter=iRenaissance),
			"Daw",
		),
		iEgyptian: "Inbw",
		iGreek: "Pnoyps",
		iNubian: _,
	},
	"Kermanshah": {  # relocated from Khalmanu
		iDravidian: "Kermanca",
		iJapanese: "Kerumansha",
		iLocal: "Kirmashan", # Kurdish
		iPersian: (
			translate("Bakhtaran", iBefore=iClassical),
			_,
		),
		iTurkish: "Kirmanshah",
	},
	"Kerri": {
		iArabic: (
			relocate("Al-Khartum Bahri", iAfter=iIndustrial),
			"Qarri",
		),
		iEnglish: relocate("Al-Khartum Bahri"),
		iNubian: _,
	},
	"Kesh": {
		iGreek: "Nautaka",
		iPersian: (
			translate("Shahrisabz", iAfter=iMedieval),
			_,
		),
	},
	"Keta": {
		iLocal: "Quittah",
		iMande: _,
		iNorse: found("Fort Prinsensten"),
	},
	"Kexholm": {
		iLocal: u"Käkisalmi", # Finnish
		iRussian: "Priozersk",
		iSwedish: _,
	},
	"Khabarovsk": {
		iChinese: "Boli",
		iRussian: (
			translate("Khabarovka", iBefore=iRenaissance),
			_,
		),
	},
	"Khalmanu": {
		iArabic: "Hulwa",
		iBabylonian: _,
		iGreek: "Chala",
		iPersian: relocate("Kermanshah"),
	},
	"Khalmer-Sede": {
		iLocal: _,
		iRussian: translate("Tazovsky", iAfter=iGlobal),
	},
	"Khambat": {
		iEnglish: "Cambay",
		iFrench: "Cambay",
		iHarappan: found("Rangpur"),
		iIndian: _,
		iPortuguese: "Cambaia",
	},
	"Khami": {
		iEnglish: relocate("Bulawayo"),
		iLocal: (
			relocate("Bulawayo", iAfter=iIndustrial),
			_,
		),
	},
	"Khanthaburi": {
		iFrench: "Khanthaboury",
		iLocal: ( # Lao
			rename("Savannakhet", iAfter=iGlobal),
			_,
		),
	},
	"Khara-Khoto": {
		iChinese: (
			translate("Heishuicheng", iAfter=iGlobal),
			"Heicheng",
		),
		iMongol: (
			translate("Khar Khot", iAfter=iGlobal),
			_,
		),
	},
	"Kharabali": {
		iMongol: found("Sarai Batu"),
		iRussian: _,
		iTurkish: "Qarabaily",
	},
	"Kharjuravahaka": {
		iIndian: (
			relocate("Mahoba", iAfter=iRenaissance),
			translate("Khajuraho", iAfter=iMedieval),
			_,
		),
	},
	"Kharkiv": {
		iArabic: "Kharkuf",
		iChinese: "Ha'erkefu",
		iDutch: "Charkiv",
		iGerman: "Charkow",
		iGreek: u"Hárkovo",
		iJapanese: "Harukiu",
		iKorean: "Hareukiu",
		iPolish: u"Charków",
		iPortuguese: u"Carcóvia",
		iRussian: "Kharkov",
		iTurkish: "Karkov",
		iUkrainian: _,
	},
	"Khemenu": {
		iArabic: "Al-Ashmunayn",
		iCoptic: "Shmun",
		iEgyptian: _,
		iEgyptianArabic: "El-Ashmunein",
		iGreek: "Hermoupolis Megale",
		iLatin: "Hermopolis Magna",
	},
	"Khersonesos": {
		iArabic: "Khirsun",
		iByzantine: "Cherson",
		iEnglish: "Chersonesus",
		iFrench: u"Chersonèse",
		iGerman: "Chersones",
		iGreek: _,
		iItalian: (
			found("Kaffa"),
			"Chersoneso",
		),
		iLatin: "Chersonesus",
		iPolish: "Chersonez",
		iRussian: (
			found("Sevastopol"),
			"Khersones",
		),
		iSpanish: "Quersoneso",
		iTurkish: (
			found("Kaffa"),
			"Hersonisos",
		),
	},
	"Khlynov": {
		iRussian: (
			translate("Kirov", bCommunist=True),
			translate("Vyatka", iBefore=iMedieval),
			translate("Vyatka", iAfter=iIndustrial),
		),
	},
	"Khotan": {
		iChinese: (
			translate("Hetian", iAfter=iGlobal),
			"Yutian",
		),
		iIndian: "Godana",
		iKushan: _,
		iLocal: "Hvatana", # Khotanese
		iTibetan: "Gosthana",
		iTurkish: "Hotan",
	},
	"Khotchino": {
		iGerman: translate("Lindemannstadt", bFascist=True),
		iRussian: (
			translate("Krasnogvardeysk", bCommunist=True, bAutocratic=True),
			translate("Trotsk", bCommunist=True),
			translate("Gatchina", iAfter=iGlobal),
			_,
		),
	},
	"Khuzdar": {
		iArabic: _,
		iHarappan: found("Togau"),
	},
	"Kiambi": {
		iCongolese: (
			translate("Kirungu", iAfter=iIndustrial),
			_,
		),
		iDutch: "Boudewijnstad",
		iFrench: "Baudoinville",
	},
	"Kiel": {  # founded on Haithabu
		iChinese: "Jier",
		iDutch: _,
		iGerman: _,
		iGreek: "Kielo",
		iPolish: "Kilonia",
		iPortuguese: u"Quília",
		iSpanish: _,
		iTurkish: _,
	},
	"Kilwa": {
		iKiswahili: _,
		iPortuguese: "Quiloa",
	},
	"Kindu": {
		iCongolese: _,
		iFrench: "Port-Empain",
	},
	"King Edward Point": {
		iEnglish: _,
		iSpanish: "Base Corbeta Uruguay",
	},
	"Kingston": {
		iEnglish: _,
		iFrench: "Fort Frontenac",
		iLocal: "Cataraqui",
	},
	"Kinjarling": {
		iEnglish: "Albany",
		iLocal: _, # Aboriginal Nyungar
	},
	"Kinshasa": {  # relocated from M'banza-Nsundi
		iCongolese: _,
		iDutch: "Leopoldstad",
		iFrench: u"Léopoldville",
	},
	"Kirkwall": {  # founded on Inbhir Nis
		iCeltic: "Kirkwaa",
		iEnglish: _,
		iNorse: u"Kirkjuvágr",
	},
	"Kirthan": {
		iPhoenician: _,
		iLatin: (
			rename("Constantina", iReligion=iOrthodoxy),
			"Cirta Iulia",
		),
	},
	"Kisangani": {
		iCongolese: _,
		iDutch: "Stanleystad",
		iFrench: "Stanleyville",
	},
	"Kismaayo": {
		iArabic: "Kismayu",
		iEnglish: (
			found("Buur Gabo"),
			"Kismayo",
		),
		iGerman: (
			found("Buur Gabo"),
			"Kismaju",
		),
		iGreek: found("Buur Gabo"),
		iItalian: "Chisimaio",
		iSomali: _,
	},
	"Kissonde": {
		iCongolese: _,
		iPortuguese: (
			translate("Porto Amboim", iAfter=iGlobal),
			"Benguela Velha",
		),
	},
	"Kisumu": {  # relocated from Mumias
		iEnglish: "Port Florence",
		iKiswahili: _,
	},
	"Kitega": {
		iGerman: found("Usumbura"),
		iLocal: (
			translate("Gitega", iAfter=iGlobal),
			_,
		),
	},
	"Kitu": {
		iQuechua: _,
		iSpanish: "Quito",
	},
	"Klagenfurt": {
		iGerman: _,
		iJapanese: "Kuraagenfuruto",
		iPolish: "Celowiec",
	},
	"Klaipeda": {
		iGerman: "Memel",
		iLocal: _,
		iPolish: "Klajpeda",
		iRussian: _,
	},
	"Kleopatris": {
		iGreek: _,
		iLatin: "Cleopatra",
	},
	"Km'": {
		iArabic: relocate("Tilimsan"),
		iLatin: "Camarata",
		iPhoenician: _,
	},
	"Knossos": {
		iArabic: rename("Chandax"),
		iGreek: (
			rename("Heraklion", iAfter=iClassical),
			_,
		),
		iLatin: "Cnossus",
	},
	"Knyazhpogost": {
		iLocal: "Jemva", # Komi
		iRussian: (
			translate("Yemva", iAfter=iDigital),
			translate("Zheleznodorozhny", iAfter=iGlobal),
			_,
		),
	},
	"Koatzakwalko": {  # founded on Lakamha
		iNahuatl: _,
		iSpanish: "Coatzacoalcos",
	},
	"Koch Behar": {  # relocated from Devikota
		iEnglish: "Cooch Behar",
		iIndian: _,
	},
	"Kochi": {  # relocated from Desinganadu
		iArabic: "Kashi",
		iDravidian: _,
		iDutch: "Cochin",
		iEnglish: "Cochin",
		iPortuguese: "Cochin",
	},
	"Kohat": {
		iHarappan: found("Rehman Dheri"),
		iPersian: _,
	},
	"Kokchetav": {
		iRussian: _,
		iTurkish: u"Kökshetau",
	},
	"Kola": {
		iLocal: u"Guoládat", # Sami
		iRussian: (
			relocate("Murmansk", iAfter=iGlobal),
			_,
		),
		iSwedish: _,
	},
	"Kolberg": {
		iGerman: _,
		iPolish: "Kolobrzeg",
	},
	"Kolchugino": {
		iRussian: (
			translate("Leninsk-Kuznetsky", bCommunist=True),
			_,
		),
	},
	"Koldaa": {
		iArabic: "Kulda",
		iFrench: found(u"Sédhiou"),
		iLocal: _, # Wolof
		iPortuguese: found("Cacheu"),
	},
	"Kolhapur": {
		iIndian: (
			translate("Vijayapura", iAfter=iRenaissance),
			_,
		),
		iPersian: "Bijapur",
	},
	u"Köln": {
		iArabic: "Kuluniya",
		iChinese: "Kelong",
		iDutch: "Keulen",
		iEnglish: "Cologne",
		iFrench: "Cologne",
		iGerman: _,
		iGreek: u"Kolonía",
		iIndian: "Kolon",
		iItalian: "Colonia",
		iJapanese: "Kerun",
		iKorean: "Koelleun",
		iLatin: "Colonia Agrippina",
		iNorse: u"Køln",
		iPolish: "Kolonia",
		iPortuguese: u"Colónia",
		iRussian: "Kyol'n",
		iSpanish: "Colonia",
		iSwedish: _,
		iThai: "Kolon",
		iTurkish: _,
		iUkrainian: "Kel'n",
	},
	"Kolonia": {  # relocated from Nan Madol
		iGerman: _,
		iPolynesian: (
			relocate("Palikir", iAfter=iGlobal),
			"Mesenieng",
		),
		iSpanish: u"Santiago de la Ascensión",
	},
	u"Königsberg": {
		iChinese: "Kenisibao",
		iDutch: "Koningsbergen",
		iGerman: _,
		iGreek: u"Kenixvérghi",
		iJapanese: "Keinihisuberuku",
		iLatin: "Regiomontium",
		iLocal: "Twangste", # Old Prussian
		iPolish: u"Królewiec",
		iPortuguese: "Conisberga",
		iRussian: (
			translate("Kaliningrad", bCommunist=True),
			"Korolevets",
		),
	},
	"Kammama": {
		iBabylonian: _,
		iGreek: (
			found("Sebasteia"),
			"Komana",
		),
		iLatin: (
			found("Sebasteia"),
			"Comana Pontica",
		),
		iHittite: _,
	},
	"Komis": {
		iGreek: "Hekatompylos",
		iPersian: (
			relocate("Damghan", iReligion=iIslam),
			translate("Qumis", iAfter=iMedieval),
			_,
		),
	},
	"Konakiri": {
		iFrench: "Conakry",
		iLocal: _,
		iMande: "Konaakiri",
		iPortuguese: "Concari",
	},
	"Kong": {
		iFrench: relocate("Buna"),
		iLocal: _,
	},
	"Korhogo": {
		iFrench: relocate(u"Odienné"),
		iLocal: _,
	},
	"Korienza": {
		iFrench: u"Korientzé",
		iLocal: _,
	},
	"Korinthos": {
		iDutch: "Korinthe",
		iEnglish: "Corinth",
		iFrench: "Corinthe",
		iGerman: "Korinth",
		iGreek: _,
		iItalian: "Corinto",
		iLatin: "Corinthus",
		iNorse: "Korinth",
		iPolish: "Korynt",
		iPortuguese: "Corinto",
		iRussian: "Korinf",
		iSpanish: "Corinto",
		iTurkish: "Korint",
	},
	"Koror": {
		iJapanese: "Kororu",
		iPolynesian: _,
	},
	"Krtn": {
		iArabic: "Kurti",
		iEgyptian: _,
		iLatin: "Cadetum",
	},
	"Koshice": {
		iFrench: "Cassovie",
		iGerman: "Kaschau",
		iLatin: "Cassovia",
		iLocal: _, # Czech
		iPolish: "Koszyce",
		iRussian: "Koshitse",
		iTurkish: u"Kösice",
		iUkrainian: "Koshytse",
	},
	"Kosti": {  # relocated from Dewaim
		iArabic: "Kusti",
		iEnglish: _,
		iGreek: _,
	},
	"Kotah": {  # relocated from Bundi
		iIndian: "Kota",
		iPersian: _,
	},
	"Kotlik": {
		iEnglish: _,
		iLocal: "Qerrulliik", # Yupik
		iRussian: _,
	},
	"Kotzebue": {
		iEnglish: _,
		iLocal: "Qikiqtagruk", # Inupiaq
	},
	"Kovongo": {
		iCongolese: _,
		iPortuguese: "Lumbala",
	},
	"Kowanyama": {
		iDutch: found("Kaap Keerweer"),
		iEnglish: _,
	},
	u"Kraków": {
		iArabic: "Krakuf",
		iChinese: "Kelakefu",
		iDutch: "Krakau",
		iEnglish: "Cracow",
		iFrench: "Cracovie",
		iGerman: "Krakau",
		iGreek: u"Krakovía",
		iItalian: "Cracovia",
		iJapanese: "Kurakufu",
		iKorean: "Keurakupeu",
		iLatin: "Cracovia",
		iPolish: _,
		iPortuguese: u"Cracóvia",
		iRussian: "Krakov",
		iSpanish: "Cracovia",
		iTurkish: "Krakov",
		iUkrainian: "Krakiv",
	},
	"Krindjabo": {
		iDutch: found("Butre"),
		iEnglish: found("Pokesu"),
		iFrench: found("Bassam"),
		iGerman: found("Pokesu"),
		iLocal: (
			translate("Abidjan", iAfter=iIndustrial),
			_,
		),
		iPortuguese: found("Axim"),
		iSwedish: found("Beyin"),
	},
	u"Krorän": {
		iChinese: "Loulan",
		iIndian: "Krorayina",
		iTurkish: _,
	},
	u"Krébédjé": {
		iFrench: found("Sibut"),
		iLocal: _,
	},
	"Kryvyi Rih": {
		iMongol: found("Kakhovka", iReligion=iIslam),
		iRussian: "Krivoy Rog",
		iUkrainian: _,
	},
	"Kuaiji": {
		iChinese: (
			translate("Shaoxing", iAfter=iMedieval),
			_,
		),
	},
	"Kuala Lumpur": {  # relocated from Melaka
		iChinese: "Jilongpo",
		iDravidian: "Kolalumpur",
		iEnglish: _,
		iJapanese: "Kuararumpuuru",
		iMalay: _,
		iNorse: u"Kúala Lúmpúr",
		iRussian: "Kuala-Lumpur",
	},
	"Kubha": {
		iArabic: "Kabul",
		iChinese: "Kaofu",
		iGreek: "Kophene",
		iHarappan: found("Tarakai Qila"),
		iIndian: _,
		iPersian: (
			translate("Kabul", iAfter=iRenaissance),
			translate("Kapul", iAfter=iMedieval),
			"Vaekereta",
		),
	},
	"Kucha": {
		iChinese: "Qiuci",
		iIndian: "Kucina",
		iMongol: u"Küsän",
		iKushan: _,
		iPersian: "Kusan",
		iTibetan: "Gusan",
		iTurkish: "Kuchar",
	},
	"Kumasi": {
		iEnglish: "Coomassie",
		iLocal: _,
	},
	"Kumayri": {
		iLocal: ( # Armenian
			translate("Gyumri", iAfter=iIndustrial),
			_,
		),
		iRussian: (
			translate("Leninakan", bCommunist=True),
			"Alexandropol",
		),
	},
	"Kumbi Saleh": {
		iArabic: "Ghanah",
		iFrench: "Koumbi Saleh",
		iMande: _,
	},
	"Kumkuduk": {
		iRussian: _,
		iTurkish: "Qumqudyq",
	},
	"Kundapur": {  # relocated from Murdeshwar
		iEnglish: "Coondapore",
		iIndian: _,
	},
	"Kunduz": {
		iArabic: "Qunduz",
		iGreek: "Aornos",
		iIndian: "Drapsaka",
		iLocal: "Varvaliz", # Bactrian
		iPersian: (
			translate("Kuhandiz", iBefore=iMedieval),
			_,
		),
	},
	"Kupang": {
		iDutch: "Koepang",
		iMalay: _,
		iPortuguese: (
			found("Dili"),
			"Coupang",
		),
	},
	"Kuressaare": {
		iGerman: "Arensburg",
		iLocal: _, # Estonian
		iRussian: translate("Kingissepa", bCommunist=True),
		iSwedish: "Arensburg",
	},
	"Kurshaura": {
		iByzantine: "Koloneia",
		iGreek: (
			found("Nyssa"),
			"Archelais",
		),
		iHittite: _,
		iLatin: "Colonia",
		iTurkish: "Aksaray",
	},
	"Kurshim": {
		iRussian: _,
		iTurkish: u"Kürshim",
	},
	"Kurushkatha": {
		iArabic: "Khujand",
		iGreek: (
			rename("Alexandria Eschate", bFound=True),
			"Kyroupolis",
		),
		iLatin: "Kyropolis",
		iPersian: (
			translate("Khodjent", iAfter=iMedieval),
			_,
		),
		iRussian: (
			translate("Leninabad", bCommunist=True),
			"Khodjent",
		),
	},
	"Kushiro": {
		iJapanese: _,
		iRussian: "Kusiro",
	},
	"Kuskatan": {
		iLocal: _, # Pipil
		iNahuatl: "Cuzcatlan",
		iSpanish: (
			found("Tegucigalpa"),
			"San Salvador",
		),
	},
	"Kuta Lingga": {
		iMalay: (
			relocate("Palangka Raya", iAfter=iIndustrial),
			_,
		),
	},
	"Kutai": {
		iDutch: relocate("Samarinda"),
		iMalay: (
			relocate("Samarinda", iAfter=iRenaissance),
			_,
		),
	},
	"Kutaraja": {
		iDutch: "Koetaradja",
		iEnglish: "Kota Radja",
		iMalay: (
			rename("Banda Aceh", iAfter=iGlobal),
			_,
		),
	},
	"Kutonou": {  # relocated from Glexwé
		iFrench: "Cotonou",
		iLocal: _,
	},
	"Kuznetsk": {
		iRussian: (
			translate("Stalinsk", bCommunist=True),
			translate("Novokuznetsk", iAfter=iGlobal),
			_,
		),
		iTurkish: "Aba-tura",
	},
	"KwaMnyamana": {
		iDutch: relocate("Pretoria"),
		iEnglish: relocate("Pretoria"),
		iLocal: _,
		iPortuguese: relocate("Pretoria"),
	},
	"Kweneng": {
		iDutch: relocate("Johannesburg"),
		iEnglish: relocate("Johannesburg"),
		iLocal: _,
	},
	"Kwito Kwanavale": {
		iCongolese: _,
		iPortuguese: "Cuito Cuanavale",
	},
	"Kyakhta": {  # relocated from Maimaicheng
		iMongol: "Hiagt",
		iRussian: _,
		iTurkish: "Khiaagta",
	},
	"Kyaingtong": {
		iBurmese: _,
		iChinese: "Jingdong",
		iEnglish: "Kengtung",
		iThai: (
			found("Chiang Rai"),
			"Chiang Tung",
		),
	},
	"Kyakyaru": {
		iChinese: "Saga",
		iTibetan: _,
	},
	"Kydonia": {
		iArabic: rename("Chania"),
		iByzantine: rename("Chania"),
		iGreek: _,
		iLatin: "Cydonia",
		iTurkish: rename("Chania"),
	},
	"Kyiv": {
		iArabic: "Kiyif",
		iCeltic: u"Cív",
		iChinese: "Jifu",
		iDutch: u"Kiëv",
		iGerman: "Kiew",
		iGreek: u"Kíevo",
		iItalian: "Kiev",
		iJapanese: "Kiiu",
		iKorean: "Kiyepeu",
		iLatin: "Kiovia",
		iNorse: u"Kænugarður",
		iPolish: u"Kijów",
		iPortuguese: "Quieve",
		iRussian: "Kiyev",
		iSpanish: "Kiev",
		iSwedish: "Kiev",
		iTurkish: "Kiev",
		iUkrainian: _,
	},
	"Kyrene": {
		iArabic: "Shihat",
		iFrench: u"Cyrène",
		iGreek: _,
		iItalian: "Cirene",
		iLatin: "Cyrene",
		iPortuguese: "Cirene",
		iRussian: "Kirena",
		iSpanish: "Cirene",
		iTurkish: "Kirene",
	},
	"Kyrrhus": {
		iArabic: (
			relocate("Antep"),
			"Kurus",
		),
		iByzantine: "Hagioupolis",
		iGreek: _,
		iHittite: relocate("Antep"),
		iLatin: "Coricium",
		iTurkish: relocate("Antep"),
	},
	
	### L ###
	
	"L'Aquila": {  # relocated from Corfinium
		iGreek: "L'Akouila",
		iItalian: _,
		iLatin: "Aquila",
		iPortuguese: u"Áquila",
		iRussian: "Akvila",
	},
	u"L'Établissement": {
		iEnglish: "Victoria",
		iFrench: _,
	},
	u"La Coruña": {
		iCeltic: "Brigantia",
		iEnglish: "Corunna",
		iFrench: "La Corogne",
		iJapanese: "Rakoruunya",
		iLatin: "Brigantium",
		iLocal: u"A Coruña", # Galician
		iPortuguese: "Corunha",
		iSpanish: _,
	},
	"La Habana": {
		iEnglish: "Havana",
		iFrench: "La Havane",
		iGerman: "Havanna",
		iGreek: u"Abána",
		iItalian: "L'Avana",
		iNorse: "Havana",
		iPortuguese: "Havana",
		iRussian: "Gavana",
		iSpanish: _,
		iTurkish: "Havana",
	},
	u"La Nouvelle-Orléans": {
		iEnglish: "New Orleans",
		iFrench: _,
		iLocal: "Bulbancha", # Choctaw
		iPortuguese: u"Nova Orleães",
		iSpanish: "Nueva Orleans",
	},
	"La Paz": {
		iLocal: "Chuqiyapu", # Aymara
		iSpanish: _,
	},
	"La Plata": {
		iGerman: found(u"Hölzel"),
		iSpanish: _,
	},
	"Lac Giao": {
		iVietnamese: (
			translate("Buon Ma Thuot", iAfter=iGlobal),
			_,
		),
	},
	"Lac La Martre": {
		iFrench: _,
		iLocal: u"Whatì",
	},
	"Ladoga": {
		iNorse: "Aldeigjuborg",
		iRussian: (
			translate("Staraya Ladoga", iAfter=iRenaissance),
			_,
		),
	},
	"Lafayette": {
		iEnglish: _,
		iFrench: "Vermillionville",
		iSpanish: found("Nueva Iberia"),
	},
	"Lagash": {
		iBabylonian: _,
		iGreek: (
			translate("Alexandria Susiana", bFound=True),
			"Charax Spasinu",
		),
	},
	"Lakamha": {
		iMayan: _,
		iNahuatl: found("Koatzakwalko"),
		iSpanish: (
			found("Villahermosa"),
			"Palenque",
		),
	},
	"Lake Harbour": {
		iEnglish: _,
		iLocal: "Kimmirut",
	},
	"Lakhnau": {  # relocated from Kanyakubja
		iChinese: "Lekenao",
		iDravidian: "Ilakno",
		iEnglish: "Lucknow",
		iIndian: (
			translate("Lakhnauti", iAfter=iMedieval),
			"Lakshmanavati",
		),
		iPersian: _,
		iRussian: _,
	},
	"Lakshmanavati": {
		iEnglish: relocate("English Bazar"),
		iIndian: (
			translate("Gauda", iAfter=iMedieval),
			_,
		),
		iPersian: (
			relocate("Rajshahi", iAfter=iIndustrial),
			translate("Jannatabad", iAfter=iRenaissance),
			"Gaur",
		),
	},
	"Lam'an'ain": {
		iEnglish: found("Belize City"),
		iMayan: _,
		iSpanish: "Lamanai",
	},
	"Lamdia": {  # founded on Zdif
		iArabic: "Al-Madiya",
		iFrench: u"Médéa",
		iBerber: "Lemdiyyet",
	},
	"Lamu": {
		iArabic: "Al-Amu",
		iGerman: found("Witu"),
		iKiswahili: _,
		iPortuguese: "Lamon",
	},
	"Langzhong": {
		iChinese: (
			translate("Baoning", iAfter=iMedieval, iBefore=iIndustrial),
			_,
		),
	},
	"Laodikeia": {  # renamed from Nahavand
		iArabic: "Ladhiqiyya",
		iGreek: _,
		iLatin: "Laodicea",
	},
	"Las Grutas": {
		iCeltic: found("Porth Madryn"),
		iSpanish: _,
	},
	"Launceston": {
		iDutch: found("Kaap Hendrick"),
		iEnglish: _,
	},
	"Lauriacum": {  # founded on Linz
		iGerman: "Enns",
		iLatin: _,
	},
	"Lautoka": {
		iEnglish: relocate("Suva"),
		iPolynesian: _,
	},
	"Lavapura": {
		iIndian: _,
		iKhmer: "Lavo",
		iThai: "Lop Buri",
	},
	"Lavapuri": {
		iCeltic: "Lahore",
		iChinese: "Lahe'er",
		iDutch: "Lahore",
		iEnglish: "Lahore",
		iFrench: "Lahore",
		iGerman: "Lahore",
		iGreek: "Lakhores",
		iHarappan: found("Harappa"),
		iIndian: (
			translate("Laahaur", iAfter=iGlobal),
			_,
		),
		iItalian: "Lahore",
		iJapanese: "Rahouru",
		iKorean: "Raholleu",
		iNorse: "Lahore",
		iPersian: "Laahor",
		iPortuguese: "Laore",
		iRussian: "Lakhor",
		iSpanish: "Lahore",
		iThai: "Lahxr",
		iTurkish: "Lahor",
	},
	"Lbayed": {
		iArabic: "Al-Bayadh",
		iBerber: _,
		iFrench: u"Géryville",
	},
	"Le Mans": {
		iCeltic: "Vindinion",
		iFrench: _,
		iLatin: "Suindinum",
	},
	"Legnica": {
		iDutch: "Liegnitz",
		iGerman: "Liegnitz",
		iLatin: "Lignitium",
		iPolish: _,
	},
	"Leilou": {
		iChinese: _,
		iVietnamese: (
			rename("Thuan Thanh", iAfter=iRenaissance),
			"Luy Lau",
		),
	},
	"Leipzig": {
		iChinese: "Laibixi",
		iEnglish: "Leipsic",
		iFrench: "Leipsick",
		iGerman: _,
		iGreek: u"Lipsía",
		iItalian: "Lipsia",
		iJapanese: "Raiputshihi",
		iKorean: "Raipeuchihi",
		iLatin: "Lipsia",
		iPolish: "Lipsk",
		iPortuguese: u"Lípsia",
		iSpanish: "Lipsia",
	},
	"Leiyang": {
		iChinese: (
			relocate("Chenzhou", iAfter=iGlobal),
			_,
		),
	},
	"Leningrad": {  # renamed from Sankt-Peterburg
		iChinese: "Lieninggele",
		iEnglish: _,
		iGerman: _,
		iJapanese: "Reninguraado",
		iKorean: "Reningeuradeu",
		iPortuguese: "Leningrado",
		iRussian: _,
		iSpanish: "Leningrado",
		iSwedish: _,
	},
	"Lethem": {
		iEnglish: _,
		iPortuguese: found("Bonfim"),
	},
	"Leticia": {
		iPortuguese: u"Letícia",
		iSpanish: _,
	},
	u"León": {
		iArabic: "Liyyun",
		iLatin: (
			found("Astorga"),
			"Castra Legionis",
		),
		iLocal: u"Llión", # Leonese
		iPortuguese: u"Leão",
		iSpanish: _,
	},
	u"Les Opélousas": {  # founded on Monroe
		iFrench: _,
		iSpanish: u"Los Opeluzás",
	},
	"Liangzhou": {
		iChinese: (
			translate("Wuwei", iAfter=iRenaissance),
			_,
		),
	},
	"Libreville": {  # founded on Mang
		iEnglish: "Baraka",
		iFrench: _,
	},
	"Lichinga": {
		iKiswahili: _,
		iPortuguese: "Vila Cabral",
	},
	"Lickan": {
		iLocal: _,
		iSpanish: "San Pedro de Atacama",
	},
	"Lidir": {
		iArabic: "Nikusiya",
		iBabylonian: _,
		iByzantine: "Leukousia",
		iFrench: relocate("Limassol"),
		iGreek: (
			translate("Leukotheon", iReligion=iOrthodoxy),
			"Ledra",
		),
		iLatin: (
			translate("Nicosia", iAfter=iMedieval),
			"Leucopolis",
		),
		iModernGreek: "Lefkosia",
		iPhoenician: found("Dyl"),
		iTurkish: "Lefkosha",
	},
	"Liepaja": {
		iChinese: "Liyapaya",
		iGerman: "Libau",
		iJapanese: "Riepaaya",
		iLocal: _, # Latvian
		iPolish: "Lipawa",
		iRussian: "Libava",
	},
	"Lihu'e": {
		iPolynesian: _,
		iRussian: found("Pa'ula'ula o Hipo"),
	},
	"Likasi": {  # relocated from Bunkeya
		iDutch: "Jadotstad",
		iFrench: "Jadotville",
		iCongolese: "Likasi",
	},
	"Lilybaeum": {  # founded on Panormus
		iArabic: "Marsallah",
		iGreek: "Lilybaion",
		iItalian: "Marsala",
		iLatin: _,
		iPhoenician: "Libuye",
	},
	"Limassol": {  # relocated from Lidir
		iByzantine: "Theodosiana",
		iEnglish: _,
		iFrench: _,
		iGerman: "Limasol",
		iGreek: "Nemesos",
		iModernGreek: "Lemesos",
		iSpanish: "Limasol",
		iTurkish: "Leymosun",
	},
	"Limoges": {
		iCeltic: "Lemovices",
		iChinese: "Liemori",
		iFrench: _,
		iLatin: "Augustoritum",
		iLocal: u"Limòtges",
	},
	"Lindon": {
		iCeltic: _,
		iEnglish: "Lincoln",
		iLatin: "Lindum",
		iNorse: found("Torksey"),
	},
	"Lingeer": {
		iFrench: u"Linguère",
		iMande: _,
	},
	"Lingling": {
		iChinese: (
			translate("Yongzhou", iAfter=iRenaissance),
			_,
		),
	},
	"Lingzhou": {
		iChinese: (
			translate("Lingwu", iAfter=iIndustrial),
			_,
		),
	},
	"Linjiang": {
		iChinese: (
			translate("Zhongxian", iAfter=iGlobal),
			translate("Zhongzhou", iAfter=iMedieval),
			_,
		),
	},
	"Linqiang": {
		iChinese: (
			translate("Xining", iAfter=iMedieval),
			_,
		),
		iTibetan: "Qingtang cheng",
	},
	"Linxiang": {
		iChinese: (
			translate("Changsha", iAfter=iMedieval),
			_,
		),
		iJapanese: "Nagasa",
		iKorean: "Jangsa",
	},
	"Linz": {
		iChinese: "Linci",
		iGerman: _,
		iKorean: "Rincheu",
		iLatin: (
			found("Lauriacum"),
			"Lentia",
		),
		iPortuguese: u"Líncia",
	},
	"Linzi": {
		iChinese: (
			translate("Zibo", iAfter=iMedieval),
			_,
		),
	},
	"Lisboa": {
		iArabic: "Al-Ishbuna",
		iCeltic: (
			translate(u"Liospóin", iAfter=iMedieval),
			"Olisippo",
		),
		iChinese: "Lisiben",
		iDutch: "Lissabon",
		iEnglish: "Lisbon",
		iFrench: "Lisbonne",
		iGerman: "Lissabon",
		iGreek: "Olissipon",
		iItalian: "Lisbona",
		iJapanese: "Risubon",
		iKorean: "Riseubon",
		iLatin: "Felicitas Iulia",
		iModernGreek: u"Lissavóna",
		iNorse: "Lissabon",
		iPersian: "Lasibun",
		iPhoenician: "Alis-Ubbo",
		iPolish: "Lizbona",
		iPortuguese: _,
		iRussian: "Lissabon",
		iSpanish: _,
		iTurkish: "Lizbon",
	},
	"Liucheng": {
		iChinese: (
			translate("Chaoyang", iAfter=iRenaissance),
			_,
		),
	},
	"Livingstonia": {  # founded on Mzimba
		iEnglish: _,
		iLocal: "Kondowe",
	},
	"Liweizhou": {
		iChinese: (
			translate("Dazhou", iAfter=iRenaissance),
			translate("Tongzhou", iAfter=iMedieval),
			_,
		),
	},
	"Lixia": {
		iChinese: (
			translate("Jinan", iAfter=iClassical),
			_,
		),
	},
	"Ljubljana": {
		iArabic: "Liyubliyana",
		iCeltic: u"Liúibleána",
		iChinese: "Lubu'eryana",
		iGerman: "Laibach",
		iGreek: "Emona",
		iIndian: "Liubliyana",
		iItalian: (
			found("Trieste"),
			"Lubiana",
		),
		iJapanese: "Ryuburyana",
		iKorean: "Ryubeullyana",
		iLatin: "Emona",
		iLocal: _, # Slovene
		iModernGreek: u"Lioubliána",
		iPolish: "Lublana",
		iPortuguese: "Liubliana",
		iRussian: "Liubliana",
		iSpanish: "Liubliana",
		iTurkish: "Lubliyana",
	},
	"Lleida": {
		iCeltic: "Iltrida",
		iLatin: "Ilerda",
		iLocal: _, # Catalan
		iSpanish: u"Lérida",
	},
	"Loango": {  # renamed from Bwali
		iCongolese: "M'banza-Loango",
		iFrench: "Loango",
		iPortuguese: "Loango",
	},
	"Loch Garman": {
		iCeltic: _,
		iEnglish: "Wexford",
		iGreek: "Manapia",
		iNorse: u"Veisafjorðr",
	},
	u"Lödöse": {
		iSwedish: (
			rename(u"Göteborg", iAfter=iRenaissance),
			_,
		),
	},
	u"Logroño": {
		iCeltic: "Uarakos",
		iFrench: "Logrogne",
		iItalian: "Logrogno",
		iLatin: (
			found("Calagurris"),
			"Vareia",
		),
		iPortuguese: "Logronho",
		iSpanish: _,
	},
	"Lombadina": {
		iEnglish: _,
		iMalay: "Kayu Jawa",
	},
	"Lome": {  # founded on Hulagan
		iFrench: u"Lomé",
		iGerman: _,
		iLocal: u"Alotimé",
	},
	"London": {
		iArabic: "Landan",
		iCeltic: "Llundain",
		iChinese: "Lundun",
		iDutch: "Londen",
		iEnglish: _,
		iFrench: "Londres",
		iGerman: _,
		iGreek: u"Londhíno",
		iItalian: "Londra",
		iJapanese: "Rondon",
		iKorean: "Reondeon",
		iLatin: "Londinium",
		iNorse: u"Lundúnir",
		iPolish: "Londyn",
		iPortuguese: "Londres",
		iSpanish: "Londres",
		iTurkish: "Londra",
		iVietnamese: "Luan Don",
	},
	"Los Angeles": {
		iArabic: "Lus Anjilus",
		iChinese: "Luoshanji",
		iEnglish: _,
		iJapanese: "Rosanzerusu",
		iKorean: "Loseuaenjelleseu",
		iLocal: "Yaanga", # Tongva
		iRussian: "Los-Andzheles",
		iSpanish: u"Los Ángeles",
	},
	"Louisbourg": {
		iFrench: _,
		iPolynesian: "Maroantsetra",
	},
	"Lovozero": {
		iLocal: u"Luujärvi",
		iRussian: _,
	},
	"Lpqy": {
		iArabic: (
			found("Misratah"),
			"Labdah",
		),
		iBerber: found("Misratah"),
		iGreek: "Leptis Megale",
		iItalian: "Lepti Maggiore",
		iLatin: (
			translate("Ulpia Traiana", bFound=True),
			"Leptis Magna",
		),
		iPhoenician: _,
	},
	"Luang Prabang": {
		iFrench: "Louangphrabang",
		iLangKhmer: "Luangphabang",
		iLocal: _, # Lao
		iVietnamese: "Xieng Thong",
	},
	"Lubango": {
		iCongolese: (
			translate("Kaluvango", bFound=True),
			_,
		),
		iPortuguese: u"Sá da Bandeira",
	},
	u"Lübeck": {
		iChinese: "Lubeike",
		iGerman: _,
		iGreek: u"Lubéke",
		iItalian: "Lubecca",
		iKorean: "Rwibekeu",
		iNorse: u"Lybæk",
		iPolish: "Lubeka",
		iPortuguese: "Lubeque",
	},
	"Lubumbashi": {  # founded on Mwansabombwe
		iCongolese: _,
		iDutch: "Elisabethstad",
		iFrench: u"Élisabethville",
	},
	"Lucus Asturum": {  # founded on Oviedo
		iLatin: _,
		iSpanish: "Llanero",
	},
	"Luebo": {  # founded on Ilebo
		iCongolese: "Lwebo",
		iDutch: _,
		iFrench: _,
	},
	"Lugo": {
		iCeltic: _,
		iLatin: "Lucus Augusti",
		iSpanish: _,
	},
	"Luguvalium": {
		iCeltic: (
			translate("Caerliwelydd", iAfter=iMedieval),
			"Luguwalion",
		),
		iEnglish: (
			found("Lancaster"),
			"Carlisle",
		),
		iLatin: _,
	},
	"Luhansk": {
		iRussian: (
			translate("Voroshilovgrad", bCommunist=True),
			"Lugansk",
		),
		iUkrainian: (
			translate("Voroshylovhrad", bCommunist=True),
			_,
		),
	},
	"Luhonono": {
		iGerman: "Schuckmannsburg",
		iLocal: _,
	},
	"Luimneach": {
		iCeltic: _,
		iChinese: "Limolike",
		iEnglish: "Limerick",
		iLatin: "Macolicum",
		iNorse: "Hlymrekr",
	},
	"Lujenda": {
		iKiswahili: _,
		iPortuguese: "Montepuez",
	},
	"Luki": {
		iFrench: "Louki",
		iRussian: (
			rename("Velikiye Luki", iAfter=iRenaissance),
			_,
		),
	},
	"Lulami": {
		iArabic: relocate("Saayi"),
		iFrench: relocate("Saayi"),
		iMande: _,
	},
	"Luling": {
		iChinese: (
			translate("Ji'an", iAfter=iMedieval),
			_,
		),
	},
	"Lund": {
		iChinese: "Longde",
		iFrench: _,
		iGerman: _,
		iLatin: "Lunda",
		iNorse: (
			found(u"Malmö"),
			_,
		),
		iSwedish: _,
	},
	u"Lüneburg": {
		iChinese: "Luneibao",
		iDutch: "Lunenburg",
		iEnglish: "Lunenburg",
		iFrench: "Lunebourg",
		iGerman: _,
		iGreek: "Leuphana",
		iItalian: "Luneburgo",
		iNorse: "Lyneborg",
		iPortuguese: "Luneburgo",
		iSpanish: "Luneburgo",
	},
	"Luombaka": {
		iLocal: _,
		iPortuguese: "Benguela",
	},
	"Luoyang": {
		iChinese: (
			translate("Dongdu", bCapital=True),
			translate("Henanfu", iAfter=iIndustrial, iBefore=iIndustrial),
			_,
		),
		iJapanese: "Rakuyou",
		iKorean: "Nakyang",
	},
	"Lutsk": {
		iGerman: "Luzk",
		iItalian: "Luc'k",
		iPolish: "Luck",
		iRussian: _,
		iUkrainian: "Lucjk",
	},
	"Luxembourg": {
		iCeltic: "Lucsamburg",
		iChinese: "Lusenbao",
		iDutch: "Luxemburg",
		iFrench: _,
		iGerman: (
			translate("Luxemburg", iAfter=iRenaissance),
			u"Lützelburg",
		),
		iGreek: u"Luxemvúrgho",
		iItalian: "Lussemburgo",
		iJapanese: "Rukusenburuku",
		iKorean: "Ruksembureukeu",
		iLatin: "Luxemburgum",
		iLocal: u"Lëtzebuerg", # Luxembourgish
		iNorse: "Luxemborg",
		iPersian: "Lakshembarg",
		iPolish: "Luksemburg",
		iPortuguese: "Luxemburgo",
		iRussian: "Lyuksemburg",
		iSpanish: "Luxemburgo",
		iTurkish: u"Lüksemburg",
		iUkrainian: "Lyuksemburh",
		iVietnamese: "Luc Sam Bao",
	},
	"Lviv": {
		iChinese: "Liwofu",
		iFrench: u"Léopol",
		iGerman: "Lemberg",
		iGreek: "Leopolis",
		iItalian: "Leopoli",
		iJapanese: "Riviu",
		iKorean: "Ribiu",
		iLatin: "Leopolis",
		iPolish: u"Lwów",
		iPortuguese: u"Leópolis",
		iRussian: "Lvov",
		iSpanish: u"Leópolis",
		iUkrainian: _,
	},
	"Lwanda": {
		iDutch: "Fort Aardenburgh",
		iCongolese: (
			translate("Luanda", bReconquest=True),
			_,
		),
		iPortuguese: u"São Paulo de Loanda"
	},
	"Lwena": {
		iLocal: _,
		iPortuguese: "Luso",
	},
	"Lya": {
		iChinese: (
			translate("Fuzhou", iAfter=iClassical),
			_,
		),
		iJapanese: "Fuutsuo",
		iKorean: "Bokju",
	},
	"Lyon": {
		iCeltic: "Lugdunon",
		iChinese: "Liang",
		iEnglish: "Lyons",
		iFrench: _,
		iGreek: "Lugdunon",
		iItalian: "Lione",
		iJapanese: "Riyon",
		iKorean: "Riong",
		iLatin: "Lugdunum",
		iModernGreek: u"Lión",
		iPolish: "Ludgun",
		iPortuguese: u"Lião",
		iSpanish: u"Lyón",
		iTurkish: "Liyon",
	},
	
	### M ###
	
	"M'Baiki": {
		iFrench: u"Mbaïki",
		iGerman: "Mbaiki",
		iLocal: _,
	},
	"M'banza-Kongo": {
		iCongolese: _,
		iPortuguese: u"São Salvador do Congo",
	},
	"M'banza-Mashita": {
		iCongolese: _,
		iDutch: relocate("Tshikapa"),
		iFrench: relocate("Tshikapa"),
	},
	"M'banza-Ngungu": {
		iCongolese: _,
		iDutch: "Thysstad",
		iFrench: "Thysville",
	},
	"M'banza-Mbata": {
		iCongolese: (
			relocate("Kikwit", iAfter=iIndustrial),
			_,
		),
		iPortuguese: found("Maquela do Zombo"),
	},
	"M'banza-Nsundi": {
		iCongolese: (
			relocate("Kinshasa", iAfter=iIndustrial),
		),
		iDutch: relocate("Kinshasa"),
		iFrench: relocate("Kinshasa"),
	},
	"Ma'tan as-Sarra": {
		iArabic: _,
		iEnglish: "Sarra",
		iItalian: "Sarra",
	},
	"Mabruk": {
		iFrench: "Mabrouk",
		iMande: _,
	},
	u"Macapá": {
		iLocal: "Macapaba",
		iPortuguese: _,
		iSpanish: "Adelantado de Nueva Andaluzia",
	},
	"Madang": {
		iGerman: "Friedrich-Wilhelmshafen",
		iLocal: _,
	},
	"Madras": {
		iEnglish: _,
		iIndian: (
			translate("Chennai", iAfter=iDigital),
			_,
		),
	},
	"Maduuna": {
		iArabic: "Maduna",
		iEnglish: "Maduna",
		iSomali: (
			relocate("Burco", iAfter=iRenaissance),
			_,
		),
	},
	"Maghama": {
		iArabic: "Silibabi",
		iFrench: u"Sélibaby",
		iMande: _,
	},
	"Mahabalipuram": {
		iDravidian: "Mallapuram",
		iDutch: relocate("Pulicat"),
		iEnglish: rename("Madras"),
		iFrench: relocate("Puducherry"),
		iIndian: _,
		iPortuguese: relocate("Pulicat"),
	},
	"Mahajanga": {
		iArabic: "Manzalaji",
		iFrench: "Majunga",
		iLocal: _, # Malagasy
		iPortuguese: "Massalagem",
	},
	"Mahikeng": {  # relocated from Kaditshwene
		iEnglish: "Mafeking",
		iLocal: _,
	},
	"Mahishmati": {
		iIndian: (
			relocate("Harda", iAfter=iRenaissance),
			_,
		),
		iPersian: relocate("Harda", iAfter=iMedieval),
	},
	"Mai Munene": {
		iCongolese: (
			translate("Mwene-Ditu", iAfter=iGlobal),
			_,
		),
	},
	"Maibang": {
		iEnglish: relocate("Shillong"),
		iIndian: (
			relocate("Silchar", iAfter=iIndustrial),
			_,
		),
	},
	"Maimaicheng": {
		iChinese: _,
		iMongol: "Altanbulag",
		iRussian: relocate("Kyakhta"),
	},
	"Mainamati": {
		iIndian: _,
		iPersian: (
			relocate("Comilla", iAfter=iRenaissance),
			u"Môynamoti",
		),
	},
	"Mainz": {
		iChinese: "Meiyinci",
		iDutch: _,
		iEnglish: translate("Mentz", iBefore=iRenaissance),
		iFrench: "Mayence",
		iGerman: _,
		iGreek: u"Maghentía",
		iItalian: "Magonza",
		iJapanese: "Maintsu",
		iKorean: "Maincheu",
		iLatin: "Moguntiacum",
		iPolish: "Moguncja",
		iPortuguese: u"Mogúncia",
		iRussian: "Maints",
		iSpanish: "Maguncia",
		iSwedish: _,
	},
	"Makanza": {
		iCongolese: _,
		iDutch: "Nieuw-Antwerpen",
		iFrench: "Nouvelle-Anvers",
	},
	"Marwa": {
		iFrench: "Maroua",
		iGerman: "Marua",
		iLocal: _,
	},
	"Makassar": {
		iChinese: "Wangjiaxi",
		iDravidian: "Makkachar",
		iDutch: "Makasar",
		iEnglish: "Macassar",
		iJapanese: "Makassaru",
		iLocal: "Mangkasara",
		iMalay: _,
		iPersia: "Maks Sar",
		iPolish: "Makasar",
		iPortuguese: u"Macáçar",
	},
	"Makat": {
		iRussian: _,
		iTurkish: "Maqat",
	},
	"Makata": {
		iFrench: "Port-Vila",
		iPolynesian: _,
	},
	"Makkah": {
		iArabic: _,
		iCeltic: "Meice",
		iDravidian: "Mekka",
		iDutch: "Mekka",
		iEnglish: "Mecca",
		iFrench: "La Mecque",
		iGerman: "Mekka",
		iGreek: "Makoraba",
		iIndian: "Makka",
		iItalian: "La Mecca",
		iJapanese: "Mekka",
		iLatin: "Macoraba",
		iMalay: "Makkah",
		iNorse: "Mekka",
		iPolish: "Mekka",
		iPortuguese: "Meca",
		iRussian: "Mekka",
		iSpanish: "La Meca",
		iSwedish: "Mekka",
		iTurkish: "Mekke",
	},
	"Makkovik": {
		iEnglish: _, # Inuktitut
		iFrench: found("Rigolet"),
		iLocal: "Maggovik",
	},
	"Maklakovo": {
		iRussian: (
			translate("Lesosibirsk", iAfter=iGlobal),
			_,
		),
	},
	"Malaqah": {
		iArabic: _,
		iCeltic: found("Orso"),
		iFrench: "Malaga",
		iGreek: "Mainake",
		iItalian: "Malaga",
		iLatin: (
			found("Orso"),
			"Malaca",
		),
		iPhoenician: "Malaka",
		iPortuguese: u"Málaga",
		iSpanish: u"Málaga",
	},
	u"Malé": {
		iArabic: "Al-Mahal",
		iDravidian: _,
		iPortuguese: "Ambria",
		iSpanish: "Ambria",
	},
	"Males": {
		iLocal: _,
		iSpanish: "Pasto",
	},
	"Malindi": {
		iKiswahili: _,
		iPortuguese: "Melinde",
	},
	u"Malmö": {  # founded on Lund
		iChinese: "Maermo",
		iGerman: "Ellenbogen",
		iIndian: "Malma",
		iJapanese: "Marume",
		iKorean: "Malmoe",
		iLatin: "Malmogia",
		iNorse: u"Malmø",
		iPortuguese: "Malmo",
		iSwedish: _,
	},
	"Manado": {
		iMalay: _,
		iLocal: "Wenang", # Tombulu
	},
	"Manchester": {
		iCeltic: "Manchain",
		iChinese: "Manchesite",
		iEnglish: _,
		iGreek: u"Mankhestría",
		iJapanese: "Manchesutaa",
		iKorean: "Maencheseuteo",
		iLatin: "Mamucium",
		iPersian: "Manchaster",
		iPortuguese: u"Manchéster",
		iSpanish: u"Mánchester",
	},
	"Mandalay": {  # relocated from Pagan
		iBurmese: _,
		iIndian: "Ratanapura",
	},
	"Mandheera": {
		iEnglish: "Mandera",
		iItalian: "Mandera",
		iSomali: _,
	},
	"Mandlakazi": {
		iLocal: _, # Zulu
		iDutch: found("Nelspruit"),
		iEnglish: found("Barberton"),
		iPortuguese: found("Xai-Xai"),
	},
	"Mandore": {
		iHarappa: found("Gilund"),
		iIndian: (
			translate("Jodhpur", iAfter=iRenaissance),
			_,
		),
	},
	"Mang": {
		iLocal: _,
		iEnglish: found("Libreville"),
		iFrench: found("Libreville"),
		iGerman: found("Kribi"),
		iSpanish: found("Bata"),
	},
	"Mangalapuram": {
		iArabic: "Manjalur",
		iDravidian: (
			translate("Mangaluru", iAfter=iRenaissance),
			_,
		),
		iEnglish: "Mangalore",
		iFrench: relocate("Mayyazhi"),
		iGreek: found("Kannur"),
		iIndian: "Manjarun",
	},
	"Manjuur": {
		iChinese: "Lubin",
		iJapanese: "Manshuuri",
		iKorean: "Manjeouli",
		iMongol: _,
		iRussian: "Manzhouli",
	},
	"Mankhamba": {
		iEnglish: relocate("Lilongwe"),
		iLocal: _,
		iPortuguese: relocate("Tete"),
	},
	"Mankoya": {
		iLocal: (
			translate("Kaoma", iAfter=iGlobal),
			_,
		),
	},
	"Manokwari": {
		iDutch: "Manokoeari",
		iGerman: relocate("Sorong"),
		iLocal: _,
	},
	"Mansa": {
		iEnglish: "Fort Rosebery",
		iLocal: _,
	},
	"Manthimba": {
		iEnglish: relocate("Blantyre"),
		iLocal: _,
	},
	"Manyakheta": {
		iEnglish: relocate("Solapur"),
		iIndian: _,
		iPersian: relocate("Gulbarga"),
	},
	"Manyikeni": {
		iLocal: _,
		iPortuguese: relocate("Vilanculos"),
	},
	"Manyoni": {
		iGerman: found("Kilimatinde"),
		iKiswahili: _,
	},
	"Maoka": {
		iJapanese: _,
		iRussian: "Kholmsk",
	},
	"Mapu Chuco": {
		iLocal: _, # Mapundugun
		iSpanish: "Santiago",
	},
	"Mapungubwe": {
		iDutch: relocate("Pietersburg"),
		iEnglish: relocate("Messina"),
		iItalian: relocate("Messina"),
		iLocal: _,
	},
	"Maqom": {
		iArabic: "Surt",
		iFrench: "Syrte",
		iItalian: "Sirte",
		iLatin: "Macomedes-Euphranta",
		iPhoenician: _,
	},
	"Maracaibo": {
		iGerman: rename(u"Neu-Nürnberg"),
		iLocal: "Marakaaya", # Wayuu
		iSpanish: _,
	},
	"Maradah": {
		iArabic: _,
		iItalian: "Marada",
	},
	"Maramuca": {  # founded on Maramuca
		iLocal: "Rimuka",
		iPortuguese: _,
	},
	"Mareeg": {
		iItalian: "Maregh",
		iSomali: _,
	},
	"Mari": {
		iArabic: found("Dayr az-Zawr"),
		iBabylonian: _,
		iGreek: found("Doura-Europos"),
		iLatin: found("Circesium"),
	},
	"Marienburg": {
		iGerman: _,
		iPolish: "Malbork",
	},
	"Mariental": {
		iGerman: _,
		iLocal: "Tsaraxeibes",
	},
	"Mariupol": {
		iRussian: _,
		iTurkish: found("Qiz Yar"),
	},
	"Marka": {
		iArabic: "Maraka",
		iGerman: "Merka",
		iGreek: "Essina",
		iItalian: "Merca",
		iSomali: _,
	},
	"Marquette": {
		iEnglish: _,
		iFrench: found("L'Anse"),
	},
	"Marseille": {
		iArabic: "Marsiliya",
		iChinese: "Masai",
		iEnglish: "Marseilles",
		iFrench: _,
		iGreek: "Massalia",
		iItalian: "Marsiglia",
		iJapanese: "Maruseiyu",
		iKorean: "Mareuseyu",
		iLatin: "Massilia",
		iPersian: "Marsi",
		iPolish: "Marsylia",
		iPortuguese: "Marselha",
		iRussian: "Marsel'",
		iSpanish: "Marsella",
		iTurkish: "Marsilya",
		iVietnamese: "Mac Xay",
	},
	"Marudi": {
		iMalay: (
			relocate("Miri", iAfter=iIndustrial),
			_,
		),
	},
	"Marzuq": {
		iArabic: _,
		iEnglish: "Murzuk",
		iFrench: "Mourzouq",
		iItalian: "Murzuch",
	},
	"Masasi": {
		iGerman: "Massassi",
		iLocal: _,
	},
	"Masqat": {
		iArabic: _,
		iEnglish: "Muscat",
		iFrench: "Mascate",
		iGerman: "Maskat",
		iItalian: "Mascate",
		iPortuguese: "Mascate",
		iRussian: "Maskat",
		iSpanish: "Mascate",
		iTurkish: "Maskat",
	},
	"Massakory": {  # founded on Bidderi
		iArabic: "Massakori",
		iFrench: _,
	},
	"Massenya": {
		iLocal: (
			relocate("Chekna", iAfter=iIndustrial),
			_,
		),
	},
	"Masuku": {
		iFrench: "Franceville",
		iLocal: _,
	},
	"Masulipatnam": {
		iDravidian: (
			translate("Machilipatnam", iAfter=iIndustrial),
			_,
		),
		iDutch: found("Palakollu"),
		iGreek: "Masalia",
		iLatin: "Maesolia",
		iPersian: "Bandar",
	},
	"Matamba": {
		iLocal: _,
		iPortuguese: (
			found(u"Kalandula"),
			"Santa Maria de Matamba",
		),
	},
	"Mathura": {
		iGreek: "Methora",
		iIndian: _,
		iPersian: relocate("Agra", iReligion=iIslam),
	},
	"Matlosana": {
		iDutch: "Klerksdorp",
		iLocal: _,
	},
	"Matsuyama": {
		iJapanese: _,
		iKorean: "Masseuyama",
	},
	"Margilan": {
		iGreek: _,
		iRussian: _,
		iTurkish: "Margilon",
	},
	"Mawk'allaqta": {
		iQuechua: _,
		iSpanish: u"Camaná",
	},
	"Mayapan": {
		iMayan: _,
		iSpanish: relocate(u"Mérida"),
	},
	"Mayapuri": {
		iChinese: "Mo-yu-lo",
		iIndian: (
			translate("Haridvara", iAfter=iMedieval),
			_,
		),
		iPersian: "Haridwar",
	},
	"Mayi": {
		iChinese: (
			translate("Shuozhou", iAfter=iMedieval),
			_,
		),
	},
	"Mayyazhi": {  # relocated from Mangalapuram
		iDravidian: _,
		iFrench: u"Mahé",
	},
	"Mazaka": {
		iArabic: "Kaisariyah",
		# iArmenian: "Mazhak",
		iBabylonian: found("Kanesh"),
		iGreek: "Kaisareia",
		iHittite: found("Kanesh"),
		iLatin: "Caesarea",
		iPersian: _,
		iTurkish: "Kayseri",
	},
	"Mbabane": {  # relocated from Bremersdorp
		iEnglish: _,
		iLocal: u"ÉMbábáne",
	},
	"Mbande": {
		iGerman: found("Tukuyu"),
		iLocal: (
			translate("Mbeya", iAfter=iIndustrial),
			_,
		),
	},
	"Mbanza-Bumbe": {
		iCongolese: _,
		iPortuguese: relocate("Ambriz"),
	},
	"Mbwila": {
		iCongolese: _,
		iPortuguese: (
			relocate("Wizidi", iAfter=iGlobal),
			u"Ambuíla",
		),
	},
	"McGrath": {
		iEnglish: _,
		iLocal: "Tochak", # Kuskokwim
	},
	"Mechetnaya": {
		iRussian: (
			translate("Pugachyov", iAfter=iGlobal),
			translate("Nikolayevsk", iAfter=iIndustrial),
			_,
		),
	},
	"Medewi": {
		iArabic: "Meruwah",
		iEgyptian: "Mjrwjw",
		iEnglish: u"Meroë",
		iGreek: "Meroe",
		iNubian: _,
	},
	"Mediolanum": {
		iArabic: "Milanu",
		iChinese: "Milan",
		iDutch: "Milaan",
		iEnglish: "Milan",
		iFrench: "Milan",
		iGerman: "Mailand",
		iGreek: "Mediolana",
		iItalian: "Milano",
		iJapanese: "Mirano",
		iKorean: "Millano",
		iLatin: _,
		iLocal: "Milan", # Milanese
		iModernGreek: u"Miláno",
		iNorse: "Mailand",
		iPersian: "Milan",
		iPolish: "Mediolan",
		iPortuguese: u"Milão",
		iRussian: "Milan",
		iSpanish: u"Milán",
	},
	"Melaka": {  # relocated from Beruas
		iArabic: "Malaqa",
		iChinese: "Maliujia",
		iDravidian: "Malakka",
		iDutch: "Malakka",
		iEnglish: (
			relocate("Kuala Lumpur", iAfter=iIndustrial),
			"Malacca",
		),
		iGerman: "Malakka",
		iItalian: "Malacca",
		iJapanese: "Marakka",
		iMalay: (
			relocate("Kuala Lumpur", iAfter=iIndustrial),
			_,
		),
		iPolish: "Malakka",
		iPortuguese: "Malaca",
		iSpanish: "Malaca",
		iTurkish: "Malakka",
	},
	"Melekess": {
		iRussian: (
			translate("Dimitrovgrad", bCommunist=True),
			_,
		),
		iMongol: (
			found("Bolghar"),
			"Melekes",
		),
	},
	"Menggala": {
		iDutch: relocate("Bandar Lampung"),
		iMalay: _,
	},
	"Mergen": {
		iChinese: "Nenjiang",
		iManchu: _,
	},
	u"Mérida": {  # relocated from Mayapan
		iMayan: "Jo'",
		iSpanish: _,
	},
	"Merv": {
		iArabic: _,
		iGreek: "Antiochia Margiana",
		iPersian: translate("Margu", iBefore=iClassical),
	},
	"Messana": {
		iFrench: "Messine",
		iGreek: "Messene",
		iItalian: "Messina",
		iJapanese: "Messhiina",
		iLatin: _,
		iLocal: "Missina", # Sicilian
		iModernGreek: u"Mesíni",
		iPolish: "Mesyna",
		iSpanish: "Mesina",
	},
	"Messewa": {
		iArabic: "Massawa",
		iEgyptian: found("Nakfa"),
		iEnglish: "Massawa",
		iEthiopian: _,
		iGerman: "Massaua",
		iItalian: "Massaua",
		iPortuguese: u"Maçuá",
		iTurkish: "Massava",
	},
	"Messina": {  # relocated from Mapungubwe
		iEnglish: _,
		iItalian: _,
		iLocal: "Musina",
	},
	"Mexicali": {
		iEnglish: "Calexico",
		iSpanish: _,
	},
	"Mikindani": {
		iKiswahili: _,
		iPortuguese: found(u"Mocímboa da Praia"),
	},
	"Meliddu": {
		iBabylonian: _,
		iGreek: "Melitene",
		iHittite: "Malidiya",
		iLocal: translate(u"Meletî", iAfter=iMedieval), # Kurdish
		iTurkish: "Malatya",
	},
	"Milwaukee": {
		iDutch: found("Oostburg"),
		iEnglish: _,
	},
	"Mingzhou": {
		iChinese: (
			translate("Ningbo", iAfter=iMedieval),
			_,
		),
		iEnglish: relocate("Zhoushan"),
	},
	"Minneapolis": {
		iEnglish: _,
		iFrench: found("Fort Beauharnois"),
	},
	"Miran": {
		iChinese: _,
		iTibetan: "Nop Chungu",
		iTurkish: "Yuni",
	},
	"Misratah": {  # founded on Lpqy
		iArabic: _,
		iBerber: "Misrata",
		iEnglish: "Misrata",
		iFrench: "Misrata",
		iItalian: "Misurata",
		iSpanish: "Misurata",
		iTurkish: "Misrata",
	},
	"Mithila": {
		iIndian: (
			translate("Darbhanga", iAfter=iMedieval),
			_,
		),
	},
	"Miyaly": {
		iRussian: _,
		iTurkish: "Miialy",
	},
	"Mogaung": {
		iBurmese: (
			translate("Myitkyina", iAfter=iIndustrial),
			_,
		),
	},
	"Moldary": {
		iRussian: (
			translate("Kurchatov", bCommunist=True),
			_,
		),
	},
	"Moling": {
		iChinese: (
			translate("Nanjing", iAfter=iGlobal),
			translate("Jiangning", iAfter=iIndustrial),
			translate("Nanjing", iAfter=iMedieval),
			translate("Jiankang", bCapital=True),
			_,
		),
		iEnglish: "Nanking",
		iJapanese: "Nankin",
		iKorean: "Namgyeong",
		iMongol: "Nanjin",
		iPortuguese: "Nanquim",
		iSpanish: u"Nankín",
		iVietnamese: "Nam Kinh",
	},
	"Mombasa": {
		iArabic: "Manbasa",
		iKiswahili: _,
		iPortuguese: u"Mombaça",
	},
	"Moncton": {
		iEnglish: _,
		iFrench: (
			found("Beaubassin"),
			"Le Coude",
		),
	},
	"Mongo": {
		iArabic: "Munqu",
		iLocal: _,
	},
	"Monroe": {
		iEnglish: _,
		iFrench: found(u"Les Opélousas"),
		iSpanish: "Fort Miro",
	},
	"Monsol": {
		iFrench: found("Fort-Rousset"),
		iLocal: _,
	},
	"Montevideo": {
		iPortuguese: u"Montevidéu",
		iSpanish: _,
	},
	"Montgomery": {  # relocated from Ajodhan
		iEnglish: _,
		iPersian: "Sahiwal",
	},
	"Montpellier": {
		iCeltic: found("Nemausus"),
		iFrench: _,
		iGreek: found("Agde"),
		iLatin: found("Nemausus"),
		iLocal: u"Montpelhièr", # Occitan
	},
	u"Montréal": {
		iEnglish: "Montreal",
		iFrench: _,
		iLocal: u"Tiohtià:ke", # Mohawk
	},
	"Moose Factory": {
		iEnglish: _,
		iFrench: "Fort Saint-Louis",
	},
	"Morobe Harbour": {
		iEnglish: _,
		iGerman: (
			translate("Lehe", iAfter=iGlobal),
			u"Preußen-Reede",
		),
		iLocal: "Lae",
	},
	"Morokweng": {
		iDutch: found("Vryburg"),
		iLocal: _,
	},
	"Morsha": {
		iRussian: (
			translate("Morshansk", iAfter=iIndustrial),
			_,
		),
	},
	"Moshaweng": {
		iDutch: found("Rustenburg"),
		iEnglish: "Gaberone",
		iLocal: (
			translate("Gaborone", iAfter=iGlobal),
			_,
		),
	},
	"Moskva": {
		iArabic: "Musku",
		iBrazilian: "Moscou",
		iCeltic: u"Moscó",
		iChinese: "Mosike",
		iDutch: "Moskou",
		iEnglish: "Moscow",
		iFrench: "Moscou",
		iGerman: "Moskau",
		iGreek: u"Móskha",
		iItalian: "Mosca",
		iJapanese: "Mosukuwa",
		iKorean: "Moseukeuba",
		iMalay: "Moskwa",
		iSpanish: u"Moscú",
		iPersian: "Mosko",
		iPolish: "Moskwa",
		iPolynesian: "Mosekao",
		iPortugal: "Moscovo",
		iRussian: _,
		iTurkish: "Moskova",
		iVietnamese: "Mac Tu Khoa",
	},
	"Muaskar": {
		iArabic: _,
		iFrench: "Mascara",
		iItalian: "Mascara",
		iLatin: found("Cohors Breucorum"),
		iTurkish: "Muasker",
	},
	"Moxomatsi": {
		iDutch: (
			found("Witbank"),
			"Machadodorp",
		),
		iLocal: (
			translate("eNtokozweni", iAfter=iGlobal),
			_,
		),
	},
	u"Möwebucht": {  # founded on Tombwa
		iDutch: u"Möwebaai",
		iEnglish: u"Möwe Bay",
		iGerman: _,
	},
	"Mozyr": {
		iPolish: "Mozyrz",
		iRussian: _,
	},
	"Mpinda": {
		iCongolese: (
			translate("Soyo", iAfter=iIndustrial),
			_,
		),
		iPortuguese: u"San António do Zaire",
	},
	"Mpwapwa": {
		iEnglish: relocate("Dodoma"),
		iGerman: relocate("Dodoma"),
		iKiswahili: _,
	},
	"Mrauk U": {  # relocated from Waithali
		iBurmese: _,
		iEnglish: "Myohaung",
	},
	"Mser": {
		iArabic: "Qusur",
		iFrench: (
			translate("Fort-Foureau", iBefore=iIndustrial),
			u"Kousséri",
		),
		iGerman: "Kusseri",
		iItalian: "Uncusciuri",
		iLocal: _,
	},
	"Msumbiji": {
		iKiswahili: _,
		iEnglish: "Mozambique",
		iPortuguese: (
			found(u"Fort São Sebastião"),
			u"Moçambique",
		),
	},
	"Mtho Lding": {
		iChinese: "Tuolin",
		iEnglish: "Tholding",
		iTibetan: _,
	},
	"Mtskheta": {
		iGreek: found("Harmozike"),
		iLocal: ( # Georgian
			relocate("Tbilisi", iAfter=iMedieval),
			_,
		),
	},
	"Mu'a": {
		iPolynesian: (
			translate("Nuku'alofa", iAfter=iIndustrial),
			_,
		),
	},
	"Muang Na Rang": {  # founded on Myeik
		iThai: (
			translate("Prachuap Khiri Khan", iAfter=iIndustrial),
			_,
		),
	},
	"Mubende": {
		iKiswahili: (
			translate("Kampala", iAfter=iIndustrial),
			_,
		),
	},
	"Mudanjiang": {
		iChinese: _,
		iJapanese: "Butankou",
		iKorean: found("Sanggyeong"),
		iManchu: "Mudan bira",
	},
	"Mukhtuya": {
		iRussian: (
			translate("Lensk", iAfter=iGlobal),
			_,
		),
	},
	"Mukiwa": {
		iQuechua: _,
		iSpanish: (
			found("Tacna"),
			"Moquegua",
		),
	},
	"Muku": {
		iLocal: _,
		iSpanish: u"Mérida",
	},
	"Multan": {  # renamed from Kashyapapura
		iEnglish: _,
		iPersian: "Maltan",
	},
	"Mumias": {
		iEnglish: relocate("Kisumu"),
		iKiswahili: _,
	},
	u"München": {  # relocated from Freising
		iArabic: "Miyunikh",
		iChinese: "Munihei",
		iDutch: _,
		iEnglish: "Munich",
		iGerman: _,
		iItalian: "Monaco",
		iJapanese: "Myunhen",
		iKorean: "Mwinhen",
		iNorse: _,
		iPersian: "Monikh",
		iPolish: u"Mnichów",
		iPortuguese: "Munique",
		iRussian: "Myunkhen",
		iSpanish: u"Múnich",
		iTurkish: u"Münih",
	},
	"Mungiki": {
		iPolynesian: _,
		iEnglish: (
			relocate("Honiara", iAfter=iGlobal),
			"Bellona",
		),
	},
	u"Münster": {
		iGerman: _,
		iKorean: "Mwinseuteo",
		iPolish: "Monastyr",
		iPortuguese: u"Monastério",
	},
	"Muqdisho": {
		iArabic: "Maqadishu",
		iEnglish: "Mogadishu",
		iGerman: "Mogadischu",
		iGreek: "Serapion",
		iItalian: "Mogadiscio",
		iLatin: "Sarapium",
		iPortuguese: u"Mogadíscio",
		iSomali: _,
	},
	"Murdeshwar": {
		iEnglish: relocate("Kundapur"),
		iIndian: (
			relocate("Bhatkal", iAfter=iMedieval),
			_,
		),
	},
	"Murom": {
		iMongol: relocate("Kasimov"),
		iRussian: _,
	},
	"Murrakush": {
		iArabic: _,
		iEnglish: "Marrakesh",
		iFrench: "Marrakech",
		iGerman: "Marrakesch",
		iGreek: found("Tmdt"),
		iLatin: found("Tmdt"),
		iPhoenician: found("Tmdt"),
		iPortuguese: "Marraquexe",
		iSpanish: "Marrakech",
		iTurkish: "Marakesh",
	},
	"Mursiyya": {
		iArabic: _,
		iCeltic: found("Cartagena"),
		iFrench: "Murcie",
		iGreek: found("Helike"),
		iLatin: found("Cartagena"),
		iPhoenician: found("Cartagena"),
		iPortuguese: u"Múrcia",
		iSpanish: "Murcia",
	},
	"Murwab": {
		iArabic: (
			relocate("Al-Bidda", iAfter=iRenaissance),
			_,
		),
	},
	"Mustaganim": {  # founded on Qartan
		iArabic: _,
		iFrench: "Mostaganem",
		iLatin: "Murustaq",
		iPhoenician: "Murustaga",
		iTurkish: u"Müstaganem",
	},
	"Musumba": {
		iCongolese: relocate("Kolwezi"),
		iDutch: relocate("Kolwezi"),
		iFrench: relocate("Kolwezi"),
		iLocal: "Musumba",
		iPortuguese: "Mussumba",
	},
	"Musuru": {  # relocated from Kalo
		iArabic: _,
		iFrench: "Moussoro",
	},
	"Muynak": {
		iRussian: _,
		iTurkish: "Moynaq",
	},
	"Muzui": {
		iArabic: "Rabyanah",
		iBerber: _,
		iEnglish: "Rabiana",
	},
	"Mwaka Kumbana": {
		iCongolese: _,
		iDutch: found("Sandoa"),
		iEnglish: found("Sandoa"),
		iPortuguese: found("Dundo"),
	},
	"Mwansabombwe": {
		iCongolese: found("Lubumbashi"),
		iDutch: found("Lubumbashi"),
		iEnglish: rename("Kazembe"),
		iFrench: found("Lubumbashi"),
		iLocal: _,
		iPortuguese: rename("Kazembe"),
	},
	"Mwanza": {
		iGerman: "Muansa",
		iKiswahili: _,
	},
	"Mwimbele": {
		iCongolese: found("Kamina"),
		iDutch: relocate("Kamina"),
		iFrench: relocate("Kamina"),
		iLocal: _,
	},
	"Mwinilunga": {
		iEnglish: relocate("Kitwe"),
		iLocal: _,
	},
	"Myeik": {
		iBurmese: _,
		iEnglish: "Mergui",
		iThai: (
			found("Muang Na Rang"),
			"Marit",
		),
	},
	"Mykolaiv": {
		iEnglish: "Nikolaev",
		iFrench: u"Mykolaïv",
		iGerman: "Mykolajiw",
		iGreek: found("Olbia"),
		iPolish: u"Mikolajów",
		iRussian: "Nikolayev",
		iSwedish: "Mykolajiv",
		iTurkish: (
			found("Ochakov"),
			translate("Mikolayiv", iAfter=iIndustrial),
			"Balaban",
		),
		iUkrainian: _,
	},
	"Mzimba": {
		iEnglish: found("Livingstonia"),
		iLocal: (
			translate("Mzuzu", iAfter=iGlobal),
			_,
		),
	},
	"Mzizima": {
		iArabic: relocate("Dar es Salaam"),
		iGerman: relocate("Dar es Salaam"),
		iGreek: "Rhapta",
		iKiswahili: (
			relocate("Dar es Salaam", iAfter=iIndustrial),
			_,
		),
	},
	
	### N ###
	
	"N'dalatando": {
		iLocal: _,
		iPortuguese: translate("Vila Salazar", bAutocratic=True),
	},
	u"N'Délé": {
		iCongolese: _,
		iFrench: u"Ndélé",
	},
	"N'gamdere": {
		iFrench: u"Ngaoundéré",
		iGerman: u"Ngaundere",
		iLocal: _, # Fula
	},
	"Na'avojowa": {
		iLocal: _, # Mayo
		iMexican: relocate(u"Ciudad Obregón", iAfter=iGlobal),
		iSpanish: (
			found("Guaymas"),
			"Navojoa",
		),
	},
	"Naberezhnye Chelny": {  # founded on Juketau
		iRussian: (
			translate("Brezhnev", bCommunist=True),
			_,
		),
	},
	"Nadezhdinsk": {
		iRussian: (
			translate("Serov", bCommunist=True),
			_,
		),
	},
	"Naeyn": {
		iPersian: (
			translate("Nain", iAfter=iMedieval),
			_,
		),
	},
	"Naga": {
		iLocal: _, # Tagalog
		iSpanish: u"Nueva Cáceres",
	},
	"Nagasaki": {
		iChinese: "Changqi",
		iJapanese: _,
	},
	"Nagaur": {
		iHarappan: found("Sandhanawala"),
		iIndian: _,
	},
	"Nagchu": {
		iChinese: (
			translate("Seruxiangba", iAfter=iGlobal),
			"Heihe",
		),
		iMongol: "Hala Wusu",
		iTibetan: _,
	},
	"Nagormo": {
		iChinese: "Ge'ermu",
		iMongol: "Golmud",
		iTibetan: _,
	},
	"Nagpur": {  # relocated from Nandivardhan
		iEnglish: "Nagpore",
		iIndian: _,
	},
	"Nagula Vancha": {  # founded on Dantewada
		iDutch: "Nagelwanze",
		iIndian: _,
	},
	"Nahavand": {
		iGreek: rename("Laodikeia"),
		iPersian: (
			translate("Nisaya", iBefore=iClassical),
			_,
		),
	},
	"Najran": {
		iArabic: _,
		iGreek: "Negrana",
	},
	"Nakhodka": {
		iChinese: found("Sucheng"),
		iRussian: _,
	},
	"Nalote": {  # founded on Nekhen
		iArabic: "Karanog",
		iNubian: _,
	},
	"Nalut": {
		iArabic: _,
		iFrench: "Nalout",
	},
	"Namay": {
		iFrench: "Niamey",
		iLocal: _,
	},
	"Namibe": {
		iCongolese: _,
		iPortuguese: u"Moçâmedes",
	},
	"Nan Madol": {
		iGerman: relocate("Kolonia"),
		iPolynesian: (
			translate("Madolenihmw", iAfter=iIndustrial),
			_,
		),
		iSpanish: relocate("Kolonia"),
	},
	"Nanaimo": {
		iEnglish: _,
		iSpanish: found("Santa Cruz de Nuca"),
	},
	"Nancy": {
		iCeltic: found("Tullum"),
		iFrench: _,
		iGerman: "Nanzig",
		iKorean: "Naensi",
		iLatin: found("Tullum"),
		iPortuguese: "Nanci",
	},
	"Nandivardhan": {
		iIndian: (
			relocate("Nagpur", iAfter=iRenaissance),
			translate("Nagardhan", iAfter=iMedieval),
			_,
		),
	},
	"Nantes": {
		iCeltic: "Naoned",
		iFrench: _,
		iGreek: "Kondeouinkon",
		iLatin: "Portus Namnetum",
		iJapanese: "Nanto",
		iKorean: "Nangteu",
	},
	"Nantou": {
		iChinese: (
			translate("Shenzhen", iAfter=iIndustrial),
			_,
		),
		iEnglish: relocate("Hong Kong"),
	},
	"Nanzheng": {
		iChinese: (
			translate("Hanzhong", iAfter=iClassical),
			_,
		),
	},
	"Napa": {
		iEgyptian: "Npt",
		iGreek: "Napata",
		iNubian: (
			relocate("Tungul", iReligion=iOrthodoxy),
			_,
		),
	},
	"Narbonne": {
		iFrench: _,
		iItalian: "Narbona",
		iLatin: "Narbo Martius",
		iPortuguese: "Narbona",
		iSpanish: "Narbona",
	},
	"Nasaf": {
		iGreek: "Eukraditeia",
		iLocal: "Nakhshab", # Sogdian
		iMongol: "Qarshi",
		iTurkish: _,
	},
	"Nassau": {
		iDutch: _,
		iEnglish: _,
		iSpanish: (
			found("San Salvador"),
			u"Nasáu",
		),
	},
	"Natal": {
		iDutch: (
			found("Frederikstad"),
			"Fort Keulen",
		),
		iPortuguese: _,
	},
	"Naushera": {
		iEnglish: "Nowshera",
		iHarappan: found("Musa Khel"),
		iPersian: (
			relocate("Khushab", iAfter=iGlobal),
			_,
		),
	},
	"Ndakaaru": {
		iDutch: found("Goeree"),
		iFrench: "Dakar",
		iGerman: found("Fort Jakob"),
		iLocal: _, # Wolof
		iMande: found("Mboul"),
		iPortuguese: "Dacar",
	},
	"Ndombe": {
		iLocal: _,
		iPortuguese: "Dombe Grande",
	},
	"Neapolis": {
		iArabic: "Nabuli",
		iChinese: "Napoli",
		iDutch: "Napels",
		iEnglish: "Naples",
		iGerman: "Neapel",
		iGreek: _,
		iItalian: "Napoli",
		iLatin: _,
		iLocal: "Napule", # Neapolitan
		iMalay: "Napoli",
		iModernGreek: u"Nápoli",
		iPolish: "Neapol",
		iPortuguese: u"Nápoles",
		iRussian: "Neapol'",
		iSpanish: u"Nápoles",
		iSwedish: "Neapel",
		iTurkish: "Napoli",
	},
	"Neemrana": {
		iHarappa: found("Siswal"),
		iIndian: (
			relocate("Rewari", iAfter=iMedieval),
			_,
		),
	},
	"Neerchokikoo": {
		iEnglish: "Portland",
		iLocal: _,
	},
	"Neh": {
		iPersian: (
			translate("Nehbandan", iAfter=iRenaissance),
			_,
		),
	},
	"Nekemte": {
		iEthiopian: _,
		iItalian: "Lechemti",
		iLocal: "Naqamtee", # Oromo
	},
	"Nekhen": {
		iArabic: relocate("Al-Maharraqa"),
		iEgyptian: _,
		iGreek: "Hierakonpolis",
		iLatin: "Hieraconpolis",
		iNubian: found("Nalote"),
	},
	"Nellore": {
		iDravidian: _,
		iDutch: found("Nizampatnam"),
		iPersian: (
			found("Nizampatnam", iReligion=iIslam),
			"Nellaur",
		),
	},
	"Nelspruit": {  # founded on Mandlakazi
		iDutch: _,
		iLocal: "Mbombela",
	},
	"Nemausus": {  # founded on Montpellier
		iCeltic: "Nemausos",
		iFrench: u"Nîmes",
		iLatin: _,
	},
	"Nerang": {
		iEnglish: (
			translate("Gold Coast", iAfter=iGlobal),
			_,
		),
		iLocal: _, # Aboriginal Yugambeh
	},
	"Nertobriga": {  # founded on Batalyaws
		iCeltic: _,
		iLatin: "Colonia Iulia",
		iSpanish: "Fregenal",
	},
	u"Neu-Nürnberg": {  # renamed from Maracaibo
		iEnglish: "New Nuremberg",
		iGerman: _,
	},
	"Neu-Ulm": {  # founded on Cedar Rapids
		iEnglish: "New Ulm",
		iGerman: _,
	},
	"Neufreiburg": {  # founded on Juiz de Fora
		iEnglish: "New Fribourg",
		iGerman: _,
		iPortuguese: "Nova Friburgo",
	},
	"Nevers": {
		iCeltic: (
			found("Bibracte"),
			"Noviodunon",
		),
		iFrench: _,
		iLatin: "Noviodunum",
	},
	"New Edinburgh": {  # founded on Ciudad de Panamá
		iEnglish: _,
		iSpanish: (
			translate("Puerto Inabaginya", iAfter=iDigital),
			u"Puerto Escocés",
		),
	},
	"New Plymouth": {  # founded on Whanganui
		iEnglish: _,
		iPolynesian: "Ngamotu",
	},
	"New York": {
		iDutch: "Nieuw-Amsterdam",
		iEnglish: _,
		iFrench: u"La Nouvelle-Angoulême",
		iRussian: "Nowy Jork",
	},
	"Newcastle": {
		iCeltic: "An Caisteal Nuadh",
		iEnglish: _,
		iLatin: "Pons Aelius",
		iNorse: found("Scarborough"),
	},
	"Newcastle, kwaZulu-Natal": {  # founded on Bulawayo
		iDutch: "Viljoensdorp",
		iEnglish: "Newcastle",
	},
	"Newcastle, New South Wales": {
		iEnglish: "Newcastle",
	},
	"Newkart": {  # relocated from Kalhu
		iArabic: "Al-Hadita",
		iBabylonian: "Hdatta",
		iPersian: _,
	},
	"Ng'wena": {
		iLocal: (
			translate("Kasama", iAfter=iIndustrial),
			_,
		),
	},
	"Nganda-ya-Kawe": {
		iLocal: _,
		iPortuguese: (
			translate("Ganda", iAfter=iDigital),
			"Vila Mariano Machado",
		),
	},
	"Ngoma": {
		iCongolese: _,
		iDutch: "Goma",
		iFrench: "Goma",
	},
	"Nguru": {
		iFrench: "N'Gourou",
		iLocal: _,
	},
	"Niani": {
		iArabic: "Nyeni",
		iMande: (
			relocate("Kankan", iAfter=iRenaissance),
			_,
		),
	},
	"Nibbur": {
		iArabic: relocate("Wasit"),
		iBabylonian: _,
		iGreek: (
			found("Artemita"),
			"Nippour",
		),
		iPersian: found("Kashkar"),
	},
	"Nizza": {
		iChinese: "Nisi",
		iEnglish: "Nice",
		iFrench: "Nice",
		iGerman: _,
		iGreek: "Nikaia",
		iItalian: _,
		iJapanese: "Niisu",
		iKorean: "Niseu",
		iLatin: "Nicaea",
		iLocal: "Nissa", # Piedmontese
		iPersian: "Nis",
		iPolish: "Nicea",
		iPortuguese: "Nice",
		iRussian: "Nitstsa",
		iSpanish: "Niza",
		iTurkish: "Nis",
	},
	u"Niðaróss": {
		iNorse: (
			rename(u"Þróndheimr", iAfter=iRenaissance),
			translate("Nidaros", iPeriod=iPeriodDenmark),
			_,
		),
	},
	"Nieuw Amsterdam": {  # renamed from Fort Nassau
		iDutch: _,
		iEnglish: "New Amsterdam",
	},
	"Nijmegen": {
		iDutch: _,
		iFrench: u"Nimègue",
		iGerman: "Nimwegen",
		iItalian: "Nimega",
		iLatin: "Noviomagus",
		iPersian: "Nayemikhan",
		iPortuguese: "Nimegue",
		iSpanish: "Nimega",
	},
	"Nikaia": {
		iArabic: "Nikiye",
		iGreek: _,
		iLatin: "Nicaea",
		iTurkish: "Iznik",
	},
	"Nikephorion": {
		iArabic: "Ar-Raqqa",
		iBabylonian: found("Rasappa"),
		iGreek: _,
		iLatin: "Nicephorium",
		iLocal: "Reca", # Kurdish
		iTurkish: "Rakka",
	},
	"Nikolayevsk": {
		iRussian: (
			translate("Kustanay", iAfter=iGlobal),
			_,
		),
		iTurkish: "Qostanai",
	},
	"Nikolayevsk-na-Amure": {
		iManchu: "Fuyori",
		iRussian: _,
	},
	"Nikomedeia": {
		iGreek: _,
		iLatin: "Nicomedia",
		iTurkish: "Izmit",
	},
	"Nikonion": {  # founded on Dubasari
		iGreek: _,
		iLatin: "Niconium",
	},
	"Ninua": {
		iArabic: (
			relocate("Al-Mawsil"),
			"Ninawa",
		),
		iBabylonian: _,
		iGreek: "Nineue",
		iHittite: "Ninuwa",
		iLatin: "Ninive",
		iTurkish: found("Kuyunjiq"),
	},
	"Nipawin": {
		iEnglish: _,
		iFrench: found(u"Fort la Jonquière")
	},
	"Nish": {
		iEnglish: _,
		iFrench: _,
		iGerman: "Nisch",
		iGreek: "Naissos",
		iItalian: "Nissa",
		iLatin: "Naissus",
		iLocal: _, # Serbian
		iPolish: "Nisz",
		iRussian: _,
		iTurkish: _,
	},
	"Nisa": {
		iGreek: "Nisaion",
		iKushan: relocate("Ashgabat"),
		iPersian: (
			translate("Mithradatkert", bCapital=True),
			_,
		),
		iTurkish: (
			relocate("Ashgabat"),
			"Nusay",
		),
	},
	"Nishapur": {
		iArabic: "Abarshahr",
		iPersian: (
			translate("Neyshabur", iAfter=iMedieval),
			_,
		),
	},
	"Nisibis": {
		iArabic: relocate("Diyarbakir"),
		iBabylonian: "Nasibina",
		iGreek: "Antiokheia tis Mygdonias",
		iLatin: _,
		iLocal: "Mtsbin", # Armenian
		iTurkish: "Nusaybin",
	},
	"Nizampatnam": {  # founded on Nellore
		iDravidian: "Peddapalli",
		iDutch: "Petapoeli",
		iEnglish: "Pettapoly",
		iPersian: _,
	},
	"Njimi": {
		iLocal: (
			translate("Mao", iAfter=iIndustrial),
			_,
		),
	},
	"Njurbel": {
		iArabic: "Awlil",
		iLocal: _,
	},
	"Nkhotakota": {
		iEnglish: "Kota Kota",
		iLocal: _,
	},
	"Nkran": {
		iDutch: (
			translate("Ussher Fort", bSmall=True),
			"Accra",
		),
		iEnglish: (
			translate("Fort James", bSmall=True),
			"Accra",
		),
		iFrench: (
			translate(u"Fort Crèvecoeur", bSmall=True),
			"Accra",
		),
		iLocal: _, # Twi
		iNorse: (
			translate("Fort Christiansborg", bSmall=True),
			"Akra",
		),
		iPortuguese: (
			translate(u"Forte de São Francisco Xavier", bSmall=True),
			"Acra",
		),
		iSpanish: "Acra",
		iSwedish: (
			translate("Fort Frederiksborg", bSmall=True),
			"Accra",
		),
		iTurkish: "Akra",
	},
	"Nkuna": {
		iFrench: "Brazzaville",
		iLocal: _, # Teke
	},
	"Nkurenkuru": {
		iDutch: relocate("Rundu"),
		iLocal: _, # Kwangali
		iPortuguese: relocate("Dirico"),
	},
	"Noatak": {
		iEnglish: _,
		iLocal: "Nuataaq", # Inupiaq
	},
	"Nomabeb": {
		iDutch: "Gobabeb",
		iEnglish: "Gobabeb",
		iGerman: "Gobabeb",
		iLocal: _,
	},
	"Nome": {
		iEnglish: _,
		iLocal: "Sitnasuaq", # Inupiaq
	},
	"Nomsoros": {
		iDutch: "Kalkfontein",
		iEnglish: found("Upington"),
		iGerman: "Karasburg",
		iLocal: _, # Khoekhoe
	},
	"Norilsk": {
		iPolish: "Norylsk",
		iRussian: _,
	},
	"Norman Wells": {
		iEnglish: _,
		iLocal: u"Tlegóhl", # Slavey
	},
	"North West River": {
		iEnglish: _,
		iFrench: "Fort Esquimaux Baie",
	},
	"Norwich": {
		iEnglish: _,
		iLatin: "Venta Icenorum",
	},
	"Nouantikum": {  # founded on Calatayud
		iCeltic: _,
		iLatin: "Numantia",
		iSpanish: "Numancia",
	},
	"Nova Trento": {  # founded on Passo Fundo
		iItalian: "Nuova Trento",
		iPortuguese: _,
	},
	"Novgorod": {
		iGerman: "Nowgorod",
		iNorse: u"Holmgarðr",
		iPolish: u"Nowogród",
		iPortuguese: u"Novogárdia",
		iRussian: _,
		iSpanish: u"Nóvgorod",
		iSwedish: u"Holmgård",
	},
	"Novo Hamburgo": {  # founded on Passo Fundo
		iGerman: "Neu-Hamburg",
		iPortuguese: _,
	},
	"Novokholmogory": {
		iChinese: "Datianshi",
		iDutch: "Sint-Michiel",
		iEnglish: "Archangel",
		iFrench: "Arkhangel",
		iGerman: "Archangelsk",
		iGreek: u"Archángelos",
		iItalian: "Arcangelo",
		iKorean: "Areuhangelseukeu",
		iPolish: "Archangielsk",
		iPortuguese: "Arcangel",
		iRussian: (
			translate("Arkhangelsk", iAfter=iRenaissance),
			_,
		),
		iSpanish: u"Arjángelsk",
		iTurkish: "Arhanghelsk",
	},
	"Novonikolayevsk": {
		iRussian: (
			translate("Novosibirsk", iAfter=iGlobal),
			_,
		),
	},
	"Nsheng": {
		iCongolese: (
			translate("Mushenge", iAfter=iIndustrial),
			_,
		),
		iDutch: relocate("Kananga"),
		iFrench: relocate("Kananga"),
		iGerman: found("Malandji"),
	},
	"Ntsweng": {
		iLocal: (
			translate("Molepolole", iAfter=iGlobal),
			_,
		),
	},
	"Nubt": {
		iArabic: "Kom Ombo",
		iCoptic: "Embo",
		iEgyptian: _,
		iGreek: "Ombos",
		iLatin: "Ambo",
	},
	"Nueva Iberia": {  # founded on Lafayette
		iEnglish: "New Iberia",
		iFrench: u"La Nouvelle-Ibérie",
		iSpanish: _,
	},
	"Nullarbor": {
		iDutch: found("'t Landt van P. Nuyts"),
		iEnglish: _,
	},
	"Numbulwar": {
		iDutch: found("Kaap Maria"),
		iEnglish: _,
	},
	u"Nürnberg": {
		iChinese: "Niulunbao",
		iDutch: "Neurenberg",
		iEnglish: "Nuremberg",
		iGerman: _,
		iGreek: u"Niremvéryi",
		iItalian: "Norimberga",
		iJapanese: "Nyurumberuku",
		iKorean: "Nwireunbereukeu",
		iPersian: "Norambarg",
		iPolish: "Norymberga",
		iPortuguese: "Nuremberga",
		iSpanish: u"Núremberg",
	},
	"Nwakcot": {
		iArabic: "Nwakshut",
		iBerber: _,
		iFrench: "Nouakchott",
		iLocal: "Nuwaaksuut", # Wolof
	},
	"Nyangwe": {
		iCongolese: _,
		iDutch: relocate("Lusambo"),
		iFrench: relocate("Lusambo"),
	},
	"Nyanza": {
		iDutch: relocate("Gisenyi"),
		iFrench: relocate("Gisenyi"),
		iGerman: relocate("Kigali"),
		iLocal: _,
	},
	"Nyen": {  # founded on Orekhov
		iLocal: "Nevanlinna", # Finnish
		iRussian: (
			relocate("Sankt-Peterburg", iAfter=iRenaissance),
			"Niyen",
		),
		iSwedish: _,
	},
	"Nyonoksa": {
		iRussian: (
			translate("Molotovsk", bCommunist=True),
			translate("Severodvinsk", iAfter=iGlobal),
			_,
		),
	},
	"Nyslott": {
		iLocal: "Savonlinna", # Finnish
		iSwedish: _,
	},
	"Nzerekore": {
		iAmerican: found("Buchanan"),
		iFrench: u"Nzérékoré",
		iLocal: _, # Ngo
		iPortuguese: u"Zerecoré",
	},
	
	### O ###
	
	"O Keo": {
		iEnglish: found("Pulo Condore"),
		iGreek: "Kattigara",
		iIndian: "Kirtinagara",
		iLatin: "Cattigara",
		iLangKhmer: _,
		iVietnamese: u"Óc Eo",
	},
	"O'okiep": {
		iDutch: relocate("Springbokfontein"),
		iEnglish: relocate("Port Nolloth"),
		iLocal: _,
	},
	"Obar Dheathain": {
		iCeltic: _,
		iChinese: "Aboding",
		iEnglish: "Aberdeen",
		iJapanese: "Abadiin",
		iLatin: found("Pinnata Castra"),
		iNorse: u"Apardjón",
		iRussian: "Aberdin",
		iTurkish: "Aberdin",
	},
	"Obdorsk": {
		iRussian: (
			translate("Salekhard", iAfter=iGlobal),
			_,
		),
	},
	"Ochakov": {  # founded on Mykolaiv
		iGreek: "Alektor",
		iRussian: _,
		iTurkish: u"Özü",
		iUkrainian: "Ochakiv",
	},
	"Oddernes": {
		iNorse: (
			relocate("Kristansand", iAfter=iRenaissance),
			_,
		),
	},
	"Odesa": {
		iGreek: u"Odhissós",
		iKorean: _,
		iPolish: "Odessa",
		iRussian: "Odessa",
		iTurkish: (
			found("Hacibey"),
			_,
		),
		iUkrainian: _,
	},
	"Oescus": {  # founded on Pleven
		iGreek: "Palatiolon",
		iLatin: _,
	},
	"Oguaa": {
		iDutch: found("Elmina"),
		iEnglish: (
			found("Fort Cormantin"),
			"Cape Coast",
		),
		iLocal: _,
		iPortuguese: (
			found("Elmina"),
			"Cabo Corso",
		),
		iSwedish: found("Carolusborg"),
	},
	"Okahandja": {
		iEnglish: found("Outjo"),
		iGerman: found("Outjo"),
		iLocal: _,
	},
	"Okango": {
		iCongolese: _,
		iDutch: relocate("Bandundu"),
		iFrench: relocate("Bandundu"),
	},
	"Okoloama": {
		iEnglish: (
			relocate("Port Harcourt", iAfter=iGlobal),
			"Bonny",
		),
		iLocal: _, # Igbo
	},
	"Olbia": {
		iByzantine: "Tharros",
		iGreek: "Tharras",
		iItalian: (
			found("Sassari", iAfter=iMedieval),
			translate("Olbia", iAfter=iGlobal),
			translate("Terranova Pausania", iAfter=iRenaissance),
			translate("Civita", iAfter=iMedieval),
			_,
		),
		iLatin: "Tarrae",
		iPhoenician: "Tara",
	},
	"Oldenburg": {
		iGerman: _,
		iItalian: "Oldemburgo",
		iPolish: "Starogard",
		iPortuguese: "Oldemburgo",
		iSpanish: "Oldemburgo",
	},
	"Oleksandrivsk": {
		iDutch: found("Chortitza"),
		iRussian: "Alexandrovsk",
		iUkrainian: (
			rename("Zaporizhia", iAfter=iGlobal),
			_,
		),
	},
	"Oleshky": {
		iRussian: (
			relocate("Kherson", iAfter=iRenaissance),
			_,
		),
	},
	"Olsztyn": {
		iGerman: "Allenstein",
		iLocal: translate("Alnasteini", iBefore=iMedieval), # Old Prussian
		iPolish: _,
		iRussian: "Ol'styn",
	},
	"Ondjiva": {
		iLocal: _,
		iPortuguese: u"Vila Pereira d'Eça",
	},
	"Ongoe": {  # founded on Chedzugwe
		iLocal: "Angwa",
		iPortuguese: _,
	},
	"Ongola": {
		iLocal: _,
		iEnglish: relocate("Jaunde"),
		iFrench: relocate("Jaunde"),
		iGerman: relocate("Jaunde"),
		iPortuguese: relocate("Jaunde"),
	},
	"Onslow": {
		iDutch: found("Willems Rivier"),
		iEnglish: _,
	},
	"Ooosook": {
		iArabic: "Sawakin",
		iEnglish: (
			relocate("Port Sudan", iAfter=iIndustrial),
			"Suakin",
		),
		iLatin: "Limen Evangelis",
		iNubian: _,
		iTurkish: "Sevakin",
	},
	"Opole": {
		iGerman: "Oppeln",
		iPolish: _,
	},
	"Opuwo": {
		iDutch: "Ohopoho",
		iEnglish: "Ohopoho",
		iGerman: "Ohopoho",
		iLocal: _,
		iPortuguese: found("Xangogo"),
	},
	"Oraea": {  # relocated from Gwadar
		iGreek: "Oraia",
		iLatin: _,
		iPersian: "Ormara",
	},
	"Ordu Baliq": {
		iChinese: "Woluduobali",
		iMongol: "Khar Balgas",
		iRussian: "Kara-Balgas",
		iTurkish: _,
	},
	"Orduqent": {
		iChinese: "Suiye",
		iPersian: "Suyab",
		iTurkish: (
			translate("Ak-Beshim", iAfter=iIndustrial),
			_,
		),
	},
	"Ordzhonikidze": {
		iLocal: "Dzaudzhikau", # Ossetian
		iRussian: (
			translate("Vladikavkaz", iAfter=iIndustrial),
			_,
		),
	},
	"Orekhov": {
		iRussian: (
			relocate("Sankt-Peterburg", iAfter=iRenaissance),
			_,
		),
		iSwedish: found("Nyen"),
	},
	"Orenburg": {
		iFrench: "Orenbourg",
		iGerman: _,
		iMongol: "Irinbur",
		iPortuguese: "Oremburgo",
		iRussian: (
			translate("Chkalov", bCommunist=True),
			_,
		),
		iSpanish: "Oremburgo",
		iTurkish: "Orinbor",
		iUkrainian: "Orenburh",
	},
	"Orense": {
		iCeltic: "Nemetobriga",
		iLatin: (
			found("Iuliobriga"),
			"Auria",
		),
		iLocal: _, # Galician
		iPortuguese: (
			found("Braganza"),
			"Ourense",
		),
		iSpanish: "Ourense",
	},
	"Orestias": {
		iGreek: _,
		iLatin: rename("Hadrianopolis"),
		iLocal: "Uskudama", # Thracian
	},
	u"Orléans": {
		iCeltic: "Cenabum",
		iFrench: _,
		iLatin: "Aurelianum",
	},
	"Orso": {  # founded on Malaqah
		iArabic: "Uxuna",
		iCeltic: _,
		iLatin: "Genetiva Iulia",
		iSpanish: "Osuna",
	},
	"Orugallu": {
		iDravidian: _,
		iEnglish: "Warangal",
		iPersian: translate("Sultanpur", iReligion=iIslam),
	},
	"Oruro": {  # renamed from Pariya
		iLocal: "Uru Uru",
		iSpanish: _,
	},
	"Osijek": {
		iCeltic: found("Sirmium"),
		iGerman: "Esseg",
		iGreek: found("Sirmium"),
		iLatin: (
			found("Sirmium"),
			"Mursa",
		),
		iLocal: _, # Croatian
		iPolish: "Osiek",
		iThai: "Osiyek",
	},
	"Oslo": {
		iArabic: "Uslu",
		iCeltic: u"Osló",
		iChinese: "Aosilu",
		iJapanese: "Osuro",
		iKorean: "Oseullo",
		iNorse: (
			rename("Kristiania", iPeriod=iPeriodDenmark, iAfter=iRenaissance, iBefore=iIndustrial),
			_,
		),
		iPersian: "Eslo",
	},
	"Otavi": {
		iLocal: _,
		iPortuguese: found(u"Vila Pereira d'Eça"),
	},
	"Otjomuise": {
		iDutch: "Windhoek",
		iGerman: "Windhuk",
		iLocal: _,
	},
	"Otomari": {
		iJapanese: _,
		iRussian: "Korsakov",
	},
	"Oudtshoorn": {
		iDutch: _,
		iEnglish: found("George"),
	},
	"Oviedo": {
		iCeltic: "Nowiion",
		iLatin: found("Lucus Asturum"),
		iLocal: u"Uviéu", # Asturian
		iSpanish: (
			relocate(u"Gijón", iAfter=iIndustrial),
			_,
		),
	},
	"Ox Te' Tuun": {
		iNahuatl: found("Xicalango"),
		iMayan: (
			translate("Calakmul", iAfter=iClassical),
			_,
		),
		iSpanish: found("Xicalango"),
	},
	"Oxford": {
		iCeltic: (
			found("Corinium"),
			"Rhydychen",
		),
		iChinese: "Niujin",
		iEnglish: _,
		iGreek: found("Corinium"),
		iJapanese: "Okkusufoodo",
		iKorean: "Okseupodeu",
		iLatin: found("Corinium"),
		iNorse: (
			found("Tamworth"),
			u"Uxnafurða",
		),
		iPolish: "Oksford",
		iPortuguese: u"Oxónia",
	},
	"Oxwitik": {
		iMayan: _,
		iNahuatl: "Copantl",
		iSpanish: (
			found("San Pedro Sula"),
			u"Copán",
		),
	},
	"Oyat": {
		iArabic: rename("Tripolis"),
		iGreek: "Oia",
		iLatin: (
			rename("Tripolis", iAfter=iMedieval),
			"Oea",
		),
		iPhoenician: _,
	},
	"Oyo-Ile": {  # relocated from Ilé-Ifè
		iEnglish: "Oyo",
		iLocal: (
			relocate("Ibadan", iAfter=iIndustrial),
			_,
		),
		iPortuguese: u"Oió",
	},
	
	### P ###
	
	"Pa' Chan": {
		iMayan: (
			translate("Yaxchilan", iAfter=iClassical),
			_,
		),
		iNahuatl: found("Tuchtlan"),
		iSpanish: relocate("Ciudad Real"),
	},
	"Pa'ula'ula o Hipo": {  # founded on Lihu'e
		iEnglish: "Fort Elizabeth",
		iPolynesian: _,
		iRussian: "Elizaventinskaya Krepost",
	},
	"Pa-Mwt": {
		iArabic: "Ad-Dakhla",
		iEgyptian: _,
		iEgyptianArabic: "El Dakla",
		iGreek: "Mothis",
	},
	u"Paço de Arcos": {  # founded on Devagiri
		iIndian: "Silvassa",
		iPortuguese: _,
	},
	"Padang": {
		iArabic: "Badangh",
		iChinese: "Badong",
		iDravidian: "Patan",
		iJapanese: "Padan",
		iKorean: _,
		iMalay: _,
		iPersian: "Pading",
		iThai: _,
	},
	"Paderborn": {
		iGerman: (
			relocate("Bielefeld", iAfter=iIndustrial),
			_,
		),
	},
	"Padua": {
		iChinese: "Paduowa",
		iDutch: _,
		iFrench: "Padoue",
		iGerman: _,
		iGreek: u"Padhóva",
		iItalian: "Padova",
		iKorean: "Padoba",
		iLatin: "Patavium",
		iLocal: "Padoa", # Venetian
		iPortuguese: u"Pádua",
		iSpanish: _,
		iSwedish: _,
	},
	"Pagan": {
		iBurmese: (
			relocate("Mandalay", iAfter=iIndustrial),
			_,
		),
		iIndian: "Arimaddanapura",
		iThai: "Phukham",
	},
	"Pagaruyung": {
		iMalay: (
			relocate("Padang", iAfter=iRenaissance),
			_,
		),
	},
	"Pahkatequayang": {
		iEnglish: "London",
		iLocal: _, # Anishinaabe
	},
	"Pahrah": {
		iEnglish: "Pura",
		iPersian: (
			rename("Iranshahr", iAfter=iGlobal),
			_,
		),
	},
	"Pakse": {  # renamed from Champassak
		iFrench: u"Paksé",
		iKhmer: _,
	},
	"Pakuan Pajajaran": {
		iDutch: "Buitenzorg",
		iJavanese: (
			translate("Bogor", bReconquest=True),
			_,
		),
	},
	"Palakollu": {  # founded on Masulipatnam
		iDutch: "Palikol",
		iEnglish: "Palacole",
		iIndian: _,
	},
	"Palembang": {
		iArabic: "Balimbanj",
		iChinese: "Jugang",
		iDravidian: "Palempan",
		iJapanese: "Parenban",
		iMalay: _,
	},
	"Palma": {
		iArabic: "Madina Mayurqa",
		iLatin: "Palmaria",
		iSpanish: _,
	},
	"Palmerston": {
		iDutch: found("Aernhems Landt"),
		iEnglish: (
			translate("Darwin", iAfter=iGlobal),
			_,
		),
		iLocal: "Garramilla", # Larrakia
	},
	"Palmyra": {
		iArabic: "Tadmur",
		iGreek: _,
		iLatin: _,
	},
	"Palu": {
		iDutch: "Paloe",
		iMalay: _,
	},
	"Pamplona": {
		iArabic: "Banbaluna",
		iChinese: "Panpuluona",
		iFrench: "Pampelune",
		iKorean: "Pampeullona",
		iLatin: "Pompaelo",
		iLocal: u"Iruña", # Basque
		iPolish: "Pampeluna",
		iSpanish: _,
	},
	"Panaji": {  # relocated from Govapuri
		iEnglish: "Panjim",
		iIndian: _,
		iLocal: "Ponnjem",
		iPortuguese: "Pangim",
	},
	"Panduranga": {
		iBurmese: "Paanduuraangyarr",
		iChinese: "Han Ro",
		iIndian: _,
		iJapanese: "Fan Ran",
		iLangKhmer: "Bandoureanhka",
		iLocal: "Panraun", # Cham
		iRussian: "Fanrang",
		iThai: "Panthurangka",
		iVietnamese: "Phan Rang",
	},
	"Pannai": {
		iJava: (
			relocate("Dumai", iAfter=iDigital),
			_,
		),
	},
	"Panormus": {
		iArabic: "Balharm",
		iChinese: "Balemo",
		iGreek: (
			found("Akragas"),
			"Panormos",
		),
		iItalian: "Palermo",
		iJapanese: "Parerumo",
		iKorean: "Pallereumo",
		iLatin: _,
		iPhoenician: found("Lilybaeum"),
	},
	"Pantikapaion": {
		iChinese: "Kechi",
		iGerman: "Kertsch",
		iGreek: _,
		iItalian: "Cercio",
		iPolish: "Kercz",
		iRussian: "Kerch",
		iTurkish: "Kerch",
	},
	"Panyu": {
		iChinese: (
			translate("Guangzhou", iAfter=iMedieval),
			_,
		),
		iDravidian: "Kuvanchu",
		iDutch: "Kanton",
		iEnglish: "Canton",
		iFrench: "Canton",
		iGerman: "Kanton",
		iGreek: "Kantona",
		iItalian: "Canton",
		iJapanese: "Koushuu",
		iKorean: "Gwangju",
		iPersian: "Khanfu",
		iPolish: "Kanton",
		iPortuguese: u"Cantão",
		iSpanish: u"Cantón",
		iThai: "Kwangcea",
		iTurkish: "Kanton",
		iVietnamese: "Quang Chau",
	},
	"Paquimeh": {
		iNahuatl: _,
		iSpanish: (
			translate("Nuevo Casas Grandes", iAfter=iIndustrial),
			"Casas Grandes",
		),
	},
	"Para": {
		iArabic: "Faras",
		iEgyptian: _,
		iCoptic: "Pharas",
		iGreek: "Pakhoras",
		iLatin: "Pachoras",
		iNubian: "Pakhoras",
	},
	u"Paraná": {
		iGerman: found("Spatzenkutter"),
		iSpanish: _,
	},
	"Parapatho": {
		iLocal: _,
		iPortuguese: (
			translate(u"António Enes", iAfter=iIndustrial),
			"Angoche",
		),
	},
	"Parau": {
		iPersian: (
			translate(u"Farâva", iAfter=iMedieval),
			_,
		),
		iRussian: "Kizyl-Arvat",
		iTurkish: (
			translate("Serdar", iAfter=iDigital),
			translate("Kyzyl-Arbat", iAfter=iRenaissance),
			"Kyzyl-Rabat",
		),
	},
	"Paris": {
		iArabic: "Baris",
		iCeltic: "Lutetia",
		iChinese: "Bali",
		iDutch: "Parijs",
		iFrench: _,
		iGerman: _,
		iGreek: u"Parísi",
		iItalian: "Parigi",
		iJapanese: "Pari",
		iKorean: "Pari",
		iLatin: (
			translate("Parisium", iAfter=iMedieval),
			"Lutetia Parisiorum",
		),
		iPolish: "Paryz",
		iPortuguese: _,
		iRussian: "Parizh",
		iSwedish: _,
		iTurkish: _,
		iVietnamese: "Ba-le",
	},
	"Pariya": {
		iQuechua: _,
		iSpanish: (
			rename("Oruro", iAfter=iIndustrial),
			"Paria",
		),
	},
	"Parsa": {
		iArabic: relocate("Sirajis"),
		iGreek: "Persepolis",
		iPersian: (
			relocate("Sirajis", iReligion=iIslam),
			_,
		),
	},
	"Pasai": {
		iMalay: (
			translate("Lhokseumawe", iAfter=iRenaissance),
			_,
		),
	},
	"Pasargad": {
		iGreek: "Pathragada",
		iLatin: "Pasargadae",
		iPersian: _,
	},
	"Passagem": {
		iPortuguese: (
			translate("Petrolina", iAfter=iIndustrial),
			_,
		),
	},
	"Passau": {
		iChinese: "Pashao",
		iGerman: _,
		iItalian: "Passavia",
		iLatin: "Castra Batava",
		iPolish: "Pasawa",
	},
	"Passo Fundo": {
		iGerman: found("Novo Hamburgo"),
		iItalian: found("Nova Trento"),
		iPortuguese: (
			relocate("Caxias do Sul", iAfter=iIndustrial),
			_,
		),
	},
	"Pataliputra": {
		iChinese: "Palinfu",
		iEnglish: rename("Patna"),
		iGreek: "Palibothra",
		iIndian: _,
		iPersian: translate("Azimabad", iReligion=iIslam),
		iTibetan: "Gron Khyer Me Tog",
	},
	"Patuanak": {
		iEnglish: _,
		iLocal: u"Wapâciwanâhk", # Cree
	},
	"Pau": {
		iCeltic: found("Elusa"),
		iFrench: _,
		iLatin: found("Elimberris"),
		iLocal: "Paue", # Basque
	},
	"Payne Bay": {
		iEnglish: _,
		iLocal: "Kangirsuk", # Inuktitut
	},
	"Peace River": {
		iEnglish: (
			translate("Fort Fork", bSmall=True),
			_,
		),
		iFrench: u"Rivière-la-Paix",
	},
	"Pekan": {
		iMalay: (
			translate("Kuantan", iAfter=iGlobal),
			_,
		),
	},
	"Pelican Narrows": {
		iEnglish: _,
		iLocal: u"Opâwikoscikanihk", # Cree
	},
	"Pella": {
		iGreek: (
			relocate("Thessaloniki", iAfter=iMedieval),
			_,
		),
		iLatin: relocate("Thessaloniki"),
	},
	"Pelly Bay": {
		iEnglish: _,
		iLocal: "Kugaaruk", # Inuktitut
	},
	"Pemba": {  # founded on Ibo
		iPortuguese: u"Porto Amélia",
		iKiswahili: _,
	},
	"Pengcheng": {
		iChinese: (
			translate("Xuzhou", iAfter=iMedieval),
			_,
		),
	},
	"Penglai": {
		iChinese: (
			translate("Yantai", iAfter=iIndustrial),
			translate("Dengzhou", iAfter=iMedieval),
			_,
		),
		iEnglish: relocate("Weihaiwei"),
	},
	"Penong": {
		iDutch: found("Eijland St. Fran"),
		iEnglish: _,
	},
	"Peoria": {
		iEnglish: _,
		iFrench: found("Fort Crevecoeur"),
	},
	"Per-Atum": {
		iArabic: relocate("Fayed"),
		iEgyptian: _,
		iGreek: "Heroopolis",
	},
	"Per-Amun": {
		iArabic: (
			translate("Bursa'id", iAfter=iIndustrial),
			"Al-Farama",
		),
		iCoptic: "Peremoun",
		iEgyptian: (
			relocate("Per-Ramessu", bCapital=True),
			_,
		),
		iEgyptianArabic: (
			translate("Borsa'id", iAfter=iIndustrial),
			"El-Farama",
		),
		iEnglish: "Port Said",
		iFrench: "Port Said",
		iGreek: "Pelousion",
		iLatin: "Pelusium",
	},
	"Per-Medjed": {  # founded on Henen-Nesut
		iArabic: relocate("Al-Minya"),
		iCoptic: "Pemdje",
		iEgyptian: _,
		iGreek: "Oxyrrhynkhopolis",
		iLatin: "Oxyrrhynchus",
	},
	"Per-Ramessu": {  # relocated from Per-Amun
		iEgyptian: _,
		iGreek: "Avaris",
	},
	"Per-Wadjet": {
		iArabic: relocate("Rashid"),
		iEgyptian: _,
		iGreek: "Bouto",
		iLatin: "Buto",
	},
	"Peremyotnoye": {
		iRussian: _,
		iTurkish: "Peremetnoe",
	},
	"Pereyaslavl": {
		iRussian: (
			translate("Ryazan", iAfter=iRenaissance),
			_,
		),
	},
	"Pergamon": {
		iByzantine: relocate("Bursa"),
		iGreek: _,
		iHittite: found("Wilusa"),
		iLatin: "Pergamus",
		iModernGreek: "Pergamos",
		iTurkish: relocate("Bursa"),
	},
	"Permskoye": {
		iRussian: (
			translate("Komsomolsk-na-Amure", bCommunist=True),
			_,
		),
	},
	"Perona": {
		iGerman: "Pernau",
		iLatin: _,
		iLocal: u"Pärnu", # Estonian
		iPolish: "Parnawa",
		iRussian: "Pirny",
	},
	"Perpignan": {
		iFrench: _,
		iItalian: "Perpignano",
		iLocal: "Perpinhan", # Occitan
		iPortuguese: u"Perpinhão", # Portuguese
		iSpanish: u"Perpiñán",
	},
	"Perusia": {
		iChinese: "Peilujia",
		iFrench: u"Pérouse",
		iGreek: _,
		iItalian: "Perugia",
		iJapanese: "Peruuja",
		iKorean: "Peruja",
		iLatin: _,
		iPortuguese: u"Perúsia",
		iSpanish: "Perusa",
	},
	"Peshawar": {  # relocated from Pushkalavati
		iArabic: "Parashawar",
		iChinese: "Baishawa",
		iIndian: "Purushapura",
		iLocal: "Pishaur", # Punjabi
		iPersian: (
			translate("Peshawar", iReligion=iIslam),
			"Peskabvar",
		),
		iThai: "Petwa",
	},
	"Pest": {
		iLocal: ( # Hungarian
			rename("Budapest", iAfter=iIndustrial),
			_,
		),
	},
	"Petawawa": {
		iEnglish: _,
		iFrench: found("Fort Dumoine"),
	},
	"Petrograd": {  # renamed from Sankt-Peterburg
		iItalian: "Pietrogrado",
		iJapanese: "Petoroguraado",
		iPolish: u"Piotrogród",
		iPortuguese: "Petrogrado",
		iRussian: (
			rename("Leningrad", bCommunist=True),
			rename("Sankt-Peterburg", bRepublican=False),
			_,
		),
		iSpanish: "Petrogrado",
	},
	"Petropavlovsk": {
		iRussian: (
			translate("Petropavlovsk-Kamchatskiy", iAfter=iGlobal),
			_,
		),
	},
	"Petropavl": {
		iRussian: "Petropavlovsk",
		iTurkish: _,
	},
	"Petrozadovsk": {
		iLocal: u"Äänislinna", # Finnish
		iRussian: (
			translate("Petrovskaya Sloboda", iBefore=iRenaissance),
			_,
		),
		iSwedish: "Onegaborg",
	},
	"Phaselis": {  # relocated from Attaleia
		iGreek: _,
		iTurkish: "Faselis",
	},
	"Philadelphia": {
		iEnglish: _,
		iSwedish: found(u"Nya Göteborg"),
	},
	"Phitsanulok": {
		iKhmer: "Song Khwae",
		iThai: (
			relocate("Sukhotai", bCapital=True),
			_,
		),
	},
	"Phnom Penh": {
		iArabic: "Bnom Benh",
		iChinese: "Jinbian",
		iGreek: "Pnom Pench",
		iJapanese: "Punonpen",
		iLangKhmer: _,
		iKorean: "Peunompen",
		iPersian: "Pnom Pen",
		iSpanish: "Nom Pen",
		iVietnamese: "Nam Vang",
	},
	"Phraaspa": {  # founded on Gazaka
		iMongol: relocate("Tabriz"),
		iPersian: (
			translate("Maragheh", iAfter=iMedieval),
			_,
		),
		iTurkish: relocate("Tabriz", iBefore=iRenaissance),
	},
	"Pietersburg": {  # relocated from Mapungubwe
		iDutch: _,
		iLocal: "Polokwane",
		iPortuguese: u"São Petersburgo",
	},
	"Pingcheng": {
		iChinese: (
			translate("Datong", iAfter=iMedieval),
			_,
		),
		iManchu: "Xijing",
	},
	"Pingyang": {
		iChinese: (
			translate("Linfen", iAfter=iMedieval),
			_,
		),
	},
	"Pinnata Castra": {  # founded on Obvar Dheathain
		iGreek: "Pteroton Stratopedon",
		iLatin: _,
	},
	"Piopiotahi": {
		iEnglish: relocate("Invercargill"),
		iPolynesian: _,
	},
	"Pipli": {  # founded on Chandraketugarh
		iDutch: "Pipely",
		iNorse: _,
	},
	"Pisco": {  # relocated from Inkawasi
		iQuechua: "Pisqu",
		iSpanish: _,
	},
	"Pithoria": {
		iEnglish: rename("Ranchi"),
		iIndian: _,
		iPersian: "Khukhragarh",
	},
	"Pitic": {
		iMexican: rename("Hermosillo", iGreatGenerals=1),
		iSpanish: _,
	},
	"Pittsburgh": {
		iEnglish: _,
		iFrench: "Fort Duquesne",
	},
	"Pleskov": {
		iArabic: "Bskuf",
		iChinese: "Pusikefu",
		iEnglish: "Plescow",
		iGerman: "Pleskau",
		iJapanese: "Pusukofu",
		iPolish: u"Psków",
		iRussian: (
			translate("Pskov", iAfter=iRenaissance),
			_,
		),
		iSpanish: "Peskov",
	},
	"Plettenbergbaai": {
		iDutch: _,
		iEnglish: "Plettenberg Bay",
		iLocal: "Knysna",
		iPortuguese: "Bahia Formosa",
	},
	"Pleven": {
		iGerman: "Plewen",
		iGreek: found("Oescus"),
		iLatin: found("Oescus"),
		iLocal: _, # Bulgarian
		iPolish: "Plewen",
		iRussian: "Plevna",
		iTurkish: "Plevne",
	},
	"Plock": {
		iGerman: (
			translate(u"Schröttersburg", bFascist=True),
			"Plotzk",
		),
		iPolish: _,
		iRussian: "Plotsk",
	},
	"Plovdiv": {
		iGreek: "Philippopolis",
		iItalian: "Filippopoli",
		iGerman: "Plowdiw",
		iLatin: "Trimontium",
		iLocal: (
			translate("Pulpudeva", iBefore=iClassical), # Thracian
			_, # Bulgarian
		),
		iModernGreek: u"Philippúpoli",
		iPolish: "Plowdiw",
		iRussian: _,
		iTurkish: "Filibe",
	},
	"Plymouth": {
		iCeltic: found("Isca"),
		iChinese: "Pulimaosi",
		iDutch: "Pleimuiden",
		iEnglish: _,
		iLatin: found("Isca"),
		iLocal: "Aberplym", # Cornish
	},
	"Plzen": {
		iDutch: "Pilsen",
		iEnglish: "Pilsen",
		iGerman: "Pilsen",
		iItalian: "Pilsen",
		iLocal: _, # Czech
		iPolish: "Pilzno",
	},
	"Point Hope": {
		iEnglish: _,
		iLocal: "Tikigaq", # Inupiaq
	},
	"Pointe-Noire": {  # founded on Bwali
		iCongolese: "Njinji",
		iFrench: _,
		iPortuguese: "Ponta Negra",
	},
	"Poitiers": {
		iCeltic: "Lemonum",
		iFrench: _,
		iLatin: "Pictavium",
	},
	"Pokesu": {  # founded on Krindjabo
		iDutch: "Hollandia",
		iEnglish: (
			translate("Princes Town"),
			"Fort Fredericksburg",
		),
		iGerman: u"Groß-Friedrichsburg",
		iLocal: _,
	},
	"Pokrovsk": {
		iGerman: "Kosakenstadt",
		iRussian: (
			translate("Engels", bCommunist=True),
			_,
		),
	},
	"Polotsk": {
		iGerman: "Polotzk",
		iPolish: "Polock",
		iRussian: _,
	},
	"Populonium": {
		iItalian: (
			found("Siena"),
			"Piombino",
		),
		iLatin: _,
		iLocal: "Populonia", # Etruscan
	},
	"Pori": {
		iLatin: "Arctopolis",
		iLocal: _, # Finnish
		iSwedish: u"Björneborg",
	},
	"Port Essington": {
		iEnglish: _,
		iMalay: found("Marege"),
	},
	"Port Hedland": {
		iDutch: found("G.F. de Wits Landt"),
		iEnglish: _,
	},
	"Port Lincoln": {
		iEnglish: _,
		iFrench: "Port Champagny",
		iLocal: "Galinyala", # Barngarla
	},
	"Port Louis": {
		iEnglish: _,
		iFrench: "Port-Louis",
	},
	"Port Nolloth": {  # relocated from Port Nolloth
		iEnglish: _,
		iLocal: "Aukwatowa",
	},
	"Port Royal": {
		iEnglish: (
			translate("Kingston", iAfter=iIndustrial),
			_,
		),
		iSpanish: found("Santiago de la Vega"),
	},
	"Port Sudan": {  # relocated from Oosook
		iArabic: "Bur Sudan",
		iEnglish: _,
		iNubian: "Bar'uut",
	},
	"Port-au-Prince": {
		iFrench: (
			translate(u"Port Républicain", bRepublican=True),
			_,
		),
		iLocal: "Yaguana", # Taino
		iPortuguese: u"Porto Príncipe",
		iSpanish: (
			found("Santa Maria del Puerto"),
			u"Puerto Príncipe",
		),
	},
	u"Port-aux-Français": {
		iDutch: "Nieuw-Amsterdam Eiland",
		iEnglish: "Heard Island",
		iFrench: _,
		iPortuguese: u"Ilha São Paulo"
	},
	"Port-Royal": {  # founded on Halifax
		iEnglish: "Annapolis Royal",
		iFrench: _,
		iLocal: "Nme'juaqnek", # Mi'kmaq
	},
	"Portel": {
		iDutch: found("Fort Oranje"),
		iPortuguese: _,
	},
	"Porth Madryn": {  # founded on Las Grutas
		iCeltic: _,
		iSpanish: "Puerto Madryn",
	},
	"Porto": {
		iArabic: "Burtugal",
		iCeltic: "Tongobriga",
		iEnglish: "Oporto",
		iItalian: "Oporto",
		iJapanese: "Poruto",
		iLatin: "Portus Cale",
		iPortuguese: _,
		iSpanish: "Oporto",
	},
	"Porto Calvo": {
		iDutch: found("Fort Bass"),
		iPortuguese: _,
	},
	"Porto Real": {
		iPortuguese: (
			translate("Porto Nacional", bRepublican=True),
			_,
		),
	},
	"Porto Seguro": {
		iLocal: "Agbodrafo",
		iPortuguese: _,
	},
	"Porto-Novo": {  # founded on Glexwé
		iLocal: _, # Yoruba
		iPortuguese: _,
	},
	"Portsmouth": {
		iCeltic: found("Durovernum"),
		iEnglish: _,
		iLatin: found("Durovernum"),
	},
	"Poste de Arkansea": {  # founded on Jonesboro
		iEnglish: "Arkansas Post",
		iFrench: _,
		iSpanish: "Puesto de Arkansas",
	},
	"Poste-de-la-Baleine": {
		iEnglish: "Great Whale River",
		iFrench: _,
		iLocal: "Kuujjuarapik", # Inuktitut
	},
	"Poti": {
		iGreek: "Phasis",
		iLocal: _, # Georgian
	},
	u"Potosí": {  # founded on Q'ochapampa
		iQuechua: "Potojsi",
		iSpanish: _,
	},
	"Poznan": {
		iChinese: "Bozinan",
		iDutch: "Posen",
		iGerman: "Posen",
		iJapanese: "Pozunani",
		iKorean: "Pojeunan",
		iPolish: _,
		iPortuguese: u"Posnânia",
	},
	"Pragjyotishpura": {
		iIndian: (
			translate("Guwahati", iAfter=iRenaissance),
			_,
		),
	},
	"Praha": {
		iArabic: "Birag",
		iChinese: "Bulage",
		iDutch: "Praag",
		iEnglish: "Prague",
		iFrench: "Prague",
		iGerman: "Prag",
		iGreek: u"Prága",
		iItalian: "Praga",
		iJapanese: "Puraha",
		iKorean: "Peuraha",
		iLatin: "Praga",
		iLocal: _, # Czech
		iMalay: _,
		iNorse: "Prag",
		iPolish: "Praga",
		iPortuguese: "Praga",
		iRussian: "Praga",
		iSpanish: "Praga",
		iTurkish: "Prag",
		iUkrainian: _,
	},
	"Presporok": {
		iCeltic: u"An Bhratasláiv",
		iChinese: "Buladisilafa",
		iEnglish: "Pressburg",
		iFrench: "Presbourg",
		iGerman: u"Preßburg",
		iGreek: "Istropolis",
		iItalian: "Posonia",
		iJapanese: "Burachisuraba",
		iKorean: "Beuratiseullaba",
		iLatin: "Posonium",
		iLocal: (  # Slovakian
			translate("Bratislava", iAfter=iIndustrial),
			_,
		),
		iModernGreek: u"Presvoúrgo",
		iPolish: "Bratyslawa",
		iUkrainian: "Bratyslava",
	},
	"Pretoria": {
		iDutch: _,
		iEnglish: _,
		iLocal: "E-Pitoli",
		iPortuguese: u"Pretória",
	},
	"Prey Nokor": {
		iBurmese: "Sainggonmyo",
		iChinese: "Xigong",
		iEnglish: "Saigon",
		iFrench: "Saigon",
		iJapanese: "Katei",
		iLangKhmer: _,
		iKorean: "Gajeong",
		iLocal: "Baigaur", # Cham
		iSpanish: u"Saigón",
		iThai: "Saingon",
		iVietnamese: (
			translate("Thanh Pho Ho Chi Minh", bCommunist=True),
			translate("Sai Gon", iAfter=iIndustrial),
			"Gia Dinh",
		),
	},
	"Prince Albert": {
		iEnglish: _,
		iFrench: found("Fort de la Corne"),
	},
	"Probolinggo": {
		iJavanese: u"Pråbålinggå",
		iMalay: _,
	},
	"Pselqet": {
		iArabic: "Ad-Dakka",
		iEgyptian: _,
		iEgyptianArabic: "El-Dakka",
		iGreek: "Pselchis",
		iNubian: found("Silimi"),
	},
	"Ptolemais Hermiou": {  # renamed from Akka
		iEgyptian: u"Psoï",
		iArabic: "El Mansha",
		iCoptic: "Bsoi",
		iGreek: _,
		iLatin: "Ptolemais Thebais",
	},
	"Pucallpa": {
		iLocal: "May Ushin", # Shipibo
		iQuechua: "Puka Allpa",
		iSpanish: _,
	},
	"Pudoga": {
		iLocal: "Puudosi", # Finnish
		iRussian: (
			translate("Pudozh", iAfter=iRenaissance),
			_,
		),
	},
	"Puducherry": {  # relocated from Kanchipuram and Mahabalipuram
		iDravidian: _,
		iEnglish: "Pondicherry",
		iFrench: u"Pondichéry",
	},
	"Puerto Baquerizo Moreno": {
		iEnglish: found("Seymour"),
		iSpanish: _,
	},
	u"Puerto Córdova": {  # founded on Haines
		iEnglish: "Cordova",
		iSpanish: _,
	},
	"Puerto Lempira": {  # founded on Black River
		iLocal: "Auhya Yari",
		iSpanish: _,
	},
	"Puerto Montt": {
		iLocal: "Meli Pulli", # Mapundugun
		iSpanish: _,
	},
	u"Puerto Peñasco": {
		iEnglish: "Rocky Point",
		iLocal: "Ge'e Suidagi", # O'odham
		iSpanish: _,
	},
	u"Puerto del Príncipe": {
		iSpanish: (
			translate(u"Camagüey", iAfter=iRenaissance),
			_,
		),
	},
	"Pukekura": {
		iEnglish: relocate("Dunedin"),
		iPolynesian: _,
	},
	"Pula": {
		iCeltic: found("Tharsatica"),
		iDutch: "Pola",
		iFrench: "Pola",
		iGerman: "Polei",
		iGreek: "Polis",
		iItalian: "Pola",
		iLatin: (
			found("Iader"),
			"Pietas Iulia",
		),
		iLocal: _, # Croatian
	},
	"Pulicat": {  # relocated from Mahabalipuram
		iDutch: "Casteel Geldria",
		iIndian: _,
		iPortuguese: "Paliacate",
	},
	"Pulo Condore": {  # founded on O Keo
		iEnglish: _,
		iFrench: "Poulo Condore",
		iMalay: _,
		iVietnamese: u"Con Đao",
	},
	"Punawadi": {
		iEnglish: "Poona",
		iHarappan: found("Daimabad"),
		iIndian: (
			translate("Pune", bResurrected=True),
			translate("Punyavishaya", iAfter=iMedieval),
			_,
		),
		iPersian: (
			found("Ahmednagar"),
			"Muhiyabad",
		),
	},
	"Puno": {  # renamed from Hatunqulla
		iQuechua: "Punu",
		iSpanish: _,
	},
	"Punvaranogadh": {
		iIndian: (
			relocate("Bhuj", iAfter=iRenaissance),
			_,
		),
	},
	"Pushkalavati": {
		iChinese: "Poshikielofati",
		iHarappan: found("Lewan"),
		iIndian: (
			relocate("Peshawar", iAfter=iMedieval),
			_,
		),
		iGreek: "Peukelaitis",
		iPersian: "Vaekereta",
	},
	"Pwn": {
		iBerber: "Beleb el-Anab",
		iByzantine: "Hippona",
		iFrench: u"Bône",
		iGreek: "Aphrodision",
		iItalian: "Bona",
		iLatin: "Hippo Regius",
		iPhoenician: _,
		iSpanish: "Bona",
		iTurkish: "Annaba",
	},
	"Pyeongyang": {
		iArabic: "Byawnyangh",
		iDutch: "Pyongyang",
		iChinese: "Pingrang",
		iEnglish: "Pyongyang",
		iFrench: "Pyongyang",
		iGerman: "Pjöngjang",
		iItalian: "Pyongyang",
		iJapanese: "Heijou",
		iKorean: _,
		iMalay: "Pyongyang",
		iNorse: "Pyongyang",
		iPolish: "Phenian",
		iPortuguese: "Pyongyang",
		iRussian: "Pkhenyan",
		iSpanish: "Pyongyang",
		iTurkish: "Pyongyang",
		iVietnamese: "Binh Nhuong",
	},
	"Pyora": {
		iRussian: (
			translate("Shimanovsk", bCommunist=True),
			_,
		),
	},
	u"Pécs": {
		iGerman: u"Fünfkirchen",
		iGreek: "Sophiane",
		iItalian: "Cinquechiese",
		iLatin: "Sopianae",
		iLocal: _, # Hungarian
		iPolish: "Pecz",
		iTurkish: "Pech",
	},
	u"Périgueux": {
		iCeltic: "Vesunna",
		iFrench: _,
		iLatin: "Vesunna",
		iLocal: "Peireguers",
	},
	
	### Q ###
	
	"Q'illu Uta": {
		iQuechua: _,
		iSpanish: (
			found(u"Valparaíso"),
			"Quillota",
		),
	},
	"Q'ochapampa": {
		iQuechua: _,
		iSpanish: (
			found(u"Potosí"),
			"Cochabamba",
		),
	},
	"Q'umarkaj": {
		iMayan: _,
		iNahuatl: "Utatlan",
		iSpanish: (
			found("Quetzaltenango"),
			u"Utatlán",
		),
	},
	"Qabala": {
		iArabic: _,
		iPersian: (
			relocate("Ganja", iAfter=iMedieval),
			"Gabala",
		),
		iRussian: relocate("Ganja"),
		iSpanish: "Gabala",
		iTurkish: "Kebele",
	},
	"Qaghiliq": {
		iChinese: (
			translate("Yecheng", iAfter=iMedieval),
			"Xiye",
		),
		iMongol: _,
		iTurkish: "Kargilik",
	},
	"Qal'at Rabah": {
		iArabic: _,
		iCeltic: found("Consuegra"),
		iLatin: found("Consuegra"),
		iSpanish: (
			found("Ciudad Real"),
			relocate("Ciudad Real", iAfter=iRenaissance),
			"Calatrava",
		),
	},
	"Qana": {
		iArabic: (
			translate("Bi'r Ali", iReligion=iIslam),
			_,
		),
		iGreek: "Kane",
		iLatin: "Cana",
	},
	"Qara Qorum": {
		iChinese: "Halahelin",
		iMongol: _,
		iRussian: "Karakorum",
	},
	"Qarqan": {
		iChinese: "Qiemo",
		iTurkish: _,
	},
	"Qart-Hadasht": {
		iArabic: (
			relocate("Tunus"),
			"Qartaj",
		),
		iByzantine: "Karthago",
		iGreek: "Karkhedon",
		iLatin: "Carthago",
		iPhoenician: _,
	},
	"Qartan": {
		iArabic: (
			found("Mustaganim"),
			"Tanas",
		),
		iFrench: u"Ténès",
		iGreek: "Kartennai",
		iLatin: "Cartennae",
		iPhoenician: _,
		iPortuguese: u"Tenés",
		iSpanish: u"Tenés",
	},
	"Qatrun": {
		iArabic: _,
		iItalian: "Gatrone",
	},
	"Qazimbazar": {  # founded on Bishnupur
		iEnglish: "Cassimbazar",
		iPersian: _,
	},
	"Qianzhong": {
		iChinese: (
			relocate("Huaihua", iAfter=iMedieval),
			_,
		),
	},
	"Qianzhou": {
		iChinese: (
			translate("Ganzhou", iAfter=iMedieval),
			_,
		),
	},
	"Qinglong": {
		iChinese: (
			translate("Shanghai", iAfter=iRenaissance),
			_,
		),
		iEnglish: _,
		iFrench: _,
		iGerman: _,
		iGreek: u"Sankái",
		iItalian: _,
		iJapanese: "Shanhai",
		iKorean: "Sanghae",
		iMongol: "Shankhain",
		iPolish: "Szanghaj",
		iPolynesian: "Hangahai",
		iPortuguese: "Xangai",
		iRussian: "Shankhay",
		iSpanish: _,
		iTurkish: "Shangay",
		iVietnamese: "Thuong Hai",
	},
	"Qiongzhou": {
		iChinese: (
			translate("Haikou", iAfter=iIndustrial),
			_,
		),
	},
	"Qiz Yar": {  # founded on Mariupol
		iRussian: (
			translate("Melitopol", iAfter=iIndustrial),
			"Novoolexandrivka",
		),
		iTurkish: _,
	},
	"Qocho": {
		iChinese: (
			relocate("Turpan", iAfter=iMedieval),
			"Gaochang",
		),
		iKushan: "Kara-Khojo",
		iTurkish: (
			relocate("Turpan", iAfter=iMedieval),
			_,
		),
	},
	"Qohaito": {
		iEgyptian: found("Adulis"),
		iEthiopian: _,
		iGreek: "Koloe",
		iItalian: relocate("Asmara"),
		iLatin: "Coloe",
	},
	"Qonirat": {
		iRussian: (
			translate("Kungrad", iAfter=iDigital),
			"Zheleznodorozhny",
		),
		iTurkish: _,
	},
	"Qoqak": {
		iChinese: "Tacheng",
		iTurkish: _,
	},
	"Queenstown": {
		iEnglish: _,
		iLocal: "Komani",
	},
	"Quelimane": {
		iJapanese: "Kerimane",
		iPortuguese: _,
		iSwahili: "Mkalimani",
	},
	"Quetzaltenango": {  # founded on Q'umarkaj
		iMayan: u"Xelajú",
		iSpanish: _,
	},
	"Qufu": {
		iChinese: _,
		iKorean: "Gokbu",
	},
	"Qulqi Tampu": {  # founded on Viluma
		iQuechua: _,
		iSpanish: "Coquimbo",
	},
	"Qupayapu": {
		iQuechua: _,
		iSpanish: u"Copiapó",
	},
	"Qurtubah": {
		iArabic: _,
		iCeltic: found("Ibolca"),
		iDutch: "Cordoba",
		iEnglish: "Cordova",
		iFrench: "Cordoue",
		iGerman: "Cordoba",
		iGreek: "Kordhova",
		iItalian: "Cordova",
		iJapanese: "Korudoba",
		iKorean: "Koreudoba",
		iLatin: "Corduba",
		iPhoenician: "Qart-Oba",
		iPolish: "Kordowa",
		iPortuguese: u"Córdova",
		iSpanish: u"Córdoba",
	},
	"Qusqu": {
		iEnglish: "Cusco",
		iQuechua: _,
		iSpanish: "Cuzco",
	},
	u"Québec": {
		iEnglish: "Quebec",
		iFrench: _,
		iLocal: u"Kébec", # Algonquian
	},
	"Qyzyl-Su": {
		iRussian: "Krasnovodsk",
		iTurkish: (
			translate(u"Türkmenbashy", iAfter=iDigital),
			_,
		),
	},
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	"Rajshahi": {  # relocated from Lakshmanavati
		iEnglish: "Beuleah",
		iPersian: _,
	},
	"Ranchi": {  # renamed from Chutia
		iEnglish: "Rachi",
		iIndian: _,
	},
	"Rasappa": {  # founded on Nikephorion
		iArabic: "Al-Resafa",
		iBabylonian: _,
		iByzantine: "Sergiopolis",
		iGreek: "Rhesapha",
		iLatin: "Risapa",
	},
	"Rashid": {  # relocated from Per-Wadjet
		iArabic: _,
		iCoptic: "Rashit",
		iEgyptian: "Ra-Shadi",
		iEnglish: "Rosetta",
		iFrench: "Rosette",
		iGreek: "Bolbitine",
		iItalian: "Rosetta",
		iTurkish: "Reshid",
	},
	"Rhizounta": {
		iChinese: "Ruizi",
		iDravidian: "Heccisi",
		iEthiopian: "Rizi",
		iGreek: _,
		iIndian: "Raiz",
		iLatin: "Rhizaeum",
		iRussian: "Riza",
		iTurkish: "Rize",
	},
	"Rigolet": {  # founded on Makkovik
		iFrench: _,
		iLocal: u"Tikigâksuagusik", # Inuktitut
	},
	"Rostov-na-Donu": {  # relocated from Cherkassk
		iPolish: u"Rostów nad Donem",
		iRussian: _,
	},
	"Rusibis": {
		iArabic: (
			translate("Al-Jadida", iAfter=iIndustrial),
			"Al-Breyja",
		),
		iBerber: "Mazighen",
		iLatin: "Portus Rutilis",
		iPhoenician: _,
		iPortuguese: u"Mazagão",
		iSpanish: "El Yadida",
	},
	"Saayi": {  # relocated from Lulami
		iArabic: "Saayi",
		iFrench: "Say",
	},
	"Safaqis": {  # founded and relocated from Tayinat
		iArabic: _,
		iBerber: "Ksar Sfaekez",
		iFrench: "Sfax",
		iGreek: "Taphrouria",
		iLatin: "Taparura",
		iTurkish: "Safakes",
	},
	"Saghalien Ula": {  # relocated from Aihun
		iChinese: (
			rename("Heihe", iAfter=iDigital),
			"Heilongjiang Cheng",
		),
		iManchu: _,
	},
	"Saidpur": {
		iGreek: "Alexandreia Nikaia",
		iHarappa: found("Harappa"),
		iIndian: _,
		iPersian: (
			relocate("Gujranwala", iAfter=iIndustrial),
			"Eminabad",
		),
	},
	"Sakkwato": {  # relocated from Birnin Kebbi
		iEnglish: "Sokoto",
		iLocal: _,
		iPortuguese: "Socoto",
	},
	"San Pedro Sula": {  # founded on Oxwitik
		iNahuatl: "Sollan",
		iSpanish: _,
	},
	"Sanggyeong": {  # founded on Mudanjiang
		iChinese: "Shangjing",
		iKorean: _,
	},
	"Sankt-Peterburg": {  # relocated from Nyen and Orekhov
		iArabic: "Sant Bitarsburg",
		iCeltic: "Cathair Pheadair",
		iChinese: "Sheng Bidebao",
		iDutch: "Sint-Petersburg",
		iEnglish: "Saint Petersburg",
		iFrench: u"Saint-Pétersbourg",
		iGerman: "Sankt Petersburg",
		iItalian: "San Pietroburgo",
		iJapanese: "Sankuto Peteruburuku",
		iKorean: "Sangteu Petereubureukeu",
		iLatin: "Petropolis",
		iNorse: "Sankt-Petersborg",
		iPolish: "Sankt Petersburg",
		iPortuguese: u"São Petersburgo",
		iRussian: (
			rename("Leningrad", bCommunist=True),
			rename("Petrograd", bRepublican=True),
			_,
		),
		iSpanish: "San Petersburgo",
		iSwedish: "Sankt Petersburg",
		iTurkish: _,
		iVietnamese: "Xanh Pe-tec-bua",
	},
	"Santa Luzia": {
		iPortuguese: (
			translate(u"Brasília", bCapital=True),
			translate(u"Luziânia", iAfter=iIndustrial),
			_,
		),
	},
	"Santiago de la Vega": {  # founded on Port Royal
		iEnglish: "Spanish Town",
		iSpanish: _,
	},
	"Sarqan": {
		iRussian: "Sarkand",
		iTurkish: _,
	},
	"Sassari": {  # founded on Olbia
		iItalian: _,
		iLocal: u"Tàtari",
		iSpanish: u"Sáçer",
		iPortuguese: u"Sássari",
	},
	"Sawhaj": {  # relocated from Abdju
		iArabic: _,
		iCoptic: "Bompaho",
		iEgyptianArabic: "Sohag",
		iGreek: "Bompae",
		iTurkish: "Sevhac",
	},
	"Saylac": {
		iArabic: "Zayla",
		iEnglish: "Zeila",
		iEthiopian: found("Asayeta"),
		iFrench: (
			found("Djibouti"),
			"Zeilah",
		),
		iGreek: "Avalites",
		iSomali: _,
		iPortuguese: u"Zeilá",
	},
	"Scarborough": {  # founded on Newcastle
		iEnglish: _,
		iNorse: u"Skarðaborg",
	},
	"Sebasteia": {  # founded on Kammama
		iGreek: _,
		iLatin: "Sebastia",
		iTurkish: "Sivas",
	},
	u"Sédhiou": {  # founded on Koldaa
		iFrench: _,
		iLocal: u"Seéju",
	},
	"Segobriga": {  # founded on Cuenca
		iCeltic: _,
		iLatin: _,
		iSpanish: "Saelices",
	},
	"Seleukeia": {
		iArabic: (
			relocate("Baghdad"),
			"Bahurasir",
		),
		iGreek: _,
		iLatin: "Seleucia",
		iPersian: (
			rename("Tysfwn"),
			"Veh-Ardashir",
		),
	},
	"Semarang": {  # relocated from Jepara
		iDutch: "Samarang",
		iJavanese: _,
	},
	"Seoul": {  # renamed from Wiryeseong
		iCeltic: u"Súl",
		iChinese: "Shou'er",
		iDravidian: "Ciyol",
		iDutch: "Seoel",
		iEnglish: "Seoul",
		iFrench: u"Séoul",
		iGerman: u"Söul",
		iItalian: "Seul",
		iKorean: _,
		iMongol: "Seul",
		iPolish: "Seul",
		iPortuguese: "Seul",
		iRussian: "Seul",
		iSpanish: u"Seúl",
		iSwedish: u"Söul",
		iThai: "Krung Sol",
		iTurkish: "Seul",
		iVietnamese: "Xo-un",
	},
	"Sevastopol": {  # founded on Kersonesos
		iDutch: "Sebastopol",
		iEnglish: "Sebastopol",
		iFrench: u"Sébastopol",
		iGerman: (
			translate("Theoderichshafen", bFascist=True),
			"Sewastopol",
		),
		iGreek: u"Sevastúpoli",
		iItalian: "Sebastopoli",
		iKorean: "Sebaseutopol",
		iPolish: "Sewastopol",
		iPortuguese: "Sebastopol",
		iRussian: _,
		iSpanish: "Sebastopol",
		iTurkish: "Akyar",
	},
	"Shabwat": {
		iArabic: (
			relocate("Ataq", iAfter=iRenaissance),
			"Shabwa",
		),
		iLocal: _, # Himyarite
	},
	"Shangdu": {  # renamed from Kaiping
		iChinese: _,
		iEnglish: "Xanadu",
		iMongol: "Shandu",
	},
	"Shangjing": {
		iChinese: (
			translate("Ha'erbin", iAfter=iIndustrial),
			_,
		),
		iEnglish: "Harbin",
		iFrench: "Harbin",
		iGreek: "Charmpin",
		iJapanese: "Harubin",
		iKorean: "Ha-eolbin",
		iPortuguese: "Harbin",
		iRussian: "Kharbin",
		iSpanish: "Harbin",
		iVietnamese: "Cap Nhi Tan",
	},
	"Shimla": {  # relocated from Kangra
		iEnglish: "Simla",
		iIndian: _,
	},
	"Shiquanhe": {  # relocated from Ger
		iChinese: _,
		iTibetan: u"Sênggêzangbo",
	},
	"Shushan": {
		iGreek: "Sousa",
		iLatin: "Susa",
		iLocal: _, # Elamite
		iPersian: (
			relocate("Ahvaz", iAfter=iMedieval),
			"Shusha",
		),
	},
	"Sibut": {  # founded on Krébédjé
		iFrench: "Fort-Sibut",
		iLocal: _,
	},
	"Siena": {  # founded on Populonium
		iEnglish: "Sienna",
		iFrench: "Sienne",
		iItalian: _,
		iPortuguese: "Sena",
		iSpanish: "Sena",
	},
	"Siggcoor": {
		iArabic: "Zighinkur",
		iEnglish: found("Bathurst"),
		iFrench: "Ziguinchor",
		iGerman: found("Fort Bayona"),
		iMande: _,
		iPortuguese: "Ziguinchor",
	},
	"Silchar": {  # relocated from Maibang
		iIndian: _,
		iPersian: u"Shilchôr",
	},
	"Silimi": {  # founded on Pselqet
		iArabic: "Qasr Ibrim",
		iCoptic: "Phrim",
		iGreek: "Primis Mikra",
		iLatin: "Primis",
		iNubian: (
			translate("Pedeme", iAfter=iMedieval),
			_,
		),
	},
	"Simferopol": {  # founded on Eupatoria
		iGerman: "Gotenburg",
		iGreek: u"Symferoúpoli",
		iItalian: "Sinferopoli",
		iMongol: "Aqmescit",
		iPolish: "Symferopol",
		iRussian: _,
		iTurkish: "Akmescit",
	},
	"Singaraja": {
		iDutch: "Singaradja",
		iLocal: _,
	},
	"Sinoia": {  # founded on Chedzugwe
		iItalian: _,
		iLocal: "Chinhoyi",
	},
	"Sirajis": {  # relocated from Parsa
		iArabic: "Shiraz",
		iPersian: _,
		iTurkish: "Siraz",
	},
	"Sirmium": {  # founded on Osijek
		iCeltic: "Sirmion",
		iGreek: "Sirmion",
		iLatin: _,
		iLocal: translate("Sremska Mitrovica", iAfter=iMedieval), # Croatian
	},
	"Sitka": {  # founded on Juneau
		iEnglish: _,
		iLocal: u"Sheet'ká",
		iRussian: "Novoarkhangel'sk",
	},
	"Smyrna": {  # relocated from Ephesos
		iCeltic: "Smiorna",
		iChinese: "Yizimier",
		iDravidian: "Icumir",
		iEnglish: _,
		iGreek: _,
		iItalian: "Smirne",
		iKorean: "Ijeumireu",
		iLatin: _,
		iModernGreek: u"Smýrni",
		iPolish: _,
		iPortuguese: "Esmirna",
		iSpanish: "Esmirna",
		iTurkish: "Izmir",
	},
	"Sopute": {  # founded on Hamath
		iArabic: "Safita",
		iPhoenician: _,
	},
	"Soria": {  # founded on Calatayud
		iArabic: "Suriya",
		iLatin: "Oria",
		iPortuguese: u"Sória",
		iSpanish: _,
	},
	"Spatzenkutter": {  # founded on Paraná
		iGerman: _,
		iSpanish: u"Asunción",
	},
	"Springbokfontein": {  # relocated from O'okiep
		iDutch: (
			translate("Springbok", iAfter=iGlobal),
			_,
		),
	},
	"St. Augustine": {
		iAmerican: relocate("Gainesville"),
		iEnglish: _,
		iFrench: "Saint Augustine",
		iSpanish: u"San Agustín",
	},
	"Stockholm": {  # renamed from Birka
		iArabic: "Istukhulm",
		iCeltic: u"Stócólm",
		iChinese: "Sidege'ermo",
		iDutch: _,
		iGerman: _,
		iGreek: u"Stokkhólmi",
		iItalian: "Stoccolma",
		iJapanese: "Sutokkuhorumu",
		iKorean: "Seutokholleum",
		iLatin: "Holmia",
		iNorse: _,
		iPolish: "Sztokholm",
		iPortuguese: "Estocolmo",
		iRussian: "Stokgol'm",
		iSpanish: "Estocolmo",
		iSwedish: _,
		iThai: "Sa-tok-home",
		iTurkish: "Stokholm",
		iUkrainian: "Stokhol'm",
	},
	"Sucheng": {  # founded on Nakhodka
		iChinese: _,
		iKorean: found("Jeongju"),
		iRussian: (
			rename("Partizansk", bCommunist=True),
			"Suchan",
		),
	},
	"Sukhotai": {  # relocated from Phitsanulok
		iKhmer: "Sokhaoty",
		iThai: _,
	},
	"Surabaya": {  # relocated from Kahuripan and Trowulan
		iArabic: "Surabaya",
		iChinese: "Sishui",
		iDravidian: "Curapaya",
		iDutch: "Soerabaja",
		iJavanese: _,
		iPersian: "Sorabaya",
		iPolish: "Surabaja",
		iPortuguese: "Surabaia",
		iRussian: "Surabaja",
	},
	"Surat": {
		iArabic: "Subara",
		iDutch: "Sourratte",
		iEnglish: _,
		iIndian: "Suryapur",
		iPersian: "Sourat",
		iPortuguese: "Suratt",
	},
	"Swakopmund": {  # founded on Ezorongondo
		iGerman: _,
		iLocal: "Otjozondjii", # Herero
	},
	"Swansea": {  # founded on Cardiff
		iCeltic: "Abertawe",
		iNorse: "Sveinsaer",
		iEnglish: _,
	},
	"Syriam": {  # relocated from Hongsawatoi
		iBurmese: "Thanlyin",
		iDutch: "Siriangh",
		iPortuguese: u"Sirião",
		iSpanish: _,
	},
	"Tabriz": {  # relocated from Gazaka
		iLocal: "Tavrezh", # Armenian
		iPersian: _,
	},
	"Tagilit": {  # founded on Al-Garnatah
		iLatin: "Tagili",
		iPhoenician: _,
		iSpanish: u"Tíjola",
	},
	"Taichung": {  # renamed from Dadun
		iChinese: "Taizhong",
		iJapanese: "Taichuu",
		iLocal: _, # Taiwanese
	},
	"Taipei": {  # renamed from Hobe
		iArabic: "Taybayh",
		iBurmese: "Htuingpe",
		iChinese: "Taibei",
		iDravidian: "Taypey",
		iEnglish: "Taipeh",
		iEthiopian: "Tayipe",
		iGerman: "Taipeh",
		iGreek: u"Taïpéi",
		iIndian: "Taipe",
		iJapanese: "Taihoku",
		iLangKhmer: "Daibi",
		iKorean: "Daebuk",
		iLatin: "Taipeia",
		iLocal: _, # Taiwanese
		iMongol: "Tajbej",
		iPersian: "Taype",
		iPolish: "Tajpej",
		iPortuguese: u"Taipé",
		iRussian: "Tajbej",
		iThai: "Thaipe",
		iTibetan: "Tha'e pe",
		iTurkish: "Taybey",
		iVietnamese: "Dai Bac",
	},
	"Taldyqorghan": {  # renamed from Iki-Oguz
		iRussian: "Taldy-Kurgan",
		iTurkish: _,
	},
	"Tamanrasset": {  # relocated from Abalessa
		iArabic: _,
		iBerber: "Tamenghast",
		iFrench: "Fort Laperrine",
	},
	"Tamworth": {  # founded on Oxford
		iEnglish: _,
		iNorse: u"Tomworðig",
	},
	"Tastil": {
		iLocal: _,
		iSpanish: relocate("San Salvador de Jujuy"),
	},
	"Tayinat": {
		iArabic: relocate("Safaqis"),
		iGreek: (
			found("Safaqis"),
			"Thaina",
		),
		iLatin: "Thaenae",
		iPhoenician: _,
	},
	"Tbessa": {
		iArabic: "Tibissa",
		iBerber: "Tibest",
		iFrench: u"Tébessa",
		iGreek: "Thebeste",
		iLatin: "Theveste",
		iPhoenician: _,
	},
	"Tbilisi": {  # relocated from Mtskheta
		iArabic: "Tiflis",
		iChinese: "Dibilisi",
		iDravidian: "Timilichi",
		iDutch: "Tiflis",
		iEnglish: "Tiflis",
		iFrench: "Tbilissi",
		iGerman: "Tiflis",
		iGreek: u"Tiflída",
		iItalian: "Tiflis",
		iJapanese: "Tobirishi",
		iKorean: "Teubillisi",
		iLocal: ( # Georgian
			translate("Tp'ilisi", iBefore=iRenaissance),
			_,
		),
		iPersian: "Teflis",
		iPolish: "Tyflis",
		iRussian: "Tiflis",
		iSpanish: "Tiflis",
		iTurkish: "Tiflis",
	},
	"Te Kai-a-te-Karoro": {
		iDutch: found("Moordenaarsbaai"),
		iEnglish: relocate("Christchurch"),
		iPolynesian: _,
	},
	"Te Whanganui-a-Tara": {
		iEnglish: "Wellington",
		iPolynesian: _,
	},
	"Tegucigalpa": {  # founded on Kuskatan
		iNahuatl: "Tecuztlicallipan",
		iSpanish: _,
	},
	"Tepy-hewet": {
		iArabic: "Atfih",
		iCoptic: "Petpeh",
		iEgyptian: _,
		iGreek: "Busiris",
		iLatin: "Aphroditopolis",
	},
	"Thanh Hoa": {  # relocated from Hoa Lu
		iChinese: "Qinghua",
		iJapanese: "Tainhoa",
		iVietnamese: _,
	},
	"Tharangamba": {  # relocated from Kanchipuram
		iDravidian: _,
		iEnglish: "Tranquebar",
		iNorse: "Trankebar",
	},
	"Tharsatica": {  # founded on Pula
		iCeltic: _,
		iGerman: "St. Veit",
		iItalian: "Fiume",
		iLatin: "Flumen",
	},
	"Thessaloniki": {  # relocated from Pella
		iArabic: "Salonik",
		iByzantine: "Thessalonika",
		iCeltic: u"Teasaloinicé",
		iEnglish: "Salonica",
		iFrench: "Thessalonique",
		iGreek: "Thessalonike",
		iItalian: "Tessalonica",
		iLatin: "Thessalonica",
		iKorean: "Tesalloniki",
		iMalay: "Tesalonika",
		iModernGreek: _,
		iPolish: "Solun",
		iPortuguese: u"Salónica",
		iRussian: "Saloniki",
		iSpanish: u"Salónica",
		iTurkish: "Selanik",
		iUkrainian: "Saloniky",
	},
	"Thinsawanargara": {
		iBurmese: _,
		iEnglish: rename("Bassein"),
		iIndian: "Kusimanagara",
	},
	"Thirukonamalai": {
		iDravidian: (
			translate("Tirukkonamalai", iAfter=iIndustrial),
			_,
		),
		iEnglish: "Trincomalee",
		iFrench: "Trinquemalay",
		iIndian: "Gokarna",
		iLocal: "Trikunamalaya", # Sinhalese
	},
	"Tilimsan": {  # relocated from Km'
		iArabic: _,
		iBerber: translate("Tagrart", iBefore=iMedieval),
		iFrench: "Tlemcen",
		iPortuguese: u"Tremecém",
		iSpanish: u"Tremecén",
	},
	"Tiwanaku": {
		iLocal: _,
		iQuechua: "Tiyawanaku",
		iSpanish: (
			relocate("La Paz"),
			"Tihuanaco",
		),
	},
	"Tmdt": {  # founded on Murrakush
		iArabic: relocate("Murrakush"),
		iGreek: "Thymiaterion",
		iLatin: "Thamusida",
		iPhoenician: _,
	},
	"Toliara": {
		iFrench: u"Tuléar",
		iLocal: _, # Malagasy
	},
	"Tombwa": {
		iCongolese: _,
		iGerman: found(u"Möwebucht"),
		iPortuguese: (
			translate(u"Tômbua", iAfter=iGlobal),
			"Porto Alexandre",
		),
	},
	"Torarica": {  # founded on Fort Zeelandia
		iDutch: "Jodensavanne",
		iPortuguese: _,
	},
	"Torksey": {  # founded on Lindon
		iEnglish: _,
		iNorse: "Thorkilsey",
	},
	"Toukyou": {  # renamed from Edo
		iCeltic: u"Tóiceo",
		iChinese: "Dongjing",
		iDravidian: "Tokkiyo",
		iDutch: "Tokio",
		iEnglish: "Tokio",
		iGerman: "Tokio",
		iGreek: u"Tókio",
		iIndian: "Tokyo",
		iItalian: "Tokio",
		iJapanese: _,
		iKorean: "Dokyo",
		iLatin: "Tocio",
		iMalay: "Tokyo",
		iNorse: "Tokyo",
		iPolish: "Tokio",
		iPortuguese: u"Tóquio",
		iRussian: "Tokio",
		iSpanish: "Tokio",
		iThai: "Tokeiyw",
		iTurkish: "Tokyo",
		iUkrainian: u"Tókio",
		iVietnamese: "Dong Kinh",
	},
	"Trieste": {  # founded on Ljubljana
		iDutch: u"Triëst",
		iGerman: "Triest",
		iGreek: u"Teryésti",
		iItalian: _,
		iJapanese: "Toriesute",
		iKorean: "Teurieseute",
		iLatin: "Tergestum",
		iPolish: "Triest",
		iPortuguese: _,
		iRussian: "Triest",
		iSpanish: _,
		iSwedish: _,
		iTurkish: "Triyeste",
	},
	"Trimontium": {  # founded on Dùn Èideann
		iCeltic: relocate(u"Dùn Èideann"),
		iEnglish: relocate(u"Dùn Èideann"),
		iLatin: _,
	},
	"Tripolis": {  # renamed from Oyat
		iArabic: "Tarabulus",
		iDutch: "Tripoli",
		iEnglish: "Tripoli",
		iFrench: "Tripoli",
		iGerman: "Tripolis",
		iGreek: "Tripoleis",
		iItalian: "Tripoli",
		iLatin: _,
		iNorse: "Tripoli",
		iPolish: "Trypolis",
		iPortuguese: u"Trípoli",
		iSpanish: u"Trípoli",
		iTurkish: "Trablus",
	},
	"Trowulan": {  # relocated from Kahuripan
		iDutch: relocate("Surabaya"),
		iJavanese: (
			relocate("Surabaya", iAfter=iRenaissance),
			translate("Wilwatikta", bCapital=True),
			_,
		),
	},
	"Trujillo": {  # relocated from Chan Chan
		iLocal: "Cuimor",
		iQuechua: "Truhillu",
		iSpanish: _,
	},
	"Tuchtlan": {  # founded on Pa' Chan
		iNahuatl: _,
		iSpanish: u"Tuxtla Gutiérrez",
	},
	"Tukuyu": {  # founded on Mbande
		iGerman: "Neu Langenburg",
		iLocal: _,
	},
	"Tullo": {  # founded on Bilbao
		iCeltic: _,
		iLatin: "Tullonium",
	},
	"Tullum": {  # founded on Nancy
		iCeltic: _,
		iFrench: "Toul",
		iGerman: "Tull",
		iLatin: "Tullum Leucorum",
	},
	"Tungul": {  # relocated from Napa
		iArabic: "Dunqula",
		iEnglish: "Dongola",
		iLatin: "Dongola",
		iNubian: _,
	},
	"Tunus": {  # relocated from Qart-Hadasht
		iArabic: _,
		iDutch: "Tunis",
		iEnglish: "Tunis",
		iFrench: "Tunis",
		iGerman: "Tunis",
		iGreek: "Tunida",
		iItalian: "Tunisi",
		iNorse: "Tunis",
		iPolish: "Tunis",
		iPortuguese: "Tunes",
		iRussian: "Tunis",
		iSpanish: u"Túnez",
		iTurkish: _,
	},
	"Tupua'i": {
		iFrench: "Tubuai",
		iPolynesian: _,
	},
	"Turpan": {  # relocated from Qocho
		iChinese: "Turfan",
		iTurkish: _,
	},
	"Tysfwn": {
		iArabic: (
			relocate("Baghdad"),
			"Taysafun",
		),
		# iArmenian: "Tizbon",
		iGreek: "Ktesiphon",
		iLatin: "Ctesiphon",
		iPersian: (
			translate("Tisfun", iAfter=iRenaissance),
			_,
		),
	},
	u"Türkistan": {
		iPersian: "Shavgar",
		iRussian: "Turkestan",
		iTurkish: _,
	},
	u"Þróndheimr": {
		iNorse: (
			translate("Trondhjem", iPeriod=iPeriodDenmark),
			translate("Trondheim", iPeriod=iPeriodNorway),
			_,
		),
	},
	"Uigandes": {
		iDutch: (
			translate("Bethanie", iAfter=iGlobal),
			"Klipfontein",
		),
		iEnglish: "Bethany",
		iGerman: "Bethanien",
		iLocal: _, # Khoekhoegowab
	},
	"Uiroconion": {  # founded on Derby
		iCeltic: _,
		iEnglish: "Wroxeter",
		iLatin: "Viroconium",
	},
	"Umtali": {  # founded on Chimoio
		iEnglish: (
			translate("Mutare", iAfter=iDigital),
			_,
		),
	},
	"Umu Aleasal": {
		iArabic: _,
		iFrench: "Oum el Assel",
	},
	"Unaaha": {
		iDutch: relocate("Kendari"),
		iLocal: _,
		iMalay: (
			relocate("Kendari", iAfter=iIndustrial),
			relocate("Baubau", iReligion=iIslam),
		),
	},
	"Upington": {  # founded on Nomsoros
		iEnglish: _,
		iLocal: "Khara hais", # Khoekhoe
	},
	"Uruvela": {
		iIndian: (
			rename("Gaya", iReligion=iBuddhism),
			_,
		),
	},
	"Usumbura": {  # founded on Kitega
		iLocal: (
			translate("Bujumbura", iAfter=iGlobal),
			_,
		),
	},
	"Velikiye Luki": {  # renamed from Luki
		iFrench: u"Velikié Louki",
		iGerman: "Welikije Luki",
		iPolish: "Wielkie Luki",
		iRussian: _,
	},
	"Vigan": {
		iChinese: "Mei'an",
		iLocal: "Bigan",
		iSpanish: (
			translate("Villa Fernandina", iBefore=iRenaissance),
			_,
		),
	},
	"Vilanculos": {  # relocated from Manyikeni
		iPortuguese: _,
		iKiswahili: "Vilankulo",
	},
	"Viluma": {
		iLocal: _, # Manpundugun
		iQuechua: found("Qulqi Tampu"),
		iSpanish: "La Serena",
	},
	"Viratnagara": {
		iIndian: (
			translate("Viratnagar", iAfter=iGlobal),
			translate("Bairath", iAfter=iMedieval),
			_,
		),
		iPersian: relocate("Jaipur"),
	},
	"Waddan": {
		iArabic: _,
		iItalian: "Ueddan",
	},
	"Wagadugu": {
		iFrench: "Ouagadougou",
		iLocal: _,
	},
	"Waithali": {  # relocated from Dhanyawadi
		iBurmese: (
			relocate("Mrauk U", iAfter=iRenaissance),
			_,
		),
		iIndian: "Vesali",
	},
	"Walilt": {  # founded on Fizaz
		iBerber: _,
		iLatin: "Volubilis",
	},
	"Wambu": {
		iEnglish: "New Lisbon",
		iLocal: (
			translate("Huambo", bReconquest=True),
			_,
		),
		iPortuguese: "Nova Lisboa",
	},
	"Waraq": {
		iQuechua: _,
		iSpanish: "Huaraz",
	},
	"Warmbad": {  # founded on Bassonsdrif
		iGerman: _,
		iLocal: "Aixa-aibes", # Nama
	},
	"Warzazat": {  # relocated from Aghmat
		iArabic: _,
		iFrench: "Ouarzazate",
	},
	"Waterford": {  # founded on Cork
		iCeltic: u"Port Láirge",
		iEnglish: _,
		iNorse: u"Veðrafjorðr",
	},
	"Weihaiwei": {  # relocated from Penglai
		iChinese: (
			translate("Weihai", bCommunist=True),
			_,
		),
		iEnglish: "Port Edward",
	},
	"Werder": {
		iEthiopian: _,
		iItalian: "Uardere",
		iSomali: "Wardheer",
	},
	"Weso": {
		iCongolese: _,
		iFrench: u"Ouésso",
		iGerman: "Wesso",
	},
	"Whanganui": {
		iDutch: found("Kaap van P. Boreel"),
		iEnglish: found("New Plymouth"),
		iPolynesian: _,
	},
	"Wilusa": {  # founded on Pergamon
		iEnglish: "Troy",
		iFrench: "Troie",
		iGerman: "Troja",
		iGreek: "Ilion",
		iHittite: _,
		iLatin: "Troia",
		iTurkish: relocate("Bursa"),
	},
	"Wiryeseong": {
		iChinese: "Hancheng",
		iEnglish: "Hansung",
		iJapanese: "Keijou",
		iKorean: (
			rename("Seoul", iAfter=iIndustrial),
			translate("Hanseong", iAfter=iRenaissance),
			translate("Namgyeong", iAfter=iMedieval),
			_,
		),
		iMongol: "Hanyangbu",
		iVietnamese: "Han Thanh",
	},
	"Witbank": {  # founded on Moxomatsi
		iDutch: _,
		iLocal: "eMalahleni",
	},
	"Witvlei": {
		iDutch: _,
		iLocal: "Uri Khubus",
	},
	"Wizidi": {  # relocated from Mbwila
		iLocal: _,
		iPortuguese: (
			translate(u"Uíge", iAfter=iDigital),
			"Carmona",
		),
	},
	"Wollongong": {
		iEnglish: _,
		iLocal: "Woolyungah", # Dharawal
	},
	"Wulabo": {
		iChinese: (
			translate("Dihua", iAfter=iRenaissance),
			translate("Luntai", iAfter=iMedieval),
			_,
		),
		iLocal: translate("Urabo", iBefore=iClassical),
		iTurkish: u"Ürümqi",
	},
	"Wuling": {
		iChinese: (
			translate("Changde", iAfter=iRenaissance),
			translate("Langzhou", iAfter=iMedieval),
			_,
		),
	},
	"Xai-Xai": {  # founded on Mandlakazi
		iLocal: _,
		iPortuguese: u"João Belo",
	},
	"Xangogo": {  # founded on Opuwo
		iLocal: _,
		iPortuguese: u"Vila Roçadas",
	},
	"Xiangping": {
		iChinese: (
			translate("Dongjing", bCapital=True),
			translate("Liaoyang", iAfter=iMedieval),
			_,
		),
		iKorean: (
			found("Baegam"),
			"Yodong",
		),
	},
	"Xicalango": {  # founded on Ox Te' Tuun
		iNahuatl: _,
		iSpanish: "Ciudad del Carmen",
	},
	u"Xigazê": {
		iChinese: (
			relocate("Nianmai", iBefore=iRenaissance),
			"Rikaze",
		),
		iEnglish: "Shigatse",
		iTibetan: _,
	},
	u"Xihuatlán": {
		iNahuatl: _,
		iSpanish: (
			found("Puerto Vallarta"),
			u"Cihuatlán",
		),
	},
	"Xiurong": {
		iChinese: (
			translate("Xinzhou", iAfter=iMedieval),
			_,
		),
	},
	"Xoconochco": {  # founded on Kaminaljuyu
		iNahuatl: _,
		iSpanish: "Soconusco",
	},
	"Yabelo": {
		iEthiopian: _,
		iItalian: "Javello",
		iSomali: "Yaabeelloo",
	},
	"Yerevan": {  # relocated or founded on Artashat
		iArabic: "Yirifan",
		iBabylonian: "Erebuni",
		iDutch: "Jerevan",
		iFrench: "Erevan",
		iGerman: "Eriwan",
		iJapanese: "Eriban",
		iLocal: _, # Armenian
		iMongol: "Yeryevan",
		iNorse: "Jerevan",
		iPersian: "Iravan",
		iPolish: "Erywan",
		iRussian: _,
		iSpanish: u"Ereván",
		iThai: "Yere Wan",
		iTurkish: "Erivan",
	},
	"Yuzhang": {
		iChinese: (
			translate("Nanchang", iAfter=iRenaissance),
			translate("Hongzhou", iAfter=iMedieval),
			_,
		),
		iKorean: "Namchang",
	},
	"Zdif": {
		iArabic: relocate("Ashir"),
		iBerber: _,
		iFrench: u"Sétif",
		iLatin: (
			found("Lamdia"),
			"Sitifis",
		),
	},
	"Zhalantun": {  # renamed from Butha
		iChinese: _,
		iManchu: "Jalan Tun",
		iMongol: _,
	},
	"Zhoushan": {  # relocated from Mingzhou
		iChinese: _,
		iEnglish: "Chusan",
	},
	"'t Landt Van Quiri": {  # founded on Hervey Bay
		iDutch: _,
		iEnglish: "Sunshine Coast",
	},
}
