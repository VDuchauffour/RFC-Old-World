# coding: utf-8

from Civics import *
from RFCUtils import *
from Areas import *
from Locations import *
from Core import *

from Events import handler
from Core import name as short
from Core import adjective as civAdjective

import CityNames as cn


### Constants ###

encoding = "utf-8"

### Dictionaries with text keys

dDefaultInsertNames = {
	iNorse : "TXT_KEY_CIV_NORSE_SCANDINAVIA",
	iKhmer : "TXT_KEY_CIV_KHMER_KAMPUCHEA",
	iNetherlands : "TXT_KEY_CIV_NETHERLANDS_ARTICLE",
	iDravidia : "TXT_KEY_CIV_DRAVIDIA_TAMIL_NADU",
	iMaya : "TXT_KEY_CIV_MAYA_YUCATAN",
	iThailand : "TXT_KEY_CIV_THAILAND_SIAM",
	iMoors : "TXT_KEY_CIV_MOORS_MOROCCO",
	iMughals : "TXT_KEY_CIV_MUGHALS_DELHI",
	iHarappa : "TXT_KEY_CIV_HARAPPA_INDUS",
}

dDefaultInsertAdjectives = {
	iNorse : "TXT_KEY_CIV_NORSE_SCANDINAVIAN",
	iKhmer : "TXT_KEY_CIV_KHMER_KAMPUCHEAN",
	iThailand : "TXT_KEY_CIV_THAILAND_SIAMESE",
	iMoors : "TXT_KEY_CIV_MOORS_MOROCCAN",
}

