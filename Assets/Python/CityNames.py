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
		):
		self.name = name
		
		self.bRenaming = bRenaming
		self.bRelocation = bRelocation
		
		self.iBefore = iBefore
		self.iAfter = iAfter
		self.iReligion = iReligion
		
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

iNumLanguages = 56
lLanguages = (
	iAmerican, iArabic, iBabylonian, iBerber, iBrazilian, 
	iBurmese, iByzantine, iCeltic, iChinese, iCongolese, 
	iCoptic, iDravidian, iDutch, iEgyptian, iEgyptianArabic, 
	iEnglish, iEthiopian, iFrench, iGerman, iGreek, 
	iHarappan, iHittite, iIndian, iItalian, iJapanese, 
	iJavanese, iLangKhmer, iKiswahili, iKorean, iKushan, 
	iLatin, iLocal, iMalay, iManchu, iMande, 
	iMayan, iModernGreek, iMongol, iNahuatl, iNorse, 
	iNubian, iPersian, iPhoenician, iPolish, iPolynesian, 
	iPortuguese, iQuechua, iUkrainian, iRussian, iSomali, 
	iSpanish, iSwedish, iThai, iTibetan, iTurkish, 
	iVietnamese,
) = range(iNumLanguages)

name_changes = {
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
	"Al-Mariyya": {
		iArabic: _,
		iChinese: "A'oumeiliya",
		iLatin: "Portus Magnus",
		iPhoenician: found("Bdrt"),
		iPortuguese: "Almeria",
		iRussian: "Almeriya",
		iSpanish: u"Almería",
	},
	"Al-Mename": {  # relocated from Dilmun, Al-Muharraq
		iArabic: _,
		iEnglish: "Manama",
	},
	"Al-Muharraq": {  # founded, relocated on Dilmun
		iArabic: (
			relocate("Al-Mename", iAfter=iGlobal),
			_,
		),
		iEnglish: relocate("Al-Mename"),
		iPortuguese: u"Forte de Barém",
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
	"Alexandrovskoye": {
		iRussian: (
			translate("Kuybyshevka-Vostochnaya", bCommunist=True),
			translate("Belogorsk", iAfter=iGlobal),
			_,
		),
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
	"Amapá": {
		iPortuguese: (
			relocate(u"Calçoene", iAfter=iGlobal),
			_,
		),
		iFrench: found("Counani"),
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
	"Ashir": {  # relocated from Zdif
		iArabic: _,
		iBerber: "Achir",
		iFrench: relocate("Lamdia"),
	},
	"Ashland": {
		iEnglish: _,
		iFrench: found("La Baye"),
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
	"Assab": {  # founded on Dongolo
		iArabic: _,
		iEthiopian: "Asab",
		iGreek: u"Arsinoë Epidiris",
		iSwahili: "Casab",
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
	"Atbasar": {
		iRussian: relocate("Kokshetav"),
		iTurkish: _,
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
	"Bandar Qasim": { # renamed from Boosaaso
		iArabic: _,
		iItalian: "Bender Cassim",
	},
	"Bandiagara": {
		iArabic: "Hamdullahi",
		iFrench: "Mopti",
		iMande: _,
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
	"Basse-Terre": {
		iEnglish: found("St. John's"),
		iFrench: _,
		iSwedish: found("Gustavia"),
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
	
	"Cadota": {
		iChinese: "Jingjue",
		iKushan: _,
		iLocal: "Niya",
	},
	"Caen": {
		iFrench: _,
		iLatin: "Catumagos",
	},
	"Cahors": {
		iCelts: "Divona",
		iFrench: _,
		iLatin: "Divona Cadurcorum",
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
	"Canosium": {
		iItalian: "Canosa",
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
	"Carnot": {  # founded on Bouar
		iFrench: _,
		iLocal: "Tendira",
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
	"Chouragarh": {
		iIndian: (
			translate("Narsinghpur", iAfter=iRenaissance),
			_,
		),
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
	"Coimbra": {
		iArabic: "Qulumriyah",
		iCeltic: "Conimbriga",
		iLatin: "Aeminium",
		iPhoenician: "Habis",
		iPortuguese: _,
		iSpanish: u"Coímbra",
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
	
	"Eau Claire": {
		iEnglish: _,
		iFrench: found("Fort Bon Secours"),
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
	
	
	
	
	
	"Gasegonyane": {
		iDutch: "Die Oog",
		iEnglish: "Kuruman",
		iLocal: _,
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
	"Govapuri": {  # relocated from Chandrapura
		iDravidian: "Gove",
		iIndian: _,
		iLocal: "Goy",
		iPortuguese: (
			relocate("Panaji", iAfter=iIndustrial),
			"Goa",
		),
	},
	"Gustavia": {  # founded on Basse-Terre
		iFrench: u"Le Carénage",
		iSwedish: _,
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
	"Hadrianopolis": {  # renamed from Orestias
		iGreek: "Adrianoupolis",
		iLatin: _,
		iTurkish: "Edirne",
	},
	"Hargeysa": {  # relocated from Däkkär
		iEnglish: "Hargeisa",
		iSomali: _,
	},
	"Harmonie": {  # founded on Evansville
		iEnglish: "New Harmony",
		iGerman: _,
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
	"Hatra": {  # renamed from Ash-shur
		iArabic: "Al-Hadr",
		iGreek: "Atra",
		iLatin: "Hatra",
		iPersian: "Hatra",
	},
	"Hegra": {
		iLocal: _, # Nabataean
		iArabic: (
			relocate("Al-Ula", iAfter=iMedieval),
			"Al-Hijr",
		),
	},
	"Hemeroskopeion": {  # founded on Alicante
		iArabic: "Daniyya",
		iGreek: _,
		iLatin: "Dianium",
		iLocal: u"Dénia", # Valencian
		iSpanish: "Denia",
	},
	"Ilperrelhelame": {
		iEnglish: "Lake Nash",
		iLocal: _, # Aboriginal Alyawarre
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
	"Induru": {
		iIndian: (
			translate("Indhrapuri", iAfter=iMedieval),
			_,
		),
		iPersian: "Nizamabad",
	},
	"Iona": {  # founded on Dùn Breatann
		iCeltic: "Eilean Idhe",
		iEnglish: "Icolmkill",
		iLatin: _,
		iNorse: "Hy",
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
	"Jijiga": {  # relocated from Däkkär
		iEthiopian: _,
		iItalian: "Giggiga",
		iSomali: "Jigjiga",
	},
	"Jolo": {
		iArabic: _,
		iChinese: "Ho Lo",
		iLocal: "Tiyanggi", # Tausug
		iSpanish: u"Joló",
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
	"Kanatha": {  # founded on Bosra
		iArabic: "Qanawat",
		iGreek: _,
		iLatin: "Canatha",
	},
	"Kantipur": {
		iChinese: "Yambu",
		iIndian: (
			translate("Kathmandu", iAfter=iRenaissance),
			_,
		),
		iLocal: "Yen",
	},
	"Karbala": {  # relocated from Barsip
		iArabic: _,
		iTurkish: "Kerbela",
	},
	"Karwar": {  # founded on Chandrapura
		iArabic: "Bait-e-Kol",
		iEnglish: "Carwar",
		iIndian: _,
		iLocal: "Kadwad",
	},
	"Kayes": {  # relocated from Diakaba
		iFrench: _,
		iMande: "Kayi",
		# iSonghai: "Xaayi",
	},
	"Kazerun": {
		iArabic: "Balad al-Atigh",
		iPersian: _,
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
	"Kinjarling": {
		iEnglish: "Albany",
		iLocal: _, # Aboriginal Nyungar
	},
	"Kleopatris": {
		iGreek: _,
		iLatin: "Cleopatra",
	},
	"Kochi": {  # relocated from Desinganadu
		iArabic: "Kashi",
		iDravidian: "Kochi",
		iDutch: "Cochin",
		iEnglish: "Cochin",
	},
	"Kokshetav": {  # relocated from Atbasar
		iRussian: _,
		iTurkish: u"Kökshetau",
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
	"Kyaingtong": {
		iBurmese: _,
		iChinese: "Jingdong",
		iEnglish: "Kengtung",
		iThai: (
			found("Chiang Rai"),
			"Chiang Tung",
		),
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
	"L'Aquila": {  # relocated from Corfinium
		iGreek: "L'Akouila",
		iItalian: _,
		iLatin: "Aquila",
		iPortuguese: u"Áquila",
		iRussian: "Akvila",
	},
	"La Paz": {
		iLocal: "Chuqiyapu", # Aymara
		iSpanish: _,
	},
	"Lamdia": {  # founded on Zdif
		iArabic: "Al-Madiya",
		iFrench: u"Médéa",
		iBerber: "Lemdiyyet",
	},
	"Likasi": {  # relocated from Bunkeya
		iDutch: "Jadotstad",
		iFrench: "Jadotville",
		iCongolese: "Likasi",
	},
	"Loango": {  # renamed from Bwali
		iCongolese: "M'banza-Loango",
		iFrench: "Loango",
		iPortuguese: "Loango",
	},
	"Lulami": {
		iArabic: relocate("Saayi"),
		iFrench: relocate("Saayi"),
		iMande: _,
	},
	"M'Baiki": {
		iFrench: u"Mbaïki",
		iGerman: "Mbaiki",
		iLocal: _,
	},
	"Maramuca": {  # founded on Maramuca
		iLocal: "Rimuka",
		iPortuguese: _,
	},
	"Massakory": {  # founded on Bidderi
		iArabic: "Massakori",
		iFrench: _,
	},
	"Montgomery": {  # relocated from Ajodhan
		iEnglish: _,
		iPersian: "Sahiwal",
	},
	"Muynak": {
		iRussian: _,
		iTurkish: "Moynaq",
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
	"Nagula Vancha": {  # founded on Dantewada
		iDutch: "Nagelwanze",
		iIndian: _,
	},
	"Narbonne": {
		iFrench: _,
		iItalian: "Narbona",
		iLatin: "Narbo Martius",
		iPortuguese: "Narbona",
		iSpanish: "Narbona",
	},
	"Nassau": {
		iDutch: _,
		iEnglish: _,
		iSpanish: (
			found("San Salvador"),
			u"Nasáu",
		),
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
	"Neu-Ulm": {  # founded on Cedar Rapids
		iEnglish: "New Ulm",
		iGerman: _,
	},
	"New Edinburgh": {  # founded on Ciudad de Panamá
		iEnglish: _,
		iSpanish: (
			translate("Puerto Inabaginya", iAfter=iDigital),
			u"Puerto Escocés",
		),
	},
	"Newcastle, kwaZulu-Natal": {  # founded on Bulawayo
		iDutch: "Viljoensdorp",
		iEnglish: "Newcastle",
	},
	"Nguru": {
		iFrench: "N'Gourou",
		iLocal: _,
	},
	"Nieuw Amsterdam": {  # renamed from Fort Nassau
		iDutch: _,
		iEnglish: "New Amsterdam",
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
	"Nouantikum": {  # founded on Calatayud
		iCeltic: _,
		iLatin: "Numantia",
		iSpanish: "Numancia",
	},
	"Okoloama": {
		iEnglish: (
			relocate("Port Harcourt", iAfter=iGlobal),
			"Bonny",
		),
		iLocal: _, # Igbo
	},
	"Ongoe": {  # founded on Chedzugwe
		iLocal: "Angwa",
		iPortuguese: _,
	},
	"Orestias": {
		iGreek: _,
		iLatin: rename("Hadrianopolis"),
		iLocal: "Uskudama", # Thracian
	},
	u"Paço de Arcos": {  # foundd on Devagiri
		iIndian: "Silvassa",
		iPortuguese: _,
	},
	"Pakse": {  # renamed from Champassak
		iFrench: u"Paksé",
		iKhmer: _,
	},
	"Panaji": {  # relocated from Govapuri
		iEnglish: "Panjim",
		iIndian: _,
		iLocal: "Ponnjem",
		iPortuguese: "Pangim",
	},
	"Parapatho": {
		iLocal: _,
		iPortuguese: (
			translate(u"António Enes", iAfter=iIndustrial),
			"Angoche",
		),
	},
	"Phaselis": {  # relocated from Attaleia
		iGreek: _,
		iTurkish: "Faselis",
	},
	"Pipli": {  # founded on Chandraketugarh
		iDutch: "Pipely",
		iNorse: _,
	},
	"Pointe-Noire": {  # founded on Bwali
		iCongolese: "Njinji",
		iFrench: _,
		iPortuguese: "Ponta Negra",
	},
	"Pokrovsk": {
		iGerman: "Kosakenstadt",
		iRussian: (
			translate("Engels", bCommunist=True),
			_,
		),
	},
	"Pori": {
		iLatin: "Arctopolis",
		iLocal: _, # Finnish
		iSwedish: u"Björneborg",
	},
	"Portel": {
		iDutch: found("Fort Oranje"),
		iPortuguese: _,
	},
	"Porto Calvo": {
		iDutch: found("Fort Bass"),
		iPortuguese: _,
	},
	"Probolinggo": {
		iJavanese: u"Pråbålinggå",
		iMalay: _,
	},
	"Ptolemais Hermiou": {  # renamed from Akka
		iEgyptian: u"Psoï",
		iArabic: "El Mansha",
		iCoptic: "Bsoi",
		iGreek: _,
		iLatin: "Ptolemais Thebais",
	},
	"Puerto Baquerizo Moreno": {
		iEnglish: found("Seymour"),
		iSpanish: _,
	},
	"Puerto Lempira": {  # founded on Black River
		iLocal: "Auhya Yari",
		iSpanish: _,
	},
	"Qazimbazar": {  # founded on Bishnupur
		iEnglish: "Cassimbazar",
		iPersian: _,
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
	"Santa Luzia": {
		iPortuguese: (
			translate(u"Brasília", bCapital=True),
			translate(u"Luziânia", iAfter=iIndustrial),
			_,
		),
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
	"Shabwat": {
		iArabic: (
			relocate("Ataq", iAfter=iRenaissance),
			"Shabwa",
		),
		iLocal: _, # Himyarite
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
	"Soria": {  # founded on Calatayud
		iArabic: "Suriya",
		iLatin: "Oria",
		iPortuguese: u"Sória",
		iSpanish: _,
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
	"Taichung": {  # renamed from Dadun
		iChinese: "Taizhong",
		iJapanese: "Taichuu",
		iLocal: _, # Taiwanese
	},
	"Tamanrasset": {  # relocated from Abalessa
		iArabic: _,
		iBerber: "Tamenghast",
		iFrench: "Fort Laperrine",
	},
	"Tiwanaku": {
		iLocal: _,
		iQuechua: "Tiyawanaku",
		iSpanish: (
			relocate("La Paz"),
			"Tihuanaco",
		),
	},
	"Toliara": {
		iFrench: u"Tuléar",
		iLocal: _, # Malagasy
	},
	"Torarica": {  # founded on Fort Zeelandia
		iDutch: "Jodensavanne",
		iPortuguese: _,
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
	"Trimontium": {  # founded on Dùn Èideann
		iCeltic: relocate(u"Dùn Èideann"),
		iEnglish: relocate(u"Dùn Èideann"),
		iLatin: _,
	},
	"Trujillo": {  # relocated from Chan Chan
		iLocal: "Cuimor",
		iQuechua: "Truhillu",
		iSpanish: _,
	},
	"Tullo": {  # founded on Bilbao
		iCeltic: _,
		iLatin: "Tullonium",
	},
	"Tupua'i": {
		iFrench: "Tubuai",
		iPolynesian: _,
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
	"Unaaha": {
		iDutch: relocate("Kendari"),
		iLocal: _,
		iMalay: (
			relocate("Kendari", iAfter=iIndustrial),
			relocate("Baubau", iReligion=iIslam),
		),
	},
	"Vigan": {
		iChinese: "Mei'an",
		iLocal: "Bigan",
		iSpanish: (
			translate("Villa Fernandina", iBefore=iRenaissance),
			_,
		),
	},
	"Viratnagara": {
		iIndian: (
			translate("Viratnagar", iAfter=iGlobal),
			translate("Bairath", iAfter=iMedieval),
			_,
		),
		iPersian: relocate("Jaipur"),
	},
	"Walilt": {  # founded on Fizaz
		iBerber: _,
		iLatin: "Volubilis",
	},
	"Warmbad": {  # founded on Bassonsdrif
		iGerman: _,
		iLocal: "Aixa-aibes", # Nama
	},
	"Warzazat": {  # relocated from Aghmat
		iArabic: _,
		iFrench: "Ouarzazate",
	},
	"Witvlei": {
		iDutch: _,
		iLocal: "Uri Khubus",
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
	"Waterford": {  # founded on Cork
		iCeltic: u"Port Láirge",
		iEnglish: _,
		iNorse: u"Veðrafjorðr",
	},
	"Zhalantun": {  # renamed from Butha
		iChinese: _,
		iManchu: "Jalan Tun",
		iMongol: _,
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
}
