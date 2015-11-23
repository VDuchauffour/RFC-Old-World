//Rhye
#ifndef CVRHYES_H
#define CVRHYES_H

using namespace std;
typedef list<char*> LISTCHAR;

// rhyes.h
#define EARTH_X					(124)
#define EARTH_Y					(68)

#define MAX_COM_SHRINE			(20)

#define GREATPALACE				(GC.getInfoTypeForString("BUILDING_GREAT_PALACE"))
#define SUMMERPALACE			(GC.getInfoTypeForString("BUILDING_GREAT_PALACE"))
//#define VERSAILLES				(GC.getInfoTypeForString("BUILDING_VERSAILLES"))
//#define FORBIDDENPALACE			(GC.getInfoTypeForString("BUILDING_FORBIDDEN_PALACE"))

#define PAGAN_TEMPLE			(GC.getInfoTypeForString("BUILDING_OBELISK"))

#define BEGIN_WONDERS				(134) // increment if normal building (not for wonders) is added
#define BEGIN_GREAT_WONDERS			(BEGIN_WONDERS+11)
#define NUM_BUILDINGS_PLAGUE		(210) // always increment when a building is added except embassies
#define NUM_BUILDINGTYPES_PLAGUE	(131) // increment when a building class is created except embassies

#define NUM_MAJOR_PLAYERS		(44)
#define NUM_PL					(44)
#define NUM_MINORS				(6)	 // Independent, Indpendent2, Natives, Celtia, Seljuks, Barbarians
#define NUM_CIVS				(52)

#define NUM_ERAS				(ERA_FUTURE+1)

enum MyTechs
{
 MYSTICISM,
 MEDITATION,
 POLYTHEISM,
 PRIESTHOOD,
 MONOTHEISM,
 MONARCHY,
 LITERATURE,
 CODEOFLAWS,
 DRAMA,
 FEUDALISM,
 THEOLOGY,
 MUSIC,
 CIVIL_SERVICE,
 GUILDS,
 DIVINERIGHT,
 PATRONAGE,
 NATIONALISM,
 MILITARY_TRADITION,
 CONSTITUTION,
 LIBERALISM,
 DEMOCRACY,
 CORPORATION,
 FASCISM,
 COMMUNISM,
 MASS_MEDIA,
 ECOLOGY,
 FISHING,
 THE_WHEEL,
 AGRICULTURE,
 POTTERY,
 AESTHETICS,
 SAILING,
 WRITING,
 MATHEMATICS,
 ALPHABET,
 CALENDAR,
 CURRENCY,
 PHILOSOPHY,
 PAPER,
 BANKING,
 EDUCATION,
 PRINTING_PRESS,
 ECONOMICS,
 ASTRONOMY,
 CHEMISTRY,
 SCIENTIFIC_METHOD,
 PHYSICS,
 BIOLOGY,
 MEDICINE,
 ELECTRICITY,
 COMBUSTION,
 FISSION,
 FLIGHT,
 ADVANCED_FLIGHT,
 PLASTICS,
 COMPOSITES,
 STEALTH,
 GENETICS,
 FIBER_OPTICS,
 FUSION,
 HUNTING,
 MINING,
 ARCHERY,
 MASONRY,
 ANIMAL_HUSBANDRY,
 BRONZEWORKING,
 HORSEBACK_RIDING,
 IRONWORKING,
 METALCASTING,
 COMPASS,
 CONSTRUCTION,
 MACHINERY,
 ENGINEERING,
 OPTICS,
 GUNPOWDER,
 REPLACEABLE_PARTS,
 MILITARY_SCIENCE,
 RIFLING,
 STEAM_POWER,
 STEEL,
 ASSEMBLY_LINE,
 RAILROAD,
 ARTILLERY,
 INDUSTRIALISM,
 RADIO,
 REFRIGERATION,
 SUPERCONDUCTORS,
 COMPUTERS,
 LASER,
 ROCKETRY,
 SATELLITES,
 ROBOTICS
};