dSpecificVassalTitles = deepdict({
	iEgypt : {
		iPhoenicia : "TXT_KEY_CIV_EGYPTIAN_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_EGYPTIAN_ETHIOPIA",
	},
	iBabylonia : {
		iPhoenicia : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iChina : {
		iKorea : "TXT_KEY_CIV_CHINESE_KOREA",
		iTurks : "TXT_KEY_CIV_CHINESE_TURKS",
		iMongols : "TXT_KEY_CIV_CHINESE_MONGOLIA",
	},
	iGreece : {
		iIndia : "TXT_KEY_CIV_GREEK_INDIA",
		iEgypt : "TXT_KEY_CIV_GREEK_EGYPT",
		iPersia : "TXT_KEY_CIV_GREEK_PERSIA",
		iRome : "TXT_KEY_CIV_GREEK_ROME",
	},
	iIndia : {
		iAztecs: "TXT_KEY_CIV_INDIAN_AZTECS",
	},
	iPersia : {
		iEgypt : "TXT_KEY_CIV_PERSIAN_EGYPT",
		iIndia : "TXT_KEY_CIV_PERSIAN_INDIA",
		iBabylonia : "TXT_KEY_CIV_PERSIAN_BABYLONIA",
		iGreece : "TXT_KEY_CIV_PERSIAN_GREECE",
		iEthiopia : "TXT_KEY_CIV_PERSIAN_ETHIOPIA",
		iArabia : "TXT_KEY_CIV_PERSIAN_ARABIA",
		iMongols : "TXT_KEY_CIV_PERSIAN_MONGOLIA",
	},
	iJapan : {
		iChina : "TXT_KEY_CIV_JAPANESE_CHINA",
		iIndia : "TXT_KEY_CIV_JAPANESE_INDIA",
		iKorea : "TXT_KEY_CIV_JAPANESE_KOREA",
		iMongols : "TXT_KEY_CIV_JAPANESE_MONGOLIA",
	},
	iByzantium : {
		iEgypt : "TXT_KEY_CIV_BYZANTINE_EGYPT",
		iBabylonia : "TXT_KEY_CIV_BYZANTINE_BABYLONIA",
		iGreece : "TXT_KEY_CIV_BYZANTINE_GREECE",
		iPhoenicia : "TXT_KEY_CIV_BYZANTINE_CARTHAGE",
		iPersia : "TXT_KEY_CIV_BYZANTINE_PERSIA",
		iRome : "TXT_KEY_CIV_BYZANTINE_ROME",
		iSpain : "TXT_KEY_CIV_BYZANTINE_SPAIN",
	},
	iNorse : {
		iEngland : "TXT_KEY_CIV_NORSE_ENGLAND",
		iRussia : "TXT_KEY_CIV_NORSE_RUSSIA",
	},
	iArabia : {
		iOttomans : "TXT_KEY_CIV_ARABIAN_OTTOMANS",
		iMughals : "TXT_KEY_CIV_ARABIAN_MUGHALS",
	},
	iMoors : {
		iArabia : "TXT_KEY_CIV_MOORISH_ARABIA",
		iMali : "TXT_KEY_CIV_MOORISH_MALI",
	},
	iSpain : {
		iPhoenicia : "TXT_KEY_CIV_SPANISH_CARTHAGE",
		iEthiopia : "TXT_KEY_CIV_SPANISH_ETHIOPIA",
		iMaya : "TXT_KEY_CIV_SPANISH_MAYA",
		iByzantium : "TXT_KEY_CIV_SPANISH_BYZANTIUM",
		iMoors : "TXT_KEY_CIV_SPANISH_MOORS",
		iFrance : "TXT_KEY_CIV_SPANISH_FRANCE",
		iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
		iMali : "TXT_KEY_CIV_SPANISH_MALI",
		iPortugal : "TXT_KEY_CIV_SPANISH_PORTUGAL",
		iAmerica : "TXT_KEY_CIV_SPANISH_AMERICA",
		iArgentina : "TXT_KEY_CIV_SPANISH_ARGENTINA",
		iColombia : "TXT_KEY_CIV_SPANISH_COLOMBIA",
	},
	iFrance : {
		iEgypt : "TXT_KEY_MANDATE_OF",
		iBabylonia : "TXT_KEY_CIV_FRENCH_BABYLONIA",
		iGreece : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iPersia : "TXT_KEY_MANDATE_OF",
		iPhoenicia : "TXT_KEY_CIV_FRENCH_PHOENICIA",
		iItaly : "TXT_KEY_CIV_FRENCH_ITALY",
		iEthiopia : "TXT_KEY_CIV_FRENCH_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_FRENCH_BYZANTIUM",
		iNorse : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iArabia : "TXT_KEY_MANDATE_OF",
		iEngland : "TXT_KEY_CIV_FRENCH_ENGLAND",
		iSpain : "TXT_KEY_CIV_FRENCH_SPAIN",
		iHolyRome : "TXT_KEY_CIV_FRENCH_HOLY_ROME",
		iPoland : "TXT_KEY_CIV_FRENCH_POLAND",
		iNetherlands : "TXT_KEY_CIV_FRENCH_NETHERLANDS",
		iMali : "TXT_KEY_CIV_FRENCH_MALI",
		iPortugal : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iInca : "TXT_KEY_CIV_FRENCH_INCA",
		iAztecs : "TXT_KEY_CIV_FRENCH_AZTECS",
		iMughals : "TXT_KEY_MANDATE_OF",
		iCongo : "TXT_KEY_ADJECTIVE_TITLE",
		iRussia : "TXT_KEY_CIV_FRANCE_DEPARTEMENTS_OF",
		iOttomans : "TXT_KEY_MANDATE_OF",
		iAmerica : "TXT_KEY_CIV_FRENCH_AMERICA",
	},
	iEngland : {
		iEgypt : "TXT_KEY_MANDATE_OF",
		iIndia : "TXT_KEY_CIV_ENGLISH_INDIA",
		iBabylonia : "TXT_KEY_CIV_ENGLISH_BABYLONIA",
		iPersia : "TXT_KEY_MANDATE_OF",
		iPhoenicia : "TXT_KEY_CIV_ENGLISH_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_ENGLISH_ETHIOPIA",
		iMaya : "TXT_KEY_CIV_ENGLISH_MAYA",
		iByzantium : "TXT_KEY_CIV_ENGLISH_BYZANTIUM",
		iNorse : "TXT_KEY_CIV_ENGLISH_NORSE",
		iArabia : "TXT_KEY_MANDATE_OF",
		iFrance : "TXT_KEY_CIV_ENGLISH_FRANCE",
		iHolyRome : "TXT_KEY_CIV_ENGLISH_HOLY_ROME",
		iGermany : "TXT_KEY_CIV_ENGLISH_GERMANY",
		iNetherlands : "TXT_KEY_CIV_ENGLISH_NETHERLANDS",
		iMali : "TXT_KEY_CIV_ENGLISH_MALI",
		iOttomans : "TXT_KEY_MANDATE_OF",
		iAmerica : "TXT_KEY_CIV_ENGLISH_AMERICA",
	},
	iHolyRome : {
		iItaly : "TXT_KEY_CIV_HOLY_ROMAN_ITALY",
		iFrance : "TXT_KEY_CIV_HOLY_ROMAN_FRANCE",
		iNetherlands : "TXT_KEY_CIV_HOLY_ROMAN_NETHERLANDS",
		iByzantium : "TXT_KEY_CIV_HOLY_ROMAN_BYZANTIUM",
		iPoland : "TXT_KEY_CIV_HOLY_ROMAN_POLAND",
	},
	iPortugal : {
		iIndia : "TXT_KEY_CIV_PORTUGUESE_INDIA",
		iMali : "TXT_KEY_CIV_PORTUGUESE_MALI",
		iCongo : "TXT_KEY_CIV_PORTUGUESE_CONGO",
		iBrazil : "TXT_KEY_CIV_PORTUGUESE_BRAZIL",
	},
	iMongols : {
		iEgypt : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iChina : "TXT_KEY_CIV_MONGOL_CHINA",
		iBabylonia : "TXT_KEY_CIV_MONGOL_BABYLONIA",
		iGreece : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iPersia : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iPhoenicia : "TXT_KEY_CIV_MONGOL_PHOENICIA",
		iRome : "TXT_KEY_CIV_MONGOL_ILKHANATE",
		iByzantium : "TXT_KEY_CIV_MONGOL_BYZANTIUM",
		iRussia : "TXT_KEY_CIV_MONGOL_RUSSIA",
		iOttomans : "TXT_KEY_CIV_MONGOL_OTTOMANS",
		iMughals : "TXT_KEY_CIV_MONGOL_MUGHALS",
	},
	iMughals : {
		iIndia : "TXT_KEY_CIV_MUGHAL_INDIA",
	},
	iRussia : {
		iTurks : "TXT_KEY_ADJECTIVE_TITLE",
		iPoland : "TXT_KEY_CIV_RUSSIAN_POLAND",
		iAmerica : "TXT_KEY_ADJECTIVE_TITLE",
	},
	iOttomans : {
		iEgypt : "TXT_KEY_CIV_OTTOMAN_EGYPT",
		iBabylonia : "TXT_KEY_CIV_OTTOMAN_BABYLONIA",
		iPersia : "TXT_KEY_CIV_OTTOMAN_PERSIA",
		iGreece : "TXT_KEY_CIV_OTTOMAN_GREECE",
		iPhoenicia : "TXT_KEY_CIV_OTTOMAN_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_OTTOMAN_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_OTTOMAN_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_OTTOMAN_ARABIA",
		iRussia : "TXT_KEY_CIV_OTTOMAN_RUSSIA",
	},
	iNetherlands : {
		iMali : "TXT_KEY_CIV_DUTCH_MALI",
		iEthiopia : "TXT_KEY_CIV_DUTCH_ETHIOPIA",
		iCongo : "TXT_KEY_CIV_DUTCH_CONGO",
		iAmerica : "TXT_KEY_CIV_DUTCH_AMERICA",
		iBrazil : "TXT_KEY_CIV_DUTCH_BRAZIL",
	},
	iGermany : {
		iHolyRome : "TXT_KEY_CIV_GERMAN_HOLY_ROME",
		iMali : "TXT_KEY_CIV_GERMAN_MALI",
		iEthiopia : "TXT_KEY_CIV_GERMAN_ETHIOPIA",
		iPoland : "TXT_KEY_CIV_GERMAN_POLAND",
	},
	iAmerica : {
		iEngland : "TXT_KEY_CIV_AMERICAN_ENGLAND",
		iJapan : "TXT_KEY_CIV_AMERICAN_JAPAN",
		iGermany : "TXT_KEY_CIV_AMERICAN_GERMANY",
		iAztecs : "TXT_KEY_CIV_AMERICAN_MEXICO",
		iMaya : "TXT_KEY_CIV_AMERICAN_MAYA",
		iKorea : "TXT_KEY_CIV_AMERICAN_KOREA",
	},
	iBrazil : {
		iArgentina : "TXT_KEY_CIV_BRAZILIAN_ARGENTINA",
	},
})

dMasterTitles = {
	iEgypt : "TXT_KEY_CIV_EGYPTIAN_VASSAL",
	iChina : "TXT_KEY_CIV_CHINESE_VASSAL",
	iIndia : "TXT_KEY_CIV_INDIAN_VASSAL",
	iPersia : "TXT_KEY_CIV_PERSIAN_VASSAL",
	iRome : "TXT_KEY_CIV_ROMAN_VASSAL",
	iJapan : "TXT_KEY_CIV_JAPANESE_VASSAL",
	iByzantium : "TXT_KEY_CIV_BYZANTINE_VASSAL",
	iTurks : "TXT_KEY_CIV_TURKIC_VASSAL",
	iArabia : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iTibet : "TXT_KEY_CIV_TIBETAN_VASSAL",
	iMoors : "TXT_KEY_CIV_ARABIAN_VASSAL",
	iSpain : "TXT_KEY_CIV_SPANISH_VASSAL",
	iFrance : "TXT_KEY_ADJECTIVE_TITLE",
	iEngland : "TXT_KEY_CIV_ENGLISH_VASSAL",
	iPoland : "TXT_KEY_CIV_POLISH_VASSAL",
	iNetherlands : "TXT_KEY_ADJECTIVE_TITLE",
	iPortugal : "TXT_KEY_ADJECTIVE_TITLE",
	iMongols : "TXT_KEY_CIV_MONGOL_VASSAL",
	iMughals : "TXT_KEY_CIV_MUGHAL_VASSAL",
	iRussia : "TXT_KEY_CIV_RUSSIAN_VASSAL",
	iOttomans : "TXT_KEY_CIV_OTTOMAN_VASSAL",
	iThailand : "TXT_KEY_CIV_THAI_VASSAL",
}

dCommunistVassalTitlesGeneric = {
	iRussia : "TXT_KEY_CIV_RUSSIA_SOVIET",
}

dCommunistVassalTitles = deepdict({
	iRussia : {
		iChina : "TXT_KEY_CIV_RUSSIA_SOVIET_REPUBLIC_ADJECTIVE",
		iTurks : "TXT_KEY_CIV_RUSSIA_SOVIET_TURKS",
		iJapan : "TXT_KEY_CIV_RUSSIA_SOVIET_JAPAN",
		iOttomans : "TXT_KEY_CIV_RUSSIA_SOVIET_OTTOMANS",
		iGermany : "TXT_KEY_CIV_RUSSIA_SOVIET_GERMANY",
	},
})

dFascistVassalTitlesGeneric = {
	iGermany : "TXT_KEY_ADJECTIVE_TITLE"
}

dFascistVassalTitles = deepdict({
	iGermany : {
		iEgypt : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iChina : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iGreece : "TXT_KEY_CIV_GERMANY_NAZI_GREECE",
		iPhoenicia : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iRome : "TXT_KEY_CIV_GERMANY_REICHSPROTEKTORAT",
		iEthiopia : "TXT_KEY_CIV_GERMANY_NAZI_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_GERMANY_NAZI_BYZANTIUM",
		iSpain : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iFrance : "TXT_KEY_CIV_GERMANY_NAZI_FRANCE",
		iEngland : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iHolyRome : "TXT_KEY_CIV_GERMANY_NAZI_HOLY_ROME",
		iNetherlands : "TXT_KEY_CIV_GERMANY_NAZI_NETHERLANDS",
		iMali : "TXT_KEY_CIV_GERMANY_NAZI_MALI",
		iPoland : "TXT_KEY_CIV_GERMANY_NAZI_POLAND",
		iPortugal : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iMughals : "TXT_KEY_CIV_GERMANY_NAZI_MUGHALS",
		iRussia : "TXT_KEY_CIV_GERMANY_NAZI_RUSSIA",
		iOttomans : "TXT_KEY_CIV_GERMANY_REICHSKOMMISSARIAT",
		iCanada : "TXT_KEY_CIV_GERMANY_NAZI_CANADA",
	},
})

dForeignAdjectives = deepdict({
	iChina : {
		iEgypt : "TXT_KEY_CIV_CHINESE_ADJECTIVE_EGYPT",
		iIndia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_INDIA",
		iBabylonia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BABYLONIA",
		iPersia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_PERSIA",
		iRome : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ROME",
		iJapan : "TXT_KEY_CIV_CHINESE_ADJECTIVE_JAPAN",
		iKorea : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KOREA",
		iByzantium : "TXT_KEY_CIV_CHINESE_ADJECTIVE_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_CHINESE_ADJECTIVE_ARABIA",
		iKhmer : "TXT_KEY_CIV_CHINESE_ADJECTIVE_KHMER",
		iMongols : "TXT_KEY_CIV_CHINESE_ADJECTIVE_MONGOLIA",
		iOttomans : "TXT_KEY_CIV_CHINESE_ADJECTIVE_OTTOMANS",
		iTibet : "TXT_KEY_CIV_CHINESE_ADJECTIVE_TIBET",
	},
})

dForeignNames = deepdict({
	iGreece : {
		iTurks : "TXT_KEY_CIV_GREEK_NAME_TURKS",
	},
	iPersia : {
		iByzantium : "TXT_KEY_CIV_PERSIAN_NAME_BYZANTIUM",
		iTurks : "TXT_KEY_CIV_PERSIAN_NAME_TURKS",
	},
	iRome : {
		iEgypt : "TXT_KEY_CIV_ROMAN_NAME_EGYPT",
		iChina : "TXT_KEY_CIV_ROMAN_NAME_CHINA",
		iBabylonia : "TXT_KEY_CIV_ROMAN_NAME_BABYLONIA",
		iGreece : "TXT_KEY_CIV_ROMAN_NAME_GREECE",
		iPersia : "TXT_KEY_CIV_ROMAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ROMAN_NAME_PHOENICIA",
		iEthiopia : "TXT_KEY_CIV_ROMAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ROMAN_NAME_BYZANTIUM",
		iNorse : "TXT_KEY_CIV_ROMAN_NAME_NORSE",
		iTurks : "TXT_KEY_CIV_ROMAN_NAME_TURKS",
		iKhmer : "TXT_KEY_CIV_ROMAN_NAME_KHMER",
		iSpain : "TXT_KEY_CIV_ROMAN_NAME_SPAIN",
		iFrance : "TXT_KEY_CIV_ROMAN_NAME_FRANCE",
		iEngland : "TXT_KEY_CIV_ROMAN_NAME_ENGLAND",
		iHolyRome : "TXT_KEY_CIV_ROMAN_NAME_HOLY_ROME",
		iGermany : "TXT_KEY_CIV_ROMAN_NAME_GERMANY",
		iNetherlands : "TXT_KEY_CIV_ROMAN_NAME_NETHERLANDS",
		iMali : "TXT_KEY_CIV_ROMAN_NAME_MALI",
		iPortugal : "TXT_KEY_CIV_ROMAN_NAME_PORTUGAL",
		iMongols : "TXT_KEY_CIV_ROMAN_NAME_MONGOLIA",
		iRussia : "TXT_KEY_CIV_ROMAN_NAME_RUSSIA",
		iOttomans : "TXT_KEY_CIV_ROMAN_NAME_OTTOMANS",
		iThailand : "TXT_KEY_CIV_ROMAN_NAME_THAILAND",
	},
	iTurks : {
		iByzantium : "TXT_KEY_CIV_TURKIC_NAME_BYZANTIUM",
	},
	iArabia : {
		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iTurks : "TXT_KEY_CIV_ARABIAN_NAME_TURKS",
		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
	},
	iTibet : {
		iChina : "TXT_KEY_CIV_TIBETAN_NAME_CHINA",
		iIndia : "TXT_KEY_CIV_TIBETAN_NAME_INDIA",
		iTurks : "TXT_KEY_CIV_TIBETAN_NAME_TURKS",
		iMongols : "TXT_KEY_CIV_TIBETAN_NAME_MONGOLIA",
	},
	iMoors : {
		iEgypt : "TXT_KEY_CIV_ARABIAN_NAME_EGYPT",
		iBabylonia : "TXT_KEY_CIV_ARABIAN_NAME_BABYLONIA",
		iPersia : "TXT_KEY_CIV_ARABIAN_NAME_PERSIA",
		iPhoenicia : "TXT_KEY_CIV_ARABIAN_NAME_CARTHAGE",
		iRome : "TXT_KEY_CIV_ARABIAN_NAME_ROME",
		iEthiopia : "TXT_KEY_CIV_ARABIAN_NAME_ETHIOPIA",
		iByzantium : "TXT_KEY_CIV_ARABIAN_NAME_BYZANTIUM",
		iArabia : "TXT_KEY_CIV_ARABIAN_NAME_ARABIA",
		iMoors : "TXT_KEY_CIV_ARABIAN_NAME_MOORS",
		iSpain : "TXT_KEY_CIV_ARABIAN_NAME_SPAIN",
		iPortugal : "TXT_KEY_CIV_ARABIAN_NAME_PORTUGAL",
	},
	iSpain : {
		iKhmer : "TXT_KEY_CIV_SPANISH_NAME_KHMER",
		iAztecs : "TXT_KEY_CIV_SPANISH_NAME_AZTECS",
		iMughals : "TXT_KEY_CIV_SPANISH_NAME_MUGHALS",
	},
	iFrance : {
		iKhmer : "TXT_KEY_CIV_FRENCH_NAME_KHMER",
		iMughals : "TXT_KEY_CIV_FRENCH_NAME_MUGHALS",
	},
	iEngland : {
		iKhmer : "TXT_KEY_CIV_ENGLISH_NAME_KHMER",
		iMughals : "TXT_KEY_CIV_ENGLISH_NAME_MUGHALS",
	},
	iRussia : {
		iPersia : "TXT_KEY_CIV_RUSSIAN_NAME_PERSIA",
	},
	iMongols : {
		iTurks : "TXT_KEY_CIV_MONGOL_NAME_TURKS"
	},
	iOttomans : {
		iPoland : "TXT_KEY_CIV_OTTOMAN_NAME_POLAND",
		iGermany : "TXT_KEY_CIV_OTTOMAN_NAME_GERMANY",
	},
	iGermany : {
		iMoors : "TXT_KEY_CIV_GERMAN_NAME_MOORS",
	},
})

lRepublicOf = [iEgypt, iIndia, iChina, iPersia, iJapan, iEthiopia, iKorea, iNorse, iTurks, iTibet, iKhmer, iHolyRome, iMali, iPoland, iMughals, iOttomans, iThailand, iIran]
lRepublicAdj = [iBabylonia, iRome, iMoors, iSpain, iFrance, iPortugal, iInca, iItaly, iAztecs, iArgentina]

lSocialistRepublicOf = [iEgypt, iMoors, iHolyRome, iBrazil, iNorse, iColombia]
lSocialistRepublicAdj = [iPersia, iTurks, iItaly, iAztecs, iIran, iArgentina]

lPeoplesRepublicOf = [iIndia, iChina, iPolynesia, iJapan, iTibet, iMali, iPoland, iMughals, iThailand, iCongo]
lPeoplesRepublicAdj = [iDravidia, iByzantium, iMongols]

lIslamicRepublicOf = [iIndia, iPersia, iMali, iMughals, iIran]

dEmpireThreshold = {
	iPhoenicia : 4,
	iPolynesia : 3,
	iDravidia : 3,
	iKorea : 4,
	iTibet : 2,
	iMoors : 3,
	iHolyRome : 3,
	iPoland : 3,
	iInca : 3,
	iMongols : 8,
	iMughals : 6,
	iItaly : 4,
	iRussia : 8,
	iIran : 4,
	iGermany : 4,
}

lChristianity = [iCatholicism, iOrthodoxy, iProtestantism]

lRespawnNameChanges = [iHolyRome, iInca, iAztecs, iMali] # TODO: this should be covered by period
lVassalNameChanges = [iInca, iAztecs, iMughals] # TODO: this should be covered by period
lChristianityNameChanges = [iInca, iAztecs] # TODO: this should be covered by period

lColonies = [iMali, iEthiopia, iCongo, iSwahili, iToltecs, iAztecs, iInca, iMaya] # TODO: could be covered by more granular continental regions

dNameChanges = { # TODO: this should be covered by period
	iPhoenicia : "TXT_KEY_CIV_CARTHAGE_SHORT_DESC",
	iAztecs : "TXT_KEY_CIV_MEXICO_SHORT_DESC",
	iInca : "TXT_KEY_CIV_PERU_SHORT_DESC",
	iHolyRome : "TXT_KEY_CIV_AUSTRIA_SHORT_DESC",
	iMali : "TXT_KEY_CIV_SONGHAI_SHORT_DESC",
	iMughals : "TXT_KEY_CIV_PAKISTAN_SHORT_DESC",
	iMoors : "TXT_KEY_CIV_MOROCCO_SHORT_DESC",
	iTurks : "TXT_KEY_CIV_UZBEKS_SHORT_DESC",
}

dAdjectiveChanges = {
	iPhoenicia : "TXT_KEY_CIV_CARTHAGE_ADJECTIVE",
	iAztecs : "TXT_KEY_CIV_MEXICO_ADJECTIVE",
	iInca : "TXT_KEY_CIV_PERU_ADJECTIVE",
	iHolyRome : "TXT_KEY_CIV_AUSTRIA_ADJECTIVE",
	iMali : "TXT_KEY_CIV_SONGHAI_ADJECTIVE",
	iMughals : "TXT_KEY_CIV_PAKISTAN_ADJECTIVE",
	iMoors : "TXT_KEY_CIV_MOROCCO_ADJECTIVE",
	iTurks : "TXT_KEY_CIV_UZBEKS_ADJECTIVE",
}

dStartingLeaders = [
# 3000 BC
{
	iIndependent : iIndependentLeader,
	iIndependent2 : iIndependentLeader,
	iNative : iNativeLeader,
	iEgypt : iDjoser,
	iIndia : iAsoka,
	iBabylonia : iSargon,
	iHarappa : iWentAntu,
	iAssyria : iAshurbanipal,
	iChina : iQinShiHuang,
	iHittites : iMursili,
	iNubia : iTaharqa,
	iGreece : iPericles,
	iPersia : iCyrus,
	iCarthage : iHiram,
	iPolynesia : iAhoeitu,
	iRome : iScipio,
	iCelts : iBrennus,
	iMaya : iPacal,
	iJapan : iKammu,
	iDravidia : iRajendra,
	iEthiopia : iEzana,
	iVietnam: iLeLoi,
	iToltecs : iTopiltzin,
	iKushans: iKanishka,
	iKorea : iWangKon,
	iByzantium : iJustinian,
	iMalays : iSriJayanasa,
	iNorse : iRagnar,
	iTurks : iBumin,
	iArabia : iHarun,
	iTibet : iSongtsen,
	iKhmer : iNeangNeak,
	iMoors : iRahman,
	iJava : iHayamWuruk,
	iSpain : iIsabella,
	iFrance : iCharlemagne,
	iEngland : iAlfred,
	iHolyRome : iBarbarossa,
	iBurma : iAnawrahta,
	iRus : iYaroslav,
	iSwahili : iDawud,
	iMali : iMansaMusa,
	iPoland : iCasimir,
	iPortugal : iAfonso,
	iInca : iHuaynaCapac,
	iItaly : iLorenzo,
	iMongols : iGenghisKhan,
	iAztecs : iMontezuma,
	iMughals : iTughluq,
	iThailand : iNaresuan,
	iSweden : iGustav,
	iRussia : iIvan,
	iOttomans : iMehmed,
	iCongo : iMbemba,
	iIran : iAbbas,
	iNetherlands : iWillemVanOranje,
	iGermany : iFrederick,
	iAmerica : iWashington,
	iArgentina : iSanMartin,
	iMexico : iJuarez,
	iColombia : iBolivar,
	iBrazil : iPedro,
	iCanada : iMacDonald,
},
# 600 AD
{
	iChina : iTaizong,
},
# 1700 AD
{
	iChina : iHongwu,
	iIndia : iShivaji,
	iDravidia : iKrishnaDevaRaya,
	iKorea : iSejong,
	iNorse : iChristian,
	iJapan : iOdaNobunaga,
	iTurks : iTamerlane,
	iSpain : iPhilip,
	iFrance : iLouis,
	iEngland : iVictoria,
	iHolyRome : iFrancis,
	iBurma : iBayinnaung,
	iVietnam : iLeLoi,
	iPoland : iSobieski,
	iPortugal : iJoao,
	iMughals : iAkbar,
	iSweden : iGustav,
	iRussia : iPeter,
	iOttomans : iSuleiman,
	iNetherlands : iWilliam,
}]

### Event handlers

@handler("GameStart")
def setup():
	iScenario = scenario()
	
	# if iScenario == i600AD:
	# 	data.civs[iChina].iAnarchyTurns += 3
		
	# elif iScenario == i1700AD:
	# 	data.civs[iEgypt].iResurrections += 1
	
@handler("playerCivAssigned")
def initName(iPlayer):
	if not is_minor(iPlayer) and player(iPlayer).getNumCities() == 0:
		setDesc(iPlayer, peoplesName(iPlayer))
		checkName(iPlayer)
		checkLeader(iPlayer)

@handler("resurrection")
def onResurrection(iPlayer):
	onRespawn(iPlayer)

def onRespawn(iPlayer):
	data.civs[iPlayer].iResurrections += 1
	
	if civ(iPlayer) in lRespawnNameChanges:
		checkNameChange(iPlayer)
		checkAdjectiveChange(iPlayer)
		
	setDesc(iPlayer, defaultTitle(iPlayer))
	checkName(iPlayer)
	checkLeader(iPlayer)

@handler("vassalState")	
def onVassalState(iMaster, iVassal):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)

	if iVassalCiv in lVassalNameChanges:
		if iVassalCiv == iMughals and iMasterCiv not in dCivGroups[iCivGroupEurope]: return
	
		data.civs[iVassal].iResurrections += 1
		checkNameChange(iVassal)
		checkAdjectiveChange(iVassal)
		
	checkName(iVassal)

