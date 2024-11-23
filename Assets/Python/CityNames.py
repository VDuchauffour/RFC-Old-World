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
	
	def __init__(self, name, bRenaming=False, bRelocation=False, iBefore=None, iAfter=None, bFound=False, bSmall=False, bCommunist=False):
		self.name = name
		
		self.bRenaming = bRenaming
		self.bRelocation = bRelocation
		
		self.iBefore = iBefore
		self.iAfter = iAfter
		
		self.bFound = bFound
		self.bSmall = bSmall
		self.bCommunist = bCommunist
	
	def isValid(self, city, bFound=False):
		if self.iBefore is not None:
			if player(city).getCurrentEra() > self.iBefore:
				return False
		
		if self.iAfter is not None:
			if player(city).getCurrentEra() < self.iAfter:
				return False
		
		if self.bFound and not bFound:
			return False
		
		if self.bSmall:
			if city.getPopulation() > player(city).getCurrentEra():
				return False
		
		if self.bCommunist:
			if not isCommunist(city.getOwner()):
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

iNumLanguages = 40
lLanguages = (
	iArabic, iBerber, iBurmese, iByzantine, iCeltic, 
	iChinese, iCoptic, iDravidian, iDutch, iEgyptian, 
	iEgyptianArabic, iEnglish, iEthiopian, iFrench, iGerman, 
	iGreek, iHarappan, iHittite, iItalian, iJapanese, 
	iLangKhmer, iKorean, iLatin, iLocal, iMalay, 
	iManchu, iModernGreek, iNorse, iNubian, iPhoenician, 
	iPolish, iPolynesian, iPortuguese, iQuechua, iRus, 
	iRussian, iSpanish, iSwedish, iThai, iTurkish,
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
		iRus: u"Aáhen",
		iRussian: u"Áhen",
		iSpanish: u"Aquisgrán",
		iThai: u"'Akhen",
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
			translate("Abakan", after=iGlobal), 
			_,
		),
	},
	"Abalessa": {
		iLangArabic: (
			relocate("Tamanrasset", after=iRenaissance),
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
	"Adramat": {
		iArabic: relocate("Al-Qayrawan"),
		iByzantine: "Justinianopolis",
		iGreek: "Adrymeton",
		iLatin: "Hadrumetum",
		iPhoenician: _,
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
		iGreek: u"Antiókheia tês en Ptolemaïdis",
		iItalian: (
			translate("San Giovanni d'Acri", iBefore=iMedieval),
			"Acri",
		),
		iLatin: "Colonia Ptolemais",
		iPhoenician: "Ak",
		iSpanish: (
			translate("San Juan de Acre", iBefore=iMedieval),
			"Acre",
		),
	},
	"Ako": (
		iJapanese: _,
		iRussian: (
			translate("Alexandrovsk-Sakhalinsky", iAfter=iGlobal),
			"Alexandrovka",
		),
	),
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
		iRussian: {
			translate("Shakhty", iAfter=iGlobal),
			_,
		},
	},
	"Alexandrovskoye": {
		iRussian: {
			translate("Kuybyshevka-Vostochnaya", bCommunist=True),
			translate("Belogorsk", iAfter=iGlobal),
			_,
		},
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
		iGreek: "Philadelphia",
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
			relocate("Phnom Penh", bIndustrial=True),
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
		iCeltic: _,
		iPersian: "Angora",
		iGreek: "Ankyra",
		iHarappan: "Ankuwash",
		iLatin: "Ancyra",
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
		iArabic: "Antakiya",
		iBabylonian: found("Alalakh"),
		iEgyptian: found("Alalakh"),
		iEnglish: "Antioch",
		iFrench: "Antioche",
		iGerman: "Antiochia",
		iGreek: _,
		iHittite: found("Alalakh"),
		iItalian: "Antiochia",
		iLatin: "Antiochia",
		iMongol: relocate("Alexandria ad Issum", bConquest=True),
		iPortuguese: "Antioquia",
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
		iRus: "Ateny",
		iRussian: "Afiny",
		iSpanish: "Atenas",
		iTurkish: "Atina",
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
		iEnglish: "Avlona"
		iGreek: "Avlonas",
		iItalian: "Valona",
		iLatin: _,
		iLocal: u"Vlorë", # Albanian
		iTurkish: "Avlonya",
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
		iPortguese: "Aujila",
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
		iDutch: "Bagdad",
		iGerman: "Bagdad",
		iLatin: "Bagdatum",
		iNorse: "Bagdad",
		iPolish: "Bagdad",
		iSpanish: "Bagdad",
		iTurkish: "Bagdat",
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
	"Baker Lake": {
		iEnglish: _,
		iLocal: "Qamani'tuaq", # Inuktitut
	},
	"Baku": {
		iArabic: "Bakuya",
		iLocal: "Baki", # Azerbaijani
		iPersian: {
			translate("Bad-kube", iBefore=iClassical),
			_,
		},
		iRussian: _,
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
		iLangKhmer: "Bang Makok",
		iThai: _,
	},
	"Banjar Masih": {
		iDutch: "Bandjermasin",
		iMalay: (
			translate("Banjarmasin", iAfter=iIndustrial),
			_,
		),
	},
	"Banten": (
		iMalay: (
			translate("Serang", iAfter=iIndustrial),
			_,
		),
	),
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
			found("Alexandreia i en Ephrati")
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
		iDutch: "Benkoelen",
		iEnglish: "Bencoolen",
		iMalay: _,
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
		iPortguese: "Belgrado",
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
		iPortguese: "Bilbau",
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
	"Birnin Kebbi": {
		iLocal: (
			relocate("Sakkwato", iReligion=iIslam),
			_,
		),
	},
	"Bishkek": {
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
		iSwahili: _,
	},
	"Bomani": {
		iArabic: rename("Baraka"),
		iDutch: rename("Baraka"),
		iFrench: rename("Baraka"),
		iSwahili: rename("Baraka"),
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
		iPortguese: u"Bordéus",
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
		iItalian: "Brema"
		iJapanese: "Buremen",
		iKorean: "Beuremen",
		iLatin: "Brema",
		iNorse: (
			translate("Brimarborg", iBefore=iMedieval),
			_,
		),
		iPolish: "Brema",
		iPortguese: "Brema",
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
		iRus: "Berestia",
		iRussian: _,
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
		iDutch: "Buchara",
		iEnglish: "Bokhara",
		iFrench: "Boukhara",
		iGreek: u"Mpoukhára",
		iLocal: translate("Buxarak", iBefore=iMedieval), # Sogdian
		iPersian: _,
		iPolish: "Bucara",
		iPortuguese: "Bucara",
		iRussian: _,
		iSpanish: u"Bujará",
		iTurkish: "Buxoro",
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
		iRus: "Bydhoshch",
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
	
	
	"Carnot": {  # founded on Bouar
		iFrench: _,
		iLocal: "Tendira",
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
	"Chernah": {  # founded on Arguin
		iLatin: "Cerne",
		iPhoenician: _,
	},
	"Cluniaco": {  # founded on Burgos
		iCeltic: _,
		iLatin: "Colonia Clunia Sulpicia",
		iSpanish: "Clunia",
	},
	"Colombo": {  # relocated from Anuratapuram
		iArabic: "Kalanpu",
		iDravidian: "Kolumpu",
		iDutch: _,
		iEnglish: _,
		iIndian: "Kolamba",
		iPortuguese: _,
	},
	"Constantinopolis": {  # renamed from Byzantion
		iArabic: "Qustantiniyya",
		iChinese: "Junshitandingbao"
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
	"Counani": {  # founded on Amapá
		iFrench: _,
		iPortuguese: "Cunani", 
	},
	"Cuito": {
		iLocal: "Kuito",
		iPortuguese: _,
	},
	"Daman": {
		iIndian: _,
		iPersian: _,
		iPortuguese: u"Damão",
	},
	"Dannemarksnagore": {  # founded on Bishnupur
		iIndian: "Gondalpara",
		iNorse: _,
	},
	"Dhanyakataka": {
		iEnglish: relocate("Bejjamwada"),
		iIndian: _,
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
	"Djibouti": {  # founded on Saylac
		iArabic: "Ghibuti",
		iFrench: _,
		iGerman: "Dschibuti",
		iItalian: "Gibuti",
		iSomali: "Jabuuti",
		iSpanish: "Yibuti",
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
	"Dvin": {  # relocated from Artashat
		iArabic: "Dabil",
		iGreek: "Tibion",
		iLocal: _, # Armenian
	},
	"Emerita Augusta": {  # founded on Batalyaws
		iArabic: "Marida",
		iLatin: _,
		iSpanish: u"Mérida",
	},
	"Flaviobriga": {  # founded on Bilbao
		iCeltic: "Portus Amanum",
		iLatin: _,
		iSpanish: "Castro Urdial
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
	"Fort Ouiatenon": {
		iEnglish: "Lafayette",
		iFrench: _,
		iLocal: "Waayaahtanonki", # Wea
	},
	u"Fort Pentaguët": {
		iFrench: _,
		iLocal: "Majabagaduce", # Abenaki
	},
	"Gustavia": {  # founded on Basse-Terre
		iFrench: u"Le Carénage",
		iSwedish: _,
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
	"Induru": {
		iIndian: (
			translate("Indhrapuri", iAfter=iMedieval),
			_,
		),
		iPersian: "Nizamabad",
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
	"Kleopatris": {
		iGreek: _,
		iLatin: "Cleopatra",
	},
	"Kokshetav": {  # relocated from Atbasar
		iRussian: _,
		iTurkish: u"Kökshetau",
	},
	"Kotah": {  # relocated from Bundi
		iIndian: "Kota",
		iPersian: _,
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
	"Newcastle, kwaZulu-Natal": {  # founded on Bulawayo
		iDutch: "Viljoensdorp",
		iEnglish: "Newcastle",
	},
	"Nguru": {
		iFrench: "N'Gourou",
		iLocal: _,
	},
	"Nikomedeia": {
		iGreek: _,
		iLatin: "Nicomedia",
		iTurkish: "Izmit",
	},
	"Okoloama": {
		iEnglish: (
			relocate("Port Harcourt", iAfter=iGlobal),
			"Bonny",
		),
		iLocal: _, # Igbo
	},
	"Orestias": {
		iGreek: _,
		iLatin: rename("Hadrianopolis"),
		iLocal: "Uskudama", # Thracian
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
	"Puerto Lempira": {  # founded on Black River
		iLocal: "Auhya Yari",
		iSpanish: _,
	},
	"Qazimbazar": {  # founded on Bishnupur
		iEnglish: "Cassimbazar",
		iPersian: _,
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
	"Singaraja": {
		iDutch: "Singaradja",
		iLocal: _,
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
		iRus: "Stokhol'm",
		iRussian: "Stokgol'm",
		iSpanish: "Estocolmo",
		iSwedish: _,
		iThai: "Sa-tok-home",
		iTurkish: "Stokholm",
	},
	"Surat": {
		iArabic: "Subara",
		iDutch: "Sourratte",
		iEnglish: _,
		iIndian: "Suryapur",
		iPersian: "Sourat",
		iPortuguese: "Suratt",
	},
	"Tamanrasset": {  # relocated from Abalessa
		iArabic: _,
		iBerber: "Tamenghast",
		iFrench: "Fort Laperrine",
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
	"Uigandes": {
		iDutch: (
			translate("Bethanie", iAfter=iGlobal),
			"Klipfontein",
		),
		iEnglish: "Bethany",
		iGerman: "Bethanien",
		iLocal: _, # Khoekhoegowab
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
	"Warmbad": {  # founded on Bassonsdrif
		iGerman: _,
		iLocal: "Aixa-aibes", # Nama
	},
	"Warzazat": {  # relocated from Aghmat
		iArabic: _,
		iFrench: "Ouarzazate",
	},
	u"Xigazê": {
		iChinese: (
			relocate("Nianmai", iBefore=iRenaissance),
			"Rikaze",
		),
		iEnglish: "Shigatse",
		iTibetan: _,
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