enum MyBuildings
{
	TRIUMPHAL_ARCH = BEGIN_WONDERS,
	GLOBE_THEATRE,
	TRADING_COMPANY,
	IBERIAN_TRADING_COMPANY,
	STOCK_EXCHANGE,
	OLYMPIC_PARK,
	NATIONAL_GALLERY,
	IRON_WORKS,
	INTERPOL,
	NATIONAL_PARK,
	RED_CROSS,
	SPHYNX,
	GREAT_LIGHTHOUSE,
	GREAT_COTHON,
	TERRACOTTA_ARMY,
	ARTEMIS,
	PYRAMIDS,
	HANGING_GARDENS,
	ORACLE,
	MOAI_STATUES,
	ISHTAR_GATE,
	SOLOMON,
	COLOSSUS,
	PARTHENON,
	STATUE_OF_ZEUS,
	SHWEDAGON_PAYA,
	KHAJURAHO,
	GREAT_LIBRARY,
	MAUSOLLOS,
	FLOATING_GARDENS,
	FLAVIAN_AMPHITHEATRE,
	GREAT_WALL,
	THEODOSIAN_WALLS,
	MACHU_PICCHU,
	BOROBUDUR,
	GRAND_CANAL,
	NOTRE_DAME,
	KUKULKAN,
	HIMEJI_CASTLE,
	BLUE_MOSQUE,
	WAT_PREAH_PISNULOK,
	TOPKAPI_PALACE,
	APOSTOLIC_PALACE,
	MEZQUITA,
	SISTINE_CHAPEL,
	LEANING_TOWER,
	RED_FORT,
	VERSAILLES,
	FORBIDDENPALACE,
	SPIRAL_MINARET,
	DOME_OF_THE_ROCK,
	SANKORE,
	TAJ_MAHAL,
	SAN_MARCO_BASILICA,
	PORCELAIN_TOWER,
	BASILS_CATHEDRAL,
	HARMANDIR_SAHIB,
	TRAFALGAR_SQUARE,
	BRANDENBURG_GATE,
	STATUE_OF_LIBERTY,
	PENTAGON,
	LUBYANKA,
	WESTMINSTER_PALACE,
	MOUNT_RUSHMORE,
	EIFFEL_TOWER,
	EMPIRE_STATE_BUILDING,
	CERN,
	WEMBLEY,
	GRACELAND,
	CRISTO_REDENTOR,
	THREE_GORGES_DAM,
	HOLLYWOOD,
	UNITED_NATIONS,
	CN_TOWER,
	SPACE_ELEVATOR,
};

enum MyReligions
{
	PROTESTANTISM,
	CATHOLICISM,
	ORTHODOXY,
	ISLAM,
	HINDUISM,
	BUDDHISM,
	CONFUCIANISM,
	TAOISM,
	ZOROASTRIANISM,
	NUM_RELIGIONS
};

enum MyEras
{
	ERA_ANCIENT,
	ERA_CLASSICAL,
	ERA_MEDIEVAL,
	ERA_RENAISSANCE,
	ERA_INDUSTRIAL,
	ERA_MODERN,
	ERA_FUTURE,
	ERA_MIDDLE_EAST,
	ERA_EAST_ASIA,
	ERA_SOUTH_ASIA,
};

enum Regions
{
	REGION_BRITAIN,
	REGION_IBERIA,
	REGION_ITALY,
	REGION_BALKANS,
	REGION_EUROPE,
	REGION_SCANDINAVIA,
	REGION_RUSSIA,
	REGION_ANATOLIA,
	REGION_MESOPOTAMIA,
	REGION_ARABIA,
	REGION_EGYPT,
	REGION_MAGHREB,
	REGION_PERSIA,
	REGION_INDIA,
	REGION_DECCAN,
	REGION_INDOCHINA,
	REGION_INDONESIA,
	REGION_CHINA,
	REGION_KOREA,
	REGION_JAPAN,
	REGION_MANCHURIA,
	REGION_TIBET,
	REGION_CENTRAL_ASIA,
	REGION_SIBERIA,
	REGION_AUSTRALIA,
	REGION_OCEANIA,
	REGION_ETHIOPIA,
	REGION_WEST_AFRICA,
	REGION_SOUTH_AFRICA,
	REGION_CANADA,
	REGION_ALASKA,
	REGION_UNITED_STATES,
	REGION_CARIBBEAN,
	REGION_MESOAMERICA,
	REGION_BRAZIL,
	REGION_ARGENTINA,
	REGION_PERU,
	REGION_COLOMBIA,
	NUM_REGIONS
};