@handler("playerChangeStateReligion")
def onPlayerChangeStateReligion(iPlayer, iReligion):
	if is_minor(iPlayer):
		return

	if civ(iPlayer) in lChristianityNameChanges and iReligion in lChristianity:
		data.civs[iPlayer].iResurrections += 1
		checkNameChange(iPlayer)
		checkAdjectiveChange(iPlayer)
		
	checkName(iPlayer)

@handler("revolution")
def onRevolution(iPlayer):
	if is_minor(iPlayer):
		return

	data.civs[iPlayer].iAnarchyTurns += 1
	
	if civ(iPlayer) == iMughals and isRepublic(iPlayer):
		checkNameChange(iPlayer)
	
	checkName(iPlayer)
	
	for iLoopPlayer in players.vassals(iPlayer):
		checkName(iLoopPlayer)
	
@handler("cityAcquired")
def onCityAcquired(iPreviousOwner, iNewOwner):
	checkName(iPreviousOwner)
	checkName(iNewOwner)

@handler("cityRazed")
def onCityRazed(city):
	iPreviousOwner = slot(Civ(city.getPreviousCiv()))
	if iPreviousOwner >= 0:
		checkName(iPreviousOwner)

@handler("cityBuilt")	
def onCityBuilt(city):
	checkName(city.getOwner())
	
@handler("playerPeriodChange")
def onPeriodChange(iPlayer, iPeriod):
	iCiv = civ(iPlayer)
	
	if iCiv == iPhoenicia:
		if iPeriod == iPeriodCarthage:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)
	
	if iCiv == iNorse:
		if iPeriod == iPeriodDenmark:
			setShort(iPlayer, text("TXT_KEY_CIV_DENMARK_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_DENMARK_ADJECTIVE"))
		elif iPeriod == iPeriodNorway:
			setShort(iPlayer, text("TXT_KEY_CIV_NORWAY_SHORT_DESC"))
			setAdjective(iPlayer, text("TXT_KEY_CIV_NORWAY_ADJECTIVE"))
	
	if iCiv == iTurks:
		if iPeriod == iPeriodUzbeks:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)
	
	if iCiv == iMoors:
		if iPeriod == iPeriodMorocco:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)
			
	if iCiv == iHolyRome:
		if iPeriod == iPeriodAustria:
			checkNameChange(iPlayer)
			checkAdjectiveChange(iPlayer)
	
	if iPeriod == -1:
		revertNameChange(iPlayer)
		revertAdjectiveChange(iPlayer)
	
	checkName(iPlayer)
	checkLeader(iPlayer)
	

@handler("religionFounded")
def onReligionFounded(_, iPlayer):
	if turn() == scenarioStartTurn():
		return

	checkName(iPlayer)


@handler("capitalMoved")
def onCapitalMoved(city):
	checkName(city.getOwner())


@handler("BeginGameTurn")
def checkTurn(iGameTurn):
	if every(10):
		for iPlayer in players.major():
			checkName(iPlayer)
			checkLeader(iPlayer)

		
def checkName(iPlayer):
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	if player(iPlayer).getNumCities() == 0: return
	setDesc(iPlayer, desc(iPlayer, title(iPlayer)))
	
def checkLeader(iPlayer):
	if player(iPlayer).isHuman(): return
	if not player(iPlayer).isAlive(): return
	if is_minor(iPlayer): return
	setLeader(iPlayer, leader(iPlayer))
	setLeaderName(iPlayer, leaderName(iPlayer))

### Setter methods for player object ###

def setDesc(iPlayer, sName):
	try:
		player(iPlayer).setCivDescription(sName)
	except:
		pass
	
def setShort(iPlayer, sShort):
	player(iPlayer).setCivShortDescription(sShort)
	
def setAdjective(iPlayer, sAdj):
	player(iPlayer).setCivAdjective(sAdj)
	
def setLeader(iPlayer, iLeader):
	if not iLeader: return
	if player(iPlayer).isHuman(): return
	if player(iPlayer).getLeader() == iLeader: return
	player(iPlayer).setLeader(iLeader)
	
def setLeaderName(iPlayer, sName):
	if not sName: return
	if infos.leader(player(iPlayer)).getText() != sName:
		player(iPlayer).setLeaderName(sName)

### Utility methods ###

def key(iPlayer, sSuffix):
	if sSuffix: sSuffix = "_%s" % sSuffix
	return "TXT_KEY_CIV_%s%s" % (str(short(iPlayer).replace(" ", "_").upper()), sSuffix)
	
def desc(iPlayer, sTextKey=str("%s1")):
	if team(iPlayer).isAVassal():
		return text(sTextKey, name(iPlayer), adjective(iPlayer), name(iPlayer, True), adjective(iPlayer, True))

	return text(sTextKey, name(iPlayer), adjective(iPlayer))