enum ECSArtStyles
{
	ARTSTYLE_AFRICA,
	ARTSTYLE_ANGLO_AMERICA,
	ARTSTYLE_ARABIA,
	ARTSTYLE_ASIA,
	ARTSTYLE_BARBARIAN,
	ARTSTYLE_CRESCENT,
	ARTSTYLE_EGYPT,
	ARTSTYLE_EUROPE,
	ARTSTYLE_GRECO_ROMAN,
	ARTSTYLE_INDIA,
	ARTSTYLE_IBERIA,
	ARTSTYLE_JAPAN,
	ARTSTYLE_MESO_AMERICA,
	ARTSTYLE_MONGOLIA,
	ARTSTYLE_NATIVE_AMERICA,
	ARTSTYLE_NORSE,
	ARTSTYLE_RUSSIA,
	ARTSTYLE_SOUTH_AMERICA,
	ARTSTYLE_SOUTH_EAST_ASIA,
	ARTSTYLE_SOUTH_PACIFIC,
};

#endif	// CVRHYES_H


extern int startingTurn[];
extern int startingTurnYear[]; // edead
//extern int fallTurnYear[];
extern char loadingTime[NUM_CIVS][4];
extern char loadingTime600AD[NUM_CIVS][4];
extern char loadingTime1700AD[NUM_CIVS][4];
extern char startingYear[NUM_CIVS][6];
extern bool startingEra[NUM_CIVS];
extern char startingYear600AD[NUM_CIVS][6];
extern bool startingEra600AD[NUM_CIVS];
extern char startingYear1700AD[NUM_CIVS][6];
extern bool startingEra1700AD[NUM_CIVS];

extern int takenTiles[NUM_PL];
extern int distanceSubtrahend[NUM_PL];
extern int distanceSubtrahendAstronomy[NUM_PL];
extern int distanceMultiply[NUM_PL];
extern int distanceMultiplyAstronomy[NUM_PL];
extern int compactEmpireModifierArray[NUM_PL];
extern int compactEmpireModifierAstronomy[NUM_PL];
extern int targetCityValueDivisor[NUM_PL];

extern int eraModifierInit[NUM_PL];
extern int eraModifierInitAstronomy[NUM_PL];
extern int cultureModifier[NUM_PL];

extern int unitCostModifier[NUM_PL];
extern int researchModifier[NUM_PL];
extern int distanceMaintenanceModifier[NUM_PL];
extern int numMaintenanceModifier[NUM_PL];
extern int civicUpkeepModifier[NUM_PL];
extern int healthModifier[NUM_PL];

extern int startingEraFound[NUM_PL];
extern int startingEraFound600AD[NUM_PL];
extern int startingEraFound1700AD[NUM_PL];
extern int startingEraFoundAstronomy[NUM_PL];
extern int startingEraRespawn[NUM_PL];
extern int unitCostModifier2[NUM_PL];
extern int wonderCostModifier[NUM_PL];
extern int buildingCostModifier[NUM_PL];
extern int inflationRateModifier[NUM_PL];
extern int greatPeopleThresholdArray[NUM_PL];
extern int currentEra[NUM_PL];
extern int currentEra600AD[NUM_PL];
extern int currentEra1700AD[NUM_PL];
extern int growthThreshold[NUM_PL];
extern int religiousTolerance[NUM_PL];

extern char uniquePower[NUM_CIVS][2][16];
extern char uniqueGoals[NUM_CIVS][3][18];
extern char rating[NUM_CIVS][6][15];

extern int lTechLeaderPenalty[NUM_ERAS];
extern int lTechBackwardsBonus[NUM_ERAS];

extern int regionSpreadFactor[NUM_REGIONS][NUM_RELIGIONS];

extern int turnPlayed[NUM_PL+NUM_MINORS]; 
extern int civSpreadFactor[NUM_PL+NUM_MINORS][NUM_RELIGIONS];
extern int borders[NUM_PL][NUM_PL];
extern int persecutionOrder[NUM_RELIGIONS][NUM_RELIGIONS-1];
extern int persecutionValue[NUM_RELIGIONS][NUM_RELIGIONS];
extern int regionMap[68][124];
extern int settlersMaps[2][NUM_PL][68][124];
extern int warMaps[2][NUM_PL][68][124];

inline int getStartingEra(PlayerTypes ePlayer, bool bAstronomy = true)
{
	if (GET_PLAYER(ePlayer).isReborn()) return startingEraRespawn[ePlayer];
	else if (bAstronomy && GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isHasTech((TechTypes)ASTRONOMY)) return startingEraFoundAstronomy[ePlayer];
	else if (getScenario() == SCENARIO_1700AD) return startingEraFound1700AD[ePlayer];
	else if (getScenario() == SCENARIO_600AD) return startingEraFound600AD[ePlayer];

	return startingEraFound[ePlayer];
}