def capitalName(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: 
		sCapitalName = cn.translateName(iEngland, capital.getName())
		if sCapitalName: 
			return sCapitalName
		
		return capital.getName()
	
	return short(iPlayer)
	
def checkNameChange(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dNameChanges:
		setShort(iPlayer, text(dNameChanges[iCiv]))
	
def checkAdjectiveChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dAdjectiveChanges:
		setAdjective(iPlayer, text(dAdjectiveChanges[iCiv]))
		
def revertNameChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dNameChanges:
		setShort(iPlayer, infos.civ(iCiv).getShortDescription(0))

def revertAdjectiveChange(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv in dAdjectiveChanges:
		setAdjective(iPlayer, infos.civ(iCiv).getAdjective(0))
	
def getColumn(iPlayer):
	lTechs = [infos.tech(iTech).getGridX() for iTech in range(iNumTechs) if team(iPlayer).isHasTech(iTech)]
	if not lTechs: return 0
	return max(lTechs)
	
### Utility methods for civilization status ###
	
def isCapitulated(iPlayer):
	return team(iPlayer).isAVassal() and team(iPlayer).isCapitulated()
	
def isEmpire(iPlayer):
	if team(iPlayer).isAVassal(): return False

	return player(iPlayer).getNumCities() >= getEmpireThreshold(iPlayer)
	
def getEmpireThreshold(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in dEmpireThreshold: 
		return dEmpireThreshold[iCiv]
	
	if iCiv == iEthiopia and not game.isReligionFounded(iIslam):
		return 4
	
	if iCiv == iRome and not player(iByzantium).isExisting():
		return 7
		
	return 5
	
def isAtWar(iPlayer):
	for iTarget in players.major():
		if team(iPlayer).isAtWar(iTarget):
			return True
	return False
	
def capitalCoords(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	if capital: return location(capital)
	
	return (-1, -1)
	
def controlsHolyCity(iPlayer, iReligion):
	holyCity = game.getHolyCity(iReligion)
	if holyCity and holyCity.getOwner() == iPlayer: return True
	
	return False
	
def controlsCity(iPlayer, (x, y)):
	plot = plot_(x, y)
	return plot.isCity() and plot.getPlotCity().getOwner() == iPlayer
	
### Naming methods ###

def name(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer) and not bIgnoreVassal:
		sVassalName = vassalName(iPlayer, master(iPlayer))
		if sVassalName: return sVassalName
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicName = republicName(iPlayer)
		if sRepublicName: return sRepublicName
		
	sSpecificName = specificName(iPlayer)
	if sSpecificName: return sSpecificName
	
	sDefaultInsertName = dDefaultInsertNames.get(iCiv)
	if sDefaultInsertName: return sDefaultInsertName
	
	return short(iPlayer)
	
def vassalName(iPlayer, iMaster):
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)

	if iMasterCiv == iRome and player(iPlayer).getPeriod() == iPeriodCarthage:
		return "TXT_KEY_CIV_ROMAN_NAME_CARTHAGE"
		
	if iCiv == iNetherlands:
		return short(iPlayer)

	sSpecificName = dForeignNames[iMasterCiv].get(iCiv)
	if sSpecificName:
		return sSpecificName
	
	return None
	
def republicName(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in [iMoors, iEngland]: return None
	
	if iCiv == iInca and data.civs[iPlayer].iResurrections > 0: return None
	
	if iCiv == iNetherlands and isCommunist(iPlayer): return "TXT_KEY_CIV_NETHERLANDS_ARTICLE"
	
	if iCiv == iTurks: return "TXT_KEY_CIV_TURKS_UZBEKISTAN"

	return short(iPlayer)
	
def peoplesName(iPlayer):
	return desc(iPlayer, key(iPlayer, "PEOPLES"))
	
def specificName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return short(iPlayer)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or civic.iReligion == iFanaticism
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
			
	if iCiv == iChina:
		if bEmpire:
			# if iEra >= iIndustrial or scenario() == i1700AD:
			# 	return "TXT_KEY_CIV_CHINA_QING"
			
			if iEra == iRenaissance and turn() >= year(1400):
				return "TXT_KEY_CIV_CHINA_MING"
	
	elif iCiv == iNubia:
		if iEra <= iClassical:
			return "TXT_KEY_CIV_NUBIA_KUSH"
			
	elif iCiv == iGreece:
		if not bCityStates and bEmpire and iEra <= iClassical:
			return "TXT_KEY_CIV_GREECE_MACEDONIA"
			
	elif iCiv == iPolynesia:
		if isCurrentCapital(iPlayer, "Kaua'i", "O'ahu", "Maui"):
			return "TXT_KEY_CIV_POLYNESIA_HAWAII"
			
		if isCurrentCapital(iPlayer, "Manu'a"):
			return "TXT_KEY_CIV_POLYNESIA_SAMOA"
			
		if isCurrentCapital(iPlayer, "Niue"):
			return "TXT_KEY_CIV_POLYNESIA_NIUE"
			
		return "TXT_KEY_CIV_POLYNESIA_TONGA"
		
	elif iCiv == iDravidia:
		# if getColumn(iPlayer) >= 11 or scenario() == i1700AD:
		# 	return "TXT_KEY_CIV_DRAVIDIA_MYSORE"
			
		if getColumn(iPlayer) >= 9:
			return "TXT_KEY_CIV_DRAVIDIA_VIJAYANAGARA"
			
	elif iCiv == iEthiopia:
		if not game.isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUM"
			
	elif iCiv == iKorea:
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_CIV_KOREA_GOGURYEO"
				
		if iEra <= iMedieval:
			return "TXT_KEY_CIV_KOREA_GORYEO"
			
		return "TXT_KEY_CIV_KOREA_JOSEON"
		
	elif iCiv == iByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_BYZANTIUM_RUM"
	
		if not bEmpire:
			if isCurrentCapital(iPlayer, "Dyrrachion"):
				return "TXT_KEY_CIV_BYZANTIUM_EPIRUS"
			
			if isCurrentCapital(iPlayer, "Athena"):
				return "TXT_KEY_CIV_BYZANTIUM_MOREA"
	
			if not isCurrentCapital(iPlayer, "Konstantinoupolis"):
				return capitalName(iPlayer)
			
	elif iCiv == iNorse:	
		if isCurrentCapital(iPlayer, "Oslo", "Nidaros"):
			return "TXT_KEY_CIV_NORSE_NORWAY"
			
		if isCurrentCapital(iPlayer, "Roskilde"):
			return "TXT_KEY_CIV_NORSE_DENMARK"
			
		return "TXT_KEY_CIV_NORSE_SCANDINAVIA"
		
	elif iCiv == iTurks:
		if capital in plots.regions(rCaucasus, rPonticSteppe):
			return "TXT_KEY_CIV_TURKS_KHAZARIA"
	
		if capital in plots.region(rAnatolia):
			return "TXT_KEY_CIV_TURKS_RUM"
			
		if iEra >= iRenaissance and not tPlayer.isAVassal():
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_UZBEKISTAN"
				
			return capitalName(iPlayer)
		
	elif iCiv == iArabia:
		if bResurrected:
			return "TXT_KEY_CIV_ARABIA_SAUDI"
			
	elif iCiv == iKhmer:
		if isCurrentCapital(iPlayer, "Pagan"):
			return "TXT_KEY_CIV_KHMER_BURMA"
			
		if isCurrentCapital(iPlayer, "Dali"):
			return "TXT_KEY_CIV_KHMER_NANZHAO"
		
		if iEra >= iIndustrial:
			return "TXT_KEY_CIV_KHMER_CAMBODIA"
			
	elif iCiv == iMoors:	
		if capital in plots.region(rIberia):
			return capitalName(iPlayer)
			
		return "TXT_KEY_CIV_MOORS_MOROCCO"
			
	elif iCiv == iJava:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_INDONESIA_MATARAM"
			
		if iEra <= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_INDONESIA_MAJAPAHIT"
		
	elif iCiv == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_SPAIN_AL_ANDALUS"
	
		bSpain = not player(iMoors).isExisting() or not player(iMoors).getCapitalCity() in plots.region(rIberia)
	
		if bSpain:
			if not player(iPortugal).isExisting() or not player(iPortugal).getCapitalCity() in plots.region(rIberia):
				return "TXT_KEY_CIV_SPAIN_IBERIA"
			
		if isCurrentCapital(iPlayer, "Barcelona", "Valencia"):
			return "TXT_KEY_CIV_SPAIN_ARAGON"
		
		if isCurrentCapital(iPlayer, "Oviedo"):
			return "TXT_KEY_CIV_SPAIN_ASTURIAS"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILE"
			
	elif iCiv == iFrance:
		if iEra == iMedieval and not player(iHolyRome).isExisting():
			return "TXT_KEY_CIV_FRANCE_FRANCIA"
			
	elif iCiv == iEngland:
		if getColumn(iPlayer) >= 11 and 1 < cities.region(rBritain) <= cities.region(rBritain).owner(iPlayer):
			return "TXT_KEY_CIV_ENGLAND_GREAT_BRITAIN"
			
	elif iCiv == iHolyRome:
		if isCurrentCapital(iPlayer, "Buda"):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARY"
	
		if not bEmpire:
			if year() < year(dBirth[iGermany]):
				return "TXT_KEY_CIV_HOLY_ROME_GERMANY"
			else:
				return "TXT_KEY_CIV_AUSTRIA_SHORT_DESC"
			
	elif iCiv == iInca:
		if bResurrected:
			if isCurrentCapital(iPlayer, "La Paz"):
				return "TXT_KEY_CIV_INCA_BOLIVIA"
				
		else:
			if not bEmpire:
				return capitalName(iPlayer)
			
	elif iCiv == iItaly:
		if not bResurrected and not bEmpire and not bCityStates:
			if isCurrentCapital(iPlayer, "Fiorenza"):
				return "TXT_KEY_CIV_ITALY_TUSCANY"
				
			return capitalName(iPlayer)
			
	elif iCiv == iRussia:
		if not (bEmpire and iEra >= iRenaissance) and not isControlled(iPlayer, plots.regions(rRuthenia, rPonticSteppe, rEuropeanArctic), 5):
			if not bCityStates and isCurrentCapital(iPlayer, "Moskva"):
				return "TXT_KEY_CIV_RUSSIA_MUSCOVY"
				
			return capitalName(iPlayer)
			
	elif iCiv == iThailand:
		if iEra <= iRenaissance:
			return "TXT_KEY_CIV_THAILAND_AYUTTHAYA"
			
	elif iCiv == iNetherlands:
		if bCityStates:
			return short(iPlayer)
			
		if isCurrentCapital(iPlayer, "Brussels", "Antwerpen"):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIUM"
			
	elif iCiv == iGermany:
		if getColumn(iPlayer) <= 14 and pPlayer.isExisting() and (not player(iHolyRome).isExisting() or not team(iHolyRome).isVassal(iPlayer)):
			return "TXT_KEY_CIV_GERMANY_PRUSSIA"
	
def adjective(iPlayer, bIgnoreVassal = False):
	iCiv = civ(iPlayer)

	if isCapitulated(iPlayer):
		iMaster = master(iPlayer)
	
		sForeignAdjective = dForeignAdjectives[civ(iMaster)].get(iPlayer)
		if sForeignAdjective: return sForeignAdjective
		
		if not bIgnoreVassal: return adjective(iMaster)
		
	if isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer):
		sRepublicAdjective = republicAdjective(iPlayer)
		if sRepublicAdjective: return sRepublicAdjective
		
	sSpecificAdjective = specificAdjective(iPlayer)
	if sSpecificAdjective: return sSpecificAdjective
	
	sDefaultInsertAdjective = dDefaultInsertAdjectives.get(iCiv)
	if sDefaultInsertAdjective: return sDefaultInsertAdjective
	
	return player(iPlayer).getCivilizationAdjective(0)
	
def republicAdjective(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iRome:
		if player(iByzantium).isExisting(): return None

	if iCiv == iByzantium:
		if player(iRome).isExisting(): return None
		
	if iCiv in [iMoors, iEngland]: return None
	
	if iCiv == iInca and data.civs[iPlayer].iResurrections > 0: return None
	
	if iCiv == iHolyRome and player(iPlayer).getPeriod() == -1: return "TXT_KEY_CIV_HOLY_ROME_GERMAN"
		
	return player(iPlayer).getCivilizationAdjective(0)
	
def specificAdjective(iPlayer):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return player(iPlayer).getCivilizationAdjective(0)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or civic.iReligion == iFanaticism
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)
	
	bMonarchy = not isCommunist(iPlayer) and not isFascist(iPlayer) and not isRepublic(iPlayer)
	
	if iCiv == iEgypt:
		if bMonarchy:
			if bResurrected:
				if tPlayer.isHasTech(iGunpowder):
					return "TXT_KEY_CIV_EGYPT_MAMLUK"
		
				if player(iArabia).isExisting():
					return "TXT_KEY_CIV_EGYPT_FATIMID"
			
				return "TXT_KEY_CIV_EGYPT_AYYUBID"
			
	elif iCiv == iIndia:
		if bMonarchy and not bCityStates and (iEra >= iMedieval or bEmpire):
			if iEra >= iRenaissance:
				return "TXT_KEY_CIV_INDIA_MARATHA"
			
			if iEra >= iMedieval:
				return "TXT_KEY_CIV_INDIA_PALA"
			
			if iReligion == iBuddhism:
				return "TXT_KEY_CIV_INDIA_MAURYA"
			
			if iReligion == iHinduism:
				return "TXT_KEY_CIV_INDIA_GUPTA"
			
	elif iCiv == iChina:
		if bMonarchy:
			if iEra >= iMedieval:
				if tPlayer.isHasTech(iPaper) and tPlayer.isHasTech(iGunpowder):
					return "TXT_KEY_CIV_CHINA_SONG"
			
				if year() >= year(600):
					return "TXT_KEY_CIV_CHINA_TANG"
				
				return "TXT_KEY_CIV_CHINA_SUI"
			
			if iEra == iClassical:
				if year() >= year(0):
					return "TXT_KEY_CIV_CHINA_HAN"
				
				return "TXT_KEY_CIV_CHINA_QIN"
			
			return "TXT_KEY_CIV_CHINA_ZHOU"
			
	elif iCiv == iBabylonia:
		if bCityStates and not bEmpire:
			return "TXT_KEY_CIV_BABYLONIA_MESOPOTAMIAN"
			
		if isCurrentCapital(iPlayer, "Ninua", "Kalhu"):
			return "TXT_KEY_CIV_BABYLONIA_ASSYRIAN"
		
		if getColumn(iPlayer) == 1:
			return "TXT_KEY_CIV_BABYLONIA_AKKADIAN"
			
	elif iCiv == iGreece:
		if iEra == iAncient:
			return "TXT_KEY_CIV_GREECE_MYCENAEAN"
	
		if not bCityStates and bEmpire and iEra <= iClassical:
			return "TXT_KEY_CIV_GREECE_MACEDONIAN"
			
	elif iCiv == iIran:
		if bEmpire:
			if iEra <= iRenaissance:
				return "TXT_KEY_CIV_PERSIA_SAFAVID"
		
			if iEra == iIndustrial:
				return "TXT_KEY_CIV_PERSIA_QAJAR"
		
			return "TXT_KEY_CIV_PERSIA_PAHLAVI"
		
	elif iCiv == iPersia:
		if pPlayer.isStateReligion() and iReligion < 0:
			return "TXT_KEY_CIV_PERSIA_MEDIAN"
	
		if bEmpire:
			if iEra <= iClassical:
				if bResurrected:
					return "TXT_KEY_CIV_PERSIA_PARTHIAN"
				
				if getColumn(iPlayer) < 6:
					return "TXT_KEY_CIV_PERSIA_ACHAEMENID"
			
			if iEra <= iMedieval: 
				return "TXT_KEY_CIV_PERSIA_SASSANID"
				
			if iEra == iRenaissance:
				return "TXT_KEY_CIV_PERSIA_SAFAVID"
	
			if iEra == iIndustrial:
				return "TXT_KEY_CIV_PERSIA_QAJAR"
	
			return "TXT_KEY_CIV_PERSIA_PAHLAVI"
				
	elif iCiv == iPolynesia:
		if isCurrentCapital(iPlayer, "Manu'a"):
			return "TXT_KEY_CIV_POLYNESIA_TUI_MANUA"
			
		return "TXT_KEY_CIV_POLYNESIA_TUI_TONGA"
		
	elif iCiv == iRome:
		if player(iByzantium).isExisting() and not team(iByzantium).isVassal(team(iCiv).getID()):
			return "TXT_KEY_CIV_ROME_WESTERN"
			
	elif iCiv == iDravidia:
		if iReligion == iIslam:
			if iEra in [iMedieval, iRenaissance]:
				return "TXT_KEY_CIV_DRAVIDIA_BAHMANI"
	
		if iEra <= iClassical:
			if isCurrentCapital(iPlayer, "Madurai", "Thiruvananthapuram"):
				return "TXT_KEY_CIV_DRAVIDIA_PANDYAN"
				
			if isCurrentCapital(iPlayer, "Cochin", "Kozhikode"):
				return "TXT_KEY_CIV_DRAVIDIA_CHERA"
				
			return "TXT_KEY_CIV_DRAVIDIA_CHOLA"
			
	elif iCiv == iEthiopia:
		if iReligion == iIslam:
			return "TXT_KEY_CIV_ETHIOPIA_ADAL"
			
		if not game.isReligionFounded(iIslam):
			return "TXT_KEY_CIV_ETHIOPIA_AKSUMITE"
			
	elif iCiv == iByzantium:
		if player(iRome).isExisting() and player(iRome).getNumCities() > 0 and not team(iRome).isVassal(team(iCiv).getID()):
			return "TXT_KEY_CIV_BYZANTIUM_EASTERN"
			
		if bEmpire and controlsCity(iPlayer, location(plots.capital(iRome))):
			return infos.civ(iRome).getAdjective(0)
			
	elif iCiv == iTurks:
		if bResurrected:
			return "TXT_KEY_CIV_TURKS_TIMURID"
	
		if capital in plots.regions(rCaucasus, rPonticSteppe):
			return "TXT_KEY_CIV_TURKS_KHAZAR"
		
		if isControlled(iPlayer, plots.regions(rPersia, rKhorasan)):
			return "TXT_KEY_CIV_TURKS_SELJUK"
		
		if capital in plots.regions(rPersia, rKhorasan):
			return "TXT_KEY_CIV_TURKS_SELJUK"
		
		if capital in plots.region(rAnatolia):
			return "TXT_KEY_CIV_TURKS_SELJUK"
			
		if iEra >= iRenaissance:
			if bEmpire:
				return "TXT_KEY_CIV_TURKS_SHAYBANID"
		
			return "TXT_KEY_CIV_TURKS_UZBEK"
		
		if cities.owner(iPlayer).all(lambda city: city.getX() < iTurkicEastWestBorder):
			return "TXT_KEY_CIV_TURKS_WESTERN_TURKIC"
		
		if cities.owner(iPlayer).all(lambda city: city.getY() >= iTurkicEastWestBorder):
			return "TXT_KEY_CIV_TURKS_EASTERN_TURKIC"
			
	elif iCiv == iArabia:
		if (bTheocracy or controlsHolyCity(iPlayer, iIslam)) and iReligion == iIslam:
			if not bEmpire:
				return "TXT_KEY_CIV_ARABIA_RASHIDUN"
				
			if isCurrentCapital(iPlayer, "Dimashq"):
				return "TXT_KEY_CIV_ARABIA_UMMAYAD"
				
			return "TXT_KEY_CIV_ARABIA_ABBASID"
			
	elif iCiv == iMoors:
		if bEmpire:
			if iEra == iMedieval:
				if bTheocracy:
					return "TXT_KEY_CIV_MOORS_ALMORAVID"
					
				return "TXT_KEY_CIV_MOORS_ALMOHAD"
				
			elif iEra == iRenaissance:
				return "TXT_KEY_CIV_MOORS_SAADI"
			
		if not capital in plots.region(rIberia):
			return "TXT_KEY_CIV_MOORS_MOROCCAN"
			
	elif iCiv == iSpain:
		bSpain = not player(iMoors).isExisting() or not player(iMoors).getCapitalCity() in plots.region(rIberia)
	
		if bSpain:
			if not player(iPortugal).isExisting() or master(iPortugal) == iPlayer or not player(iPortugal).getCapitalCity() in plots.region(rIberia):
				return "TXT_KEY_CIV_SPAIN_IBERIAN"
			
		if isCurrentCapital(iPlayer, "Barcelona", "Valencia"):
			return "TXT_KEY_CIV_SPAIN_ARAGONESE"
		
		if isCurrentCapital(iPlayer, "Oviedo"):
			return "TXT_KEY_CIV_SPAIN_ASTURIAN"
			
		if not bSpain:
			return "TXT_KEY_CIV_SPAIN_CASTILIAN"
			
	elif iCiv == iFrance:
		if iEra == iMedieval and not player(iHolyRome).isExisting():
			return "TXT_KEY_CIV_FRANCE_FRANKISH"
	
	elif iCiv == iKhmer:
		if bMonarchy:
			return infos.civ(iKhmer).getAdjective(0)
			
	elif iCiv == iEngland:
		if getColumn(iPlayer) >= 11 and 1 < cities.region(rBritain) <= cities.region(rBritain).owner(iPlayer):
			return "TXT_KEY_CIV_ENGLAND_BRITISH"
			
	elif iCiv == iHolyRome:
		if isCurrentCapital(iPlayer, "Buda"):
			return "TXT_KEY_CIV_HOLY_ROME_HUNGARIAN"
	
		if player(iGermany).isExisting() and civic.iLegitimacy == iConstitution:
			return "TXT_KEY_CIV_HOLY_ROME_AUSTRO_HUNGARIAN"
			
		iVassals = 0
		for iLoopCiv in dCivGroups[iCivGroupEurope]:
			iLoopPlayer = slot(iLoopCiv)
			if iLoopPlayer >= 0 and master(iLoopPlayer) == iPlayer:
				iVassals += 1
				
		if iVassals >= 2:
			return "TXT_KEY_CIV_HOLY_ROME_HABSBURG"
			
		if not bEmpire and year() < year(dBirth[iGermany]):
			return "TXT_KEY_CIV_HOLY_ROME_GERMAN"
			
	elif iCiv == iMali:
		if iEra >= iRenaissance and isCurrentCapital(iPlayer, "Gao"):
			return "TXT_KEY_CIV_MALI_SONGHAI"
			
	elif iCiv == iInca:
		if bResurrected:
			if isCurrentCapital(iPlayer, "La Paz"):
				return "TXT_KEY_CIV_INCA_BOLIVIAN"
				
	elif iCiv == iItaly:
		if bCityStates and bWar:
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_LOMBARD"
				
	elif iCiv == iMongols:
		if not bEmpire and iEra <= iRenaissance:
			if capital.getRegionID() == rPersia:
				return "TXT_KEY_CIV_MONGOLIA_HULAGU"
				
			if location(capital) != location(plots.capital(iMongols)) and capital.getRegionID() in [rCentralAsianSteppe, rTarimBasin, rKhorasan]:
				return "TXT_KEY_CIV_MONGOLIA_CHAGATAI"
				
			if 2 * cities.regions(rNorthChina, rSouthChina).owner(iPlayer).count() >= cities.regions(rNorthChina, rSouthChina).count():
				return "TXT_KEY_CIV_MONGOLIA_YUAN"
				
		if bMonarchy:
			return "TXT_KEY_CIV_MONGOLIA_MONGOL"
	
	elif iCiv == iMughals:
		if not tPlayer.isHasTech(iFirearms):
			return "TXT_KEY_CIV_MUGHALS_GHORID"
				
	elif iCiv == iOttomans:
		return "TXT_KEY_CIV_OTTOMANS_OTTOMAN"
			
	elif iCiv == iNetherlands:
		if isCurrentCapital(iPlayer, "Brussels", "Antwerpen"):
			return "TXT_KEY_CIV_NETHERLANDS_BELGIAN"
			
	elif iCiv == iGermany:
		if getColumn(iPlayer) <= 14 and player(iHolyRome).isExisting() and not team(iHolyRome).isVassal(iPlayer):
			return "TXT_KEY_CIV_GERMANY_PRUSSIAN"
	
### Title methods ###

def title(iPlayer):
	if isCapitulated(iPlayer):
		sVassalTitle = vassalTitle(iPlayer, master(iPlayer))
		if sVassalTitle: return sVassalTitle
		
	if isCommunist(iPlayer):
		sCommunistTitle = communistTitle(iPlayer)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iPlayer):
		sFascistTitle = fascistTitle(iPlayer)
		if sFascistTitle: return sFascistTitle
		
	if isRepublic(iPlayer):
		sRepublicTitle = republicTitle(iPlayer)
		if sRepublicTitle: return sRepublicTitle
		
	sSpecificTitle = specificTitle(iPlayer)
	if sSpecificTitle: return sSpecificTitle
	
	return defaultTitle(iPlayer)
	
def vassalTitle(iPlayer, iMaster):
	iMasterCiv = civ(iMaster)
	iCiv = civ(iPlayer)

	if isCommunist(iMaster):
		sCommunistTitle = dCommunistVassalTitles[iMasterCiv].get(iCiv)
		if sCommunistTitle: return sCommunistTitle
		
		sCommunistTitle = dCommunistVassalTitlesGeneric.get(iMasterCiv)
		if sCommunistTitle: return sCommunistTitle
		
	if isFascist(iMaster):
		sFascistTitle = dFascistVassalTitles[iMasterCiv].get(iCiv)
		if sFascistTitle: return sFascistTitle
		
		sFascistTitle = dFascistVassalTitlesGeneric.get(iMasterCiv)
		if sFascistTitle: return sFascistTitle
				
	if player(iMaster).getPeriod == iPeriodAustria and iCiv == iPoland:
		return "TXT_KEY_CIV_AUSTRIAN_POLAND"
		
	if iMasterCiv == iEngland and iCiv == iMughals:
		if not player(iIndia).isExisting():
			return dSpecificVassalTitles[iEngland][iIndia]
	
	if iMasterCiv == iEgypt and player(iMasterCiv).getStateReligion() == iIslam:
		return dMasterTitles[iArabia]

	sSpecificTitle = dSpecificVassalTitles[iMasterCiv].get(iCiv)
	if sSpecificTitle: return sSpecificTitle

	sMasterTitle = dMasterTitles.get(iMasterCiv)
	if sMasterTitle: return sMasterTitle
		
	if iCiv in lColonies and iMasterCiv not in lColonies:
		return "TXT_KEY_COLONY_OF"
	
	return "TXT_KEY_PROTECTORATE_OF"
	
def communistTitle(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv in lSocialistRepublicOf: return "TXT_KEY_SOCIALIST_REPUBLIC_OF"
	if iCiv in lSocialistRepublicAdj: return "TXT_KEY_SOCIALIST_REPUBLIC_ADJECTIVE"
	if iCiv in lPeoplesRepublicOf: return "TXT_KEY_PEOPLES_REPUBLIC_OF"
	if iCiv in lPeoplesRepublicAdj: return "TXT_KEY_PEOPLES_REPUBLIC_ADJECTIVE"

	return key(iPlayer, "COMMUNIST")
	
def fascistTitle(iPlayer):
	return key(iPlayer, "FASCIST")
	
def republicTitle(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)

	if iCiv == iHolyRome and pPlayer.getPeriod() == -1:
		return "TXT_KEY_CIV_HOLY_ROME_CONFEDERATION"
	
	if iCiv == iPoland:
		if pPlayer.getCurrentEra() <= iIndustrial:
			return key(iPlayer, "COMMONWEALTH")
	
	if iCiv == iEngland:
		iEra = pPlayer.getCurrentEra()
		if isEmpire(iPlayer) and iEra == iIndustrial:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iGlobal:
			return "TXT_KEY_CIV_ENGLAND_UNITED_REPUBLIC"
	
	if iCiv == iAmerica:
		if civics(iPlayer).iSociety in [iManorialism, iSlavery]:
			return key(iPlayer, "CSA")
			
	if iCiv == iColombia:
		if isControlled(iPlayer, plots.regions(rNewGranada, rAndes)):
			return "TXT_KEY_CIV_COLOMBIA_FEDERATION_ANDES"
			
	if pPlayer.getStateReligion() == iIslam:
		if iCiv in lIslamicRepublicOf: return "TXT_KEY_ISLAMIC_REPUBLIC_OF"

		if iCiv == iOttomans: return key(iPlayer, "ISLAMIC_REPUBLIC")
		
	if iCiv in lRepublicOf: return "TXT_KEY_REPUBLIC_OF"
	if iCiv in lRepublicAdj: return "TXT_KEY_REPUBLIC_ADJECTIVE"
	
	return key(iPlayer, "REPUBLIC")

def defaultTitle(iPlayer):
	return desc(iPlayer, key(iPlayer, "DEFAULT"))
	
def specificTitle(iPlayer, lPreviousOwners=[]):
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iCiv = civ(iPlayer)
	
	civic = civics(iPlayer)
	
	iNumCities = pPlayer.getNumCities()
	if iNumCities == 0: return defaultTitle(iPlayer)
	
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = capitalCoords(iPlayer)
	bAnarchy = pPlayer.isAnarchy()
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or civic.iReligion == iFanaticism
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bCapitulated = isCapitulated(iPlayer)
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	bWar = isAtWar(iPlayer)

	if iCiv == iEgypt:
		# if bResurrected or scenario() >= i600AD:
		# 	if iReligion == iIslam:
		# 		if bTheocracy: return "TXT_KEY_CALIPHATE_ADJECTIVE"
		# 		return "TXT_KEY_SULTANATE_ADJECTIVE"
		# 	return "TXT_KEY_KINGDOM_ADJECTIVE"
			
		if player(iPlayer).getPeriod() == iPeriodPtolemaicEgypt or slot(iGreece) in lPreviousOwners:
			return "TXT_KEY_CIV_EGYPT_PTOLEMAIC"
			
		if bCityStates:
			return "TXT_KEY_CIV_EGYPT_NOMES"
		
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
		
		if iReligion in [iOrthodoxy, iCatholicism, iProtestantism]:
			return "TXT_KEY_CIV_EGYPT_COPTIC"
				
		if iEra == iAncient:
			if iAnarchyTurns == 0: return "TXT_KEY_CIV_EGYPT_OLD_KINGDOM"
			if iAnarchyTurns <= turns(1): return "TXT_KEY_CIV_EGYPT_MIDDLE_KINGDOM"
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"
		
		if iEra == iClassical:
			return "TXT_KEY_CIV_EGYPT_NEW_KINGDOM"
			
	elif iCiv == iIndia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iRenaissance:
			return "TXT_KEY_CONFEDERACY_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_INDIA_GANA_SANGHAS"
		
		if iEra <= iClassical:
			return "TXT_KEY_CIV_INDIA_MAHAJANAPADAS"
			
	elif iCiv == iChina:
		if bEmpire:
			# if iEra >= iIndustrial or scenario() == i1700AD:
			# 	return "TXT_KEY_EMPIRE_OF"
			
			if iEra == iRenaissance and year() >= year(1400):
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iBabylonia:
		if bCityStates and not bEmpire:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
		if bEmpire and iEra > iAncient:
			return "TXT_KEY_CIV_BABYLONIA_NEO_EMPIRE"
			
	elif iCiv == iGreece:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
		if bCityStates and period(iCiv) == -1:				
			if bWar:
				return "TXT_KEY_CIV_GREECE_LEAGUE"
				
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
	elif iCiv == iPersia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iPhoenicia:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
			
	elif iCiv == iPolynesia:
		if isCurrentCapital(iPlayer, "Kaua'i", "O'ahu", "Maui"):
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iRome:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_REPUBLIC_ADJECTIVE"
			
	elif iCiv == iColombia:
		if bEmpire:
			if isControlled(iPlayer, plots.regions(rNewGranada, rAndes)):
				return "TXT_KEY_CIV_COLOMBIA_EMPIRE_ANDES"
		
			return "TXT_KEY_CIV_COLOMBIA_EMPIRE"
			
	elif iCiv == iJapan:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
		if civic.iLegitimacy == iBureaucracy:
			return "TXT_KEY_EMPIRE_OF"
			
		if iEra >= iIndustrial:
			return "TXT_KEY_EMPIRE_OF"
			
	elif iCiv == iDravidia:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if getColumn(iPlayer) >= 9:
			return "TXT_KEY_KINGDOM_OF"
		
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iEthiopia:
		if bCityStates:
			return "TXT_KEY_CITY_STATES_ADJECTIVE"
	
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_ADJECTIVE"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
	
	elif iCiv == iKorea:
		if iEra >= iIndustrial:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
		if iEra == iClassical:
			if bEmpire:
				return "TXT_KEY_EMPIRE_OF"
				
		if bCityStates:
			return "TXT_KEY_CIV_KOREA_SAMHAN"
				
		if iReligion >= 0:
			return "TXT_KEY_KINGDOM_OF"
			
	elif iCiv == iByzantium:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if not bEmpire and location(capital) != location(plots.capital(iCiv)):
			if capital.getRegionID() == rAnatolia:
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_CIV_BYZANTIUM_DESPOTATE"
			
	elif iCiv == iNorse:
		if bCityStates:
			return "TXT_KEY_CIV_NORSE_ALTHINGS"
		
		if isControlled(iPlayer, plots.region(rBritain)):
			return "TXT_KEY_CIV_NORSE_NORTH_SEA_EMPIRE"
				
		if iReligion < 0 and iEra < iRenaissance:
			return "TXT_KEY_CIV_NORSE_NORSE_KINGDOMS"
			
		if bEmpire:
			if iEra <= iMedieval:
				return "TXT_KEY_CIV_NORSE_KALMAR_UNION"
				
			if iEra == iRenaissance:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
	elif iCiv == iTurks:
		if bCityStates:
			return "TXT_KEY_CIV_TURKS_KURULTAI"
			
		if iReligion >= 0:
			if bEmpire:
				if isControlled(iPlayer, plots.core(iPersia)) and not bResurrected:
					return "TXT_KEY_CIV_TURKS_GREAT_EMPIRE"
			
				return "TXT_KEY_EMPIRE_ADJECTIVE"
			
			if not isControlled(iPlayer, plots.core(iPersia)):
				return "TXT_KEY_CIV_TURKS_KHANATE_OF"
				
			if iReligion == iIslam:
				if isControlled(iPlayer, plots.core(iPersia)):
					return "TXT_KEY_SULTANATE_ADJECTIVE"
			
				return "TXT_KEY_SULTANATE_OF"
				
			return "TXT_KEY_KINGDOM_OF"
			
		if bEmpire:
			return "TXT_KEY_CIV_TURKS_KHAGANATE"
			
	elif iCiv == iArabia:
		if bResurrected:
			return "TXT_KEY_KINGDOM_OF"
			
		if iReligion == iIslam and (bTheocracy or controlsHolyCity(iPlayer, iIslam)):
			return "TXT_KEY_CALIPHATE_ADJECTIVE"
			
	elif iCiv == iTibet:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iKhmer:
		if iEra <= iRenaissance and isCurrentCapital(iPlayer, "Angkor"):
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra >= iIndustrial:
			return "TXT_KEY_KINGDOM_OF"
			
		if isCurrentCapital(iPlayer, "Dai La"):
			return "TXT_KEY_CIV_KHMER_DAI_VIET"
			
	elif iCiv == iMoors:
		if bCityStates:
			return "TXT_KEY_CIV_MOORS_TAIFAS"
			
		if iReligion == iIslam and capital in plots.region(rIberia):
			if bEmpire:
				return "TXT_KEY_CALIPHATE_OF"
				
			return "TXT_KEY_CIV_MOORS_EMIRATE_OF"
			
		if bEmpire and iEra <= iRenaissance:
			if iReligion == iIslam and bTheocracy:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iJava:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
	elif iCiv == iSpain:
		if iReligion == iIslam:
			return "TXT_KEY_SULTANATE_OF"
			
		if bEmpire and iEra > iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra == iMedieval and isCurrentCapital(iPlayer, "Barcelona", "Valencia"):
			return "TXT_KEY_CIV_SPAIN_CROWN_OF"
			
	elif iCiv == iFrance:
		if not capital in cities.core(iFrance):
			return "TXT_KEY_CIV_FRANCE_EXILE"
			
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if civic.iLegitimacy == iStratocracy:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not player(iHolyRome).isExisting() and iEra == iMedieval:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iEngland:
		if capital not in cities.core(iEngland):
			return "TXT_KEY_CIV_ENGLAND_EXILE"
			
		if iEra == iMedieval and player(iFrance).isExisting() and team(iFrance).isAVassal() and civ(master(iFrance)) == iEngland:
			return "TXT_KEY_CIV_ENGLAND_ANGEVIN_EMPIRE"
			
		if getColumn(iPlayer) >= 11:
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
		
			if 1 < cities.region(rBritain) <= cities.region(rBritain).owner(iPlayer):
				return "TXT_KEY_CIV_ENGLAND_UNITED_KINGDOM_OF"
			
	elif iCiv == iHolyRome:
		if bCityStates and player(iPlayer).getPeriod() == -1:
			return "TXT_KEY_CIV_HOLY_ROME_FREE_CITIES"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if isCurrentCapital(iPlayer, "Buda"):
			return "TXT_KEY_KINGDOM_OF"
			
		if player(iGermany).isExisting():
			return "TXT_KEY_CIV_HOLY_ROME_ARCHDUCHY_OF"
			
	# Nothing for Mali
	
	elif iCiv == iPoland:
		if iEra >= iRenaissance and bEmpire:
			return "TXT_KEY_CIV_POLAND_COMMONWEALTH"
			
		# if scenario() == i1700AD and turn() < year(1790):
		# 	return "TXT_KEY_CIV_POLAND_COMMONWEALTH"
			
		if isCurrentCapital(iPlayer, "Kowno", "Medvegalis", "Wilno", "Ryga"):
			return "TXT_KEY_CIV_POLAND_GRAND_DUCHY_OF"
			
	elif iCiv == iPortugal:
		if capital in cities.core(iBrazil) and not player(iBrazil).isExisting():
			return "TXT_KEY_CIV_PORTUGAL_BRAZIL"
			
		if not capital in plots.region(rIberia):
			return "TXT_KEY_CIV_PORTUGAL_EXILE"
			
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iInca:
		if not bResurrected:
			if bEmpire:
				return "TXT_KEY_CIV_INCA_FOUR_REGIONS"
				
	elif iCiv == iItaly:
		if bCityStates:
			if bWar:
				return "TXT_KEY_CIV_ITALY_LEAGUE"
				
			return "TXT_KEY_CIV_ITALY_MARITIME_REPUBLICS"
			
		if not bResurrected:
			if iReligion == iCatholicism:
				if bTheocracy:
					return "TXT_KEY_CIV_ITALY_PAPAL_STATES"
				
				if isCurrentCapital(iPlayer, "Roma"):
					return "TXT_KEY_CIV_ITALY_PAPAL_STATES"
					
			if not bEmpire:
				return "TXT_KEY_CIV_ITALY_DUCHY_OF"
				
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iMongols:
		if capital.getRegionID() == rPersia:
			return "TXT_KEY_CIV_MONGOLIA_ILKHANATE"
	
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if iEra <= iRenaissance:
			if iNumCities <= 3:
				return "TXT_KEY_CIV_MONGOLIA_KHAMAG"
				
			return "TXT_KEY_CIV_MONGOLIA_KHANATE"
			
	elif iCiv == iAztecs:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if bCityStates:
			return "TXT_KEY_CIV_AZTECS_ALTEPETL"
				
	elif iCiv == iMughals:
		if bResurrected:
			if bEmpire:
				return "TXT_KEY_EMPIRE_OF"
				
			return "TXT_KEY_SULTANATE_OF"
	
		if not bEmpire and not tPlayer.isHasTech(iFirearms):
			return "TXT_KEY_SULTANATE_OF"
		
	elif iCiv == iRussia:
		if bEmpire and iEra >= iRenaissance:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
		
		if iEra <= iMedieval:
			if (civic.iGovernment == iRepublic and civic.iLegitimacy in [iVassalage, iCitizenship]) or (civic.iGovernment == iElective and civic.iLegitimacy == iCitizenship):
				return "TXT_KEY_CIV_RUSSIA_MEDIEVAL_REPUBLIC"
			
			if civic.iGovernment == iElective:
				if isCurrentCapital(iPlayer, "Kiev"):
					return "TXT_KEY_CIV_RUSSIA_KIEVAN_RUS"
				
				return "TXT_KEY_CIV_RUSSIA_RUS"
			
		if isControlled(iPlayer, plots.regions(rRuthenia, rPonticSteppe, rEuropeanArctic), 5):
			return "TXT_KEY_CIV_RUSSIA_TSARDOM_OF"
		
		if isCurrentCapital(iPlayer, "Kiev"):
			return "TXT_KEY_CIV_RUSSIA_GRAND_PRINCIPALITY"
			
	elif iCiv == iOttomans:
		if iReligion == iIslam:
			if bTheocracy and game.getHolyCity(iIslam) and game.getHolyCity(iIslam).getOwner() == iPlayer:
				return "TXT_KEY_CALIPHATE_ADJECTIVE"
				
			if bEmpire:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_SULTANATE_ADJECTIVE"
			
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iThailand:
		if iEra >= iIndustrial and bEmpire:
			return "TXT_KEY_EMPIRE_OF"

	elif iCiv == iNetherlands:
		if bCityStates:
			return "TXT_KEY_CIV_NETHERLANDS_REPUBLIC"
		
		if capital not in cities.core(iNetherlands):
			return "TXT_KEY_CIV_NETHERLANDS_EXILE"
			
		if bEmpire:
			if iEra >= iIndustrial:
				return "TXT_KEY_EMPIRE_ADJECTIVE"
				
			return "TXT_KEY_CIV_NETHERLANDS_UNITED_KINGDOM_OF"
			
	elif iCiv == iGermany:
		if iEra >= iIndustrial and bEmpire:
			if player(iHolyRome).isExisting() and team(iHolyRome).isExisting() and civ(master(iHolyRome)) == iGermany:
				return "TXT_KEY_CIV_GERMANY_GREATER_EMPIRE"
				
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iAmerica:
		if civic.iSociety in [iSlavery, iManorialism]:
			if isControlled(iPlayer, plots.region(rMesoamerica)) and isControlled(iPlayer, plots.region(rCaribbean)):
				return "TXT_KEY_CIV_AMERICA_GOLDEN_CIRCLE"
		
			return "TXT_KEY_CIV_AMERICA_CSA"
			
	elif iCiv == iArgentina:
		if bEmpire:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
		if not at(capital, plots.capital(iCiv)):
			return "TXT_KEY_CIV_ARGENTINA_CONFEDERATION"
	
	elif iCiv == iMexico:
		if bEmpire or iDespotism in civic:
			return "TXT_KEY_EMPIRE_ADJECTIVE"
			
	elif iCiv == iBrazil:
		if bEmpire:
			return "TXT_KEY_EMPIRE_OF"
			
	return None
			
### Leader methods ###

def startingLeader(identifier):
	if not isinstance(identifier, Civ):
		identifier = civ(identifier)
		
	return dStartingLeaders[scenario()].get(identifier, dStartingLeaders[i500AD][identifier])
	
def leader(iPlayer):
	iCiv = civ(iPlayer)

	if is_minor(iPlayer): return None
	
	if not player(iPlayer).isAlive(): return None
	
	if player(iPlayer).isHuman(): return None
	
	pPlayer = player(iPlayer)
	tPlayer = team(iPlayer)
	iReligion = pPlayer.getStateReligion()
	capital = player(iPlayer).getCapitalCity()
	tCapitalCoords = (capital.getX(), capital.getY())
	civic = civics(iPlayer)
	bEmpire = isEmpire(iPlayer)
	bCityStates = isCityStates(iPlayer)
	bTheocracy = civic.iLegitimacy == iTheocracy or civic.iReligion == iFanaticism
	bResurrected = data.civs[iPlayer].iResurrections > 0
	bMonarchy = not (isCommunist(iPlayer) or isFascist(iPlayer) or isRepublic(iPlayer))
	iAnarchyTurns = data.civs[iPlayer].iAnarchyTurns
	iEra = pPlayer.getCurrentEra()
	iGameEra = game.getCurrentEra()
	
	if iCiv == iEgypt:
		if not bMonarchy and iEra >= iGlobal: return iNasser
		
		# if bResurrected or scenario() >= i600AD: return iBaibars
		
		if player(iPlayer).getPeriod() == iPeriodPtolemaicEgypt: return iPtolemy
		
		if getColumn(iPlayer) >= 3: return iRamesses
		
		if year() >= year(-1600): return iHatshepsut
		
	elif iCiv == iIndia:
		if not bMonarchy and iEra >= iGlobal: return iGandhi
		
		if iEra >= iRenaissance: return iShivaji
		
		if getColumn(iPlayer) >= 5: return iChandragupta
		
	elif iCiv == iChina:
		if isCommunist(iPlayer) or isRepublic(iPlayer) and iEra >= iIndustrial: return iMao
			
		if iEra >= iRenaissance and year() >= year(1400): return iHongwu
	
		if bResurrected: return iHongwu
		
		# if scenario() >= i1700AD: return iHongwu
		
		if iEra >= iMedieval: return iTaizong
		
	elif iCiv == iBabylonia:
		if year() >= year(-1600): return iHammurabi
		
	elif iCiv == iGreece:
		if iEra >= iIndustrial: return iGeorge
		
		if bResurrected and getColumn(iPlayer) >= 11: return iGeorge
	
		if bEmpire: return iAlexanderTheGreat
		
		if not bCityStates: return iAlexanderTheGreat
		
	elif iCiv == iIran:
		if iEra >= iGlobal: return iKhomeini
		
	elif iCiv == iPersia:
		if getColumn(iPlayer) >= 6: return iShapur
			
		if bEmpire:
			return iDarius
			
	elif iCiv == iPhoenicia:
		if not bCityStates: return iHannibal
		
		if capital.getRegionID() not in [rMesopotamia, rAnatolia]: return iHannibal
		
	elif iCiv == iRome:
		if not bCityStates: return iAugustus
		
		if tPlayer.isHasTech(iGeneralship): return iJuliusCaesar
		
	elif iCiv == iKorea:		
		if iEra >= iRenaissance: return iSejong
		
		# if scenario() >= i1700AD: return iSejong
	
	elif iCiv == iKhmer:
		if iEra >= iMedieval: return iSuryavarman
		
	elif iCiv == iJapan:
		if iEra >= iIndustrial: return iMeiji
		
		if tPlayer.isHasTech(iFeudalism): return iOdaNobunaga
		
	elif iCiv == iEthiopia:
		if iEra >= iIndustrial: return iMenelik
		
		if iEra >= iMedieval: return iZaraYaqob
		
	elif iCiv == iDravidia:
		if iEra >= iRenaissance: return iKrishnaDevaRaya
		
	elif iCiv == iByzantium:
		if year() >= year(1000): return iBasil
		
	elif iCiv == iNorse:
		if iEra >= iGlobal: return iGerhardsen
		
	elif iCiv == iTurks:
		if bResurrected: return iTamerlane
		
		if year() >= year(1700): return iTamerlane
	
		if year() >= year(1000) or pPlayer.getPeriod() == iPeriodSeljuks: return iAlpArslan
		
	elif iCiv == iArabia:
		if year() >= year(1000): return iSaladin
		
	elif iCiv == iTibet:
		if year() >= year(1500): return iLobsangGyatso
		
	elif iCiv == iMoors:
		if player(iPlayer).getNumCities() > 0 and not capital in plots.region(rIberia): return iYaqub
		
	elif iCiv == iJava:
		if iEra >= iGlobal: return iSuharto
		
		if bEmpire: return iHayamWuruk
		
	elif iCiv == iSpain:
		if isFascist(iPlayer): return iFranco
		
		if any(data.dFirstContactConquerors.values()): return iPhilip
		
	elif iCiv == iFrance:
		if iEra >= iGlobal: return iDeGaulle
		
		if iEra >= iIndustrial: return iNapoleon
		
		if iEra >= iRenaissance: return iLouis
		
	elif iCiv == iEngland:
		if iEra >= iGlobal: return iChurchill
		
		if iEra >= iIndustrial: return iVictoria
		
		# if scenario() == i1700AD: return iVictoria
		
		if iEra >= iRenaissance: return iElizabeth
		
	elif iCiv == iHolyRome:
		if iEra >= iIndustrial: return iFrancis
		
		# if scenario() == i1700AD: return iFrancis
		
		if iEra >= iRenaissance: return iCharles
			
	elif iCiv == iPoland:
		if iEra >= iGlobal: return iWalesa
		
		if isFascist(iPlayer) or isCommunist(iPlayer): return iPilsudski
	
		if iEra >= iRenaissance: return iSobieski
		
		# if scenario() == i1700AD: return iSobieski
		
	elif iCiv == iPortugal:
		if iEra >= iIndustrial: return iMaria
		
		if tPlayer.isHasTech(iCartography): return iJoao
		
	elif iCiv == iInca:
		if iEra >= iIndustrial: return iCastilla
		
		if bResurrected and year() >= year(1600): return iCastilla
	
	elif iCiv == iItaly:
		if isFascist(iPlayer): return iMussolini
	
		if iEra >= iIndustrial: return iCavour
		
	elif iCiv == iMongols:
		if year() >= year(1400): return iKublaiKhan
		
	elif iCiv == iMexico:
		if bMonarchy: return iSantaAnna
		
		if isFascist(iPlayer): return iSantaAnna
		
		if iEra >= iGlobal: return iCardenas
			
	elif iCiv == iMughals:
		if iEra >= iGlobal: return iBhutto
	
		if getColumn(iPlayer) >= 10: return iAkbar
		
	elif iCiv == iRussia:
		if iEra >= iIndustrial:
			if not bMonarchy: return iStalin
			
			return iAlexanderI
			
		if iEra >= iRenaissance:
			if year() >= year(1750): return iCatherine
			
			return iPeter
		
	elif iCiv == iOttomans:
		if not bMonarchy and iEra >= iIndustrial: return iAtaturk
		
		if iEra >= iRenaissance: return iSuleiman
				
	elif iCiv == iThailand:
		if iEra >= iIndustrial: return iMongkut
		
	elif iCiv == iNetherlands:
		if year() >= year(1650): return iWilliam

	elif iCiv == iGermany:
		if isFascist(iPlayer): return iHitler
		
		if getColumn(iPlayer) >= 14: return iBismarck
		
	elif iCiv == iAmerica:
		if iEra >= iGlobal: return iRoosevelt
		
		if year() >= year(1850): return iLincoln
		
	elif iCiv == iArgentina:
		if iEra >= iGlobal: return iPeron
	
	elif iCiv == iBrazil:
		if iEra >= iGlobal: return iVargas
		
	elif iCiv == iCanada:
		if iEra >= iGlobal: return iTrudeau
		
	return startingLeader(iPlayer)
		
	
def leaderName(iPlayer):
	iCiv = civ(iPlayer)
	pPlayer = player(iPlayer)
	iLeader = pPlayer.getLeader()
	
	if iCiv == iChina:
		if iLeader == iHongwu:
			if year() >= year(1700):
				return "TXT_KEY_LEADER_KANGXI"
				
	elif iCiv == iDravidia:
		if iLeader == iKrishnaDevaRaya:
			if year() >= year(1700):
				return "TXT_KEY_LEADER_TIPU_SULTAN"
				
	return None