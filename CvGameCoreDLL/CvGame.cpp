// game.cpp

#include "CvGameCoreDLL.h"
#include "CvGameCoreUtils.h"
#include "CvGame.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvPlayerAI.h"
#include "CvRandom.h"
#include "CvTeamAI.h"
#include "CvGlobals.h"
#include "CvInitCore.h"
#include "CvMapGenerator.h"
#include "CvArtFileMgr.h"
#include "CvDiploParameters.h"
#include "CvReplayMessage.h"
#include "CyArgsList.h"
#include "CvInfos.h"
#include "CvPopupInfo.h"
#include "FProfiler.h"
#include "CvReplayInfo.h"
#include "CvGameTextMgr.h"
#include <set>
#include "CvEventReporter.h"
#include "CvMessageControl.h"

// interface uses
#include "CvDLLInterfaceIFaceBase.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLPythonIFaceBase.h"

// BUG - start
#include "BugMod.h"
#include "CvBugOptions.h"
// BUG - end

#include "CvRhyes.h" //Rhye
#include <algorithm>
#include <cstdio>

// Public Functions...

CvGame::CvGame()
{
	m_aiRankPlayer = new int[MAX_PLAYERS];        // Ordered by rank...
	m_aiPlayerRank = new int[MAX_PLAYERS];        // Ordered by player ID...
	m_aiPlayerScore = new int[MAX_PLAYERS];       // Ordered by player ID...
	m_aiRankTeam = new int[MAX_TEAMS];						// Ordered by rank...
	m_aiTeamRank = new int[MAX_TEAMS];						// Ordered by team ID...
	m_aiTeamScore = new int[MAX_TEAMS];						// Ordered by team ID...

	// Leoreth
	m_aiTechRankTeam = new int[MAX_TEAMS];
	m_aiCivPeriod = new char[NUM_CIVS];
	m_aiCivilizationHistory = new std::hash_map<int, std::hash_map<int, int> >[NUM_HISTORY_TYPES];
	m_aiFirstDiscovered = NULL;
	m_aiFirstDiscoveredTurn = NULL;

	m_paiUnitCreatedCount = NULL;
	m_paiUnitClassCreatedCount = NULL;
	m_paiBuildingClassCreatedCount = NULL;
	m_paiProjectCreatedCount = NULL;
	m_paiForceCivicCount = NULL;
	m_paiVoteOutcome = NULL;
	m_paiReligionGameTurnFounded = NULL;
	m_paiCorporationGameTurnFounded = NULL;
	m_aiSecretaryGeneralTimer = NULL;
	m_aiVoteTimer = NULL;
	m_aiDiploVote = NULL;

	m_pabSpecialUnitValid = NULL;
	m_pabSpecialBuildingValid = NULL;
	m_abReligionSlotTaken = NULL;

	m_paHolyCity = NULL;
	m_paHeadquarters = NULL;

	m_pReplayInfo = NULL;

	m_aiShrineBuilding = NULL;
	m_aiShrineReligion = NULL;

	reset(NO_HANDICAP, true);
}


CvGame::~CvGame()
{
	uninit();

	SAFE_DELETE_ARRAY(m_aiRankPlayer);
	SAFE_DELETE_ARRAY(m_aiPlayerRank);
	SAFE_DELETE_ARRAY(m_aiPlayerScore);
	SAFE_DELETE_ARRAY(m_aiRankTeam);
	SAFE_DELETE_ARRAY(m_aiTeamRank);
	SAFE_DELETE_ARRAY(m_aiTeamScore);

	// Leoreth
	SAFE_DELETE_ARRAY(m_aiTechRankTeam);
	SAFE_DELETE_ARRAY(m_aiCivPeriod);
}


//Rhye - start (jdog)
void CvGame::logMsg(char* format, ... )
{
	static char buf[2048];
	_vsnprintf( buf, 2048-4, format, (char*)(&format+1) );
	gDLL->logMsg("sdkDbg.log", buf);
}
//Rhye - end


void CvGame::init(HandicapTypes eHandicap)
{
	bool bValid;
	int iStartTurn;
	int iEstimateEndTurn;
	int iI;

	//--------------------------------
	// Init saved data
	reset(eHandicap);

	//--------------------------------
	// Init containers
	m_deals.init();
	m_voteSelections.init();
	m_votesTriggered.init();

	m_mapRand.init(GC.getInitCore().getMapRandSeed() % 73637381);
	m_sorenRand.init(GC.getInitCore().getSyncRandSeed() % 52319761);

	//--------------------------------
	// Init non-saved data

	//--------------------------------
	// Init other game data

	// Turn off all MP options if it's a single player game
	if (GC.getInitCore().getType() == GAME_SP_NEW ||
		GC.getInitCore().getType() == GAME_SP_SCENARIO)
	{
		for (iI = 0; iI < NUM_MPOPTION_TYPES; ++iI)
		{
			setMPOption((MultiplayerOptionTypes)iI, false);
		}
	}

	// If this is a hot seat game, simultaneous turns is always off
	if (isHotSeat() || isPbem())
	{
		setMPOption(MPOPTION_SIMULTANEOUS_TURNS, false);
	}
	// If we didn't set a time in the Pitboss, turn timer off
	if (isPitboss() && getPitbossTurnTime() == 0)
	{
		setMPOption(MPOPTION_TURN_TIMER, false);
	}

	if (isMPOption(MPOPTION_SHUFFLE_TEAMS))
	{
		int aiTeams[MAX_CIV_PLAYERS];

		int iNumPlayers = 0;
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (GC.getInitCore().getSlotStatus((PlayerTypes)i) == SS_TAKEN)
			{
				aiTeams[iNumPlayers] = GC.getInitCore().getTeam((PlayerTypes)i);
				++iNumPlayers;
			}
		}

		for (int i = 0; i < iNumPlayers; i++)
		{
			int j = (getSorenRand().get(iNumPlayers - i, NULL) + i);

			if (i != j)
			{
				int iTemp = aiTeams[i];
				aiTeams[i] = aiTeams[j];
				aiTeams[j] = iTemp;
			}
		}

		iNumPlayers = 0;
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (GC.getInitCore().getSlotStatus((PlayerTypes)i) == SS_TAKEN)
			{
				GC.getInitCore().setTeam((PlayerTypes)i, (TeamTypes)aiTeams[iNumPlayers]);
				++iNumPlayers;
			}
		}
	}

	if (isOption(GAMEOPTION_LOCK_MODS))
	{
		if (isGameMultiPlayer())
		{
			setOption(GAMEOPTION_LOCK_MODS, false);
		}
		else
		{
			static const int iPasswordSize = 8;
			char szRandomPassword[iPasswordSize];
			for (int i = 0; i < iPasswordSize-1; i++)
			{
				szRandomPassword[i] = getSorenRandNum(128, NULL);
			}
			szRandomPassword[iPasswordSize-1] = 0;

			GC.getInitCore().setAdminPassword(szRandomPassword);
		}
	}

	//edead: start hack to allow late start with different game speeds
	/*if (getScenario() == SCENARIO_600AD) //late start condition
	{
		if (getGameTurn() == 181)
		{
			setGameTurn(getGameTurnForYear(600, -3000, GC.getInitCore().getCalendar(), GC.getInitCore().getGameSpeed()));
		}
	}

	if (getScenario() == SCENARIO_1700AD)
	{
		if (getGameTurn() == 321)
		{
			setGameTurn(getGameTurnForYear(1700, -3000, GC.getInitCore().getCalendar(), GC.getInitCore().getGameSpeed()));
		}
	}*/
	//edead: end

	if (getGameTurn() == 0)
	{
		iStartTurn = 0;

		for (iI = 0; iI < GC.getGameSpeedInfo(getGameSpeedType()).getNumTurnIncrements(); iI++)
		{
			iStartTurn += GC.getGameSpeedInfo(getGameSpeedType()).getGameTurnInfo(iI).iNumGameTurnsPerIncrement;
		}

		iStartTurn *= GC.getEraInfo(getStartEra()).getStartPercent();
		iStartTurn /= 100;

		setGameTurn(iStartTurn);
	}

	setStartTurn(getGameTurn());

	if (getMaxTurns() == 0)
	{
		iEstimateEndTurn = 0;

		for (iI = 0; iI < GC.getGameSpeedInfo(getGameSpeedType()).getNumTurnIncrements(); iI++)
		{
			iEstimateEndTurn += GC.getGameSpeedInfo(getGameSpeedType()).getGameTurnInfo(iI).iNumGameTurnsPerIncrement;
		}

		setEstimateEndTurn(iEstimateEndTurn);

		if (getEstimateEndTurn() > getGameTurn())
		{
			bValid = false;

			for (iI = 0; iI < GC.getNumVictoryInfos(); iI++)
			{
				if (isVictoryValid((VictoryTypes)iI))
				{
					if (GC.getVictoryInfo((VictoryTypes)iI).isEndScore())
					{
						bValid = true;
						break;
					}
				}
			}

			if (bValid)
			{
				setMaxTurns(getEstimateEndTurn() - getGameTurn());
			}
		}
	}
	else
	{
		setEstimateEndTurn(getGameTurn() + getMaxTurns());
	}

	setStartYear(GC.getDefineINT("START_YEAR"));

	for (iI = 0; iI < GC.getNumSpecialUnitInfos(); iI++)
	{
		if (GC.getSpecialUnitInfo((SpecialUnitTypes)iI).isValid())
		{
			makeSpecialUnitValid((SpecialUnitTypes)iI);
		}
	}

	for (iI = 0; iI < GC.getNumSpecialBuildingInfos(); iI++)
	{
		if (GC.getSpecialBuildingInfo((SpecialBuildingTypes)iI).isValid())
		{
			makeSpecialBuildingValid((SpecialBuildingTypes)iI);
		}
	}

	AI_init();

	doUpdateCacheOnTurn();
}

//
// Set initial items (units, techs, etc...)
//
void CvGame::setInitialItems()
{
	PROFILE_FUNC();

	//initFreeState();
	assignStartingPlots();
	normalizeStartingPlots();
	initFreeUnits();

	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)i);
		if (kPlayer.isAlive())
		{
			kPlayer.AI_updateFoundValues();
		}
	}
}

// BUG - MapFinder - start
// from HOF Mod - Dianthus
bool CvGame::canRegenerateMap() const
{
	if (GC.getGameINLINE().getElapsedGameTurns() != 0) return false;
	if (GC.getGameINLINE().isGameMultiPlayer()) return false;
	if (GC.getInitCore().getWBMapScript()) return false;

	// EF: TODO clear contact at start of regenerateMap()?
	for (int iI = 1; iI < MAX_CIV_TEAMS; iI++)
	{
		CvTeam& team=GET_TEAM((TeamTypes)iI);
		for (int iJ = 0; iJ < iI; iJ++)
		{
			if (team.isHasMet((TeamTypes)iJ)) return false;
		}
	}
	return true;
}
// BUG - MapFinder - end

void CvGame::regenerateMap()
{
	int iI;

	if (GC.getInitCore().getWBMapScript())
	{
		return;
	}

	setFinalInitialized(false);

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		GET_PLAYER((PlayerTypes)iI).killUnits();
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		GET_PLAYER((PlayerTypes)iI).killCities();
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		GET_PLAYER((PlayerTypes)iI).killAllDeals();
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		GET_PLAYER((PlayerTypes)iI).setFoundedFirstCity(false);
		GET_PLAYER((PlayerTypes)iI).setStartingPlot(NULL, false);
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		GC.getMapINLINE().setRevealedPlots(((TeamTypes)iI), false);
	}

	gDLL->getEngineIFace()->clearSigns();

	GC.getMapINLINE().erasePlots();

	CvMapGenerator::GetInstance().generateRandomMap();
	CvMapGenerator::GetInstance().addGameElements();

	gDLL->getEngineIFace()->RebuildAllPlots();

	CvEventReporter::getInstance().resetStatistics();

	setInitialItems();

	initScoreCalculation();
	setFinalInitialized(true);

	GC.getMapINLINE().setupGraphical();
	gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);

	gDLL->getInterfaceIFace()->setCycleSelectionCounter(1);

	gDLL->getEngineIFace()->AutoSave(true);

// BUG - AutoSave - start
	gDLL->getPythonIFace()->callFunction(PYBugModule, "gameStartSave");
// BUG - AutoSave - end

	// EF - This doesn't work until after the game has had time to update.
	//      Centering on the starting location is now done by MapFinder using BugUtil.delayCall().
	//      Must leave this here for non-BUG
	if (NO_PLAYER != getActivePlayer())
	{
		CvPlot* pPlot = GET_PLAYER(getActivePlayer()).getStartingPlot();

		if (NULL != pPlot)
		{
			gDLL->getInterfaceIFace()->lookAt(pPlot->getPoint(), CAMERALOOKAT_NORMAL);
		}
	}
}


void CvGame::uninit()
{
	SAFE_DELETE_ARRAY(m_aiShrineBuilding);
	SAFE_DELETE_ARRAY(m_aiShrineReligion);
	SAFE_DELETE_ARRAY(m_paiUnitCreatedCount);
	SAFE_DELETE_ARRAY(m_paiUnitClassCreatedCount);
	SAFE_DELETE_ARRAY(m_paiBuildingClassCreatedCount);
	SAFE_DELETE_ARRAY(m_paiProjectCreatedCount);
	SAFE_DELETE_ARRAY(m_paiForceCivicCount);
	SAFE_DELETE_ARRAY(m_paiVoteOutcome);
	SAFE_DELETE_ARRAY(m_paiReligionGameTurnFounded);
	SAFE_DELETE_ARRAY(m_paiCorporationGameTurnFounded);
	SAFE_DELETE_ARRAY(m_aiSecretaryGeneralTimer);
	SAFE_DELETE_ARRAY(m_aiVoteTimer);
	SAFE_DELETE_ARRAY(m_aiDiploVote);

	// Leoreth
	SAFE_DELETE_ARRAY(m_aiFirstDiscovered);
	SAFE_DELETE_ARRAY(m_aiFirstDiscoveredTurn);

	SAFE_DELETE_ARRAY(m_pabSpecialUnitValid);
	SAFE_DELETE_ARRAY(m_pabSpecialBuildingValid);
	SAFE_DELETE_ARRAY(m_abReligionSlotTaken);

	SAFE_DELETE_ARRAY(m_paHolyCity);
	SAFE_DELETE_ARRAY(m_paHeadquarters);

	m_aszDestroyedCities.clear();
	m_aszGreatPeopleBorn.clear();

	m_deals.uninit();
	m_voteSelections.uninit();
	m_votesTriggered.uninit();

	m_mapRand.uninit();
	m_sorenRand.uninit();

	clearReplayMessageMap();
	SAFE_DELETE(m_pReplayInfo);

	m_aPlotExtraYields.clear();
	m_aPlotExtraCosts.clear();
	m_mapVoteSourceReligions.clear();
	m_aeInactiveTriggers.clear();
}


// FUNCTION: reset()
// Initializes data members that are serialized.
void CvGame::reset(HandicapTypes eHandicap, bool bConstructorCall)
{
	int iI;

	//--------------------------------
	// Uninit class
	uninit();

	m_iElapsedGameTurns = 0;
	m_iStartTurn = 0;
	m_iStartYear = 0;
	m_iEstimateEndTurn = 0;
	m_iTurnSlice = 0;
	m_iCutoffSlice = 0;
	m_iNumGameTurnActive = 0;
	m_iNumCities = 0;
	m_iTotalPopulation = 0;
	m_iTradeRoutes = 0;
	m_iFreeTradeCount = 0;
	m_iNoNukesCount = 0;
	m_iNukesExploded = 0;
	m_iMaxPopulation = 0;
	m_iMaxLand = 0;
	m_iMaxTech = 0;
	m_iMaxWonders = 0;
	m_iInitPopulation = 0;
	m_iInitLand = 0;
	m_iInitTech = 0;
	m_iInitWonders = 0;
	m_iAIAutoPlay = 0;
	m_iCircumnavigated = -1; //Rhye
	m_iMedianTechValue = 0; // Leoreth

	// Leoreth: graphics paging
	m_iXResolution = 1024;
	m_iYResolution = 720;

	m_uiInitialTime = 0;

	m_bScoreDirty = false;
	m_bCircumnavigated = false;
	m_bDebugMode = false;
	m_bDebugModeCache = false;
	m_bFinalInitialized = false;
	m_bPbemTurnSent = false;
	m_bHotPbemBetweenTurns = false;
	m_bPlayerOptionsSent = false;
	m_bNukesValid = false;

	m_eHandicap = eHandicap;
	m_ePausePlayer = NO_PLAYER;
	m_eBestLandUnit = NO_UNIT;
	m_eWinner = NO_TEAM;
	m_eVictory = NO_VICTORY;
	m_eGameState = GAMESTATE_ON;
	m_eCityScreenOwner = NO_PLAYER;

	// Leoreth
	m_eGreatPeopleNotifications = NOTIFICATIONS_ALL;
	m_eReligionSpreadNotifications = NOTIFICATIONS_ALL;
	m_eGreatPeopleNotifications = NOTIFICATIONS_ALL;

	m_szScriptData = "";

	// Leoreth: graphics paging
	m_iLastLookatX = -1;
	m_iLastLookatY = -1;
	m_bWasGraphicsPagingEnabled = false;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_aiRankPlayer[iI] = 0;
		m_aiPlayerRank[iI] = 0;
		m_aiPlayerScore[iI] = 0;
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_aiRankTeam[iI] = 0;
		m_aiTeamRank[iI] = 0;
		m_aiTeamScore[iI] = 0;

		m_aiTechRankTeam[iI] = 0; // Leoreth
	}

	// Leoreth
	for (iI = 0; iI < NUM_CIVS; iI++)
	{
		m_aiCivPeriod[iI] = NO_PERIOD;
	}

	for (iI = 0; iI < NUM_HISTORY_TYPES; iI++)
	{
		m_aiCivilizationHistory[iI].clear();
	}

	if (!bConstructorCall)
	{
		FAssertMsg(m_paiUnitCreatedCount==NULL, "about to leak memory, CvGame::m_paiUnitCreatedCount");
		m_paiUnitCreatedCount = new int[GC.getNumUnitInfos()];
		for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
		{
			m_paiUnitCreatedCount[iI] = 0;
		}

		FAssertMsg(m_paiUnitClassCreatedCount==NULL, "about to leak memory, CvGame::m_paiUnitClassCreatedCount");
		m_paiUnitClassCreatedCount = new int[GC.getNumUnitClassInfos()];
		for (iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
		{
			m_paiUnitClassCreatedCount[iI] = 0;
		}

		FAssertMsg(m_paiBuildingClassCreatedCount==NULL, "about to leak memory, CvGame::m_paiBuildingClassCreatedCount");
		m_paiBuildingClassCreatedCount = new int[GC.getNumBuildingClassInfos()];
		for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
		{
			m_paiBuildingClassCreatedCount[iI] = 0;
		}

		FAssertMsg(m_paiProjectCreatedCount==NULL, "about to leak memory, CvGame::m_paiProjectCreatedCount");
		m_paiProjectCreatedCount = new int[GC.getNumProjectInfos()];
		for (iI = 0; iI < GC.getNumProjectInfos(); iI++)
		{
			m_paiProjectCreatedCount[iI] = 0;
		}

		FAssertMsg(m_paiForceCivicCount==NULL, "about to leak memory, CvGame::m_paiForceCivicCount");
		m_paiForceCivicCount = new int[GC.getNumCivicInfos()];
		for (iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			m_paiForceCivicCount[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumVoteInfos(), "GC.getNumVoteInfos() is not greater than zero in CvGame::reset");
		FAssertMsg(m_paiVoteOutcome==NULL, "about to leak memory, CvGame::m_paiVoteOutcome");
		m_paiVoteOutcome = new PlayerVoteTypes[GC.getNumVoteInfos()];
		for (iI = 0; iI < GC.getNumVoteInfos(); iI++)
		{
			m_paiVoteOutcome[iI] = NO_PLAYER_VOTE;
		}

		FAssertMsg(0 < GC.getNumVoteSourceInfos(), "GC.getNumVoteSourceInfos() is not greater than zero in CvGame::reset");
		FAssertMsg(m_aiDiploVote==NULL, "about to leak memory, CvGame::m_aiDiploVote");
		m_aiDiploVote = new int[GC.getNumVoteSourceInfos()];
		for (iI = 0; iI < GC.getNumVoteSourceInfos(); iI++)
		{
			m_aiDiploVote[iI] = 0;
		}

		FAssertMsg(m_pabSpecialUnitValid==NULL, "about to leak memory, CvGame::m_pabSpecialUnitValid");
		m_pabSpecialUnitValid = new bool[GC.getNumSpecialUnitInfos()];
		for (iI = 0; iI < GC.getNumSpecialUnitInfos(); iI++)
		{
			m_pabSpecialUnitValid[iI] = false;
		}

		FAssertMsg(m_pabSpecialBuildingValid==NULL, "about to leak memory, CvGame::m_pabSpecialBuildingValid");
		m_pabSpecialBuildingValid = new bool[GC.getNumSpecialBuildingInfos()];
		for (iI = 0; iI < GC.getNumSpecialBuildingInfos(); iI++)
		{
			m_pabSpecialBuildingValid[iI] = false;
		}

		FAssertMsg(m_paiReligionGameTurnFounded==NULL, "about to leak memory, CvGame::m_paiReligionGameTurnFounded");
		m_paiReligionGameTurnFounded = new int[GC.getNumReligionInfos()];
		FAssertMsg(m_abReligionSlotTaken==NULL, "about to leak memory, CvGame::m_abReligionSlotTaken");
		m_abReligionSlotTaken = new bool[GC.getNumReligionInfos()];
		FAssertMsg(m_paHolyCity==NULL, "about to leak memory, CvGame::m_paHolyCity");
		m_paHolyCity = new IDInfo[GC.getNumReligionInfos()];
		for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			m_paiReligionGameTurnFounded[iI] = -1;
			m_paHolyCity[iI].reset();
			m_abReligionSlotTaken[iI] = false;
		}

		FAssertMsg(m_paiCorporationGameTurnFounded==NULL, "about to leak memory, CvGame::m_paiCorporationGameTurnFounded");
		m_paiCorporationGameTurnFounded = new int[GC.getNumCorporationInfos()];
		m_paHeadquarters = new IDInfo[GC.getNumCorporationInfos()];
		for (iI = 0; iI < GC.getNumCorporationInfos(); iI++)
		{
			m_paiCorporationGameTurnFounded[iI] = -1;
			m_paHeadquarters[iI].reset();
		}

		FAssertMsg(m_aiShrineBuilding==NULL, "about to leak memory, CvGame::m_aiShrineBuilding");
		FAssertMsg(m_aiShrineReligion==NULL, "about to leak memory, CvGame::m_aiShrineReligion");
		m_aiShrineBuilding = new int[GC.getNumBuildingInfos()];
		m_aiShrineReligion = new int[GC.getNumBuildingInfos()];
		for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
		{
			m_aiShrineBuilding[iI] = (int) NO_BUILDING;
			m_aiShrineReligion[iI] = (int) NO_RELIGION;
		}

		FAssertMsg(m_aiSecretaryGeneralTimer==NULL, "about to leak memory, CvGame::m_aiSecretaryGeneralTimer");
		FAssertMsg(m_aiVoteTimer==NULL, "about to leak memory, CvGame::m_aiVoteTimer");
		m_aiSecretaryGeneralTimer = new int[GC.getNumVoteSourceInfos()];
		m_aiVoteTimer = new int[GC.getNumVoteSourceInfos()];
		for (iI = 0; iI < GC.getNumVoteSourceInfos(); iI++)
		{
			m_aiSecretaryGeneralTimer[iI] = 0;
			m_aiVoteTimer[iI] = 0;
		}

		FAssert(m_aiFirstDiscovered == NULL);
		FAssert(m_aiFirstDiscoveredTurn == NULL);
		m_aiFirstDiscovered = new char[GC.getNumTechInfos()];
		m_aiFirstDiscoveredTurn = new int[GC.getNumTechInfos()];
		for (iI = 0; iI < GC.getNumTechInfos(); iI++)
		{
			m_aiFirstDiscovered[iI] = NO_CIVILIZATION;
			m_aiFirstDiscoveredTurn[iI] = -1;
		}
	}

	m_deals.removeAll();
	m_voteSelections.removeAll();
	m_votesTriggered.removeAll();

	m_mapRand.reset();
	m_sorenRand.reset();

	m_iNumSessions = 1;

	m_iShrineBuildingCount = 0;
	m_iNumCultureVictoryCities = 0;
	m_eCultureVictoryCultureLevel = NO_CULTURELEVEL;

	if (!bConstructorCall)
	{
		AI_reset();
	}

		// Sanguo Mod Performance start, added by poyuzhe 07.27.09
	UnitTypes eUnit;
	std::vector<UnitTypes> aUpgradeUnits;

	for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		eUnit = (UnitTypes)iI;
		aUpgradeUnits.clear();
		do
		{
			for (int iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++)
			{
				if (GC.getUnitInfo(eUnit).getUpgradeUnitClass(iJ))
				{
					GC.getUnitInfo((UnitTypes)iI).addUpgradeUnitClassTypes(iJ);
					aUpgradeUnits.push_back((UnitTypes)GC.getUnitClassInfo((UnitClassTypes)iJ).getDefaultUnitIndex());
				}
			}
			if (aUpgradeUnits.size() > 0)
			{
				eUnit = aUpgradeUnits.front();
				aUpgradeUnits.erase(aUpgradeUnits.begin());
			}
			else
			{
				break;
			}
		}while(aUpgradeUnits.size() >= 0);
	}
	// Sanguo Mod Performance, end
}


void CvGame::initDiplomacy()
{
	PROFILE_FUNC();

	// Forced peace at the beginning of Advanced starts
	if (isOption(GAMEOPTION_ADVANCED_START))
	{
		CLinkList<TradeData> player1List;
		CLinkList<TradeData> player2List;
		TradeData kTradeData;
		setTradeItem(&kTradeData, TRADE_PEACE_TREATY);
		player1List.insertAtEnd(kTradeData);
		player2List.insertAtEnd(kTradeData);

		for (int iPlayer1 = 0; iPlayer1 < MAX_CIV_PLAYERS; ++iPlayer1)
		{
			CvPlayer& kLoopPlayer1 = GET_PLAYER((PlayerTypes)iPlayer1);

			if (kLoopPlayer1.isAlive())
			{
				for (int iPlayer2 = iPlayer1 + 1; iPlayer2 < MAX_CIV_PLAYERS; ++iPlayer2)
				{
					CvPlayer& kLoopPlayer2 = GET_PLAYER((PlayerTypes)iPlayer2);

					if (kLoopPlayer2.isAlive())
					{
						if (GET_TEAM(kLoopPlayer1.getTeam()).canChangeWarPeace(kLoopPlayer2.getTeam()))
						{
							implementDeal((PlayerTypes)iPlayer1, (PlayerTypes)iPlayer2, &player1List, &player2List);
						}
					}
				}
			}
		}
	}
}


void CvGame::initFreeState()
{
	bool bValid;
	int iI, iJ, iK;

	for (iI = 0; iI < GC.getNumTechInfos(); iI++)
	{
		for (iJ = 0; iJ < MAX_TEAMS; iJ++)
		{
			if (GET_TEAM((TeamTypes)iJ).isAlive())
			{
				bValid = false;

				if (!bValid)
				{
					if ((GC.getHandicapInfo(getHandicapType()).isFreeTechs(iI)) ||
						  (!(GET_TEAM((TeamTypes)iJ).isHuman())&& GC.getHandicapInfo(getHandicapType()).isAIFreeTechs(iI)) ||
						  (GC.getTechInfo((TechTypes)iI).getEra() < getStartEra()))
					{
						bValid = true;
					}
				}

				if (!bValid)
				{
					for (iK = 0; iK < MAX_PLAYERS; iK++)
					{
						if (GET_PLAYER((PlayerTypes)iK).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iK).getTeam() == iJ)
							{
								if (GC.getCivilizationInfo(GET_PLAYER((PlayerTypes)iK).getCivilizationType()).isCivilizationFreeTechs(iI))
								{
									bValid = true;
									break;
								}
							}
						}
					}
				}

				GET_TEAM((TeamTypes)iJ).setHasTech(((TechTypes)iI), bValid, NO_PLAYER, false, false);
				if (bValid && GC.getTechInfo((TechTypes)iI).isMapVisible())
				{
					GC.getMapINLINE().setRevealedPlots((TeamTypes)iJ, true, true);
				}
			}
		}
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).initFreeState();
		}
	}
}


void CvGame::initFreeUnits()
{
	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if ((GET_PLAYER((PlayerTypes)iI).getNumUnits() == 0) && (GET_PLAYER((PlayerTypes)iI).getNumCities() == 0))
			{
				GET_PLAYER((PlayerTypes)iI).initFreeUnits();
			}
		}
	}
}


void CvGame::assignStartingPlots()
{
	PROFILE_FUNC();

	CvPlot* pPlot;
	CvPlot* pBestPlot;
	bool bStartFound;
	bool bValid;
	int iRandOffset;
	int iLoopTeam;
	int iLoopPlayer;
	int iHumanSlot;
	int iValue;
	int iBestValue;
	int iI, iJ, iK;

	std::vector<int> playerOrder;
	std::vector<int>::iterator playerOrderIter;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getStartingPlot() == NULL)
			{
				iBestValue = 0;
				pBestPlot = NULL;

				for (iJ = 0; iJ < GC.getMapINLINE().numPlotsINLINE(); iJ++)
				{
					gDLL->callUpdater();	// allow window updates during launch

					pPlot = GC.getMapINLINE().plotByIndexINLINE(iJ);

					if (pPlot->isStartingPlot())
					{
						bValid = true;

						for (iK = 0; iK < MAX_CIV_PLAYERS; iK++)
						{
							if (GET_PLAYER((PlayerTypes)iK).isAlive())
							{
								if (GET_PLAYER((PlayerTypes)iK).getStartingPlot() == pPlot)
								{
									bValid = false;
									break;
								}
							}
						}

						if (bValid)
						{
							iValue = (1 + getSorenRandNum(1000, "Starting Plot"));

							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								pBestPlot = pPlot;
							}
						}
					}
				}

				if (pBestPlot != NULL)
				{
					GET_PLAYER((PlayerTypes)iI).setStartingPlot(pBestPlot, true);
				}
			}
		}
	}

	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "assignStartingPlots"))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			// Python override
			return;
		}
	}

	if (isTeamGame())
	{
		for (int iPass = 0; iPass < 2 * MAX_PLAYERS; ++iPass)
		{
			bStartFound = false;

			iRandOffset = getSorenRandNum(countCivTeamsAlive(), "Team Starting Plot");

			for (iI = 0; iI < MAX_CIV_TEAMS; iI++)
			{
				iLoopTeam = ((iI + iRandOffset) % MAX_CIV_TEAMS);

				if (GET_TEAM((TeamTypes)iLoopTeam).isAlive())
				{
					for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iJ).getTeam() == iLoopTeam)
							{
								if (GET_PLAYER((PlayerTypes)iJ).getStartingPlot() == NULL)
								{
									CvPlot* pStartingPlot = GET_PLAYER((PlayerTypes)iJ).findStartingPlot();

									if (NULL != pStartingPlot)
									{
										GET_PLAYER((PlayerTypes)iJ).setStartingPlot(pStartingPlot, true);
										playerOrder.push_back(iJ);
									}
									bStartFound = true;
									break;
								}
							}
						}
					}
				}
			}

			if (!bStartFound)
			{
				break;
			}
		}

		//check all players have starting plots
		for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
		{
			FAssertMsg(!GET_PLAYER((PlayerTypes)iJ).isAlive() || GET_PLAYER((PlayerTypes)iJ).getStartingPlot() != NULL, "Player has no starting plot");
		}
	}
	else if (isGameMultiPlayer())
	{
		iRandOffset = getSorenRandNum(countCivPlayersAlive(), "Player Starting Plot");

		for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			iLoopPlayer = ((iI + iRandOffset) % MAX_CIV_PLAYERS);

			if (GET_PLAYER((PlayerTypes)iLoopPlayer).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iLoopPlayer).isHuman())
				{
					if (GET_PLAYER((PlayerTypes)iLoopPlayer).getStartingPlot() == NULL)
					{
						GET_PLAYER((PlayerTypes)iLoopPlayer).setStartingPlot(GET_PLAYER((PlayerTypes)iLoopPlayer).findStartingPlot(), true);
						playerOrder.push_back(iLoopPlayer);
					}
				}
			}
		}

		for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (!(GET_PLAYER((PlayerTypes)iI).isHuman()))
				{
					if (GET_PLAYER((PlayerTypes)iI).getStartingPlot() == NULL)
					{
						GET_PLAYER((PlayerTypes)iI).setStartingPlot(GET_PLAYER((PlayerTypes)iI).findStartingPlot(), true);
						playerOrder.push_back(iI);
					}
				}
			}
		}
	}
	else
	{
		iHumanSlot = range((((countCivPlayersAlive() - 1) * GC.getHandicapInfo(getHandicapType()).getStartingLocationPercent()) / 100), 0, (countCivPlayersAlive() - 1));

		for (iI = 0; iI < iHumanSlot; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (!(GET_PLAYER((PlayerTypes)iI).isHuman()))
				{
					if (GET_PLAYER((PlayerTypes)iI).getStartingPlot() == NULL)
					{
						GET_PLAYER((PlayerTypes)iI).setStartingPlot(GET_PLAYER((PlayerTypes)iI).findStartingPlot(), true);
						playerOrder.push_back(iI);
					}
				}
			}
		}

		for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).isHuman())
				{
					if (GET_PLAYER((PlayerTypes)iI).getStartingPlot() == NULL)
					{
						GET_PLAYER((PlayerTypes)iI).setStartingPlot(GET_PLAYER((PlayerTypes)iI).findStartingPlot(), true);
						playerOrder.push_back(iI);
					}
				}
			}
		}

		for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getStartingPlot() == NULL)
				{
					GET_PLAYER((PlayerTypes)iI).setStartingPlot(GET_PLAYER((PlayerTypes)iI).findStartingPlot(), true);
					playerOrder.push_back(iI);
				}
			}
		}
	}

	//Now iterate over the player starts in the original order and re-place them.
	for (playerOrderIter = playerOrder.begin(); playerOrderIter != playerOrder.end(); ++playerOrderIter)
	{
		GET_PLAYER((PlayerTypes)(*playerOrderIter)).setStartingPlot(GET_PLAYER((PlayerTypes)(*playerOrderIter)).findStartingPlot(), true);
	}
}

// Swaps starting locations until we have reached the optimal closeness between teams
// (caveat: this isn't quite "optimal" because we could get stuck in local minima, but it's pretty good)

void CvGame::normalizeStartingPlotLocations()
{
	CvPlot* apNewStartPlots[MAX_CIV_PLAYERS];
	int* aaiDistances[MAX_CIV_PLAYERS];
	int aiStartingLocs[MAX_CIV_PLAYERS];
	int iI, iJ;

	// Precalculate distances between all starting positions:
	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			gDLL->callUpdater();	// allow window to update during launch
			aaiDistances[iI] = new int[iI];
			for (iJ = 0; iJ < iI; iJ++)
			{
				aaiDistances[iI][iJ] = 0;
			}
			CvPlot *pPlotI = GET_PLAYER((PlayerTypes)iI).getStartingPlot();
			if (pPlotI != NULL)
			{
				for (iJ = 0; iJ < iI; iJ++)
				{
					if (GET_PLAYER((PlayerTypes)iJ).isAlive())
					{
						CvPlot *pPlotJ = GET_PLAYER((PlayerTypes)iJ).getStartingPlot();
						if (pPlotJ != NULL)
						{
							int iDist = GC.getMapINLINE().calculatePathDistance(pPlotI, pPlotJ);
							if (iDist == -1)
							{
								// 5x penalty for not being on the same area, or having no passable route
								iDist = 5*plotDistance(pPlotI->getX_INLINE(), pPlotI->getY_INLINE(), pPlotJ->getX_INLINE(), pPlotJ->getY_INLINE());
							}
							aaiDistances[iI][iJ] = iDist;
						}
					}
				}
			}
		}
		else
		{
			aaiDistances[iI] = NULL;
		}
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		aiStartingLocs[iI] = iI; // each player starting in own location
	}

	int iBestScore = getTeamClosenessScore(aaiDistances, aiStartingLocs);
	bool bFoundSwap = true;
	while (bFoundSwap)
	{
		bFoundSwap = false;
		for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				for (iJ = 0; iJ < iI; iJ++)
				{
					if (GET_PLAYER((PlayerTypes)iJ).isAlive())
					{
						int iTemp = aiStartingLocs[iI];
						aiStartingLocs[iI] = aiStartingLocs[iJ];
						aiStartingLocs[iJ] = iTemp;
						int iScore = getTeamClosenessScore(aaiDistances, aiStartingLocs);
						if (iScore < iBestScore)
						{
							iBestScore = iScore;
							bFoundSwap = true;
						}
						else
						{
							// Swap them back:
							iTemp = aiStartingLocs[iI];
							aiStartingLocs[iI] = aiStartingLocs[iJ];
							aiStartingLocs[iJ] = iTemp;
						}
					}
				}
			}
		}
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		apNewStartPlots[iI] = NULL;
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (aiStartingLocs[iI] != iI)
			{
				apNewStartPlots[iI] = GET_PLAYER((PlayerTypes)aiStartingLocs[iI]).getStartingPlot();
			}
		}
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (apNewStartPlots[iI] != NULL)
			{
				GET_PLAYER((PlayerTypes)iI).setStartingPlot(apNewStartPlots[iI], false);
			}
		}
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		SAFE_DELETE_ARRAY(aaiDistances[iI]);
	}
}


void CvGame::normalizeAddRiver()
{
	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			CvPlot* pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
				if (!pStartingPlot->isFreshWater())
				{
					// if we will be able to add a lake, then use old river code
					if (normalizeFindLakePlot((PlayerTypes)iI) != NULL)
					{
						CvMapGenerator::GetInstance().doRiver(pStartingPlot);
					}
					// otherwise, use new river code which is much more likely to succeed
					else
					{
						CvMapGenerator::GetInstance().addRiver(pStartingPlot);
					}

					// add floodplains to any desert tiles the new river passes through
					for (int iK = 0; iK < GC.getMapINLINE().numPlotsINLINE(); iK++)
					{
						CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(iK);
						FAssert(pPlot != NULL);

						for (int iJ = 0; iJ < GC.getNumFeatureInfos(); iJ++)
						{
							if (GC.getFeatureInfo((FeatureTypes)iJ).isRequiresRiver())
							{
								if (pPlot->canHaveFeature((FeatureTypes)iJ))
								{
									if (GC.getFeatureInfo((FeatureTypes)iJ).getAppearanceProbability() == 10000)
									{
										if (pPlot->getBonusType() != NO_BONUS)
										{
											pPlot->setBonusType(NO_BONUS);
										}
										pPlot->setFeatureType((FeatureTypes)iJ);
										break;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}


void CvGame::normalizeRemovePeaks()
{
	CvPlot* pStartingPlot;
	CvPlot* pLoopPlot;
	int iRange;
	int iDX, iDY;
	int iI;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
				iRange = 3;

				for (iDX = -(iRange); iDX <= iRange; iDX++)
				{
					for (iDY = -(iRange); iDY <= iRange; iDY++)
					{
						pLoopPlot = plotXY(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iDX, iDY);

						if (pLoopPlot != NULL)
						{
							if (pLoopPlot->isPeak())
							{
								pLoopPlot->setPlotType(PLOT_HILLS);
							}
						}
					}
				}
			}
		}
	}
}

void CvGame::normalizeAddLakes()
{
	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			CvPlot* pLakePlot = normalizeFindLakePlot((PlayerTypes)iI);
			if (pLakePlot != NULL)
			{
				pLakePlot->setPlotType(PLOT_OCEAN);
			}
		}
	}
}

CvPlot* CvGame::normalizeFindLakePlot(PlayerTypes ePlayer)
{
	if (!GET_PLAYER(ePlayer).isAlive())
	{
		return NULL;
	}

	CvPlot* pStartingPlot = GET_PLAYER(ePlayer).getStartingPlot();
	if (pStartingPlot != NULL)
	{
		if (!(pStartingPlot->isFreshWater()))
		{
			for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
			{
				CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);

				if (pLoopPlot != NULL)
				{
					if (!(pLoopPlot->isWater()))
					{
						if (!(pLoopPlot->isCoastalLand()))
						{
							if (!(pLoopPlot->isRiver()))
							{
								if (pLoopPlot->getBonusType() == NO_BONUS)
								{
									bool bStartingPlot = false;

									for (int iK = 0; iK < MAX_CIV_PLAYERS; iK++)
									{
										if (GET_PLAYER((PlayerTypes)iK).isAlive())
										{
											if (GET_PLAYER((PlayerTypes)iK).getStartingPlot() == pLoopPlot)
											{
												bStartingPlot = true;
												break;
											}
										}
									}

									if (!bStartingPlot)
									{
										return pLoopPlot;
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return NULL;
}


void CvGame::normalizeRemoveBadFeatures()
{
	CvPlot* pStartingPlot;
	CvPlot* pLoopPlot;
	int iI, iJ;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
				for (iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot->getFeatureType() != NO_FEATURE)
						{
							if ((GC.getFeatureInfo(pLoopPlot->getFeatureType()).getYieldChange(YIELD_FOOD) <= 0) &&
								(GC.getFeatureInfo(pLoopPlot->getFeatureType()).getYieldChange(YIELD_PRODUCTION) <= 0))
							{
								pLoopPlot->setFeatureType(NO_FEATURE);
							}
						}
					}
				}

				int iX, iY;
				int iCityRange = CITY_PLOTS_RADIUS;
				int iExtraRange = 2;
				int iMaxRange = iCityRange + iExtraRange;

				for (iX = -iMaxRange; iX <= iMaxRange; iX++)
				{
					for (iY = -iMaxRange; iY <= iMaxRange; iY++)
					{
						pLoopPlot = plotXY(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iX, iY);
						if (pLoopPlot != NULL)
						{
							int iDistance = plotDistance(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());
							if (iDistance <= iMaxRange)
							{
								if (pLoopPlot->getFeatureType() != NO_FEATURE)
								{
									if ((GC.getFeatureInfo(pLoopPlot->getFeatureType()).getYieldChange(YIELD_FOOD) <= 0) &&
										(GC.getFeatureInfo(pLoopPlot->getFeatureType()).getYieldChange(YIELD_PRODUCTION) <= 0))
									{
										if (pLoopPlot->isWater())
										{
											if (pLoopPlot->isAdjacentToLand() || (!(iDistance == iMaxRange) && (getSorenRandNum(2, "Remove Bad Feature") == 0)))
											{
												pLoopPlot->setFeatureType(NO_FEATURE);
											}
										}
										else
										{
											if (!(iDistance == iMaxRange) && (getSorenRandNum((2 + (pLoopPlot->getBonusType() == NO_BONUS) ? 0 : 2), "Remove Bad Feature") == 0))
											{
												pLoopPlot->setFeatureType(NO_FEATURE);
											}
										}
									}
								}
							}
						}
					}
				}
			}
        }
	}
}


void CvGame::normalizeRemoveBadTerrain()
{
	CvPlot* pStartingPlot;
	CvPlot* pLoopPlot;
	int iI, iK;
	int iX, iY;

	int iTargetFood;
	int iTargetTotal;
	int iPlotFood;
	int iPlotProduction;


	int iCityRange = CITY_PLOTS_RADIUS;
	int iExtraRange = 1;
	int iMaxRange = iCityRange + iExtraRange;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
			    for (iX = -iMaxRange; iX <= iMaxRange; iX++)
			    {
			        for (iY = -iMaxRange; iY <= iMaxRange; iY++)
			        {
			            pLoopPlot = plotXY(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iX, iY);
                        if (pLoopPlot != NULL)
                        {
                            int iDistance = plotDistance(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());
                            if (iDistance <= iMaxRange)
                            {
                                if (!(pLoopPlot->isWater()) && ((iDistance <= iCityRange) || (pLoopPlot->isCoastalLand()) || (0 == getSorenRandNum(1 + iDistance - iCityRange, "Map Upgrade Terrain Food"))))
                                {
                                    iPlotFood = GC.getTerrainInfo(pLoopPlot->getTerrainType()).getYield(YIELD_FOOD);
                                    iPlotProduction = GC.getTerrainInfo(pLoopPlot->getTerrainType()).getYield(YIELD_PRODUCTION);
                                    if ((iPlotFood + iPlotProduction) <= 1)
                                    {
                                        iTargetFood = 1;
                                        iTargetTotal = 1;
                                        if (pLoopPlot->getBonusType(GET_PLAYER((PlayerTypes)iI).getTeam()) != NO_BONUS)
                                        {
                                            iTargetFood = 1;
                                            iTargetTotal = 2;
                                        }
                                        else if ((iPlotFood == 1) || (iDistance <= iCityRange))
                                        {
                                            iTargetFood = 1 + getSorenRandNum(2, "Map Upgrade Terrain Food");
                                            iTargetTotal = 2;
                                        }
                                        else
                                        {
                                            iTargetFood = pLoopPlot->isCoastalLand() ? 2 : 1;
                                            iTargetTotal = 2;
                                        }

                                        for (iK = 0; iK < GC.getNumTerrainInfos(); iK++)
                                        {
                                            if (!(GC.getTerrainInfo((TerrainTypes)iK).isWater()))
                                            {
                                                if ((GC.getTerrainInfo((TerrainTypes)iK).getYield(YIELD_FOOD) >= iTargetFood) &&
                                                    (GC.getTerrainInfo((TerrainTypes)iK).getYield(YIELD_FOOD) + GC.getTerrainInfo((TerrainTypes)iK).getYield(YIELD_PRODUCTION)) == iTargetTotal)
                                                {
                                                    if ((pLoopPlot->getFeatureType() == NO_FEATURE) || GC.getFeatureInfo(pLoopPlot->getFeatureType()).isTerrain(iK))
                                                    {
                                                        pLoopPlot->setTerrainType((TerrainTypes)iK);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }

			            }
			        }
				}
			}
		}
	}
}


void CvGame::normalizeAddFoodBonuses()
{
	bool bIgnoreLatitude = pythonIsBonusIgnoreLatitudes();

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			CvPlot* pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
				int iFoodBonus = 0;
				int iGoodNatureTileCount = 0;

				for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);

					if (pLoopPlot != NULL)
					{
						BonusTypes eBonus = pLoopPlot->getBonusType(GET_PLAYER((PlayerTypes)iI).getTeam());

						if (eBonus != NO_BONUS)
						{
							if (GC.getBonusInfo(eBonus).getYieldChange(YIELD_FOOD) > 0)
							{
								if ((GC.getBonusInfo(eBonus).getTechCityTrade() == NO_TECH) || (GC.getTechInfo((TechTypes)(GC.getBonusInfo(eBonus).getTechCityTrade())).getEra() <= getStartEra()))
								{
									if (pLoopPlot->isWater())
									{
										iFoodBonus += 2;
									}
									else
									{
										iFoodBonus += 3;
									}
								}
							}
							else if (pLoopPlot->calculateBestNatureYield(YIELD_FOOD, GET_PLAYER((PlayerTypes)iI).getTeam()) >= 2)
						    {
						        iGoodNatureTileCount++;
						    }
						}
						else
						{
                            if (pLoopPlot->calculateBestNatureYield(YIELD_FOOD, GET_PLAYER((PlayerTypes)iI).getTeam()) >= 3)
						    {
						        iGoodNatureTileCount++;
						    }
						}
					}
				}

				int iTargetFoodBonusCount = 3;
				iTargetFoodBonusCount += (iGoodNatureTileCount == 0) ? 2 : 0;

				for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					if (iFoodBonus >= iTargetFoodBonusCount)
					{
						break;
					}

					CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot != pStartingPlot)
						{
							if (pLoopPlot->getBonusType() == NO_BONUS)
							{
								for (int iK = 0; iK < GC.getNumBonusInfos(); iK++)
								{
									if (GC.getBonusInfo((BonusTypes)iK).isNormalize())
									{
										if (GC.getBonusInfo((BonusTypes)iK).getYieldChange(YIELD_FOOD) > 0)
										{
											if ((GC.getBonusInfo((BonusTypes)iK).getTechCityTrade() == NO_TECH) || (GC.getTechInfo((TechTypes)(GC.getBonusInfo((BonusTypes)iK).getTechCityTrade())).getEra() <= getStartEra()))
											{
												if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isHasTech((TechTypes)(GC.getBonusInfo((BonusTypes)iK).getTechReveal())))
												{
													if (pLoopPlot->canHaveBonus(((BonusTypes)iK), bIgnoreLatitude))
													{
														pLoopPlot->setBonusType((BonusTypes)iK);
														if (pLoopPlot->isWater())
														{
															iFoodBonus += 2;
														}
														else
														{
															iFoodBonus += 3;
														}
														break;
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}


void CvGame::normalizeAddGoodTerrain()
{
	CvPlot* pStartingPlot;
	CvPlot* pLoopPlot;
	bool bChanged;
	int iGoodPlot;
	int iI, iJ, iK;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
				iGoodPlot = 0;

				for (iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot != pStartingPlot)
						{
							if ((pLoopPlot->calculateNatureYield(YIELD_FOOD, GET_PLAYER((PlayerTypes)iI).getTeam()) >= GC.getFOOD_CONSUMPTION_PER_POPULATION()) &&
								  (pLoopPlot->calculateNatureYield(YIELD_PRODUCTION, GET_PLAYER((PlayerTypes)iI).getTeam()) > 0))
							{
								iGoodPlot++;
							}
						}
					}
				}

				for (iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					if (iGoodPlot >= 4)
					{
						break;
					}

					pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot != pStartingPlot)
						{
							if (!(pLoopPlot->isWater()))
							{
								if (!(pLoopPlot->isHills()))
								{
									if (pLoopPlot->getBonusType() == NO_BONUS)
									{
										bChanged = false;

										if (pLoopPlot->calculateNatureYield(YIELD_FOOD, GET_PLAYER((PlayerTypes)iI).getTeam()) < GC.getFOOD_CONSUMPTION_PER_POPULATION())
										{
											for (iK = 0; iK < GC.getNumTerrainInfos(); iK++)
											{
												if (!(GC.getTerrainInfo((TerrainTypes)iK).isWater()))
												{
													if (GC.getTerrainInfo((TerrainTypes)iK).getYield(YIELD_FOOD) >= GC.getFOOD_CONSUMPTION_PER_POPULATION())
													{
														pLoopPlot->setTerrainType((TerrainTypes)iK);
														bChanged = true;
														break;
													}
												}
											}
										}

										if (pLoopPlot->calculateNatureYield(YIELD_PRODUCTION, GET_PLAYER((PlayerTypes)iI).getTeam()) == 0)
										{
											for (iK = 0; iK < GC.getNumFeatureInfos(); iK++)
											{
												if ((GC.getFeatureInfo((FeatureTypes)iK).getYieldChange(YIELD_FOOD) >= 0) &&
													  (GC.getFeatureInfo((FeatureTypes)iK).getYieldChange(YIELD_PRODUCTION) > 0))
												{
													if (GC.getFeatureInfo((FeatureTypes)iK).isTerrain(pLoopPlot->getTerrainType()))
													{
														pLoopPlot->setFeatureType((FeatureTypes)iK);
														bChanged = true;
														break;
													}
												}
											}
										}

										if (bChanged)
										{
											iGoodPlot++;
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}


void CvGame::normalizeAddExtras()
{
	bool bIgnoreLatitude = pythonIsBonusIgnoreLatitudes();

	int iTotalValue = 0;
	int iPlayerCount = 0;
	int iBestValue = 0;
	int iWorstValue = MAX_INT;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			CvPlot* pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
				int iValue = GET_PLAYER((PlayerTypes)iI).AI_foundValue(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), -1, true);
				iTotalValue += iValue;
                iPlayerCount++;

                iBestValue = std::max(iValue, iBestValue);
                iWorstValue = std::min(iValue, iWorstValue);
			}
		}
	}

	//iTargetValue = (iTotalValue + iBestValue) / (iPlayerCount + 1);
	int iTargetValue = (iBestValue * 4) / 5;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			gDLL->callUpdater();	// allow window to update during launch
			CvPlot* pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

			if (pStartingPlot != NULL)
			{
                int iCount = 0;
				int iFeatureCount = 0;
				int aiShuffle[NUM_CITY_PLOTS];
				shuffleArray(aiShuffle, NUM_CITY_PLOTS, getMapRand());

				for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					if (GET_PLAYER((PlayerTypes)iI).AI_foundValue(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), -1, true) >= iTargetValue)
					{
						break;
					}
					if (getSorenRandNum((iCount + 2), "Setting Feature Type") <= 1)
					{
						CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), aiShuffle[iJ]);

						if (pLoopPlot != NULL)
						{
							if (pLoopPlot != pStartingPlot)
							{
								if (pLoopPlot->getBonusType() == NO_BONUS)
								{
									if (pLoopPlot->getFeatureType() == NO_FEATURE)
									{
										for (int iK = 0; iK < GC.getNumFeatureInfos(); iK++)
										{
											if ((GC.getFeatureInfo((FeatureTypes)iK).getYieldChange(YIELD_FOOD) + GC.getFeatureInfo((FeatureTypes)iK).getYieldChange(YIELD_PRODUCTION)) > 0)
											{
												if (pLoopPlot->canHaveFeature((FeatureTypes)iK))
												{
													pLoopPlot->setFeatureType((FeatureTypes)iK);
													iCount++;
													break;
												}
											}
										}
									}

									iFeatureCount += (pLoopPlot->getFeatureType() != NO_FEATURE) ? 1 : 0;
								}
							}
						}
					}
				}

				int iCoastFoodCount = 0;
				int iOceanFoodCount = 0;
				int iOtherCount = 0;
				int iWaterCount = 0;
				for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);
					if (pLoopPlot != NULL)
					{
						if (pLoopPlot != pStartingPlot)
						{
							if (pLoopPlot->isWater())
							{
								iWaterCount++;
								if (pLoopPlot->getBonusType() != NO_BONUS)
								{
									if (pLoopPlot->isAdjacentToLand())
									{
										iCoastFoodCount++;
									}
									else
									{
										iOceanFoodCount++;
									}
								}
							}
							else
							{
								if (pLoopPlot->getBonusType() != NO_BONUS)
								{
									iOtherCount++;
								}
							}
						}
					}
				}

			    bool bLandBias = (iWaterCount > NUM_CITY_PLOTS / 2);

                shuffleArray(aiShuffle, NUM_CITY_PLOTS, getMapRand());

				for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
				    CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), aiShuffle[iJ]);

                    if ((pLoopPlot != NULL) && (pLoopPlot != pStartingPlot))
                    {
                        if (getSorenRandNum(((bLandBias && pLoopPlot->isWater()) ? 2 : 1), "Placing Bonuses") == 0)
                        {
                        	if ((iOtherCount * 3 + iOceanFoodCount * 2 + iCoastFoodCount * 2) >= 12)
                        	{
                        		break;
                        	}

                            if (GET_PLAYER((PlayerTypes)iI).AI_foundValue(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), -1, true) >= iTargetValue)
                            {
                                break;
                            }

						    bool bCoast = (pLoopPlot->isWater() && pLoopPlot->isAdjacentToLand());
						    bool bOcean = (pLoopPlot->isWater() && !bCoast);
							if ((pLoopPlot != pStartingPlot)
                                && !(bCoast && (iCoastFoodCount > 2))
                                && !(bOcean && (iOceanFoodCount > 2)))
							{
								for (int iPass = 0; iPass < 2; iPass++)
								{
									if (pLoopPlot->getBonusType() == NO_BONUS)
									{
										for (int iK = 0; iK < GC.getNumBonusInfos(); iK++)
										{
											if (GC.getBonusInfo((BonusTypes)iK).isNormalize())
											{
											    //???no bonuses with negative yields?
												if ((GC.getBonusInfo((BonusTypes)iK).getYieldChange(YIELD_FOOD) >= 0) &&
													  (GC.getBonusInfo((BonusTypes)iK).getYieldChange(YIELD_PRODUCTION) >= 0))
												{
													if ((GC.getBonusInfo((BonusTypes)iK).getTechCityTrade() == NO_TECH) || (GC.getTechInfo((TechTypes)(GC.getBonusInfo((BonusTypes)iK).getTechCityTrade())).getEra() <= getStartEra()))
													{
														if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isHasTech((TechTypes)(GC.getBonusInfo((BonusTypes)iK).getTechReveal())))
														{
															if ((iPass == 0) ? CvMapGenerator::GetInstance().canPlaceBonusAt(((BonusTypes)iK), pLoopPlot->getX(), pLoopPlot->getY(), bIgnoreLatitude) : pLoopPlot->canHaveBonus(((BonusTypes)iK), bIgnoreLatitude))
															{
																pLoopPlot->setBonusType((BonusTypes)iK);
																iCoastFoodCount += bCoast ? 1 : 0;
																iOceanFoodCount += bOcean ? 1 : 0;
																iOtherCount += !(bCoast || bOcean) ? 1 : 0;
																break;
															}
														}
													}
												}
											}
										}

										if (bLandBias && !pLoopPlot->isWater() && pLoopPlot->getBonusType() == NO_BONUS)
										{
											if (((iFeatureCount > 4) && (pLoopPlot->getFeatureType() != NO_FEATURE))
												&& ((iCoastFoodCount + iOceanFoodCount) > 2))
											{
												if (getSorenRandNum(2, "Clear feature to add bonus") == 0)
												{
												pLoopPlot->setFeatureType(NO_FEATURE);

													for (iK = 0; iK < GC.getNumBonusInfos(); iK++)
													{
														if (GC.getBonusInfo((BonusTypes)iK).isNormalize())
														{
															//???no bonuses with negative yields?
															if ((GC.getBonusInfo((BonusTypes)iK).getYieldChange(YIELD_FOOD) >= 0) &&
																  (GC.getBonusInfo((BonusTypes)iK).getYieldChange(YIELD_PRODUCTION) >= 0))
															{
																if ((GC.getBonusInfo((BonusTypes)iK).getTechCityTrade() == NO_TECH) || (GC.getTechInfo((TechTypes)(GC.getBonusInfo((BonusTypes)iK).getTechCityTrade())).getEra() <= getStartEra()))
																{
																	if ((iPass == 0) ? CvMapGenerator::GetInstance().canPlaceBonusAt(((BonusTypes)iK), pLoopPlot->getX(), pLoopPlot->getY(), bIgnoreLatitude) : pLoopPlot->canHaveBonus(((BonusTypes)iK), bIgnoreLatitude))
																	{
																		pLoopPlot->setBonusType((BonusTypes)iK);
																		iOtherCount++;
																		break;
																	}
																}
															}
														}
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}

				shuffleArray(aiShuffle, NUM_CITY_PLOTS, getMapRand());

				for (iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					if (GET_PLAYER((PlayerTypes)iI).AI_foundValue(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), -1, true) >= iTargetValue)
					{
						break;
					}

					CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), aiShuffle[iJ]);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot != pStartingPlot)
						{
							if (pLoopPlot->getBonusType() == NO_BONUS)
							{
								if (pLoopPlot->getFeatureType() == NO_FEATURE)
								{
									for (int iK = 0; iK < GC.getNumFeatureInfos(); iK++)
									{
										if ((GC.getFeatureInfo((FeatureTypes)iK).getYieldChange(YIELD_FOOD) + GC.getFeatureInfo((FeatureTypes)iK).getYieldChange(YIELD_PRODUCTION)) > 0)
										{
											if (pLoopPlot->canHaveFeature((FeatureTypes)iK))
											{
												pLoopPlot->setFeatureType((FeatureTypes)iK);
												break;
											}
										}
									}
								}
							}
						}
					}
				}

				int iHillsCount = 0;

				for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					CvPlot* pLoopPlot =plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), iJ);
					if (pLoopPlot != NULL)
					{
						if (pLoopPlot->isHills())
						{
							iHillsCount++;
						}
					}
				}
				shuffleArray(aiShuffle, NUM_CITY_PLOTS, getMapRand());
				for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
				{
					if (iHillsCount >= 3)
					{
						break;
					}
					CvPlot* pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), aiShuffle[iJ]);
					if (pLoopPlot != NULL)
					{
						if (!pLoopPlot->isWater())
						{
							if (!pLoopPlot->isHills())
							{
								if ((pLoopPlot->getFeatureType() == NO_FEATURE) ||
									!GC.getFeatureInfo(pLoopPlot->getFeatureType()).isRequiresFlatlands())
								{
									if ((pLoopPlot->getBonusType() == NO_BONUS) ||
										GC.getBonusInfo(pLoopPlot->getBonusType()).isHills())
									{
										pLoopPlot->setPlotType(PLOT_HILLS, false, true);
										iHillsCount++;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}


void CvGame::normalizeStartingPlots()
{
	PROFILE_FUNC();

	if (!(GC.getInitCore().getWBMapScript()) || GC.getInitCore().getWBMapNoPlayers())
	{
		if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeStartingPlotLocations", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
		{
			normalizeStartingPlotLocations();
		}
	}

	if (GC.getInitCore().getWBMapScript())
	{
		return;
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeAddRiver", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeAddRiver();
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeRemovePeaks", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeRemovePeaks();
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeAddLakes", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeAddLakes();
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeRemoveBadFeatures", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeRemoveBadFeatures();
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeRemoveBadTerrain", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeRemoveBadTerrain();
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeAddFoodBonuses", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeAddFoodBonuses();
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeAddGoodTerrain", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeAddGoodTerrain();
	}

	if (!gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "normalizeAddExtras", NULL)  || gDLL->getPythonIFace()->pythonUsingDefaultImpl())
	{
		normalizeAddExtras();
	}
}

// For each of n teams, let the closeness score for that team be the average distance of an edge between two players on that team.
// This function calculates the closeness score for each team and returns the sum of those n scores.
// The lower the result, the better "clumped" the players' starting locations are.
//
// Note: for the purposes of this function, player i will be assumed to start in the location of player aiStartingLocs[i]

int CvGame::getTeamClosenessScore(int** aaiDistances, int* aiStartingLocs)
{
	int iScore = 0;

	for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; iTeam++)
	{
		if (GET_TEAM((TeamTypes)iTeam).isAlive())
		{
			int iTeamTotalDist = 0;
			int iNumEdges = 0;
			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
			{
				if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
				{
					if (GET_PLAYER((PlayerTypes)iPlayer).getTeam() == (TeamTypes)iTeam)
					{
						for (int iOtherPlayer = 0; iOtherPlayer < iPlayer; iOtherPlayer++)
						{
							if (GET_PLAYER((PlayerTypes)iOtherPlayer).getTeam() == (TeamTypes)iTeam)
							{
								// Add the edge between these two players that are on the same team
								iNumEdges++;
								int iPlayerStart = aiStartingLocs[iPlayer];
								int iOtherPlayerStart = aiStartingLocs[iOtherPlayer];

								if (iPlayerStart < iOtherPlayerStart) // Make sure that iPlayerStart > iOtherPlayerStart
								{
									int iTemp = iPlayerStart;
									iPlayerStart = iOtherPlayerStart;
									iOtherPlayerStart = iTemp;
								}
								else if (iPlayerStart == iOtherPlayerStart)
								{
									FAssertMsg(false, "Two players are (hypothetically) assigned to the same starting location!");
								}
								iTeamTotalDist += aaiDistances[iPlayerStart][iOtherPlayerStart];
							}
						}
					}
				}
			}

			int iTeamScore;
			if (iNumEdges == 0)
			{
				iTeamScore = 0;
			}
			else
			{
				iTeamScore = iTeamTotalDist/iNumEdges; // the avg distance between team edges is the team score
			}

			iScore += iTeamScore;
		}
	}
	return iScore;
}


void CvGame::update()
{
	PROFILE("CvGame::update");

	CvPlot* lookatPlot = gDLL->getInterfaceIFace()->getLookAtPlot();
	if ( lookatPlot != NULL )
	{
		//	Sample th BUG setting in the main thread on entry to game update here (it requires a Python call
		//	so we don't want it happening in background, or more frequently than once per turn slice)
		bool bPagingEnabled = getBugOptionBOOL("MainInterface__EnableGraphicalPaging", false);
		GC.setGraphicalDetailPagingEnabled(bPagingEnabled);

		if ( m_bWasGraphicsPagingEnabled != bPagingEnabled)
		{
			for(int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
			{
				CvPlot*	pPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
				if ( pPlot != NULL )
				{
					if ( m_bWasGraphicsPagingEnabled )
					{
						pPlot->setShouldHaveFullGraphics(true);
					}
					else
					{
						pPlot->setShouldHaveFullGraphics(false);
					}
				}
			}
		}

		m_bWasGraphicsPagingEnabled = bPagingEnabled;

		if ( GC.getGraphicalDetailPagingEnabled() )
		{
			if ( (m_iLastLookatX != lookatPlot->getX_INLINE() || m_iLastLookatY != lookatPlot->getY_INLINE()) )
			{
				int pageInRange = GC.getGraphicalDetailPageInRange();
				CvPlot::notePageRenderStart((pageInRange*2+1)*(pageInRange*2+1));

				for(int iX = -pageInRange; iX <= pageInRange; iX++)
				{
					for(int iY = -pageInRange; iY <= pageInRange; iY++)
					{
						CvPlot* pPlot = plotXY(lookatPlot->getX_INLINE(),lookatPlot->getY_INLINE(),iX,iY);

						if ( pPlot != NULL )
						{
							pPlot->setShouldHaveFullGraphics(true);
						}
					}
				}

				m_iLastLookatX = lookatPlot->getX_INLINE();
				m_iLastLookatY = lookatPlot->getY_INLINE();
			}

			CvPlot::EvictGraphicsIfNecessary();
		}
	}

	if (!gDLL->GetWorldBuilderMode() || isInAdvancedStart())
	{
		sendPlayerOptions();

		// sample generic event
		//Rhye - start (this must not be commented as in Kael's mod)
		CyArgsList pyArgs;
		pyArgs.add(getTurnSlice());
		CvEventReporter::getInstance().genericEvent("gameUpdate", pyArgs.makeFunctionArgs());

		if (getTurnSlice() == 0)
		{
			// edead: disable autosave during autoplay
			if (GC.getDefineINT("NO_AUTOSAVE_DURING_AUTOPLAY") == 0 || (getGameTurn() > 0 && getAIAutoPlay() == 0))
			{
				gDLL->getEngineIFace()->AutoSave(true);
			}
			// edead: end
			//gDLL->getEngineIFace()->AutoSave(true);
		}

		if (getNumGameTurnActive() == 0)
		{
			if (!isPbem() || !getPbemTurnSent())
			{
				doTurn();
			}
		}

		updateScore();

		updateWar();

		updateMoves();

		updateTimers();

		updateTurnTimer();

		AI_updateAssignWork();

		testAlive();

		if ((getAIAutoPlay() == 0) && !(gDLL->GetAutorun()) /*&& GAMESTATE_EXTENDED != getGameState()*/)
		{
			if (countHumanPlayersAlive() == 0)
			{
				setGameState(GAMESTATE_OVER);
			}
		}

		changeTurnSlice(1);

		if (NO_PLAYER != getActivePlayer() && GET_PLAYER(getActivePlayer()).getAdvancedStartPoints() >= 0 && !gDLL->getInterfaceIFace()->isInAdvancedStart())
		{
			gDLL->getInterfaceIFace()->setInAdvancedStart(true);
			gDLL->getInterfaceIFace()->setWorldBuilder(true);
		}
	}
}

struct techRankCompare
{
	bool operator() (TeamTypes eTeam1, TeamTypes eTeam2)
	{
		return GET_TEAM(eTeam1).getTotalTechValue() > GET_TEAM(eTeam2).getTotalTechValue();
	}
};

void CvGame::updateTechRanks()
{
	std::vector<TeamTypes> techRankedTeams;
	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		techRankedTeams.push_back((TeamTypes)iI);
	}

	techRankCompare cmp;
	std::sort(techRankedTeams.begin(), techRankedTeams.end(), cmp);

	int iIndex = 0;
	for (std::vector<TeamTypes>::iterator it = techRankedTeams.begin(); it != techRankedTeams.end(); ++it)
	{
		setTechRank(iIndex++, *it);

		if (iIndex == countCivTeamsAlive() / 2)
		{
			setMedianTechValue(GET_TEAM(*it).getTotalTechValue());
		}
	}
}

void CvGame::setTechRank(int iRank, TeamTypes eTeam)
{
	m_aiTechRankTeam[eTeam] = iRank;
}

int CvGame::getTechRank(TeamTypes eTeam) const
{
	return m_aiTechRankTeam[(int)eTeam];
}

void CvGame::setMedianTechValue(int iValue)
{
	m_iMedianTechValue = iValue;
}

int CvGame::getMedianTechValue() const
{
	return m_iMedianTechValue;
}


void CvGame::updateScore(bool bForce)
{
	bool abPlayerScored[MAX_CIV_PLAYERS];
	bool abTeamScored[MAX_CIV_TEAMS];
	int iScore;
	int iBestScore;
	PlayerTypes eBestPlayer;
	TeamTypes eBestTeam;
	int iI, iJ, iK;

	if (!isScoreDirty() && !bForce)
	{
		return;
	}

	setScoreDirty(false);

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		abPlayerScored[iI] = false;
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		iBestScore = MIN_INT;
		eBestPlayer = NO_PLAYER;

		for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
		{
			if (!abPlayerScored[iJ])
			{
				iScore = GET_PLAYER((PlayerTypes)iJ).calculateScore(false);

				if (iScore >= iBestScore)
				{
					iBestScore = iScore;
					eBestPlayer = (PlayerTypes)iJ;
				}
			}
		}

		abPlayerScored[eBestPlayer] = true;

		setRankPlayer(iI, eBestPlayer);
		setPlayerRank(eBestPlayer, iI);
		setPlayerScore(eBestPlayer, iBestScore);
		setCivilizationHistory(HISTORY_SCORE, GET_PLAYER(eBestPlayer).getCivilizationType(), getGameTurn(), iBestScore);
	}

	for (iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		abTeamScored[iI] = false;
	}

	for (iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		iBestScore = MIN_INT;
		eBestTeam = NO_TEAM;

		for (iJ = 0; iJ < MAX_CIV_TEAMS; iJ++)
		{
			if (!abTeamScored[iJ])
			{
				iScore = 0;

				for (iK = 0; iK < MAX_CIV_PLAYERS; iK++)
				{
					if (GET_PLAYER((PlayerTypes)iK).getTeam() == iJ)
					{
						iScore += getPlayerScore((PlayerTypes)iK);
					}
				}

				if (iScore >= iBestScore)
				{
					iBestScore = iScore;
					eBestTeam = (TeamTypes)iJ;
				}
			}
		}

		abTeamScored[eBestTeam] = true;

		setRankTeam(iI, eBestTeam);
		setTeamRank(eBestTeam, iI);
		setTeamScore(eBestTeam, iBestScore);
	}
}

void CvGame::updatePlotGroups()
{
	PROFILE_FUNC();

	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).updatePlotGroups();
		}
	}
}


void CvGame::updateBuildingCommerce()
{
	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).updateBuildingCommerce();
		}
	}
}


void CvGame::updateCitySight(bool bIncrement)
{
	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).updateCitySight(bIncrement, false);
		}
	}

	updatePlotGroups();
}


void CvGame::updateTradeRoutes()
{
	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).updateTradeRoutes();
		}
	}
}


void CvGame::testExtendedGame()
{
	int iI;

	if (getGameState() != GAMESTATE_OVER)
	{
		return;
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).isHuman())
			{
				if (GET_PLAYER((PlayerTypes)iI).isExtendedGame())
				{
					setGameState(GAMESTATE_EXTENDED);
					break;
				}
			}
		}
	}
}


void CvGame::cityPushOrder(CvCity* pCity, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl) const
{
	if (pCity->getProduction() > 0)
	{
		CvMessageControl::getInstance().sendPushOrder(pCity->getID(), eOrder, iData, bAlt, bShift, !bShift);
	}
	else if ((eOrder == ORDER_TRAIN) && (pCity->getProductionUnit() == iData))
	{
		CvMessageControl::getInstance().sendPushOrder(pCity->getID(), eOrder, iData, bAlt, !bCtrl, bCtrl);
	}
	else
	{
		CvMessageControl::getInstance().sendPushOrder(pCity->getID(), eOrder, iData, bAlt, bShift, bCtrl);
	}
}


void CvGame::selectUnit(CvUnit* pUnit, bool bClear, bool bToggle, bool bSound) const
{
	PROFILE_FUNC();

	CLLNode<IDInfo>* pEntityNode;
	CvSelectionGroup* pSelectionGroup;
	bool bSelectGroup;
	bool bGroup;

	if (gDLL->getInterfaceIFace()->getHeadSelectedUnit() == NULL)
	{
		bSelectGroup = true;
	}
	else if (gDLL->getInterfaceIFace()->getHeadSelectedUnit()->getGroup() != pUnit->getGroup())
	{
		bSelectGroup = true;
	}
	else if (pUnit->IsSelected() && !(gDLL->getInterfaceIFace()->mirrorsSelectionGroup()))
	{
		bSelectGroup = !bToggle;
	}
	else
	{
		bSelectGroup = false;
	}

	gDLL->getInterfaceIFace()->clearSelectedCities();

	if (bClear)
	{
		gDLL->getInterfaceIFace()->clearSelectionList();
		bGroup = false;
	}
	else
	{
		bGroup = gDLL->getInterfaceIFace()->mirrorsSelectionGroup();
	}

	if (bSelectGroup)
	{
		pSelectionGroup = pUnit->getGroup();

		gDLL->getInterfaceIFace()->selectionListPreChange();

		pEntityNode = pSelectionGroup->headUnitNode();

		while (pEntityNode != NULL)
		{
			FAssertMsg(::getUnit(pEntityNode->m_data), "null entity in selection group");
			gDLL->getInterfaceIFace()->insertIntoSelectionList(::getUnit(pEntityNode->m_data), false, bToggle, bGroup, bSound, true);

			pEntityNode = pSelectionGroup->nextUnitNode(pEntityNode);
		}

		gDLL->getInterfaceIFace()->selectionListPostChange();
	}
	else
	{
		gDLL->getInterfaceIFace()->insertIntoSelectionList(pUnit, false, bToggle, bGroup, bSound);
	}

	gDLL->getInterfaceIFace()->makeSelectionListDirty();
}


void CvGame::selectGroup(CvUnit* pUnit, bool bShift, bool bCtrl, bool bAlt) const
{
	PROFILE_FUNC();

	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pUnitPlot;
	bool bGroup;

	FAssertMsg(pUnit != NULL, "pUnit == NULL unexpectedly");

	if (bAlt || bCtrl)
	{
		gDLL->getInterfaceIFace()->clearSelectedCities();

		if (!bShift)
		{
			gDLL->getInterfaceIFace()->clearSelectionList();
			bGroup = true;
		}
		else
		{
			bGroup = gDLL->getInterfaceIFace()->mirrorsSelectionGroup();
		}

		pUnitPlot = pUnit->plot();

		pUnitNode = pUnitPlot->headUnitNode();

		gDLL->getInterfaceIFace()->selectionListPreChange();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = pUnitPlot->nextUnitNode(pUnitNode);

			if (pLoopUnit->getOwnerINLINE() == getActivePlayer())
			{
				if (pLoopUnit->canMove())
				{
					if (!isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || getTurnSlice() - pLoopUnit->getLastMoveTurn() > GC.getDefineINT("MIN_TIMER_UNIT_DOUBLE_MOVES"))
					{
						if (bAlt || (pLoopUnit->getUnitType() == pUnit->getUnitType()))
						{
							gDLL->getInterfaceIFace()->insertIntoSelectionList(pLoopUnit, false, false, bGroup, false, true);
						}
					}
				}
			}
		}

		gDLL->getInterfaceIFace()->selectionListPostChange();
	}
	else
	{
		gDLL->getInterfaceIFace()->selectUnit(pUnit, !bShift, bShift, true);
	}
}


void CvGame::selectAll(CvPlot* pPlot) const
{
	CvUnit* pSelectUnit;
	CvUnit* pCenterUnit;

	pSelectUnit = NULL;

	if (pPlot != NULL)
	{
		pCenterUnit = pPlot->getDebugCenterUnit();

		if ((pCenterUnit != NULL) && (pCenterUnit->getOwnerINLINE() == getActivePlayer()))
		{
			pSelectUnit = pCenterUnit;
		}
	}

	if (pSelectUnit != NULL)
	{
		gDLL->getInterfaceIFace()->selectGroup(pSelectUnit, false, false, true);
	}
}


bool CvGame::selectionListIgnoreBuildingDefense() const
{
	PROFILE_FUNC();

	CLLNode<IDInfo>* pSelectedUnitNode;
	CvUnit* pSelectedUnit;
	bool bIgnoreBuilding;
	bool bAttackLandUnit;

	bIgnoreBuilding = false;
	bAttackLandUnit = false;

	pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

	while (pSelectedUnitNode != NULL)
	{
		pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
		pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);

		if (pSelectedUnit != NULL)
		{
			if (pSelectedUnit->ignoreBuildingDefense())
			{
				bIgnoreBuilding = true;
			}

			if ((pSelectedUnit->getDomainType() == DOMAIN_LAND) && pSelectedUnit->canAttack())
			{
				bAttackLandUnit = true;
			}
		}
	}

	if (!bIgnoreBuilding && !bAttackLandUnit)
	{
		if (getBestLandUnit() != NO_UNIT)
		{
			bIgnoreBuilding = GC.getUnitInfo(getBestLandUnit()).isIgnoreBuildingDefense();
		}
	}

	return bIgnoreBuilding;
}


void CvGame::implementDeal(PlayerTypes eWho, PlayerTypes eOtherWho, CLinkList<TradeData>* pOurList, CLinkList<TradeData>* pTheirList, bool bForce)
{
	CvDeal* pDeal;

	FAssertMsg(eWho != NO_PLAYER, "Who is not assigned a valid value");
	FAssertMsg(eOtherWho != NO_PLAYER, "OtherWho is not assigned a valid value");
	FAssertMsg(eWho != eOtherWho, "eWho is not expected to be equal with eOtherWho");

	pDeal = addDeal();
	pDeal->init(pDeal->getID(), eWho, eOtherWho);
	pDeal->addTrades(pOurList, pTheirList, !bForce);
	if ((pDeal->getLengthFirstTrades() == 0) && (pDeal->getLengthSecondTrades() == 0))
	{
		pDeal->kill();
	}
}


void CvGame::verifyDeals()
{
	CvDeal* pLoopDeal;
	int iLoop;

	for(pLoopDeal = firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = nextDeal(&iLoop))
	{
		pLoopDeal->verify();
	}
}


/* Globeview configuration control:
If bStarsVisible, then there will be stars visible behind the globe when it is on
If bWorldIsRound, then the world will bend into a globe; otherwise, it will show up as a plane  */
void CvGame::getGlobeviewConfigurationParameters(TeamTypes eTeam, bool& bStarsVisible, bool& bWorldIsRound)
{
	if(GET_TEAM(eTeam).isMapCentering() || isCircumnavigated())
	{
		bStarsVisible = true;
		bWorldIsRound = true;
	}
	else
	{
		bStarsVisible = false;
		bWorldIsRound = false;
	}
}


int CvGame::getSymbolID(int iSymbol)
{
	return gDLL->getInterfaceIFace()->getSymbolID(iSymbol);
}


int CvGame::getAdjustedPopulationPercent(VictoryTypes eVictory) const
{
	int iPopulation;
	int iBestPopulation;
	int iNextBestPopulation;
	int iI;

	if (GC.getVictoryInfo(eVictory).getPopulationPercentLead() == 0)
	{
		return 0;
	}

	if (getTotalPopulation() == 0)
	{
		return 100;
	}

	iBestPopulation = 0;
	iNextBestPopulation = 0;

	for (iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			iPopulation = GET_TEAM((TeamTypes)iI).getTotalPopulation();

			if (iPopulation > iBestPopulation)
			{
				iNextBestPopulation = iBestPopulation;
				iBestPopulation = iPopulation;
			}
			else if (iPopulation > iNextBestPopulation)
			{
				iNextBestPopulation = iPopulation;
			}
		}
	}

	return std::min(100, (((iNextBestPopulation * 100) / getTotalPopulation()) + GC.getVictoryInfo(eVictory).getPopulationPercentLead()));
}


int CvGame::getProductionPerPopulation(HurryTypes eHurry)
{
	if (NO_HURRY == eHurry)
	{
		return 0;
	}
	return (GC.getHurryInfo(eHurry).getProductionPerPopulation() * 100) / std::max(1, GC.getGameSpeedInfo(getGameSpeedType()).getHurryPercent());
}


int CvGame::getAdjustedLandPercent(VictoryTypes eVictory) const
{
	int iPercent;

	if (GC.getVictoryInfo(eVictory).getLandPercent() == 0)
	{
		return 0;
	}

	iPercent = GC.getVictoryInfo(eVictory).getLandPercent();

	//Rhye
	//iPercent -= (countCivTeamsEverAlive() * 2);
	iPercent -= (countCivTeamsAlive() * 2);

	return std::max(iPercent, GC.getVictoryInfo(eVictory).getMinLandPercent());
}


bool CvGame::isTeamVote(VoteTypes eVote) const
{
	return (GC.getVoteInfo(eVote).isSecretaryGeneral() || GC.getVoteInfo(eVote).isVictory());
}


bool CvGame::isChooseElection(VoteTypes eVote) const
{
	return !(GC.getVoteInfo(eVote).isSecretaryGeneral());
}


bool CvGame::isTeamVoteEligible(TeamTypes eTeam, VoteSourceTypes eVoteSource) const
{
	CvTeam& kTeam = GET_TEAM(eTeam);

	// Leoreth: not for minors
	if (kTeam.isMinorCiv())
	{
		return false;
	}

	if (kTeam.isForceTeamVoteEligible(eVoteSource))
	{
		return true;
	}

	if (!kTeam.isFullMember(eVoteSource))
	{
		return false;
	}

	int iCount = 0;
	for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iI);
		if (kLoopTeam.isAlive())
		{
			if (kLoopTeam.isForceTeamVoteEligible(eVoteSource))
			{
				++iCount;
			}
		}
	}

	int iExtraEligible = GC.getDefineINT("TEAM_VOTE_MIN_CANDIDATES") - iCount;
	if (iExtraEligible <= 0)
	{
		return false;
	}

	for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		if (iI != eTeam)
		{
			CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iI);
			if (kLoopTeam.isAlive())
			{
				if (!kLoopTeam.isForceTeamVoteEligible(eVoteSource))
				{
					if (kLoopTeam.isFullMember(eVoteSource))
					{
						int iLoopVotes = kLoopTeam.getVotes(NO_VOTE, eVoteSource);
						int iVotes = kTeam.getVotes(NO_VOTE, eVoteSource);
						if (iLoopVotes > iVotes || (iLoopVotes == iVotes && iI < eTeam))
						{
							iExtraEligible--;
						}
					}
				}
			}
		}
	}

	return (iExtraEligible > 0);
}


int CvGame::countVote(const VoteTriggeredData& kData, PlayerVoteTypes eChoice) const
{
	int iCount = 0;
	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isMinorCiv())
		{
			continue;
		}

		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (getPlayerVote(((PlayerTypes)iI), kData.getID()) == eChoice)
			{
				iCount += GET_PLAYER((PlayerTypes)iI).getVotes(kData.kVoteOption.eVote, kData.eVoteSource);
			}
		}
	}

	return iCount;
}


int CvGame::countPossibleVote(VoteTypes eVote, VoteSourceTypes eVoteSource) const
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isMinorCiv())
		{
			continue;
		}

		iCount += GET_PLAYER((PlayerTypes)iI).getVotes(eVote, eVoteSource);
	}

	return iCount;
}



TeamTypes CvGame::findHighestVoteTeam(const VoteTriggeredData& kData) const
{
	TeamTypes eBestTeam = NO_TEAM;
	int iBestCount = 0;

	if (isTeamVote(kData.kVoteOption.eVote))
	{
		for (int iI = 0; iI < MAX_CIV_TEAMS; ++iI)
		{
			if (GET_TEAM((TeamTypes)iI).isMinorCiv())
			{
				continue;
			}

			if (GET_TEAM((TeamTypes)iI).isAlive())
			{
				int iCount = countVote(kData, (PlayerVoteTypes)iI);

				if (iCount > iBestCount)
				{
					iBestCount = iCount;
					eBestTeam = (TeamTypes)iI;
				}
			}
		}
	}

	return eBestTeam;
}


int CvGame::getVoteRequired(VoteTypes eVote, VoteSourceTypes eVoteSource) const
{
	return ((countPossibleVote(eVote, eVoteSource) * GC.getVoteInfo(eVote).getPopulationThreshold()) / 100);
}


TeamTypes CvGame::getSecretaryGeneral(VoteSourceTypes eVoteSource) const
{
	int iI;

	if (!canHaveSecretaryGeneral(eVoteSource))
	{
		for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); ++iBuilding)
		{
			if (GC.getBuildingInfo((BuildingTypes)iBuilding).getVoteSourceType() == eVoteSource)
			{
				for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
				{
					CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);

					if (kLoopPlayer.isMinorCiv())
					{
						continue;
					}

					if (kLoopPlayer.isAlive())
					{
						if (kLoopPlayer.getBuildingClassCount((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iBuilding).getBuildingClassType()) > 0)
						{
							ReligionTypes eReligion = getVoteSourceReligion(eVoteSource);
							if (NO_RELIGION == eReligion || kLoopPlayer.getStateReligion() == eReligion)
							{
								return kLoopPlayer.getTeam();
							}
						}
					}
				}
			}
		}
	}
	else
	{
		for (iI = 0; iI < GC.getNumVoteInfos(); iI++)
		{
			if (GC.getVoteInfo((VoteTypes)iI).isVoteSourceType(eVoteSource))
			{
				if (GC.getVoteInfo((VoteTypes)iI).isSecretaryGeneral())
				{
					if (isVotePassed((VoteTypes)iI))
					{
						return ((TeamTypes)(getVoteOutcome((VoteTypes)iI)));
					}
				}
			}
		}
	}


	return NO_TEAM;
}

bool CvGame::canHaveSecretaryGeneral(VoteSourceTypes eVoteSource) const
{
	for (int iI = 0; iI < GC.getNumVoteInfos(); iI++)
	{
		if (GC.getVoteInfo((VoteTypes)iI).isVoteSourceType(eVoteSource))
		{
			if (GC.getVoteInfo((VoteTypes)iI).isSecretaryGeneral())
			{
				return true;
			}
		}
	}

	return false;
}

void CvGame::clearSecretaryGeneral(VoteSourceTypes eVoteSource)
{
	for (int j = 0; j < GC.getNumVoteInfos(); ++j)
	{
		CvVoteInfo& kVote = GC.getVoteInfo((VoteTypes)j);

		if (kVote.isVoteSourceType(eVoteSource))
		{
			if (kVote.isSecretaryGeneral())
			{
				VoteTriggeredData kData;
				kData.eVoteSource = eVoteSource;
				kData.kVoteOption.eVote = (VoteTypes)j;
				kData.kVoteOption.iCityId = -1;
				kData.kVoteOption.szText.empty();
				kData.kVoteOption.ePlayer = NO_PLAYER;
				setVoteOutcome(kData, NO_PLAYER_VOTE);
				setSecretaryGeneralTimer(eVoteSource, 0);
			}
		}
	}
}

void CvGame::updateSecretaryGeneral()
{
	for (int i = 0; i < GC.getNumVoteSourceInfos(); ++i)
	{
		TeamTypes eSecretaryGeneral = getSecretaryGeneral((VoteSourceTypes)i);
		if (NO_TEAM != eSecretaryGeneral && !GET_TEAM(eSecretaryGeneral).isFullMember((VoteSourceTypes)i))
		{
			clearSecretaryGeneral((VoteSourceTypes)i);
		}
	}
}

int CvGame::countCivPlayersAlive() const
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive() && !GET_PLAYER((PlayerTypes)iI).isMinorCiv())
		{
			iCount++;
		}
	}

	return iCount;
}

int CvGame::countMajorPlayersAlive() const
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isMinorCiv())
		{
			continue;
		}

		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iCount++;
		}
	}

	return iCount;
}

int CvGame::countCivPlayersEverAlive() const
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iI);
		if (kPlayer.isEverAlive())
		{
			if (kPlayer.getParent() == NO_PLAYER)
			{
				iCount++;
			}
		}
	}

	return iCount;
}


int CvGame::countCivTeamsAlive() const
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive() && !GET_TEAM((TeamTypes)iI).isMinorCiv())
		{
			iCount++;
		}
	}

	return iCount;
}


int CvGame::countCivTeamsEverAlive() const
{
	std::set<int> setTeamsEverAlive;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iI);
		if (kPlayer.isEverAlive())
		{
			if (kPlayer.getParent() == NO_PLAYER)
			{
				setTeamsEverAlive.insert(kPlayer.getTeam());
			}
		}
	}

	return setTeamsEverAlive.size();
}


int CvGame::countHumanPlayersAlive() const
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iI);
		if (kPlayer.isAlive() && kPlayer.isHuman())
		{
			iCount++;
		}
	}

	return iCount;
}

int CvGame::countTotalCivPower()
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iI);
		if (kPlayer.isAlive())
		{
			iCount += kPlayer.getPower();
		}
	}

	return iCount;
}


int CvGame::countTotalNukeUnits()
{
	int iCount = 0;
	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iI);
		if (kPlayer.isAlive())
		{
			iCount += kPlayer.getNumNukeUnits();
		}
	}

	return iCount;
}


int CvGame::countKnownTechNumTeams(TechTypes eTech)
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isEverAlive())
		{
			if (GET_TEAM((TeamTypes)iI).isHasTech(eTech))
			{
				iCount++;
			}
		}
	}

	return iCount;
}


int CvGame::getNumFreeBonuses(BuildingTypes eBuilding)
{
	if (GC.getBuildingInfo(eBuilding).getNumFreeBonuses() == -1)
	{
		if (GC.getMapINLINE().getWorldSize() == -1)
		{
			return 7;
		}

		return GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getNumFreeBuildingBonuses();
	}
	else
	{
		return GC.getBuildingInfo(eBuilding).getNumFreeBonuses();
	}
}


int CvGame::countReligionLevels(ReligionTypes eReligion)
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iCount += GET_PLAYER((PlayerTypes)iI).getHasReligionCount(eReligion);
		}
	}

	return iCount;
}

int CvGame::countCorporationLevels(CorporationTypes eCorporation)
{
	int iCount = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);
		if (kLoopPlayer.isAlive())
		{
			iCount += GET_PLAYER((PlayerTypes)iI).getHasCorporationCount(eCorporation);
		}
	}

	return iCount;
}

void CvGame::replaceCorporation(CorporationTypes eCorporation1, CorporationTypes eCorporation2)
{
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);
		if (kLoopPlayer.isAlive())
		{
			int iIter;
			for (CvCity* pCity = kLoopPlayer.firstCity(&iIter); NULL != pCity; pCity = kLoopPlayer.nextCity(&iIter))
			{
				if (pCity->isHasCorporation(eCorporation1))
				{
					pCity->setHasCorporation(eCorporation1, false, false, false);
					pCity->setHasCorporation(eCorporation2, true, true);
				}
			}

			for (CvUnit* pUnit = kLoopPlayer.firstUnit(&iIter); NULL != pUnit; pUnit = kLoopPlayer.nextUnit(&iIter))
			{
				if (pUnit->getUnitInfo().getCorporationSpreads(eCorporation1) > 0)
				{
					pUnit->kill(false);
				}
			}
		}
	}
}


int CvGame::calculateReligionPercent(ReligionTypes eReligion) const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;
	int iI;

	if (getTotalPopulation() == 0)
	{
		return 0;
	}

	iCount = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
			{
				if (pLoopCity->isHasReligion(eReligion))
				{
					iCount += pLoopCity->getReligionPopulation(eReligion);
				}
			}
		}
	}

	return ((iCount * 100) / getTotalPopulation());
}


int CvGame::goldenAgeLength() const
{
	int iLength;

	iLength = GC.getDefineINT("GOLDEN_AGE_LENGTH");

	iLength *= GC.getGameSpeedInfo(getGameSpeedType()).getGoldenAgePercent();
	iLength /= 100;

	return iLength;
}

int CvGame::victoryDelay(VictoryTypes eVictory) const
{
	FAssert(eVictory >= 0 && eVictory < GC.getNumVictoryInfos());

	int iLength = GC.getVictoryInfo(eVictory).getVictoryDelayTurns();

	iLength *= GC.getGameSpeedInfo(getGameSpeedType()).getVictoryDelayPercent();
	iLength /= 100;

	return iLength;
}



int CvGame::getImprovementUpgradeTime(ImprovementTypes eImprovement) const
{
	int iTime;

	iTime = GC.getImprovementInfo(eImprovement).getUpgradeTime();

	iTime *= GC.getGameSpeedInfo(getGameSpeedType()).getImprovementPercent();
	iTime /= 100;

	iTime *= GC.getEraInfo(getStartEra()).getImprovementPercent();
	iTime /= 100;

	return iTime;
}


bool CvGame::canTrainNukes() const
{
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iI);
		if (kPlayer.isAlive())
		{
			for (int iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++)
			{
				UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(kPlayer.getCivilizationType()).getCivilizationUnits((UnitClassTypes)iJ);

				if (NO_UNIT != eUnit)
				{
					if (-1 != GC.getUnitInfo(eUnit).getNukeRange())
					{
						if (kPlayer.canTrain(eUnit))
						{
							return true;
						}
					}
				}
			}
		}
	}

	return false;
}


EraTypes CvGame::getCurrentEra() const
{
	int iEra;
	int iCount;
	int iI;

	iEra = 0;
	iCount = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iEra += GET_PLAYER((PlayerTypes)iI).getCurrentEra();
			iCount++;
		}
	}

	if (iCount > 0)
	{
		return ((EraTypes)(iEra / iCount));
	}

	return NO_ERA;
}


TeamTypes CvGame::getActiveTeam() const
{
	if (getActivePlayer() == NO_PLAYER)
	{
		return NO_TEAM;
	}
	else
	{
		return (TeamTypes)GET_PLAYER(getActivePlayer()).getTeam();
	}
}


CivilizationTypes CvGame::getActiveCivilizationType() const
{
	if (getActivePlayer() == NO_PLAYER)
	{
		return NO_CIVILIZATION;
	}
	else
	{
		return (CivilizationTypes)GET_PLAYER(getActivePlayer()).getCivilizationType();
	}
}


bool CvGame::isNetworkMultiPlayer() const
{
	return GC.getInitCore().getMultiplayer();
}


bool CvGame::isGameMultiPlayer() const
{
	return (isNetworkMultiPlayer() || isPbem() || isHotSeat());
}


bool CvGame::isTeamGame() const
{
	FAssert(countCivPlayersAlive() >= countCivTeamsAlive());
	return (countCivPlayersAlive() > countCivTeamsAlive());
}


bool CvGame::isModem()
{
	return gDLL->IsModem();
}
void CvGame::setModem(bool bModem)
{
	if (bModem)
	{
		gDLL->ChangeINIKeyValue("CONFIG", "Bandwidth", "modem");
	}
	else
	{
		gDLL->ChangeINIKeyValue("CONFIG", "Bandwidth", "broadband");
	}

	gDLL->SetModem(bModem);
}


void CvGame::reviveActivePlayer()
{
	if (!(GET_PLAYER(getActivePlayer()).isAlive()))
	{
		setAIAutoPlay(0);

		GC.getInitCore().setSlotStatus(getActivePlayer(), SS_TAKEN);

		CvEventReporter::getInstance().autoplayEnded();

		// Let Python handle it
		//Rhye - start
//Speed: Modified by Kael 04/19/2007
//		long lResult=0;
//		CyArgsList argsList;
//		argsList.add(getActivePlayer());
//
//		gDLL->getPythonIFace()->callFunction(PYGameModule, "doReviveActivePlayer", argsList.makeFunctionArgs(), &lResult);
//		if (lResult == 1)
//		{
//			return;
//		}
//Speed: End Modify
		//Rhye - end

		//GET_PLAYER(getActivePlayer()).initUnit(((UnitTypes)0), 0, 0); //Rhye
		//GET_PLAYER(getActivePlayer()).initUnit(((UnitTypes)GC.getInfoTypeForString("UNIT_CATAPULT")), 0, 0); //Rhye (catapult)
		//logMsg("init catapult in 00"); //Rhye

		// Leoreth
		GET_PLAYER(getActivePlayer()).verifyAlive();
	}
}


int CvGame::getNumHumanPlayers()
{
	return GC.getInitCore().getNumHumans();
}

int CvGame::getGameTurn()
{
	return GC.getInitCore().getGameTurn();
}


void CvGame::setGameTurn(int iNewValue)
{
	if (getGameTurn() != iNewValue)
	{
		GC.getInitCore().setGameTurn(iNewValue);
		FAssert(getGameTurn() >= 0);

		updateBuildingCommerce();

		setScoreDirty(true);

		gDLL->getInterfaceIFace()->setDirty(TurnTimer_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
	}
}


void CvGame::incrementGameTurn()
{
	setGameTurn(getGameTurn() + 1);
}


int CvGame::getTurnYear(int iGameTurn)
{
	// moved the body of this method to Game Core Utils so we have access for other games than the current one (replay screen in HOF)
	return getTurnYearForGame(iGameTurn, getStartYear(), getCalendar(), getGameSpeedType());
}


int CvGame::getGameTurnYear()
{
	return getTurnYear(getGameTurn());
}


int CvGame::getElapsedGameTurns() const
{
	return m_iElapsedGameTurns;
}


void CvGame::incrementElapsedGameTurns()
{
	m_iElapsedGameTurns++;
}


int CvGame::getMaxTurns() const
{
	return GC.getInitCore().getMaxTurns();
}


void CvGame::setMaxTurns(int iNewValue)
{
	GC.getInitCore().setMaxTurns(iNewValue);
	FAssert(getMaxTurns() >= 0);
}


void CvGame::changeMaxTurns(int iChange)
{
	setMaxTurns(getMaxTurns() + iChange);
}


int CvGame::getMaxCityElimination() const
{
	return GC.getInitCore().getMaxCityElimination();
}


void CvGame::setMaxCityElimination(int iNewValue)
{
	GC.getInitCore().setMaxCityElimination(iNewValue);
	FAssert(getMaxCityElimination() >= 0);
}

int CvGame::getNumAdvancedStartPoints() const
{
	return GC.getInitCore().getNumAdvancedStartPoints();
}


void CvGame::setNumAdvancedStartPoints(int iNewValue)
{
	GC.getInitCore().setNumAdvancedStartPoints(iNewValue);
	FAssert(getNumAdvancedStartPoints() >= 0);
}

int CvGame::getStartTurn() const
{
	return m_iStartTurn;
}


void CvGame::setStartTurn(int iNewValue)
{
	m_iStartTurn = iNewValue;
}


int CvGame::getStartYear() const
{
	return m_iStartYear;
}


void CvGame::setStartYear(int iNewValue)
{
	m_iStartYear = iNewValue;
}


int CvGame::getEstimateEndTurn() const
{
	return m_iEstimateEndTurn;
}


void CvGame::setEstimateEndTurn(int iNewValue)
{
	m_iEstimateEndTurn = iNewValue;
}


int CvGame::getTurnSlice() const
{
	return m_iTurnSlice;
}


int CvGame::getMinutesPlayed() const
{
	return (getTurnSlice() / gDLL->getTurnsPerMinute());
}


int CvGame::getSecondsPlayed() const
{
	return getTurnSlice() / gDLL->getTurnsPerSecond();
}


void CvGame::setTurnSlice(int iNewValue)
{
	m_iTurnSlice = iNewValue;
}


void CvGame::changeTurnSlice(int iChange)
{
	setTurnSlice(getTurnSlice() + iChange);
}


int CvGame::getCutoffSlice() const
{
	return m_iCutoffSlice;
}


void CvGame::setCutoffSlice(int iNewValue)
{
	m_iCutoffSlice = iNewValue;
}


void CvGame::changeCutoffSlice(int iChange)
{
	setCutoffSlice(getCutoffSlice() + iChange);
}


int CvGame::getTurnSlicesRemaining()
{
	return (getCutoffSlice() - getTurnSlice());
}


void CvGame::resetTurnTimer()
{
	// We should only use the turn timer if we are in multiplayer
	if (isMPOption(MPOPTION_TURN_TIMER))
	{
		if (getElapsedGameTurns() > 0 || !isOption(GAMEOPTION_ADVANCED_START))
		{
			// Determine how much time we should allow
			int iTurnLen = getMaxTurnLen();
			if (getElapsedGameTurns() == 0 && !isPitboss())
			{
				// Let's allow more time for the initial turn
				TurnTimerTypes eTurnTimer = GC.getInitCore().getTurnTimer();
				FAssertMsg(eTurnTimer >= 0 && eTurnTimer < GC.getNumTurnTimerInfos(), "Invalid TurnTimer selection in InitCore");
				iTurnLen = (iTurnLen * GC.getTurnTimerInfo(eTurnTimer).getFirstTurnMultiplier());
			}
			// Set the current turn slice to start the 'timer'
			setCutoffSlice(getTurnSlice() + iTurnLen);
		}
	}
}

void CvGame::incrementTurnTimer(int iNumTurnSlices)
{
	if (isMPOption(MPOPTION_TURN_TIMER))
	{
		// If the turn timer has expired, we shouldn't increment it as we've sent our turn complete message
		if (getTurnSlice() <= getCutoffSlice())
		{
			changeCutoffSlice(iNumTurnSlices);
		}
	}
}


int CvGame::getMaxTurnLen()
{
	if (isPitboss())
	{
		// Use the user provided input
		// Turn time is in hours
		return ( getPitbossTurnTime() * 3600 * 4);
	}
	else
	{
		int iMaxUnits = 0;
		int iMaxCities = 0;

		// Find out who has the most units and who has the most cities
		// Calculate the max turn time based on the max number of units and cities
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			if (GET_PLAYER((PlayerTypes)i).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)i).getNumUnits() > iMaxUnits)
				{
					iMaxUnits = GET_PLAYER((PlayerTypes)i).getNumUnits();
				}
				if (GET_PLAYER((PlayerTypes)i).getNumCities() > iMaxCities)
				{
					iMaxCities = GET_PLAYER((PlayerTypes)i).getNumCities();
				}
			}
		}

		// Now return turn len based on base len and unit and city bonuses
		TurnTimerTypes eTurnTimer = GC.getInitCore().getTurnTimer();
		FAssertMsg(eTurnTimer >= 0 && eTurnTimer < GC.getNumTurnTimerInfos(), "Invalid TurnTimer Selection in InitCore");
		return ( GC.getTurnTimerInfo(eTurnTimer).getBaseTime() +
			    (GC.getTurnTimerInfo(eTurnTimer).getCityBonus()*iMaxCities) +
				(GC.getTurnTimerInfo(eTurnTimer).getUnitBonus()*iMaxUnits) );
	}
}


int CvGame::getTargetScore() const
{
	return GC.getInitCore().getTargetScore();
}


void CvGame::setTargetScore(int iNewValue)
{
	GC.getInitCore().setTargetScore(iNewValue);
	FAssert(getTargetScore() >= 0);
}


int CvGame::getNumGameTurnActive()
{
	return m_iNumGameTurnActive;
}


int CvGame::countNumHumanGameTurnActive() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isHuman())
		{
			if (GET_PLAYER((PlayerTypes)iI).isTurnActive())
			{
				iCount++;
			}
		}
	}

	return iCount;
}


void CvGame::changeNumGameTurnActive(int iChange)
{
	m_iNumGameTurnActive = (m_iNumGameTurnActive + iChange);
	FAssert(getNumGameTurnActive() >= 0);
}


int CvGame::getNumCities() const
{
	return m_iNumCities;
}


int CvGame::getNumCivCities() const
{
	int iNumCities = getNumCities();

	iNumCities -= GET_PLAYER(BARBARIAN_PLAYER).getNumCities();

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isMinorCiv())
		{
			iNumCities -= GET_PLAYER((PlayerTypes)iI).getNumCities();
		}
	}

	return (getNumCities() - GET_PLAYER(BARBARIAN_PLAYER).getNumCities());
}


void CvGame::changeNumCities(int iChange)
{
	m_iNumCities = (m_iNumCities + iChange);
	FAssert(getNumCities() >= 0);
}


int CvGame::getTotalPopulation() const
{
	return m_iTotalPopulation;
}


void CvGame::changeTotalPopulation(int iChange)
{
	m_iTotalPopulation = (m_iTotalPopulation + iChange);
	FAssert(getTotalPopulation() >= 0);
}


int CvGame::getTradeRoutes() const
{
	return m_iTradeRoutes;
}


void CvGame::changeTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iTradeRoutes = (m_iTradeRoutes + iChange);
		FAssert(getTradeRoutes() >= 0);

		updateTradeRoutes();
	}
}


int CvGame::getFreeTradeCount() const
{
	return m_iFreeTradeCount;
}


bool CvGame::isFreeTrade() const
{
	return (getFreeTradeCount() > 0);
}


void CvGame::changeFreeTradeCount(int iChange)
{
	bool bOldFreeTrade;

	if (iChange != 0)
	{
		bOldFreeTrade = isFreeTrade();

		m_iFreeTradeCount = (m_iFreeTradeCount + iChange);
		FAssert(getFreeTradeCount() >= 0);

		if (bOldFreeTrade != isFreeTrade())
		{
			updateTradeRoutes();
		}
	}
}


int CvGame::getNoNukesCount() const
{
	return m_iNoNukesCount;
}


bool CvGame::isNoNukes() const
{
	return (getNoNukesCount() > 0);
}


void CvGame::changeNoNukesCount(int iChange)
{
	m_iNoNukesCount = (m_iNoNukesCount + iChange);
	FAssert(getNoNukesCount() >= 0);
}


int CvGame::getSecretaryGeneralTimer(VoteSourceTypes eVoteSource) const
{
	FAssert(eVoteSource >= 0);
	FAssert(eVoteSource < GC.getNumVoteSourceInfos());
	return m_aiSecretaryGeneralTimer[eVoteSource];
}


void CvGame::setSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iNewValue)
{
	FAssert(eVoteSource >= 0);
	FAssert(eVoteSource < GC.getNumVoteSourceInfos());
	m_aiSecretaryGeneralTimer[eVoteSource] = iNewValue;
	FAssert(getSecretaryGeneralTimer(eVoteSource) >= 0);
}


void CvGame::changeSecretaryGeneralTimer(VoteSourceTypes eVoteSource, int iChange)
{
	setSecretaryGeneralTimer(eVoteSource, getSecretaryGeneralTimer(eVoteSource) + iChange);
}


int CvGame::getVoteTimer(VoteSourceTypes eVoteSource) const
{
	FAssert(eVoteSource >= 0);
	FAssert(eVoteSource < GC.getNumVoteSourceInfos());
	return m_aiVoteTimer[eVoteSource];
}


void CvGame::setVoteTimer(VoteSourceTypes eVoteSource, int iNewValue)
{
	FAssert(eVoteSource >= 0);
	FAssert(eVoteSource < GC.getNumVoteSourceInfos());
	m_aiVoteTimer[eVoteSource] = iNewValue;
	FAssert(getVoteTimer(eVoteSource) >= 0);
}


void CvGame::changeVoteTimer(VoteSourceTypes eVoteSource, int iChange)
{
	setVoteTimer(eVoteSource, getVoteTimer(eVoteSource) + iChange);
}


int CvGame::getNukesExploded() const
{
	return m_iNukesExploded;
}


void CvGame::changeNukesExploded(int iChange)
{
	m_iNukesExploded = (m_iNukesExploded + iChange);
}


int CvGame::getMaxPopulation() const
{
	return m_iMaxPopulation;
}


int CvGame::getMaxLand() const
{
	return m_iMaxLand;
}


int CvGame::getMaxTech() const
{
	return m_iMaxTech;
}


int CvGame::getMaxWonders() const
{
	return m_iMaxWonders;
}


int CvGame::getInitPopulation() const
{
	return m_iInitPopulation;
}


int CvGame::getInitLand() const
{
	return m_iInitLand;
}


int CvGame::getInitTech() const
{
	return m_iInitTech;
}


int CvGame::getInitWonders() const
{
	return m_iInitWonders;
}


void CvGame::initScoreCalculation()
{
	// initialize score calculation
	int iMaxFood = 0;
	for (int i = 0; i < GC.getMapINLINE().numPlotsINLINE(); i++)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(i);
		if (!pPlot->isWater() || pPlot->isAdjacentToLand())
		{
			iMaxFood += pPlot->calculateBestNatureYield(YIELD_FOOD, NO_TEAM);
		}
	}
	m_iMaxPopulation = getPopulationScore(iMaxFood / std::max(1, GC.getFOOD_CONSUMPTION_PER_POPULATION()));
	m_iMaxLand = getLandPlotsScore(GC.getMapINLINE().getLandPlots());
	m_iMaxTech = 0;
	for (int i = 0; i < GC.getNumTechInfos(); i++)
	{
		m_iMaxTech += getTechScore((TechTypes)i);
	}
	m_iMaxWonders = 0;
	for (int i = 0; i < GC.getNumBuildingClassInfos(); i++)
	{
		m_iMaxWonders += getWonderScore((BuildingClassTypes)i);
	}

	if (NO_ERA != getStartEra())
	{
		int iNumSettlers = GC.getEraInfo(getStartEra()).getStartingUnitMultiplier();
		m_iInitPopulation = getPopulationScore(iNumSettlers * (GC.getEraInfo(getStartEra()).getFreePopulation() + 1));
		m_iInitLand = getLandPlotsScore(iNumSettlers *  NUM_CITY_PLOTS);
	}
	else
	{
		m_iInitPopulation = 0;
		m_iInitLand = 0;
	}

	m_iInitTech = 0;
	for (int i = 0; i < GC.getNumTechInfos(); i++)
	{
		if (GC.getTechInfo((TechTypes)i).getEra() < getStartEra())
		{
			m_iInitTech += getTechScore((TechTypes)i);
		}
		else
		{
			// count all possible free techs as initial to lower the score from immediate retirement
			for (int iCiv = 0; iCiv < GC.getNumCivilizationInfos(); iCiv++)
			{
				if (GC.getCivilizationInfo((CivilizationTypes)iCiv).isPlayable())
				{
					if (GC.getCivilizationInfo((CivilizationTypes)iCiv).isCivilizationFreeTechs(i))
					{
						m_iInitTech += getTechScore((TechTypes)i);
						break;
					}
				}
			}
		}
	}
	m_iInitWonders = 0;
}


int CvGame::getAIAutoPlay()
{
	return m_iAIAutoPlay;
}


void CvGame::setAIAutoPlay(int iNewValue)
{
	int iOldValue;

	iOldValue = getAIAutoPlay();

	if (iOldValue != iNewValue)
	{
		m_iAIAutoPlay = std::max(0, iNewValue);

		if ((iOldValue == 0) && (getAIAutoPlay() > 0))
		{
			GET_PLAYER(getActivePlayer()).killUnits();
			GET_PLAYER(getActivePlayer()).killCities();
		}
	}
}


void CvGame::changeAIAutoPlay(int iChange)
{
	setAIAutoPlay(getAIAutoPlay() + iChange);
}


unsigned int CvGame::getInitialTime()
{
	return m_uiInitialTime;
}


void CvGame::setInitialTime(unsigned int uiNewValue)
{
	m_uiInitialTime = uiNewValue;
}


bool CvGame::isScoreDirty() const
{
	return m_bScoreDirty;
}


void CvGame::setScoreDirty(bool bNewValue)
{
	m_bScoreDirty = bNewValue;
}


bool CvGame::isCircumnavigated() const
{
	return m_bCircumnavigated;
}


void CvGame::makeCircumnavigated()
{
	m_bCircumnavigated = true;
}

//Rhye - start
int CvGame::getCircumnavigated()
{
	return m_iCircumnavigated;
}


void CvGame::setCircumnavigated(int i)
{
	m_iCircumnavigated = i;
}
//Rhye - end

bool CvGame::circumnavigationAvailable() const
{
	if (isCircumnavigated())
	{
		return false;
	}

	// Leoreth: no circumnavigation in 1700 AD
	if (getScenario() == SCENARIO_1700AD)
	{
		return false;
	}

	if (GC.getDefineINT("CIRCUMNAVIGATE_FREE_MOVES") == 0)
	{
		return false;
	}

	CvMap& kMap = GC.getMapINLINE();

	if (!(kMap.isWrapXINLINE()) && !(kMap.isWrapYINLINE()))
	{
		return false;
	}

	if (kMap.getLandPlots() > ((kMap.numPlotsINLINE() * 2) / 3))
	{
		return false;
	}

	return true;
}

bool CvGame::isDiploVote(VoteSourceTypes eVoteSource) const
{
	return (getDiploVoteCount(eVoteSource) > 0);
}


int CvGame::getDiploVoteCount(VoteSourceTypes eVoteSource) const
{
	FAssert(eVoteSource >= 0 && eVoteSource < GC.getNumVoteSourceInfos());
	return m_aiDiploVote[eVoteSource];
}


void CvGame::changeDiploVote(VoteSourceTypes eVoteSource, int iChange)
{
	FAssert(eVoteSource >= 0 && eVoteSource < GC.getNumVoteSourceInfos());

	if (0 != iChange)
	{
		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
		{
			GET_PLAYER((PlayerTypes)iPlayer).processVoteSourceBonus(eVoteSource, false);
		}

		m_aiDiploVote[eVoteSource] += iChange;
		FAssert(getDiploVoteCount(eVoteSource) >= 0);

		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
		{
			GET_PLAYER((PlayerTypes)iPlayer).processVoteSourceBonus(eVoteSource, true);
		}
	}
}

bool CvGame::canDoResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const
{
	if (GC.getVoteInfo(kData.eVote).isVictory())
	{
		for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iTeam);

			if (kTeam.isVotingMember(eVoteSource))
			{
				if (kTeam.getVotes(kData.eVote, eVoteSource) >= getVoteRequired(kData.eVote, eVoteSource))
				{
					// Can't vote on a winner if one team already has all the votes necessary to win
					return false;
				}
			}
		}
	}

	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);

		if (kPlayer.isVotingMember(eVoteSource))
		{
			if (!kPlayer.canDoResolution(eVoteSource, kData))
			{
				return false;
			}
		}
		else if (kPlayer.isAlive() && !kPlayer.isBarbarian() && !kPlayer.isMinorCiv())
		{
			// all players need to be able to vote for a diplo victory
			if (GC.getVoteInfo(kData.eVote).isVictory())
			{
				return false;
			}
		}
	}

	return true;
}

bool CvGame::isValidVoteSelection(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const
{
	if (NO_PLAYER != kData.ePlayer)
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);
		if (!kPlayer.isAlive() || kPlayer.isBarbarian() || kPlayer.isMinorCiv())
		{
			return false;
		}
	}

	if (NO_PLAYER != kData.eOtherPlayer)
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.eOtherPlayer);
		if (!kPlayer.isAlive() || kPlayer.isBarbarian() || kPlayer.isMinorCiv())
		{
			return false;
		}
	}

	int iNumVoters = 0;
	for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
	{
		if (GET_TEAM((TeamTypes)iTeam).isVotingMember(eVoteSource))
		{
			++iNumVoters;
		}
	}
	if (iNumVoters < GC.getVoteInfo(kData.eVote).getMinVoters())
	{
		return false;
	}

	if (GC.getVoteInfo(kData.eVote).isOpenBorders())
	{
		bool bOpenWithEveryone = true;
		for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
		{
			if (GET_TEAM((TeamTypes)iTeam1).isFullMember(eVoteSource))
			{
				for (int iTeam2 = iTeam1 + 1; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
				{
					CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);

					if (kTeam2.isFullMember(eVoteSource))
					{
						if (!kTeam2.isOpenBorders((TeamTypes)iTeam1))
						{
							bOpenWithEveryone = false;
							break;
						}
					}
				}
			}
		}
		if (bOpenWithEveryone)
		{
			return false;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isDefensivePact())
	{
		bool bPactWithEveryone = true;
		for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
		{
			if (GET_TEAM((TeamTypes)iTeam1).isFullMember(eVoteSource))
			{
				for (int iTeam2 = iTeam1 + 1; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
				{
					CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);

					if (kTeam2.isFullMember(eVoteSource))
					{
						if (!kTeam2.isDefensivePact((TeamTypes)iTeam1))
						{
							bPactWithEveryone = false;
							break;
						}
					}
				}
			}
		}
		if (bPactWithEveryone)
		{
			return false;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForcePeace())
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (GET_TEAM(kPlayer.getTeam()).isAVassal())
		{
			return false;
		}

		if (!kPlayer.isFullMember(eVoteSource))
		{
			return false;
		}

		bool bValid = false;

		for (int iTeam2 = 0; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
		{
			if (atWar(kPlayer.getTeam(), (TeamTypes)iTeam2))
			{
				CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);

				if (kTeam2.isVotingMember(eVoteSource))
				{
					bValid = true;
					break;
				}
			}
		}

		if (!bValid)
		{
			return false;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceNoTrade())
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (kPlayer.isFullMember(eVoteSource))
		{
			return false;
		}

		bool bNoTradeWithEveryone = true;
		for (int iPlayer2 = 0; iPlayer2 < MAX_CIV_PLAYERS; ++iPlayer2)
		{
			CvPlayer& kPlayer2 = GET_PLAYER((PlayerTypes)iPlayer2);
			if (kPlayer2.getTeam() != kPlayer.getTeam())
			{
				if (kPlayer2.isFullMember(eVoteSource))
				{
					if (kPlayer2.canStopTradingWithTeam(kPlayer.getTeam()))
					{
						bNoTradeWithEveryone = false;
						break;
					}
				}
			}
		}
		// Not an option if already at war with everyone
		if (bNoTradeWithEveryone)
		{
			return false;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceWar())
	{
		ReligionTypes eVoteSourceReligion = GC.getGame().getVoteSourceReligion(eVoteSource);
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);
		CvTeam& kTeam = GET_TEAM(kPlayer.getTeam());

		if (kTeam.isAVassal())
		{
			return false;
		}

		// Leoreth: full member status lost if resolution is defied
		if (kPlayer.isFullMember(eVoteSource))
		{
			return false;
		}

		// Leoreth: can still never target the current secretary general
		if (kPlayer.getTeam() == getSecretaryGeneral(eVoteSource))
		{
			return false;
		}

		// Leoreth: crusade target if at war with a full member or controlling the holy city
		if (eVoteSourceReligion != NO_RELIGION)
		{
			bool bDefensiveCrusade = false;
			bool bOffensiveCrusade = false;
				
			if (GC.getGame().getHolyCity(eVoteSourceReligion) != NULL && GC.getGame().getHolyCity(eVoteSourceReligion)->getOwner() == kPlayer.getID())
			{
				bOffensiveCrusade = true;
			}

			if (kPlayer.countNumBuildings((BuildingTypes)GC.getInfoTypeForString("BUILDING_CATHOLIC_SHRINE")) > 0)
			{
				bOffensiveCrusade = true;
			}

			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
			{
				if (GET_PLAYER((PlayerTypes)iPlayer).isMinorCiv())
				{
					continue;
				}

				if (GET_PLAYER((PlayerTypes)iPlayer).isFullMember(eVoteSource))
				{
					if (GET_TEAM(GET_PLAYER((PlayerTypes)iPlayer).getTeam()).isAtWar(kPlayer.getTeam()))
					{
						bDefensiveCrusade = true;
						break;
					}
				}
			}

			if (!bDefensiveCrusade && !bOffensiveCrusade)
			{
				return false;
			}
		}

		return true;

		bool bAtWarWithEveryone = true;
		for (int iTeam2 = 0; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
		{
			if (iTeam2 != kPlayer.getTeam())
			{
				CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);
				if (kTeam2.isFullMember(eVoteSource))
				{
					if (!kTeam2.isAtWar(kPlayer.getTeam()) && kTeam2.canChangeWarPeace(kPlayer.getTeam()))
					{
						bAtWarWithEveryone = false;
						break;
					}
				}
			}
		}
		// Not an option if already at war with everyone
		if (bAtWarWithEveryone)
		{
			return false;
		}

		// Can be passed against a non-member only if he is already at war with a member
		// Leoreth: changed, non-members can always be targeted
		/*if (!kPlayer.isVotingMember(eVoteSource))
		{
			bool bValid = false;
			for (int iTeam2 = 0; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
			{
				if (atWar(kPlayer.getTeam(), (TeamTypes)iTeam2))
				{
					CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);

					if (kTeam2.isFullMember(eVoteSource))
					{
						bValid = true;
						break;
					}
				}
			}

			if (!bValid)
			{
				return false;
			}
		}*/
	}
	else if (GC.getVoteInfo(kData.eVote).isAssignCity())
	{
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);
		if (kPlayer.isFullMember(eVoteSource) || !kPlayer.isVotingMember(eVoteSource))
		{
			return false;
		}

		CvCity* pCity = kPlayer.getCity(kData.iCityId);
		FAssert(NULL != pCity);
		if (NULL == pCity)
		{
			return false;
		}

		// Leoreth: last city cannot be voted away
		if (kPlayer.getNumCities() <= 1)
		{
			return false;
		}

		if (NO_PLAYER == kData.eOtherPlayer)
		{
			return false;
		}

		CvPlayer& kOtherPlayer = GET_PLAYER(kData.eOtherPlayer);
		if (kOtherPlayer.getTeam() == kPlayer.getTeam())
		{
			return false;
		}

		if (atWar(kPlayer.getTeam(), GET_PLAYER(kData.eOtherPlayer).getTeam()))
		{
			return false;
		}

		if (!kOtherPlayer.isFullMember(eVoteSource))
		{
			return false;
		}

		if (kOtherPlayer.isHuman() && isOption(GAMEOPTION_ONE_CITY_CHALLENGE))
		{
			return false;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).getEspionage() > 0)
	{
		if (NO_PLAYER == kData.ePlayer)
		{
			return false;
		}

		if (NO_PLAYER == kData.eOtherPlayer)
		{
			return false;
		}

		if (GET_PLAYER(kData.eOtherPlayer).getTeam() == getSecretaryGeneral(eVoteSource))
		{
			return false;
		}

		if (!GET_PLAYER(kData.eOtherPlayer).isFullMember(eVoteSource))
		{
			return false;
		}

		if (GET_TEAM(GET_PLAYER(kData.eOtherPlayer).getTeam()).isVassal(GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return false;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).getGoldPercent() > 0)
	{
		if (NO_PLAYER == kData.ePlayer)
		{
			return false;
		}

		// impossible if there is a war between full members
		for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
		{
			CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);
			if (kTeam1.isFullMember(eVoteSource))
			{
				for (int iTeam2 = iTeam1+1; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
				{
					CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);
					if (kTeam2.isFullMember(eVoteSource))
					{
						if (kTeam1.isAtWar((TeamTypes)iTeam2)) return false;
					}
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isRevokeMembership())
	{
		if (NO_PLAYER == kData.ePlayer)
		{
			return false;
		}

		if (GET_PLAYER(kData.ePlayer).getTeam() == getSecretaryGeneral(eVoteSource))
		{
			return false;
		}

		if (!GET_PLAYER(kData.ePlayer).isFullMember(eVoteSource))
		{
			return false;
		}

		if (GET_TEAM(GET_PLAYER(kData.ePlayer).getTeam()).isVassal(getSecretaryGeneral(eVoteSource)))
		{
			return false;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isDecolonize())
	{
		if (NO_PLAYER == kData.ePlayer)
		{
			return false;
		}
		
		CvCity* pCity = GET_PLAYER(kData.ePlayer).getCity(kData.iCityId);
		FAssert(NULL != pCity);
		if (NULL == pCity)
		{
			return false;
		}

		// only civs at peace can be forced to decolonize
		CvTeam& kTeam = GET_TEAM(GET_PLAYER(kData.ePlayer).getTeam());
		for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			if (GET_TEAM((TeamTypes)iI).isMinorCiv())
			{
				continue;
			}

			if (kTeam.isAtWar((TeamTypes)iI))
			{
				return false;
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isReleaseCivilization())
	{
		if (kData.ePlayer == NO_PLAYER)
		{
			return false;
		}

		if (kData.eOtherPlayer == NO_PLAYER)
		{
			return false;
		}

		if (GET_TEAM(GET_PLAYER(kData.ePlayer).getTeam()).isVassal(getSecretaryGeneral(eVoteSource)))
		{
			return false;
		}
	}

	if (!canDoResolution(eVoteSource, kData))
	{
		return false;
	}

	return true;
}


bool CvGame::isDebugMode() const
{
	return m_bDebugModeCache;
}


void CvGame::toggleDebugMode()
{
	m_bDebugMode = ((m_bDebugMode) ? false : true);
	updateDebugModeCache();

	GC.getMapINLINE().updateVisibility();
	GC.getMapINLINE().updateSymbols();
	GC.getMapINLINE().updateMinimapColor();

	gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);

	//gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);

	if (m_bDebugMode)
	{
		gDLL->getEngineIFace()->PushFogOfWar(FOGOFWARMODE_OFF);
	}
	else
	{
		gDLL->getEngineIFace()->PopFogOfWar();
	}
	gDLL->getEngineIFace()->setFogOfWarFromStack();
}

void CvGame::updateDebugModeCache()
{
	if ((gDLL->getChtLvl() > 0) || (gDLL->GetWorldBuilderMode()))
	{
		m_bDebugModeCache = m_bDebugMode;
	}
	else
	{
		m_bDebugModeCache = false;
	}
}

int CvGame::getPitbossTurnTime() const
{
	return GC.getInitCore().getPitbossTurnTime();
}

void CvGame::setPitbossTurnTime(int iHours)
{
	GC.getInitCore().setPitbossTurnTime(iHours);
}


bool CvGame::isHotSeat() const
{
	return (GC.getInitCore().getHotseat());
}

bool CvGame::isPbem() const
{
	return (GC.getInitCore().getPbem());
}



bool CvGame::isPitboss() const
{
	return (GC.getInitCore().getPitboss());
}

bool CvGame::isSimultaneousTeamTurns() const
{
	if (!isNetworkMultiPlayer())
	{
		return false;
	}

	if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
	{
		return false;
	}

	return true;
}

bool CvGame::isFinalInitialized() const
{
	return m_bFinalInitialized;
}


void CvGame::setFinalInitialized(bool bNewValue)
{
	PROFILE_FUNC();

	int iI;

	if (isFinalInitialized() != bNewValue)
	{
		m_bFinalInitialized = bNewValue;

		if (isFinalInitialized())
		{
			updatePlotGroups();

			GC.getMapINLINE().updateIrrigated();

			for (iI = 0; iI < MAX_TEAMS; iI++)
			{
				if (GET_TEAM((TeamTypes)iI).isAlive())
				{
					GET_TEAM((TeamTypes)iI).AI_updateAreaStragies();
				}
			}
		}
	}
}


bool CvGame::getPbemTurnSent() const
{
	return m_bPbemTurnSent;
}


void CvGame::setPbemTurnSent(bool bNewValue)
{
	m_bPbemTurnSent = bNewValue;
}


bool CvGame::getHotPbemBetweenTurns() const
{
	return m_bHotPbemBetweenTurns;
}


void CvGame::setHotPbemBetweenTurns(bool bNewValue)
{
	m_bHotPbemBetweenTurns = bNewValue;
}


bool CvGame::isPlayerOptionsSent() const
{
	return m_bPlayerOptionsSent;
}


void CvGame::sendPlayerOptions(bool bForce)
{
	int iI;

	if (getActivePlayer() == NO_PLAYER)
	{
		return;
	}

	if (!isPlayerOptionsSent() || bForce)
	{
		m_bPlayerOptionsSent = true;

		for (iI = 0; iI < NUM_PLAYEROPTION_TYPES; iI++)
		{
			gDLL->sendPlayerOption(((PlayerOptionTypes)iI), gDLL->getPlayerOption((PlayerOptionTypes)iI));
		}
	}
}


PlayerTypes CvGame::getActivePlayer() const
{
	return GC.getInitCore().getActivePlayer();
}


void CvGame::setActivePlayer(PlayerTypes eNewValue, bool bForceHotSeat)
{
	PlayerTypes eOldActivePlayer = getActivePlayer();
	if (eOldActivePlayer != eNewValue)
	{
		int iActiveNetId = ((NO_PLAYER != eOldActivePlayer) ? GET_PLAYER(eOldActivePlayer).getNetID() : -1);
		//Rhye - start
		GC.getInitCore().setSlotStatus(eOldActivePlayer, SS_COMPUTER);
		GC.getInitCore().setSlotStatus(eNewValue, SS_TAKEN);
		//Rhye
		GC.getInitCore().setActivePlayer(eNewValue);

		if (GET_PLAYER(eNewValue).isHuman() && (isHotSeat() || isPbem() || bForceHotSeat))
		{
			gDLL->getPassword(eNewValue);
			setHotPbemBetweenTurns(false);
			gDLL->getInterfaceIFace()->dirtyTurnLog(eNewValue);

			if (NO_PLAYER != eOldActivePlayer)
			{
				int iInactiveNetId = GET_PLAYER(eNewValue).getNetID();
				GET_PLAYER(eNewValue).setNetID(iActiveNetId);
				GET_PLAYER(eOldActivePlayer).setNetID(iInactiveNetId);
			}

			GET_PLAYER(eNewValue).showMissedMessages();

			if (countHumanPlayersAlive() == 1 && isPbem())
			{
				// Nobody else left alive
				GC.getInitCore().setType(GAME_HOTSEAT_NEW);
			}

			sendPlayerOptions(true); //Rhye

			if (isHotSeat() || bForceHotSeat)
			{
				sendPlayerOptions(true);
			}

			// Leoreth: allow winning again after switching
			if (getGameState() == GAMESTATE_EXTENDED)
			{
				setGameState(GAMESTATE_ON);
			}
		}

		if (!isHotSeat())
		{
			for (int iI = 0; iI < NUM_PLAYEROPTION_TYPES; iI++)
			{
				GET_PLAYER(eNewValue).setOption((PlayerOptionTypes)iI, GET_PLAYER(eOldActivePlayer).isOption((PlayerOptionTypes)iI));
			}
		}

		if (GC.IsGraphicsInitialized())
		{
			GC.getMapINLINE().updateFog();
			GC.getMapINLINE().updateVisibility();
			GC.getMapINLINE().updateSymbols();
			GC.getMapINLINE().updateMinimapColor();

			updateUnitEnemyGlow();

			gDLL->getInterfaceIFace()->setInAdvancedStart(false); // Leoreth
			gDLL->getInterfaceIFace()->setWorldBuilder(false); // Leoreth
			gDLL->getInterfaceIFace()->setEndTurnMessage(false);

			gDLL->getInterfaceIFace()->clearSelectedCities();
			gDLL->getInterfaceIFace()->clearSelectionList();

			gDLL->getInterfaceIFace()->setDirty(PercentButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);

			gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(BlockadedPlots_DIRTY_BIT, true);
		}

		CvEventReporter::getInstance().playerSwitch(eOldActivePlayer, eNewValue);
	}
}

void CvGame::updateUnitEnemyGlow()
{
	//update unit enemy glow
	for(int i=0;i<MAX_PLAYERS;i++)
	{
		PlayerTypes playerType = (PlayerTypes) i;
		int iLoop;
		for(CvUnit *pLoopUnit = GET_PLAYER(playerType).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER(playerType).nextUnit(&iLoop))
		{
			//update glow
			gDLL->getEntityIFace()->updateEnemyGlow(pLoopUnit->getUnitEntity());
		}
	}
}

HandicapTypes CvGame::getHandicapType() const
{
	return m_eHandicap;
}

void CvGame::setHandicapType(HandicapTypes eHandicap)
{
	m_eHandicap = eHandicap;
}

PlayerTypes CvGame::getPausePlayer() const
{
	return m_ePausePlayer;
}


bool CvGame::isPaused() const
{
	return (getPausePlayer() != NO_PLAYER);
}


void CvGame::setPausePlayer(PlayerTypes eNewValue)
{
	m_ePausePlayer = eNewValue;
}


UnitTypes CvGame::getBestLandUnit() const
{
	return m_eBestLandUnit;
}


int CvGame::getBestLandUnitCombat() const
{
	if (getBestLandUnit() == NO_UNIT)
	{
		return 1;
	}

	return std::max(1, GC.getUnitInfo(getBestLandUnit()).getCombat());
}


void CvGame::setBestLandUnit(UnitTypes eNewValue)
{
	if (getBestLandUnit() != eNewValue)
	{
		m_eBestLandUnit = eNewValue;

		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
	}
}


TeamTypes CvGame::getWinner() const
{
	return m_eWinner;
}


VictoryTypes CvGame::getVictory() const
{
	return m_eVictory;
}


void CvGame::setWinner(TeamTypes eNewWinner, VictoryTypes eNewVictory)
{
	CvWString szBuffer;

	if ((getWinner() != eNewWinner) || (getVictory() != eNewVictory))
	{
		m_eWinner = eNewWinner;
		m_eVictory = eNewVictory;

		if (getVictory() != NO_VICTORY)
		{
			if (getWinner() != NO_TEAM)
			{
				//Rhye - start
				//szBuffer = gDLL->getText("TXT_KEY_GAME_WON", GET_TEAM(getWinner()).getName().GetCString(), GC.getVictoryInfo(getVictory()).getTextKeyWide());
				szBuffer = gDLL->getText("TXT_KEY_GAME_WON", GET_PLAYER((PlayerTypes)getWinner()).getCivilizationShortDescription(), GC.getVictoryInfo(getVictory()).getTextKeyWide());
				//Rhye - end
				addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, GET_TEAM(getWinner()).getLeaderID(), szBuffer, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
			}

			if ((getAIAutoPlay() > 0) || gDLL->GetAutorun())
			{
				setGameState(GAMESTATE_EXTENDED);
			}
			else
			{
				setGameState(GAMESTATE_OVER);
			}
		}

		gDLL->getInterfaceIFace()->setDirty(Center_DIRTY_BIT, true);
		CvEventReporter::getInstance().victory(eNewWinner, eNewVictory);
		//gDLL->getInterfaceIFace()->setDirty(Soundtrack_DIRTY_BIT, true);
	}
}


GameStateTypes CvGame::getGameState() const
{
	return m_eGameState;
}


void CvGame::setGameState(GameStateTypes eNewValue)
{
	CvPopupInfo* pInfo;
	int iI;

	if (getGameState() != eNewValue)
	{
		m_eGameState = eNewValue;

		if (eNewValue == GAMESTATE_OVER)
		{
			CvEventReporter::getInstance().gameEnd();

// BUG - AutoSave - start
			gDLL->getPythonIFace()->callFunction(PYBugModule, "gameEndSave");
// BUG - AutoSave - end

			showEndGameSequence();

			for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isHuman())
				{
					// One more turn?
					pInfo = new CvPopupInfo(BUTTONPOPUP_EXTENDED_GAME);
					if (NULL != pInfo)
					{
						GET_PLAYER((PlayerTypes)iI).addPopup(pInfo);
					}
				}
			}
		}

		gDLL->getInterfaceIFace()->setDirty(Cursor_DIRTY_BIT, true);
	}
}


GameSpeedTypes CvGame::getGameSpeedType() const
{
	return GC.getInitCore().getGameSpeed();
}


EraTypes CvGame::getStartEra() const
{
	return GC.getInitCore().getEra();
}


CalendarTypes CvGame::getCalendar() const
{
	return GC.getInitCore().getCalendar();
}


PlayerTypes CvGame::getRankPlayer(int iRank) const
{
	FAssertMsg(iRank >= 0, "iRank is expected to be non-negative (invalid Rank)");
	FAssertMsg(iRank < MAX_PLAYERS, "iRank is expected to be within maximum bounds (invalid Rank)");
	return (PlayerTypes)m_aiRankPlayer[iRank];
}


void CvGame::setRankPlayer(int iRank, PlayerTypes ePlayer)
{
	FAssertMsg(iRank >= 0, "iRank is expected to be non-negative (invalid Rank)");
	FAssertMsg(iRank < MAX_PLAYERS, "iRank is expected to be within maximum bounds (invalid Rank)");

	if (getRankPlayer(iRank) != ePlayer)
	{
		m_aiRankPlayer[iRank] = ePlayer;

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


int CvGame::getPlayerRank(PlayerTypes ePlayer) const
{
	FAssertMsg(ePlayer >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(ePlayer < MAX_PLAYERS, "ePlayer is expected to be within maximum bounds (invalid Index)");
	return m_aiPlayerRank[ePlayer];
}


void CvGame::setPlayerRank(PlayerTypes ePlayer, int iRank)
{
	FAssertMsg(ePlayer >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(ePlayer < MAX_PLAYERS, "ePlayer is expected to be within maximum bounds (invalid Index)");
	// Sanguo Mod Performance start, added by poyuzhe 07.26.09
	if (iRank != m_aiPlayerRank[ePlayer])
	{
		for (int iI = 0; iI < GC.getMAX_PLAYERS(); iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				GET_PLAYER(ePlayer).AI_invalidateAttitudeCache((PlayerTypes)iI);
				GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(ePlayer);
			}
		}
	}
	// Sanguo Mod Performance, end
	m_aiPlayerRank[ePlayer] = iRank;
	FAssert(getPlayerRank(ePlayer) >= 0);
}


int CvGame::getPlayerScore(PlayerTypes ePlayer)	const
{
	FAssertMsg(ePlayer >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(ePlayer < MAX_PLAYERS, "ePlayer is expected to be within maximum bounds (invalid Index)");
	return m_aiPlayerScore[ePlayer];
}


void CvGame::setPlayerScore(PlayerTypes ePlayer, int iScore)
{
	FAssertMsg(ePlayer >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(ePlayer < MAX_PLAYERS, "ePlayer is expected to be within maximum bounds (invalid Index)");

	if (getPlayerScore(ePlayer) != iScore)
	{
		m_aiPlayerScore[ePlayer] = iScore;
		FAssert(getPlayerScore(ePlayer) >= 0);

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


TeamTypes CvGame::getRankTeam(int iRank) const
{
	FAssertMsg(iRank >= 0, "iRank is expected to be non-negative (invalid Rank)");
	FAssertMsg(iRank < MAX_TEAMS, "iRank is expected to be within maximum bounds (invalid Index)");
	return (TeamTypes)m_aiRankTeam[iRank];
}


void CvGame::setRankTeam(int iRank, TeamTypes eTeam)
{
	FAssertMsg(iRank >= 0, "iRank is expected to be non-negative (invalid Rank)");
	FAssertMsg(iRank < MAX_TEAMS, "iRank is expected to be within maximum bounds (invalid Index)");

	if (getRankTeam(iRank) != eTeam)
	{
		m_aiRankTeam[iRank] = eTeam;

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


int CvGame::getTeamRank(TeamTypes eTeam) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");
	return m_aiTeamRank[eTeam];
}


void CvGame::setTeamRank(TeamTypes eTeam, int iRank)
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");
	m_aiTeamRank[eTeam] = iRank;
	FAssert(getTeamRank(eTeam) >= 0);
}


int CvGame::getTeamScore(TeamTypes eTeam) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");
	return m_aiTeamScore[eTeam];
}


void CvGame::setTeamScore(TeamTypes eTeam, int iScore)
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");
	m_aiTeamScore[eTeam] = iScore;
	FAssert(getTeamScore(eTeam) >= 0);
}


bool CvGame::isOption(GameOptionTypes eIndex) const
{
	return GC.getInitCore().getOption(eIndex);
}


void CvGame::setOption(GameOptionTypes eIndex, bool bEnabled)
{
	GC.getInitCore().setOption(eIndex, bEnabled);
}


bool CvGame::isMPOption(MultiplayerOptionTypes eIndex) const
{
	return GC.getInitCore().getMPOption(eIndex);
}


void CvGame::setMPOption(MultiplayerOptionTypes eIndex, bool bEnabled)
{
	GC.getInitCore().setMPOption(eIndex, bEnabled);
}


bool CvGame::isForcedControl(ForceControlTypes eIndex) const
{
	return GC.getInitCore().getForceControl(eIndex);
}


void CvGame::setForceControl(ForceControlTypes eIndex, bool bEnabled)
{
	GC.getInitCore().setForceControl(eIndex, bEnabled);
}


int CvGame::getUnitCreatedCount(UnitTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiUnitCreatedCount[eIndex];
}


void CvGame::incrementUnitCreatedCount(UnitTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiUnitCreatedCount[eIndex]++;
}


int CvGame::getUnitClassCreatedCount(UnitClassTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiUnitClassCreatedCount[eIndex];
}


bool CvGame::isUnitClassMaxedOut(UnitClassTypes eIndex, int iExtra)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isWorldUnitClass(eIndex))
	{
		return false;
	}

	FAssertMsg(getUnitClassCreatedCount(eIndex) <= GC.getUnitClassInfo(eIndex).getMaxGlobalInstances(), "Index is expected to be within maximum bounds (invalid Index)");

	return ((getUnitClassCreatedCount(eIndex) + iExtra) >= GC.getUnitClassInfo(eIndex).getMaxGlobalInstances());
}


void CvGame::incrementUnitClassCreatedCount(UnitClassTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiUnitClassCreatedCount[eIndex]++;
}


int CvGame::getBuildingClassCreatedCount(BuildingClassTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBuildingClassCreatedCount[eIndex];
}


bool CvGame::isBuildingClassMaxedOut(BuildingClassTypes eIndex, int iExtra)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isWorldWonderClass(eIndex))
	{
		return false;
	}

	FAssertMsg(getBuildingClassCreatedCount(eIndex) <= GC.getBuildingClassInfo(eIndex).getMaxGlobalInstances(), "Index is expected to be within maximum bounds (invalid Index)");

	return ((getBuildingClassCreatedCount(eIndex) + iExtra) >= GC.getBuildingClassInfo(eIndex).getMaxGlobalInstances());
}


void CvGame::incrementBuildingClassCreatedCount(BuildingClassTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiBuildingClassCreatedCount[eIndex]++;
}


int CvGame::getProjectCreatedCount(ProjectTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiProjectCreatedCount[eIndex];
}


bool CvGame::isProjectMaxedOut(ProjectTypes eIndex, int iExtra)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isWorldProject(eIndex))
	{
		return false;
	}

	FAssertMsg(getProjectCreatedCount(eIndex) <= GC.getProjectInfo(eIndex).getMaxGlobalInstances(), "Index is expected to be within maximum bounds (invalid Index)");

	return ((getProjectCreatedCount(eIndex) + iExtra) >= GC.getProjectInfo(eIndex).getMaxGlobalInstances());
}


void CvGame::incrementProjectCreatedCount(ProjectTypes eIndex, int iExtra)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiProjectCreatedCount[eIndex] += iExtra;
}


int CvGame::getForceCivicCount(CivicTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiForceCivicCount[eIndex];
}


bool CvGame::isForceCivic(CivicTypes eIndex) const
{
	return (getForceCivicCount(eIndex) > 0);
}


bool CvGame::isForceCivicOption(CivicOptionTypes eCivicOption) const
{
	int iI;

	for (iI = 0; iI < GC.getNumCivicInfos(); iI++)
	{
		if (GC.getCivicInfo((CivicTypes)iI).getCivicOptionType() == eCivicOption)
		{
			if (isForceCivic((CivicTypes)iI))
			{
				return true;
			}
		}
	}

	return false;
}


void CvGame::changeForceCivicCount(CivicTypes eIndex, int iChange)
{
	bool bOldForceCivic;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		bOldForceCivic = isForceCivic(eIndex);

		m_paiForceCivicCount[eIndex] += iChange;
		FAssert(getForceCivicCount(eIndex) >= 0);

		if (bOldForceCivic != isForceCivic(eIndex))
		{
			verifyCivics();
		}
	}
}


PlayerVoteTypes CvGame::getVoteOutcome(VoteTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumVoteInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiVoteOutcome[eIndex];
}


bool CvGame::isVotePassed(VoteTypes eIndex) const
{
	PlayerVoteTypes ePlayerVote = getVoteOutcome(eIndex);

	if (isTeamVote(eIndex))
	{
		return (ePlayerVote >= 0 && ePlayerVote < MAX_CIV_TEAMS);
	}
	else
	{
		return (ePlayerVote == PLAYER_VOTE_YES);
	}
}


void CvGame::setVoteOutcome(const VoteTriggeredData& kData, PlayerVoteTypes eNewValue)
{
	bool bOldPassed;

	VoteTypes eIndex = kData.kVoteOption.eVote;
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumVoteInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (getVoteOutcome(eIndex) != eNewValue)
	{
		bOldPassed = isVotePassed(eIndex);

		m_paiVoteOutcome[eIndex] = eNewValue;

		if (bOldPassed != isVotePassed(eIndex))
		{
			processVote(kData, ((isVotePassed(eIndex)) ? 1 : -1));
		}
	}

	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kPlayer.isAlive())
		{
			kPlayer.setVote(kData.getID(), NO_PLAYER_VOTE);
		}
	}
}


int CvGame::getReligionGameTurnFounded(ReligionTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiReligionGameTurnFounded[eIndex];
}


void CvGame::setReligionGameTurnFounded(ReligionTypes eReligion, int iGameTurn)
{
	m_paiReligionGameTurnFounded[eReligion] = iGameTurn;
}


bool CvGame::isReligionFounded(ReligionTypes eIndex)
{
	return (getReligionGameTurnFounded(eIndex) != -1);
}


void CvGame::makeReligionFounded(ReligionTypes eIndex, PlayerTypes ePlayer)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isReligionFounded(eIndex))
	{
		FAssertMsg(getGameTurn() != -1, "getGameTurn() is not expected to be equal with -1");
		setReligionGameTurnFounded(eIndex, getGameTurn());

		CvEventReporter::getInstance().religionFounded(eIndex, ePlayer);

		// Sanguo Mod Performance start, added by poyuzhe 07.26.09
		for (int iI = 0; iI < GC.getMAX_PLAYERS(); iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getStateReligion() == eIndex)
			{
				GET_PLAYER(ePlayer).AI_invalidateAttitudeCache((PlayerTypes)iI);
				GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(ePlayer);
			}
		}
		// Sanguo Mod Performance, end
	}
}

bool CvGame::isReligionSlotTaken(ReligionTypes eReligion) const
{
	FAssertMsg(eReligion >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eReligion < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_abReligionSlotTaken[eReligion];
}

void CvGame::setReligionSlotTaken(ReligionTypes eReligion, bool bTaken)
{
	FAssertMsg(eReligion >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eReligion < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_abReligionSlotTaken[eReligion] = bTaken;
}


int CvGame::getCorporationGameTurnFounded(CorporationTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiCorporationGameTurnFounded[eIndex];
}


bool CvGame::isCorporationFounded(CorporationTypes eIndex)
{
	//return true; //Leoreth: corporations don't get founded anymore
	return (getCorporationGameTurnFounded(eIndex) != -1);
}


void CvGame::makeCorporationFounded(CorporationTypes eIndex, PlayerTypes ePlayer)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isCorporationFounded(eIndex))
	{
		FAssertMsg(getGameTurn() != -1, "getGameTurn() is not expected to be equal with -1");
		m_paiCorporationGameTurnFounded[eIndex] = getGameTurn();

		CvEventReporter::getInstance().corporationFounded(eIndex, ePlayer);
	}
}

bool CvGame::isVictoryValid(VictoryTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumVictoryInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return GC.getInitCore().getVictory(eIndex);
}

void CvGame::setVictoryValid(VictoryTypes eIndex, bool bValid)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumVictoryInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	GC.getInitCore().setVictory(eIndex, bValid);
}


bool CvGame::isSpecialUnitValid(SpecialUnitTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialUnitInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_pabSpecialUnitValid[eIndex];
}


void CvGame::makeSpecialUnitValid(SpecialUnitTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialUnitInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_pabSpecialUnitValid[eIndex] = true;
}


bool CvGame::isSpecialBuildingValid(SpecialBuildingTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_pabSpecialBuildingValid[eIndex];
}


void CvGame::makeSpecialBuildingValid(SpecialBuildingTypes eIndex, bool bAnnounce)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!m_pabSpecialBuildingValid[eIndex])
	{
		m_pabSpecialBuildingValid[eIndex] = true;


		if (bAnnounce)
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_SPECIAL_BUILDING_VALID", GC.getSpecialBuildingInfo(eIndex).getTextKeyWide());

			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PROJECT_COMPLETED", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
				}
			}
		}
	}
}


bool CvGame::isNukesValid() const
{
	return m_bNukesValid;
}


void CvGame::makeNukesValid(bool bValid)
{
	m_bNukesValid = bValid;
}

bool CvGame::isInAdvancedStart() const
{
	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
	{
		if ((GET_PLAYER((PlayerTypes)iPlayer).getAdvancedStartPoints() >= 0) && GET_PLAYER((PlayerTypes)iPlayer).isHuman())
		{
			return true;
		}
	}

	return false;
}

void CvGame::setVoteChosen(int iSelection, int iVoteId)
{
	VoteSelectionData* pVoteSelectionData = getVoteSelection(iVoteId);
	if (NULL != pVoteSelectionData)
	{
		addVoteTriggered(*pVoteSelectionData, iSelection);
	}

	deleteVoteSelection(iVoteId);
}


CvCity* CvGame::getHolyCity(ReligionTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return getCity(m_paHolyCity[eIndex]);
}


void CvGame::setHolyCity(ReligionTypes eIndex, CvCity* pNewValue, bool bAnnounce)
{
	CvWString szBuffer;
	CvCity* pOldValue;
	CvCity* pHolyCity;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	pOldValue = getHolyCity(eIndex);

	if (pOldValue != pNewValue)
	{
		  // religion visibility now part of espionage
		//updateCitySight(false, true);

		if (pNewValue != NULL)
		{
			m_paHolyCity[eIndex] = pNewValue->getIDInfo();
		}
		else
		{
			m_paHolyCity[eIndex].reset();
		}

		// religion visibility now part of espionage
		//updateCitySight(true, true);

		if (pOldValue != NULL)
		{
			pOldValue->changeReligionInfluence(eIndex, -(GC.getDefineINT("HOLY_CITY_INFLUENCE")));

			pOldValue->updateReligionCommerce();

			pOldValue->setInfoDirty(true);
		}

		if (getHolyCity(eIndex) != NULL)
		{
			pHolyCity = getHolyCity(eIndex);

			//pHolyCity->setHasReligion(eIndex, true, bAnnounce, true);
			pHolyCity->spreadReligion(eIndex, false);
			pHolyCity->changeReligionInfluence(eIndex, GC.getDefineINT("HOLY_CITY_INFLUENCE"));

			pHolyCity->updateReligionCommerce();

			pHolyCity->setInfoDirty(true);

			if (bAnnounce)
			{
				if (isFinalInitialized() && !(gDLL->GetWorldBuilderMode()))
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_REL_FOUNDED", GC.getReligionInfo(eIndex).getTextKeyWide(), pHolyCity->getNameKey());
					addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, pHolyCity->getOwnerINLINE(), szBuffer, pHolyCity->getX_INLINE(), pHolyCity->getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

					for (iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							if (pHolyCity->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_REL_FOUNDED", GC.getReligionInfo(eIndex).getTextKeyWide(), pHolyCity->getNameKey());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getDefineINT("EVENT_MESSAGE_TIME_LONG"), szBuffer, GC.getReligionInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getReligionInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), pHolyCity->getX_INLINE(), pHolyCity->getY_INLINE());
							}
							else
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_REL_FOUNDED_UNKNOWN", GC.getReligionInfo(eIndex).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getDefineINT("EVENT_MESSAGE_TIME_LONG"), szBuffer, GC.getReligionInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getReligionInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
							}
						}
					}
				}
			}
		}

		AI_makeAssignWorkDirty();
	}
}


CvCity* CvGame::getHeadquarters(CorporationTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return getCity(m_paHeadquarters[eIndex]);
}


void CvGame::setHeadquarters(CorporationTypes eIndex, CvCity* pNewValue, bool bAnnounce)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	CvCity* pOldValue = getHeadquarters(eIndex);

	if (pOldValue != pNewValue)
	{
		if (pNewValue != NULL)
		{
			m_paHeadquarters[eIndex] = pNewValue->getIDInfo();
		}
		else
		{
			m_paHeadquarters[eIndex].reset();
		}

		if (pOldValue != NULL)
		{
			pOldValue->updateCorporation();

			pOldValue->setInfoDirty(true);
		}

		CvCity* pHeadquarters = getHeadquarters(eIndex);

		if (NULL != pHeadquarters)
		{
			pHeadquarters->setHasCorporation(eIndex, true, bAnnounce);
			pHeadquarters->updateCorporation();
			pHeadquarters->setInfoDirty(true);

			if (bAnnounce)
			{
				if (isFinalInitialized() && !(gDLL->GetWorldBuilderMode()))
				{
					CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_FOUNDED", GC.getCorporationInfo(eIndex).getTextKeyWide(), pHeadquarters->getNameKey());
					addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, pHeadquarters->getOwnerINLINE(), szBuffer, pHeadquarters->getX_INLINE(), pHeadquarters->getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

					for (int iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							if (pHeadquarters->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
							{
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getDefineINT("EVENT_MESSAGE_TIME_LONG"), szBuffer, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), pHeadquarters->getX_INLINE(), pHeadquarters->getY_INLINE());
							}
							else
							{
								CvWString szBuffer2 = gDLL->getText("TXT_KEY_MISC_CORPORATION_FOUNDED_UNKNOWN", GC.getCorporationInfo(eIndex).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getDefineINT("EVENT_MESSAGE_TIME_LONG"), szBuffer2, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
							}
						}
					}
				}
			}
		}

		AI_makeAssignWorkDirty();
	}
}


PlayerVoteTypes CvGame::getPlayerVote(PlayerTypes eOwnerIndex, int iVoteId) const
{
	FAssert(eOwnerIndex >= 0);
	FAssert(eOwnerIndex < MAX_CIV_PLAYERS);
	FAssert(NULL != getVoteTriggered(iVoteId));

	return GET_PLAYER(eOwnerIndex).getVote(iVoteId);
}


void CvGame::setPlayerVote(PlayerTypes eOwnerIndex, int iVoteId, PlayerVoteTypes eNewValue)
{
	FAssert(eOwnerIndex >= 0);
	FAssert(eOwnerIndex < MAX_CIV_PLAYERS);
	FAssert(NULL != getVoteTriggered(iVoteId));

	GET_PLAYER(eOwnerIndex).setVote(iVoteId, eNewValue);
}


void CvGame::castVote(PlayerTypes eOwnerIndex, int iVoteId, PlayerVoteTypes ePlayerVote)
{
	VoteTriggeredData* pTriggeredData = getVoteTriggered(iVoteId);
	if (NULL != pTriggeredData)
	{
		CvVoteInfo& kVote = GC.getVoteInfo(pTriggeredData->kVoteOption.eVote);
		if (kVote.isAssignCity())
		{
			FAssert(pTriggeredData->kVoteOption.ePlayer != NO_PLAYER);
			CvPlayer& kCityPlayer = GET_PLAYER(pTriggeredData->kVoteOption.ePlayer);

			if (GET_PLAYER(eOwnerIndex).getTeam() != kCityPlayer.getTeam())
			{
				switch (ePlayerVote)
				{
				case PLAYER_VOTE_YES:
					kCityPlayer.AI_changeMemoryCount(eOwnerIndex, MEMORY_VOTED_AGAINST_US, 1);
					break;
				case PLAYER_VOTE_NO:
					kCityPlayer.AI_changeMemoryCount(eOwnerIndex, MEMORY_VOTED_FOR_US, 1);
					break;
				default:
					break;
				}
			}
		}
		else if (isTeamVote(pTriggeredData->kVoteOption.eVote))
		{
			if ((PlayerVoteTypes)GET_PLAYER(eOwnerIndex).getTeam() != ePlayerVote)
			{
				for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
				{
					CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
					if (kLoopPlayer.isAlive())
					{
						if (kLoopPlayer.getTeam() != GET_PLAYER(eOwnerIndex).getTeam() && kLoopPlayer.getTeam() == (TeamTypes)ePlayerVote)
						{
							kLoopPlayer.AI_changeMemoryCount(eOwnerIndex, MEMORY_VOTED_FOR_US, 1);
						}
					}
				}
			}
		}

		setPlayerVote(eOwnerIndex, iVoteId, ePlayerVote);
	}
}


std::string CvGame::getScriptData() const
{
	return m_szScriptData;
}


void CvGame::setScriptData(std::string szNewValue)
{
	m_szScriptData = szNewValue;
}

const CvWString & CvGame::getName()
{
	return GC.getInitCore().getGameName();
}


void CvGame::setName(const TCHAR* szName)
{
	GC.getInitCore().setGameName(szName);
}


bool CvGame::isDestroyedCityName(CvWString& szName) const
{
	std::vector<CvWString>::const_iterator it;

	for (it = m_aszDestroyedCities.begin(); it != m_aszDestroyedCities.end(); it++)
	{
		if (*it == szName)
		{
			return true;
		}
	}

	return false;
}

void CvGame::addDestroyedCityName(const CvWString& szName)
{
	m_aszDestroyedCities.push_back(szName);
}

bool CvGame::isGreatPersonBorn(CvWString& szName) const
{
	std::vector<CvWString>::const_iterator it;

	for (it = m_aszGreatPeopleBorn.begin(); it != m_aszGreatPeopleBorn.end(); it++)
	{
		if (*it == szName)
		{
			return true;
		}
	}

	return false;
}

void CvGame::addGreatPersonBornName(const CvWString& szName)
{
	m_aszGreatPeopleBorn.push_back(szName);
}


// Protected Functions...

void CvGame::doTurn()
{
	PROFILE_BEGIN("CvGame::doTurn()");

	int aiShuffle[MAX_PLAYERS];
	int iLoopPlayer;
	int iI;

	//Rhye
	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		GET_PLAYER((PlayerTypes)iI).m_bTurnPlayed = false;
	}

	// END OF TURN
	CvEventReporter::getInstance().beginGameTurn( getGameTurn() );

	doUpdateCacheOnTurn();

	updateScore();

	doDeals();

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			GET_TEAM((TeamTypes)iI).doTurn();
		}
	}

	GC.getMapINLINE().doTurn();

	//Rhye
	//createBarbarianCities();

	createBarbarianUnits();

	doGlobalWarming();

	//Rhye - comment this to stop religion founding
	//doHolyCity();

	//doHeadquarters();

	doDiploVote();

	gDLL->getInterfaceIFace()->setEndTurnMessage(false);
	gDLL->getInterfaceIFace()->setHasMovedUnit(false);

	if (getAIAutoPlay() > 0)
	{
		changeAIAutoPlay(-1);

		if (getAIAutoPlay() == 0)
		{
			reviveActivePlayer();
		}
	}

	CvEventReporter::getInstance().endGameTurn(getGameTurn());

	incrementGameTurn();
	incrementElapsedGameTurns();

	if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
	{
		shuffleArray(aiShuffle, MAX_PLAYERS, getSorenRand());

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			iLoopPlayer = aiShuffle[iI];

			if (GET_PLAYER((PlayerTypes)iLoopPlayer).isAlive())
			{
				GET_PLAYER((PlayerTypes)iLoopPlayer).setTurnActive(true);
			}
		}
	}
	else if (isSimultaneousTeamTurns())
	{
		for (iI = 0; iI < MAX_TEAMS; iI++)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iI);
			if (kTeam.isAlive())
			{
				kTeam.setTurnActive(true);
				FAssert(getNumGameTurnActive() == kTeam.getAliveCount());
			}

			break;
		}
	}
	else
	{
		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (isPbem() && GET_PLAYER((PlayerTypes)iI).isHuman())
				{
					if (iI == getActivePlayer())
					{
						// Nobody else left alive
						GC.getInitCore().setType(GAME_HOTSEAT_NEW);
						GET_PLAYER((PlayerTypes)iI).setTurnActive(true);
					}
					else if (!getPbemTurnSent())
					{
						gDLL->sendPbemTurn((PlayerTypes)iI);
					}
				}
				else
				{
					GET_PLAYER((PlayerTypes)iI).setTurnActive(true);
					FAssert(getNumGameTurnActive() == 1);
				}

				break;
			}
		}
	}

	testVictory();

	gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->DoTurn();

	PROFILE_END();

	stopProfilingDLL();

	// edead: disable autosave during autoplay
	if (GC.getDefineINT("NO_AUTOSAVE_DURING_AUTOPLAY") == 0 || (getGameTurn() > 0 && getAIAutoPlay() == 0))
	{
		gDLL->getEngineIFace()->AutoSave();
	}
	// edead: end
	//gDLL->getEngineIFace()->AutoSave();
}


void CvGame::doDeals()
{
	CvDeal* pLoopDeal;
	int iLoop;

	verifyDeals();

	for(pLoopDeal = firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = nextDeal(&iLoop))
	{
		pLoopDeal->doTurn();
	}
}


void CvGame::doGlobalWarming()
{
	int iGlobalWarmingDefense = 0;

// BUG - Global Warming Mod - start
#ifdef _MOD_GWARM
	int iTreeHuggerDefenseBonus = GC.getDefineINT("TREEHUGGER_DEFENSE_BONUS");
	bool abTreeHugger[MAX_PLAYERS];

	for (int iI = 0; iI < MAX_PLAYERS; iI++)//GWMod Loop to look for environmentalism witten by EmperorFool
	{
		abTreeHugger[iI] = false;
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			for (int iJ = 0; iJ < GC.getNumCivicOptionInfos(); iJ++)
			{
				CivicTypes eCivic = GET_PLAYER((PlayerTypes)iI).getCivics((CivicOptionTypes)iJ);
				if (GC.getCivicInfo(eCivic).getExtraHealth() != 0)
				{
					abTreeHugger[iI] = true;
					break;
				}
			}
		}
	}
#endif

	for (int i = 0; i < GC.getMapINLINE().numPlotsINLINE(); ++i)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(i);

#ifdef _MOD_GWARM
		if (pPlot->getFeatureType() != NO_FEATURE)
		{
			int iFeatureWarmingDefense = GC.getFeatureInfo(pPlot->getFeatureType()).getWarmingDefense();
			if (iFeatureWarmingDefense > 0)
			{
				PlayerTypes eCulturalOwner = pPlot->getOwner();
				if (eCulturalOwner != NO_PLAYER)
				{
					if (abTreeHugger[eCulturalOwner])
					{
						iGlobalWarmingDefense += (iFeatureWarmingDefense) * (iTreeHuggerDefenseBonus);
					}
					else
					{
						iGlobalWarmingDefense += iFeatureWarmingDefense;
					}
				}
				else
				{
					iGlobalWarmingDefense += iFeatureWarmingDefense;
				}
			}
		}
#else
		/*if (!pPlot->isWater())
		{
			if (pPlot->getFeatureType() != NO_FEATURE)
			{
				if (GC.getFeatureInfo(pPlot->getFeatureType()).getGrowthProbability() > 0) // hack, but we don't want to add new XML field in the patch just for this
				{
					++iGlobalWarmingDefense;
				}
			}
		}*/

		// Leoreth
		if (pPlot->getFeatureType() != NO_FEATURE)
		{
			iGlobalWarmingDefense += GC.getFeatureInfo(pPlot->getFeatureType()).getGlobalWarmingDefense();
		}
#endif
	}
	iGlobalWarmingDefense = iGlobalWarmingDefense * GC.getDefineINT("GLOBAL_WARMING_FOREST") / std::max(1, GC.getMapINLINE().getLandPlots());

	int iUnhealthWeight = GC.getDefineINT("GLOBAL_WARMING_UNHEALTH_WEIGHT");
#ifdef _MOD_GWARM
	int iBonusWeight = GC.getDefineINT("GLOBAL_WARMING_BONUS_WEIGHT");
	int iPowerWeight = GC.getDefineINT("GLOBAL_WARMING_POWER_WEIGHT");
#endif
	int iGlobalWarmingValue = 0;
	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
	{
		CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iPlayer);
		if (kPlayer.isAlive())
		{
			int iLoop;
			for (CvCity* pCity = kPlayer.firstCity(&iLoop); pCity != NULL; pCity = kPlayer.nextCity(&iLoop))
			{
#ifdef _MOD_GWARM
				iGlobalWarmingValue -= (pCity->totalBadBuildingHealth() * iUnhealthWeight) + (pCity->getBonusBadHealth() * iBonusWeight) + (pCity->getPowerBadHealth() * iPowerWeight); //GWMod Changed to be total building bad health and to include power and bonuses M.A.
#else
				//iGlobalWarmingValue -= pCity->getBuildingBadHealth() * iUnhealthWeight;
				iGlobalWarmingValue -= (pCity->getBuildingBadHealth() + pCity->getPowerBadHealth() + pCity->getCorporationUnhealth()) * iUnhealthWeight; // Leoreth
				//iGlobalWarmingValue += pCity->getYieldRate(YIELD_PRODUCTION) * 25;
#endif
				// Leoreth: account for plague, we do not want early global warming
				if (pCity->isHasRealBuilding(BUILDING_PLAGUE))
				{
					iGlobalWarmingValue += GC.getBuildingInfo(BUILDING_PLAGUE).getHealth() * iUnhealthWeight;
				}
			}
		}
	}
	iGlobalWarmingValue /= GC.getMapINLINE().numPlotsINLINE();

#ifdef _MOD_GWARM
#else
	//iGlobalWarmingValue += getNukesExploded() * GC.getDefineINT("GLOBAL_WARMING_NUKE_WEIGHT") / 100; // Leoreth: disabled
#endif

	//TerrainTypes eWarmingTerrain = ((TerrainTypes)(GC.getDefineINT("GLOBAL_WARMING_TERRAIN")));
#ifdef _MOD_GWARM
	TerrainTypes eFrozenTerrain = ((TerrainTypes)(GC.getDefineINT("FROZEN_TERRAIN")));
	TerrainTypes eColdTerrain = ((TerrainTypes)(GC.getDefineINT("COLD_TERRAIN")));
	TerrainTypes eTemperateTerrain = ((TerrainTypes)(GC.getDefineINT("TEMPERATE_TERRAIN")));
	TerrainTypes eDryTerrain = ((TerrainTypes)(GC.getDefineINT("DRY_TERRAIN")));
	TerrainTypes eBarrenTerrain = ((TerrainTypes)(GC.getDefineINT("BARREN_TERRAIN")));
	TerrainTypes eShallowsTerrain = ((TerrainTypes)(GC.getDefineINT("SHALLOW_WATER_TERRAIN")));

	FeatureTypes eColdFeature = ((FeatureTypes)(GC.getDefineINT("COLD_FEATURE")));
	FeatureTypes eTemperateFeature = ((FeatureTypes)(GC.getDefineINT("TEMPERATE_FEATURE")));
	FeatureTypes eWarmFeature = ((FeatureTypes)(GC.getDefineINT("WARM_FEATURE")));
	FeatureTypes eFalloutFeature = ((FeatureTypes)(GC.getDefineINT("NUKE_FEATURE")));
#endif

	CvEventReporter::getInstance().globalWarming(iGlobalWarmingValue, iGlobalWarmingDefense);

	int iGlobalWarmingEffect = iGlobalWarmingValue - iGlobalWarmingDefense;

	if (iGlobalWarmingEffect > 0)
	{
		for (int iI = 0; iI < iGlobalWarmingEffect; iI++)
		{
			if (true || getSorenRandNum(iGlobalWarmingValue + iGlobalWarmingDefense, "Global Warming") >= iGlobalWarmingDefense)
			{
#ifdef _MOD_GWARM
				CvPlot* pPlot = GC.getMapINLINE().syncRandPlot(RANDPLOT_NOT_CITY); // GWMod removed check for water tile M.A.
#else
				CvPlot* pPlot = GC.getMapINLINE().syncRandPlot(RANDPLOT_LAND | RANDPLOT_NOT_CITY);
#endif

				if (pPlot != NULL)
				{
					bool bChanged = false;

#ifdef _MOD_GWARM
					if (pPlot->getFeatureType() != NO_FEATURE)
					{
						if (pPlot->getFeatureType() != GC.getDefineINT("NUKE_FEATURE"))
						{
							// GWMod won't remove features if underlaying terrain can melt
							if (pPlot->getFeatureType() != eColdFeature)
							{
								if ((pPlot->calculateBestNatureYield(YIELD_FOOD, NO_TEAM) > 1) && (pPlot->getFeatureType() == eTemperateFeature))
								{
									pPlot->setFeatureType(eWarmFeature);
									bChanged = true;
								}
								else if (pPlot->getTerrainType() == eColdTerrain)
								{
									pPlot->setTerrainType(eTemperateTerrain);
									bChanged = true;
								}
								else if (pPlot->getTerrainType() == eFrozenTerrain)
								{
									pPlot->setTerrainType(eColdTerrain);
									bChanged = true;
								}
								else
								{
									pPlot->setFeatureType(NO_FEATURE);
									bChanged = true;
								}
							}
							else
							{
								pPlot->setFeatureType(NO_FEATURE);
								bChanged = true;
							}
						}
					}
					else if (!pPlot->isWater())  // GWMod added check for water tile M.A.
					{
						// GWMod stepped terrain changes M.A.
						if (pPlot->getTerrainType() == eBarrenTerrain)
						{
							if (isOption(GAMEOPTION_RISING_SEAS))
							{
								if (pPlot->isCoastalLand())
								{
									if (!pPlot->isHills() && !pPlot->isPeak())
									{
										pPlot->setTerrainType(eShallowsTerrain);
										bChanged = true;
									}
								}
							}
						}
						else if (pPlot->getTerrainType() == eDryTerrain)
						{
							pPlot->setTerrainType(eBarrenTerrain);
							bChanged = true;
						}
						else if (pPlot->getTerrainType() == eTemperateTerrain)
						{
							pPlot->setTerrainType(eDryTerrain);
							bChanged = true;
						}
						else if (pPlot->getTerrainType() == eColdTerrain)
						{
							pPlot->setTerrainType(eTemperateTerrain);
							bChanged = true;
						}
						else if (pPlot->getTerrainType() == eFrozenTerrain)
						{
							pPlot->setTerrainType(eColdTerrain);
							bChanged = true;
						}
					}
#else
					TerrainTypes eCurrentTerrain = pPlot->getTerrainType();
					TerrainTypes eWarmingTerrain = (TerrainTypes)GC.getTerrainInfo(eCurrentTerrain).getGlobalWarmingTerrainType();

					FeatureTypes eCurrentFeature = pPlot->getFeatureType();

					if (eCurrentFeature != NO_FEATURE)
					{
						if (eCurrentFeature != GC.getDefineINT("NUKE_FEATURE")) // should be nuke immune and also be part of elseif
						{
							pPlot->setFeatureType(NO_FEATURE);
							bChanged = true;
						}
					}
					else if (eWarmingTerrain != NO_TERRAIN && eCurrentTerrain != eWarmingTerrain)
					{
						//if (pPlot->calculateTotalBestNatureYield(NO_TEAM) > 1) // Leoreth
						{
							pPlot->setTerrainType(eWarmingTerrain);
							bChanged = true;
						}
					}
#endif

					if (bChanged)
					{
						CvEventReporter::getInstance().globalWarmingEffect(pPlot, bChanged, eCurrentTerrain, pPlot->getTerrainType(), eCurrentFeature);

						pPlot->setImprovementType(NO_IMPROVEMENT);

						CvCity* pCity = GC.getMapINLINE().findCity(pPlot->getX_INLINE(), pPlot->getY_INLINE());
						if (pCity != NULL)
						{
							if (pPlot->isVisible(pCity->getTeam(), false))
							{
								CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_GLOBAL_WARMING_NEAR_CITY", pCity->getNameKey());
								gDLL->getInterfaceIFace()->addMessage(pCity->getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_GLOBALWARMING", MESSAGE_TYPE_INFO, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pPlot->getX_INLINE(), pPlot->getY_INLINE(), true, true);
							}
						}
					}
				}
			}
		}
	}
	
#ifdef _MOD_GWARM
	//Nuclear Winter
	int iNuclearWinterValue = 0;
	iNuclearWinterValue += getNukesExploded() * GC.getDefineINT("GLOBAL_WARMING_NUKE_WEIGHT") / 100;

	for (int iI = 0; iI < iNuclearWinterValue; iI++)
	{
		if (getSorenRandNum(100, "Nuclear Fallout") + iGlobalWarmingDefense < GC.getDefineINT("NUCLEAR_WINTER_PROB"))
		{
			CvPlot* pPlot = GC.getMapINLINE().syncRandPlot(RANDPLOT_LAND | RANDPLOT_NOT_CITY);
			FeatureTypes eFeature = pPlot->getFeatureType();

			if (pPlot != NULL)
			{
				bool bChanged = false;
				if (pPlot->getFeatureType() != NO_FEATURE)
				{
					if (pPlot->getFeatureType() != GC.getDefineINT("NUKE_FEATURE"))
					{
						if (pPlot->getFeatureType() != eColdFeature)
						{
							pPlot->setFeatureType(NO_FEATURE);
							bChanged = true;
						}
					}
				}
				else
				{
					pPlot->setFeatureType(eFalloutFeature);
					bChanged = true;
				}
				if (getSorenRandNum(100, "Nuclear Winter") + iGlobalWarmingDefense < GC.getDefineINT("NUCLEAR_WINTER_PROB"))
				{
					if (pPlot->getTerrainType() == eColdTerrain)
					{
						pPlot->setTerrainType(eFrozenTerrain);
						bChanged = true;
					}
					if (pPlot->calculateTotalBestNatureYield(NO_TEAM) > 1)
					{
						pPlot->setTerrainType(eColdTerrain);
						bChanged = true;
					}
				}
				if (bChanged)
				{
					pPlot->setImprovementType(NO_IMPROVEMENT);

					CvCity* pCity = GC.getMapINLINE().findCity(pPlot->getX_INLINE(), pPlot->getY_INLINE());
					if (pCity != NULL)
					{
						if (pPlot->isVisible(pCity->getTeam(), false))
						{
							CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_NUCLEAR_WINTER_NEAR_CITY", pCity->getNameKey());
							gDLL->getInterfaceIFace()->addMessage(pCity->getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_GLOBALWARMING", MESSAGE_TYPE_INFO, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pPlot->getX_INLINE(), pPlot->getY_INLINE(), true, true);
						}
					}
				}
			}
		}
	}
#endif
// BUG - Global Warming Mod - end
}


void CvGame::doHolyCity()
{
	PlayerTypes eBestPlayer;
	TeamTypes eBestTeam;
	long lResult;
	int iValue;
	int iBestValue;
	int iI, iJ, iK;

	lResult = 0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doHolyCity", NULL, &lResult);
	if (lResult == 1)
	{
		return;
	}

	if (getElapsedGameTurns() < 5 && !isOption(GAMEOPTION_ADVANCED_START))
	{
		return;
	}

	int iRandOffset = getSorenRandNum(GC.getNumReligionInfos(), "Holy City religion offset");
	for (int iLoop = 0; iLoop < GC.getNumReligionInfos(); ++iLoop)
	{
		iI = ((iLoop + iRandOffset) % GC.getNumReligionInfos());

		if (!isReligionSlotTaken((ReligionTypes)iI))
		{
			iBestValue = MAX_INT;
			eBestTeam = NO_TEAM;

			for (iJ = 0; iJ < MAX_TEAMS; iJ++)
			{
				if (GET_TEAM((TeamTypes)iJ).isAlive())
				{
					if (GC.getReligionInfo((ReligionTypes)iI).getTechPrereq() != -1 && GET_TEAM((TeamTypes)iJ).isHasTech((TechTypes)(GC.getReligionInfo((ReligionTypes)iI).getTechPrereq())))
					{
						if (GET_TEAM((TeamTypes)iJ).getNumCities() > 0)
						{
							iValue = getSorenRandNum(10, "Found Religion (Team)");

							for (iK = 0; iK < GC.getNumReligionInfos(); iK++)
							{
								int iReligionCount = GET_TEAM((TeamTypes)iJ).getHasReligionCount((ReligionTypes)iK);

								if (iReligionCount > 0)
								{
									iValue += iReligionCount * 20;
								}
							}

							if (iValue < iBestValue)
							{
								iBestValue = iValue;
								eBestTeam = ((TeamTypes)iJ);
							}
						}
					}
				}
			}

			if (eBestTeam != NO_TEAM)
			{
				iBestValue = MAX_INT;
				eBestPlayer = NO_PLAYER;

				for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
				{
					if (GET_PLAYER((PlayerTypes)iJ).isAlive())
					{
						if (GET_PLAYER((PlayerTypes)iJ).getTeam() == eBestTeam)
						{
							if (GET_PLAYER((PlayerTypes)iJ).getNumCities() > 0)
							{
								iValue = getSorenRandNum(10, "Found Religion (Player)");

								if (!(GET_PLAYER((PlayerTypes)iJ).isHuman()))
								{
									iValue += 10;
								}

								for (iK = 0; iK < GC.getNumReligionInfos(); iK++)
								{
									int iReligionCount = GET_PLAYER((PlayerTypes)iJ).getHasReligionCount((ReligionTypes)iK);

									if (iReligionCount > 0)
									{
										iValue += iReligionCount * 20;
									}
								}

								if (iValue < iBestValue)
								{
									iBestValue = iValue;
									eBestPlayer = ((PlayerTypes)iJ);
								}
							}
						}
					}
				}

				if (eBestPlayer != NO_PLAYER)
				{
					ReligionTypes eReligion = (ReligionTypes)iI;

					if (isOption(GAMEOPTION_PICK_RELIGION))
					{
						eReligion = GET_PLAYER(eBestPlayer).AI_chooseReligion();
					}

					if (NO_RELIGION != eReligion)
					{
						GET_PLAYER(eBestPlayer).foundReligion(eReligion, (ReligionTypes)iI, false);
					}
				}
			}
		}
	}
}


void CvGame::doHeadquarters()
{
	long lResult = 0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doHeadquarters", NULL, &lResult);
	if (lResult == 1)
	{
		return;
	}

	if (getElapsedGameTurns() < 5)
	{
		return;
	}

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		CvCorporationInfo& kCorporation = GC.getCorporationInfo((CorporationTypes)iI);
		if (!isCorporationFounded((CorporationTypes)iI))
		{
			int iBestValue = MAX_INT;
			TeamTypes eBestTeam = NO_TEAM;

			for (int iJ = 0; iJ < MAX_TEAMS; iJ++)
			{
				CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iJ);
				if (kLoopTeam.isAlive())
				{
					if (NO_TECH != kCorporation.getTechPrereq() && kLoopTeam.isHasTech((TechTypes)(kCorporation.getTechPrereq())))
					{
						if (kLoopTeam.getNumCities() > 0)
						{
							bool bHasBonus = false;
							for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
							{
								if (NO_BONUS != kCorporation.getPrereqBonus(i) && kLoopTeam.hasBonus((BonusTypes)kCorporation.getPrereqBonus(i)))
								{
									bHasBonus = true;
									break;
								}
							}

							if (bHasBonus)
							{
								int iValue = getSorenRandNum(10, "Found Corporation (Team)");

								for (int iK = 0; iK < GC.getNumCorporationInfos(); iK++)
								{
									int iCorporationCount = GET_PLAYER((PlayerTypes)iJ).getHasCorporationCount((CorporationTypes)iK);

									if (iCorporationCount > 0)
									{
										iValue += iCorporationCount * 20;
									}
								}

								if (iValue < iBestValue)
								{
									iBestValue = iValue;
									eBestTeam = ((TeamTypes)iJ);
								}
							}
						}
					}
				}
			}

			if (eBestTeam != NO_TEAM)
			{
				iBestValue = MAX_INT;
				PlayerTypes eBestPlayer = NO_PLAYER;

				for (int iJ = 0; iJ < MAX_PLAYERS; iJ++)
				{
					CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iJ);
					if (kLoopPlayer.isAlive())
					{
						if (kLoopPlayer.getTeam() == eBestTeam)
						{
							if (kLoopPlayer.getNumCities() > 0)
							{
								bool bHasBonus = false;
								for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
								{
									if (NO_BONUS != kCorporation.getPrereqBonus(i) && kLoopPlayer.hasBonus((BonusTypes)kCorporation.getPrereqBonus(i)))
									{
										bHasBonus = true;
										break;
									}
								}

								if (bHasBonus)
								{
									int iValue = getSorenRandNum(10, "Found Religion (Player)");

									if (!kLoopPlayer.isHuman())
									{
										iValue += 10;
									}

									for (int iK = 0; iK < GC.getNumCorporationInfos(); iK++)
									{
										int iCorporationCount = GET_PLAYER((PlayerTypes)iJ).getHasCorporationCount((CorporationTypes)iK);

										if (iCorporationCount > 0)
										{
											iValue += iCorporationCount * 20;
										}
									}

									if (iValue < iBestValue)
									{
										iBestValue = iValue;
										eBestPlayer = ((PlayerTypes)iJ);
									}
								}
							}
						}
					}
				}

				if (eBestPlayer != NO_PLAYER)
				{
					GET_PLAYER(eBestPlayer).foundCorporation((CorporationTypes)iI);
				}
			}
		}
	}
}


void CvGame::doDiploVote()
{
	doVoteResults();

	doVoteSelection();
}


void CvGame::createBarbarianCities()
{
	CvPlot* pLoopPlot;
	CvPlot* pBestPlot;
//	long lResult; //Rhye (Kael)
	int iTargetCities;
	int iValue;
	int iBestValue;
	int iI;

	if (getMaxCityElimination() > 0)
	{
		return;
	}

	if (isOption(GAMEOPTION_NO_BARBARIANS))
	{
		return;
	}

	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	lResult = 0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "createBarbarianCities", NULL, &lResult);
//	if (lResult == 1)
//	{
//		return;
//	}
//Speed: End Modify
	//Rhye - end

	if (GC.getEraInfo(getCurrentEra()).isNoBarbCities())
	{
		return;
	}

	if (GC.getHandicapInfo(getHandicapType()).getUnownedTilesPerBarbarianCity() <= 0)
	{
		return;
	}

	if (getNumCivCities() < (countCivPlayersAlive() * 2))
	{
		return;
	}

	if (getElapsedGameTurns() < (((GC.getHandicapInfo(getHandicapType()).getBarbarianCityCreationTurnsElapsed() * GC.getGameSpeedInfo(getGameSpeedType()).getBarbPercent()) / 100) / std::max(getStartEra() + 1, 1)))
	{
		return;
	}

	if (getSorenRandNum(100, "Barb City Creation") >= GC.getHandicapInfo(getHandicapType()).getBarbarianCityCreationProb())
	{
		return;
	}

	iBestValue = 0;
	pBestPlot = NULL;

	int iTargetCitiesMultiplier = 100;
	{
		int iTargetBarbCities = (getNumCivCities() * 5 * GC.getHandicapInfo(getHandicapType()).getBarbarianCityCreationProb()) / 100;
		int iBarbCities = GET_PLAYER(BARBARIAN_PLAYER).getNumCities();
		if (iBarbCities < iTargetBarbCities)
		{
			iTargetCitiesMultiplier += (300 * (iTargetBarbCities - iBarbCities)) / iTargetBarbCities;
		}

		if (isOption(GAMEOPTION_RAGING_BARBARIANS))
		{
			iTargetCitiesMultiplier *= 3;
			iTargetCitiesMultiplier /= 2;
		}
	}


	for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (!(pLoopPlot->isWater()))
		{
			if (!(pLoopPlot->isVisibleToCivTeam()))
			{
				iTargetCities = pLoopPlot->area()->getNumUnownedTiles();

				if (pLoopPlot->area()->getNumCities() == pLoopPlot->area()->getCitiesPerPlayer(BARBARIAN_PLAYER))
				{
					iTargetCities *= 3;
				}

				int iUnownedTilesThreshold = GC.getHandicapInfo(getHandicapType()).getUnownedTilesPerBarbarianCity();

				if (pLoopPlot->area()->getNumTiles() < (iUnownedTilesThreshold / 3))
				{
					iTargetCities *= iTargetCitiesMultiplier;
					iTargetCities /= 100;
				}

				iTargetCities /= std::max(1, iUnownedTilesThreshold);

				if (pLoopPlot->area()->getCitiesPerPlayer(BARBARIAN_PLAYER) < iTargetCities)
				{
					iValue = GET_PLAYER(BARBARIAN_PLAYER).AI_foundValue(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), GC.getDefineINT("MIN_BARBARIAN_CITY_STARTING_DISTANCE"));

					if (iTargetCitiesMultiplier > 100)
					{
						iValue *= pLoopPlot->area()->getNumOwnedTiles();
					}

					iValue += (100 + getSorenRandNum(50, "Barb City Found"));
					iValue /= 100;

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestPlot = pLoopPlot;
					}
				}
			}
		}
	}

	if (pBestPlot != NULL)
	{
		GET_PLAYER(BARBARIAN_PLAYER).found(pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE());
	}
}


void CvGame::createBarbarianUnits()
{
	CvUnit* pLoopUnit;
	CvArea* pLoopArea;
	CvPlot* pPlot;
	UnitAITypes eBarbUnitAI;
	UnitTypes eBestUnit;
	UnitTypes eLoopUnit;
	bool bAnimals;
//	long lResult; //Rhye (Kael)
	int iNeededBarbs;
	int iDivisor;
	int iValue;
	int iBestValue;
	int iLoop;
	int iI, iJ;

	if (isOption(GAMEOPTION_NO_BARBARIANS))
	{
		return;
	}

	//Rhye - start
//Speed: Modified by Kael 04/19/2007
//	lResult = 0;
//	gDLL->getPythonIFace()->callFunction(PYGameModule, "createBarbarianUnits", NULL, &lResult);
//	if (lResult == 1)
//	{
//		return;
//	}
//Speed: End Modify
	//Rhye - end

	bAnimals = false;

	if (GC.getEraInfo(getCurrentEra()).isNoBarbUnits())
	{
		bAnimals = true;
	}

	if (getNumCivCities() < ((countCivPlayersAlive() * 3) / 2) && !isOption(GAMEOPTION_ONE_CITY_CHALLENGE))
	{
		bAnimals = true;
	}

	if (getElapsedGameTurns() < ((GC.getHandicapInfo(getHandicapType()).getBarbarianCreationTurnsElapsed() * GC.getGameSpeedInfo(getGameSpeedType()).getBarbPercent()) / 100))
	{
		bAnimals = true;
	}

	if (bAnimals)
	{
		createAnimals();
	}
	else
	{
		return; //Rhye (so that it create just animals)

		for(pLoopArea = GC.getMapINLINE().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoop))
		{
			if (pLoopArea->isWater())
			{
				eBarbUnitAI = UNITAI_ATTACK_SEA;
				iDivisor = GC.getHandicapInfo(getHandicapType()).getUnownedWaterTilesPerBarbarianUnit();
			}
			else
			{
				eBarbUnitAI = UNITAI_ATTACK;
				iDivisor = GC.getHandicapInfo(getHandicapType()).getUnownedTilesPerBarbarianUnit();
			}

			if (isOption(GAMEOPTION_RAGING_BARBARIANS))
			{
				iDivisor = std::max(1, (iDivisor / 2));
			}

			if (iDivisor > 0)
			{
				iNeededBarbs = ((pLoopArea->getNumUnownedTiles() / iDivisor) - pLoopArea->getUnitsPerPlayer(BARBARIAN_PLAYER)); // XXX eventually need to measure how many barbs of eBarbUnitAI we have in this area...

				if (iNeededBarbs > 0)
				{
					iNeededBarbs = ((iNeededBarbs / 4) + 1);

					for (iI = 0; iI < iNeededBarbs; iI++)
					{
						pPlot = GC.getMapINLINE().syncRandPlot((RANDPLOT_NOT_VISIBLE_TO_CIV | RANDPLOT_ADJACENT_LAND | RANDPLOT_PASSIBLE), pLoopArea->getID(), GC.getDefineINT("MIN_BARBARIAN_STARTING_DISTANCE"));

						if (pPlot != NULL)
						{
							//Rhye - start (no partially impassable terrains)
							if ((pPlot->getTerrainType() <= 3) && (pPlot->getFeatureType() >= 2) && (pPlot->getFeatureType() <= 4))
							{
							//Rhye - end
							eBestUnit = NO_UNIT;
							iBestValue = 0;

							for (iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++)
							{
								bool bValid = false;
								eLoopUnit = ((UnitTypes)(GC.getCivilizationInfo(GET_PLAYER(BARBARIAN_PLAYER).getCivilizationType()).getCivilizationUnits(iJ)));

								if (eLoopUnit != NO_UNIT)
								{
									CvUnitInfo& kUnit = GC.getUnitInfo(eLoopUnit);

									bValid = (kUnit.getCombat() > 0 && !kUnit.isOnlyDefensive());

									if (bValid)
									{
										if (pLoopArea->isWater() && kUnit.getDomainType() != DOMAIN_SEA)
										{
											bValid = false;
										}
										else if (!pLoopArea->isWater() && kUnit.getDomainType() != DOMAIN_LAND)
										{
											bValid = false;
										}
									}

									if (bValid)
									{
										if (!GET_PLAYER(BARBARIAN_PLAYER).canTrain(eLoopUnit))
										{
											bValid = false;
										}
									}

									if (bValid)
									{
										if (NO_BONUS != kUnit.getPrereqAndBonus())
										{
											if (!GET_TEAM(BARBARIAN_TEAM).isHasTech((TechTypes)GC.getBonusInfo((BonusTypes)kUnit.getPrereqAndBonus()).getTechCityTrade()))
											{
												bValid = false;
											}
										}
									}

									if (bValid)
									{
										bool bFound = false;
										bool bRequires = false;
										for (int i = 0; i < GC.getNUM_UNIT_PREREQ_OR_BONUSES(); ++i)
										{
											if (NO_BONUS != kUnit.getPrereqOrBonuses(i))
											{
												TechTypes eTech = (TechTypes)GC.getBonusInfo((BonusTypes)kUnit.getPrereqOrBonuses(i)).getTechCityTrade();
												if (NO_TECH != eTech)
												{
													bRequires = true;

													if (GET_TEAM(BARBARIAN_TEAM).isHasTech(eTech))
													{
														bFound = true;
														break;
													}
												}
											}
										}

										if (bRequires && !bFound)
										{
											bValid = false;
										}
									}

									if (bValid)
									{
										iValue = (1 + getSorenRandNum(1000, "Barb Unit Selection"));

										if (kUnit.getUnitAIType(eBarbUnitAI))
										{
											iValue += 200;
										}

										if (iValue > iBestValue)
										{
											eBestUnit = eLoopUnit;
											iBestValue = iValue;
										}
									}
								}
							}

							if (eBestUnit != NO_UNIT)
							{
								GET_PLAYER(BARBARIAN_PLAYER).initUnit(eBestUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE(), eBarbUnitAI);
							}
							//Rhye - start
							}
							//Rhye - end
						}
					}
				}
			}
		}

		for (pLoopUnit = GET_PLAYER(BARBARIAN_PLAYER).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER(BARBARIAN_PLAYER).nextUnit(&iLoop))
		{
			if (pLoopUnit->isAnimal())
			{
				pLoopUnit->kill(false);
				break;
			}
		}
	}
}


void CvGame::createAnimals()
{
	CvArea* pLoopArea;
	CvPlot* pPlot;
	UnitTypes eBestUnit;
	UnitTypes eLoopUnit;
	int iNeededAnimals;
	int iValue;
	int iBestValue;
	int iLoop;
	int iI, iJ;

	if (GC.getEraInfo(getCurrentEra()).isNoAnimals())
	{
		return;
	}

	if (GC.getHandicapInfo(getHandicapType()).getUnownedTilesPerGameAnimal() <= 0)
	{
		return;
	}

	if (getNumCivCities() < countCivPlayersAlive())
	{
		return;
	}

	if (getElapsedGameTurns() < 5)
	{
		return;
	}

	for(pLoopArea = GC.getMapINLINE().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoop))
	{
		if (!(pLoopArea->isWater()))
		{
			iNeededAnimals = ((pLoopArea->getNumUnownedTiles() / GC.getHandicapInfo(getHandicapType()).getUnownedTilesPerGameAnimal()) - pLoopArea->getUnitsPerPlayer(BARBARIAN_PLAYER));

			if (iNeededAnimals > 0)
			{
				iNeededAnimals = ((iNeededAnimals / 5) + 1);

				for (iI = 0; iI < iNeededAnimals; iI++)
				{
					pPlot = GC.getMapINLINE().syncRandPlot((RANDPLOT_NOT_VISIBLE_TO_CIV | RANDPLOT_PASSIBLE), pLoopArea->getID(), GC.getDefineINT("MIN_ANIMAL_STARTING_DISTANCE"));

					if (pPlot != NULL)
					{
						eBestUnit = NO_UNIT;
						iBestValue = 0;

						for (iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++)
						{
							eLoopUnit = ((UnitTypes)(GC.getCivilizationInfo(GET_PLAYER(BARBARIAN_PLAYER).getCivilizationType()).getCivilizationUnits(iJ)));

							if (eLoopUnit != NO_UNIT)
							{
								if (GC.getUnitInfo(eLoopUnit).getUnitAIType(UNITAI_ANIMAL))
								{
									if ((pPlot->getFeatureType() != NO_FEATURE) ? GC.getUnitInfo(eLoopUnit).getFeatureNative(pPlot->getFeatureType()) : GC.getUnitInfo(eLoopUnit).getTerrainNative(pPlot->getTerrainType()))
									{
										iValue = (1 + getSorenRandNum(1000, "Animal Unit Selection"));

										if (iValue > iBestValue)
										{
											eBestUnit = eLoopUnit;
											iBestValue = iValue;
										}
									}
								}
							}
						}

						if (eBestUnit != NO_UNIT)
						{
							GET_PLAYER(BARBARIAN_PLAYER).initUnit(eBestUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE(), UNITAI_ANIMAL);
						}
					}
				}
			}
		}
	}
}


void CvGame::updateWar()
{
	int iI, iJ;

	if (isOption(GAMEOPTION_ALWAYS_WAR))
	{
		for (iI = 0; iI < MAX_TEAMS; iI++)
		{
			CvTeam& kTeam1 = GET_TEAM((TeamTypes)iI);
			if (kTeam1.isAlive() && kTeam1.isHuman())
			{
				for (iJ = 0; iJ < MAX_TEAMS; iJ++)
				{
					CvTeam& kTeam2 = GET_TEAM((TeamTypes)iJ);
					if (kTeam2.isAlive() && !kTeam2.isHuman())
					{
						FAssert(iI != iJ);

						if (kTeam1.isHasMet((TeamTypes)iJ))
						{
							if (!kTeam1.isAtWar((TeamTypes)iJ))
							{
								kTeam1.declareWar(((TeamTypes)iJ), false, NO_WARPLAN);
							}
						}
					}
				}
			}
		}
	}
}


void CvGame::updateMoves()
{
	CvSelectionGroup* pLoopSelectionGroup;
	int aiShuffle[MAX_PLAYERS];
	int iLoop;
	int iI;

	if (isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
	{
		shuffleArray(aiShuffle, MAX_PLAYERS, getSorenRand());
	}
	else
	{
		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			aiShuffle[iI] = iI;
		}
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayer& player = GET_PLAYER((PlayerTypes)(aiShuffle[iI]));

		if (player.isAlive())
		{
			if (player.isTurnActive())
			{
				if (!(player.isAutoMoves()))
				{
					player.AI_unitUpdate();

					if (!(player.isHuman()))
					{
						if (!(player.hasBusyUnit()) && !(player.hasReadyUnit(true)))
						{
							player.setAutoMoves(true);
						}
					}
				}

				if (player.isAutoMoves())
				{
					for(pLoopSelectionGroup = player.firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = player.nextSelectionGroup(&iLoop))
					{
						pLoopSelectionGroup->autoMission();
					}

					if (!(player.hasBusyUnit()))
					{
						player.setAutoMoves(false);
					}
				}
			}
		}
	}
}


void CvGame::verifyCivics()
{
	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).verifyCivics();
		}
	}
}


void CvGame::updateTimers()
{
	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).updateTimers();
		}
	}
}


void CvGame::updateTurnTimer()
{
	int iI;

	// Are we using a turn timer?
	if (isMPOption(MPOPTION_TURN_TIMER))
	{
		if (getElapsedGameTurns() > 0 || !isOption(GAMEOPTION_ADVANCED_START))
		{
			// Has the turn expired?
			if (getTurnSlice() > getCutoffSlice())
			{
				for (iI = 0; iI < MAX_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).isTurnActive())
					{
						GET_PLAYER((PlayerTypes)iI).setEndTurn(true);

						if (!isMPOption(MPOPTION_SIMULTANEOUS_TURNS) && !isSimultaneousTeamTurns())
						{
							break;
						}
					}
				}
			}
		}
	}
}


void CvGame::testAlive()
{
	int iI;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		GET_PLAYER((PlayerTypes)iI).verifyAlive();
	}
}

bool CvGame::testVictory(VictoryTypes eVictory, TeamTypes eTeam, bool* pbEndScore) const
{
	FAssert(eVictory >= 0 && eVictory < GC.getNumVictoryInfos());
	FAssert(eTeam >=0 && eTeam < MAX_CIV_TEAMS);
	FAssert(GET_TEAM(eTeam).isAlive());

	bool bValid = isVictoryValid(eVictory);
	if (pbEndScore)
	{
		*pbEndScore = false;
	}

	if (bValid)
	{
		if (GC.getVictoryInfo(eVictory).isEndScore())
		{
			if (pbEndScore)
			{
				*pbEndScore = true;
			}

			if (getMaxTurns() == 0)
			{
				bValid = false;
			}
			else if (getElapsedGameTurns() < getMaxTurns())
			{
				bValid = false;
			}
			else
			{
				bool bFound = false;

				for (int iK = 0; iK < MAX_CIV_TEAMS; iK++)
				{
					if (GET_TEAM((TeamTypes)iK).isMinorCiv())
					{
						continue;
					}

					if (GET_TEAM((TeamTypes)iK).isAlive())
					{
						if (iK != eTeam)
						{
							if (getTeamScore((TeamTypes)iK) >= getTeamScore(eTeam))
							{
								bFound = true;
								break;
							}
						}
					}
				}

				if (bFound)
				{
					bValid = false;
				}
			}
		}
	}

	if (bValid)
	{
		if (GC.getVictoryInfo(eVictory).isTargetScore())
		{
			if (getTargetScore() == 0)
			{
				bValid = false;
			}
			else if (getTeamScore(eTeam) < getTargetScore())
			{
				bValid = false;
			}
			else
			{
				bool bFound = false;

				for (int iK = 0; iK < MAX_CIV_TEAMS; iK++)
				{
					if (GET_TEAM((TeamTypes)iK).isAlive())
					{
						if (iK != eTeam)
						{
							if (getTeamScore((TeamTypes)iK) >= getTeamScore(eTeam))
							{
								bFound = true;
								break;
							}
						}
					}
				}

				if (bFound)
				{
					bValid = false;
				}
			}
		}
	}

	if (bValid)
	{
		if (GC.getVictoryInfo(eVictory).isConquest())
		{
			if (GET_TEAM(eTeam).getNumCities() == 0)
			{
				bValid = false;
			}
			else
			{
				bool bFound = false;

				for (int iK = 0; iK < MAX_CIV_TEAMS; iK++)
				{
					if (GET_TEAM((TeamTypes)iK).isAlive())
					{
						if (iK != eTeam && !GET_TEAM((TeamTypes)iK).isVassal(eTeam))
						{
							if (GET_TEAM((TeamTypes)iK).getNumCities() > 0)
							{
								bFound = true;
								break;
							}
						}
					}
				}

				if (bFound)
				{
					bValid = false;
				}
			}
		}
	}

	if (bValid)
	{
		if (GC.getVictoryInfo(eVictory).isDiploVote())
		{
			bool bFound = false;

			for (int iK = 0; iK < GC.getNumVoteInfos(); iK++)
			{
				if (GC.getVoteInfo((VoteTypes)iK).isVictory())
				{
					if (getVoteOutcome((VoteTypes)iK) == eTeam)
					{
						bFound = true;
						break;
					}
				}
			}

			if (!bFound)
			{
				bValid = false;
			}
		}
	}

	if (bValid)
	{
		if (getAdjustedPopulationPercent(eVictory) > 0)
		{
			if (100 * GET_TEAM(eTeam).getTotalPopulation() < getTotalPopulation() * getAdjustedPopulationPercent(eVictory))
			{
				bValid = false;
			}
		}
	}

	if (bValid)
	{
		if (getAdjustedLandPercent(eVictory) > 0)
		{
			if (100 * GET_TEAM(eTeam).getTotalLand() < GC.getMapINLINE().getLandPlots() * getAdjustedLandPercent(eVictory))
			{
				bValid = false;
			}
		}
	}

	if (bValid)
	{
		if (GC.getVictoryInfo(eVictory).getReligionPercent() > 0)
		{
			bool bFound = false;

			if (getNumCivCities() > (countCivPlayersAlive() * 2))
			{
				for (int iK = 0; iK < GC.getNumReligionInfos(); iK++)
				{
					if (GET_TEAM(eTeam).hasHolyCity((ReligionTypes)iK))
					{
						if (calculateReligionPercent((ReligionTypes)iK) >= GC.getVictoryInfo(eVictory).getReligionPercent())
						{
							bFound = true;
							break;
						}
					}

					if (bFound)
					{
						break;
					}
				}
			}

			if (!bFound)
			{
				bValid = false;
			}
		}
	}

	if (bValid)
	{
		if ((GC.getVictoryInfo(eVictory).getCityCulture() != NO_CULTURELEVEL) && (GC.getVictoryInfo(eVictory).getNumCultureCities() > 0))
		{
			int iCount = 0;

			for (int iK = 0; iK < MAX_CIV_PLAYERS; iK++)
			{
				if (GET_PLAYER((PlayerTypes)iK).isAlive())
				{
					if (GET_PLAYER((PlayerTypes)iK).getTeam() == eTeam)
					{
						int iLoop;
						for (CvCity* pLoopCity = GET_PLAYER((PlayerTypes)iK).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iK).nextCity(&iLoop))
						{
							if (pLoopCity->getCultureLevel() >= GC.getVictoryInfo(eVictory).getCityCulture())
							{
								iCount++;
							}
						}
					}
				}
			}

			if (iCount < GC.getVictoryInfo(eVictory).getNumCultureCities())
			{
				bValid = false;
			}
		}
	}

	if (bValid)
	{
		if (GC.getVictoryInfo(eVictory).getTotalCultureRatio() > 0)
		{
			int iThreshold = ((GET_TEAM(eTeam).countTotalCulture() * 100) / GC.getVictoryInfo(eVictory).getTotalCultureRatio());

			bool bFound = false;

			for (int iK = 0; iK < MAX_CIV_TEAMS; iK++)
			{
				if (GET_TEAM((TeamTypes)iK).isAlive())
				{
					if (iK != eTeam)
					{
						if (GET_TEAM((TeamTypes)iK).countTotalCulture() > iThreshold)
						{
							bFound = true;
							break;
						}
					}
				}
			}

			if (bFound)
			{
				bValid = false;
			}
		}
	}

	if (bValid)
	{
		for (int iK = 0; iK < GC.getNumBuildingClassInfos(); iK++)
		{
			if (GC.getBuildingClassInfo((BuildingClassTypes) iK).getVictoryThreshold(eVictory) > GET_TEAM(eTeam).getBuildingClassCount((BuildingClassTypes)iK))
			{
				bValid = false;
				break;
			}
		}
	}

	if (bValid)
	{
		for (int iK = 0; iK < GC.getNumProjectInfos(); iK++)
		{
			if (GC.getProjectInfo((ProjectTypes) iK).getVictoryMinThreshold(eVictory) > GET_TEAM(eTeam).getProjectCount((ProjectTypes)iK))
			{
				bValid = false;
				break;
			}
		}
	}

	if (bValid)
	{
		long lResult = 1;
		CyArgsList argsList;
		argsList.add(eVictory);
		gDLL->getPythonIFace()->callFunction(PYGameModule, "isVictory", argsList.makeFunctionArgs(), &lResult);
		if (0 == lResult)
		{
			bValid = false;
		}
	}

	return bValid;
}

void CvGame::testVictory()
{
	bool bEndScore = false;

	if (getVictory() != NO_VICTORY)
	{
		return;
	}

	if (getGameState() == GAMESTATE_EXTENDED)
	{
		return;
	}

	updateScore();

	long lResult = 1;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "isVictoryTest", NULL, &lResult);
	if (lResult == 0)
	{
		return;
	}

	std::vector<std::vector<int> > aaiWinners;

	for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iI);
		if (kLoopTeam.isAlive())
		{
			if (!(kLoopTeam.isMinorCiv()))
			{
				//Rhye - start (Historical victory should not be checked - it's triggered by python
				// Leoreth: same for religious
				//for (int iJ = 0; iJ < GC.getNumVictoryInfos(); iJ++)
				for (int iJ = 0; iJ < GC.getNumVictoryInfos()-2; iJ++)
				//Rhye - end
				{
					if (testVictory((VictoryTypes)iJ, (TeamTypes)iI, &bEndScore))
					{
						if (kLoopTeam.getVictoryCountdown((VictoryTypes)iJ) < 0)
						{
							if (kLoopTeam.getVictoryDelay((VictoryTypes)iJ) == 0)
							{
								kLoopTeam.setVictoryCountdown((VictoryTypes)iJ, 0);
							}
						}

						//update victory countdown
						if (kLoopTeam.getVictoryCountdown((VictoryTypes)iJ) > 0)
						{
							kLoopTeam.changeVictoryCountdown((VictoryTypes)iJ, -1);
						}

						if (kLoopTeam.getVictoryCountdown((VictoryTypes)iJ) == 0)
						{
							if (getSorenRandNum(100, "Victory Success") < kLoopTeam.getLaunchSuccessRate((VictoryTypes)iJ))
							{
								std::vector<int> aWinner;
								aWinner.push_back(iI);
								aWinner.push_back(iJ);
								aaiWinners.push_back(aWinner);
							}
							else
							{
								kLoopTeam.resetVictoryProgress();
							}
						}
					}
				}
			}
		}

	}

	if (aaiWinners.size() > 0)
	{
		int iWinner = getSorenRandNum(aaiWinners.size(), "Victory tie breaker");
		setWinner(((TeamTypes)aaiWinners[iWinner][0]), ((VictoryTypes)aaiWinners[iWinner][1]));
	}

	if (getVictory() == NO_VICTORY)
	{
		if (getMaxTurns() > 0)
		{
			if (getElapsedGameTurns() >= getMaxTurns())
			{
				if (!bEndScore)
				{
					if ((getAIAutoPlay() > 0) || gDLL->GetAutorun())
					{
						setGameState(GAMESTATE_EXTENDED);
					}
					else
					{
						setGameState(GAMESTATE_OVER);
					}
				}
			}
		}
	}
}


void CvGame::processVote(const VoteTriggeredData& kData, int iChange)
{
	CvVoteInfo& kVote = GC.getVoteInfo(kData.kVoteOption.eVote);

	changeTradeRoutes(kVote.getTradeRoutes() * iChange);
	changeFreeTradeCount(kVote.isFreeTrade() ? iChange : 0);
	changeNoNukesCount(kVote.isNoNukes() ? iChange : 0);

	for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
	{
		changeForceCivicCount((CivicTypes)iI, kVote.isForceCivic(iI) ? iChange : 0);
	}


	if (iChange > 0)
	{
		if (kVote.isOpenBorders())
		{
			for (int iTeam1 = 0; iTeam1 < MAX_CIV_PLAYERS; ++iTeam1)
			{
				CvTeam& kLoopTeam1 = GET_TEAM((TeamTypes)iTeam1);
				if (kLoopTeam1.isVotingMember(kData.eVoteSource))
				{
					// Leoreth: unaffected by defied, but passed resolution
					if (getPlayerVote((PlayerTypes)iTeam1, kData.getID()) == PLAYER_VOTE_NEVER)
						continue;

					for (int iTeam2 = iTeam1 + 1; iTeam2 < MAX_CIV_PLAYERS; ++iTeam2)
					{
						// Leoreth: unaffected by defied, but passed resolution
						if (getPlayerVote((PlayerTypes)iTeam2, kData.getID()) == PLAYER_VOTE_NEVER)
							continue;

						CvTeam& kLoopTeam2 = GET_TEAM((TeamTypes)iTeam2);
						if (kLoopTeam2.isVotingMember(kData.eVoteSource))
						{
							kLoopTeam1.signOpenBorders((TeamTypes)iTeam2);
						}
					}
				}
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}
		else if (kVote.isDefensivePact())
		{
			for (int iTeam1 = 0; iTeam1 < MAX_CIV_PLAYERS; ++iTeam1)
			{
				CvTeam& kLoopTeam1 = GET_TEAM((TeamTypes)iTeam1);
				if (kLoopTeam1.isVotingMember(kData.eVoteSource))
				{
					// Leoreth: unaffected by defied, but passed resolution
					if (getPlayerVote((PlayerTypes)iTeam1, kData.getID()) == PLAYER_VOTE_NEVER)
						continue;

					for (int iTeam2 = iTeam1 + 1; iTeam2 < MAX_CIV_PLAYERS; ++iTeam2)
					{
						// Leoreth: unaffected by defied, but passed resolution
						if (getPlayerVote((PlayerTypes)iTeam2, kData.getID()) == PLAYER_VOTE_NEVER)
							continue;

						CvTeam& kLoopTeam2 = GET_TEAM((TeamTypes)iTeam2);
						if (kLoopTeam2.isVotingMember(kData.eVoteSource))
						{
							kLoopTeam1.signDefensivePact((TeamTypes)iTeam2);
						}
					}
				}
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}
		else if (kVote.isForcePeace())
		{
			FAssert(NO_PLAYER != kData.kVoteOption.ePlayer);
			CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);

			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				// Leoreth: unaffected by defied, but passed resolution
				if (getPlayerVote((PlayerTypes)iPlayer, kData.getID()) == PLAYER_VOTE_NEVER)
					continue;

				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
				if (kLoopPlayer.getTeam() != kPlayer.getTeam())
				{
					if (kLoopPlayer.isVotingMember(kData.eVoteSource))
					{
						//Rhye - start
						//kLoopPlayer.forcePeace(kData.kVoteOption.ePlayer);
						if (atWar(kPlayer.getTeam(), kLoopPlayer.getTeam())) {
							kLoopPlayer.forcePeace(kData.kVoteOption.ePlayer);
							CvEventReporter::getInstance().peaceBrokered(GET_TEAM(getSecretaryGeneral(kVote.isVoteSourceType(0) ? (VoteSourceTypes)0 : (VoteSourceTypes)1)).getLeaderID(), (PlayerTypes)iPlayer, kData.kVoteOption.ePlayer);
						}
						//Rhye - end
					}
				}
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}
		else if (kVote.isForceNoTrade())
		{
			FAssert(NO_PLAYER != kData.kVoteOption.ePlayer);
			CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);

			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				// Leoreth: unaffected by defied, but passed resolution
				if (getPlayerVote((PlayerTypes)iPlayer, kData.getID()) == PLAYER_VOTE_NEVER)
					continue;

				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
				if (kLoopPlayer.isVotingMember(kData.eVoteSource))
				{
					if (kLoopPlayer.canStopTradingWithTeam(kPlayer.getTeam()))
					{
						kLoopPlayer.stopTradingWithTeam(kPlayer.getTeam());
					}
				}
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}
		else if (kVote.isForceWar())
		{
			FAssert(NO_PLAYER != kData.kVoteOption.ePlayer);
			CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);

			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				// Leoreth: unaffected by defied, but passed resolution
				if (getPlayerVote((PlayerTypes)iPlayer, kData.getID()) == PLAYER_VOTE_NEVER)
					continue;

				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
				if (kLoopPlayer.isVotingMember(kData.eVoteSource))
				{
					if (GET_TEAM(kLoopPlayer.getTeam()).canChangeWarPeace(kPlayer.getTeam()))
					{
						GET_TEAM(kLoopPlayer.getTeam()).declareWar(kPlayer.getTeam(), false, WARPLAN_DOGPILE);
					}
				}
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}
		else if (kVote.isAssignCity())
		{
			FAssert(NO_PLAYER != kData.kVoteOption.ePlayer);
			CvPlayer& kPlayer = GET_PLAYER(kData.kVoteOption.ePlayer);
			CvCity* pCity = kPlayer.getCity(kData.kVoteOption.iCityId);
			FAssert(NULL != pCity);

			if (NULL != pCity)
			{
				// Leoreth: city assignment can be defied, but leads to war with the civs that voted yes
				if (getPlayerVote(pCity->getOwnerINLINE(), kData.getID()) == PLAYER_VOTE_NEVER)
				{
					for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isMinorCiv())
						{
							continue;
						}

						if (getPlayerVote((PlayerTypes)iI, kData.getID()) == PLAYER_VOTE_YES)
						{
							GET_TEAM((TeamTypes)iI).declareWar((TeamTypes)pCity->getOwnerINLINE(), true, WARPLAN_LIMITED);
						}
					}
				}
				else
				{
					if (NO_PLAYER != kData.kVoteOption.eOtherPlayer && kData.kVoteOption.eOtherPlayer != pCity->getOwnerINLINE())
					{
						GET_PLAYER(kData.kVoteOption.eOtherPlayer).acquireCity(pCity, false, true, true);
					}
				}
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}

		if (kVote.isRevokeMembership())
		{
			GET_PLAYER(kData.kVoteOption.ePlayer).setLoyalMember(kData.eVoteSource, false);
		}

		if (kVote.getGoldPercent() > 0)
		{
			int iGold;
			int iTotalGold = 0;

			for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isMinorCiv())
				{
					continue;
				}

				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);

				// Leoreth: unaffected by defied, but passed resolution
				if (getPlayerVote((PlayerTypes)iI, kData.getID()) == PLAYER_VOTE_NEVER) continue;

				if (kData.kVoteOption.ePlayer == iI) continue;

				if (kLoopPlayer.isFullMember(kData.eVoteSource))
				{
					iGold = kLoopPlayer.getGold() * kVote.getGoldPercent();
					iGold /= 100;
					iTotalGold += iGold;
					kLoopPlayer.changeGold(-iGold);
				}
			}

			if (kData.kVoteOption.ePlayer != NO_PLAYER)
			{
				GET_PLAYER(kData.kVoteOption.ePlayer).changeGold(iTotalGold / 2);
				gDLL->getInterfaceIFace()->addMessage(kData.kVoteOption.ePlayer, true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_APOSTOLIC_PALACE_COLLECT_TITHE", iTotalGold / 2), "", MESSAGE_TYPE_MAJOR_EVENT, "", (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), -1, -1, true, true);
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}

		if (kVote.getEspionage() > 0)
		{
			PlayerTypes ePlayer = kData.kVoteOption.ePlayer;
			PlayerTypes eOtherPlayer = kData.kVoteOption.eOtherPlayer;

			if (ePlayer != NO_PLAYER && eOtherPlayer != NO_PLAYER)
			{
				GET_TEAM(GET_PLAYER(ePlayer).getTeam()).changeEspionagePointsAgainstTeam(GET_PLAYER(eOtherPlayer).getTeam(), kVote.getEspionage() * GET_PLAYER(ePlayer).getReligionPopulation(GC.getGame().getVoteSourceReligion(kData.eVoteSource)));
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}

		if (kVote.getHappiness() < 0)
		{
			int iLoop;
			for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);

				if (kLoopPlayer.isMinorCiv())
				{
					continue;
				}

				// Leoreth: unaffected by defied, but passed resolution
				if (getPlayerVote((PlayerTypes)iI, kData.getID()) == PLAYER_VOTE_NEVER)
				{
					continue;
				}

				if (kLoopPlayer.isFullMember(kData.eVoteSource))
				{
					for (CvCity* pLoopCity = kLoopPlayer.firstCity(&iLoop); NULL != pLoopCity; pLoopCity = kLoopPlayer.nextCity(&iLoop))
					{
						ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(kData.eVoteSource);

						if (NO_RELIGION == eReligion || pLoopCity->isHasReligion(eReligion))
						{
							int iAngerLength = pLoopCity->flatDefyResolutionAngerLength();
							if (NO_RELIGION != eReligion && pLoopCity->isHasReligion(eReligion))
							{
								iAngerLength /= std::max(1, pLoopCity->getReligionCount());
							}

							pLoopCity->changeDefyResolutionAngerTimer(iAngerLength);
						}
					}
				}
			}

			if (kVote.isDecolonize())
			{
				CvCity* pCity = GET_PLAYER(kData.kVoteOption.ePlayer).getCity(kData.kVoteOption.iCityId);

				pCity->liberate(false);
			}

			if (kVote.isReleaseCivilization())
			{
				GET_PLAYER(kData.kVoteOption.ePlayer).splitEmpire(kData.kVoteOption.eOtherPlayer);
			}

			setVoteOutcome(kData, NO_PLAYER_VOTE);
		}
	}
}


int CvGame::getIndexAfterLastDeal()
{
	return m_deals.getIndexAfterLast();
}


int CvGame::getNumDeals()
{
	return m_deals.getCount();
}


 CvDeal* CvGame::getDeal(int iID)
{
	return ((CvDeal *)(m_deals.getAt(iID)));
}


CvDeal* CvGame::addDeal()
{
	return ((CvDeal *)(m_deals.add()));
}


 void CvGame::deleteDeal(int iID)
{
	m_deals.removeAt(iID);
	gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
}

CvDeal* CvGame::firstDeal(int *pIterIdx, bool bRev)
{
	return !bRev ? m_deals.beginIter(pIterIdx) : m_deals.endIter(pIterIdx);
}


CvDeal* CvGame::nextDeal(int *pIterIdx, bool bRev)
{
	return !bRev ? m_deals.nextIter(pIterIdx) : m_deals.prevIter(pIterIdx);
}


 CvRandom& CvGame::getMapRand()
{
	return m_mapRand;
}


int CvGame::getMapRandNum(int iNum, const char* pszLog)
{
	return m_mapRand.get(iNum, pszLog);
}


CvRandom& CvGame::getSorenRand()
{
	return m_sorenRand;
}


int CvGame::getSorenRandNum(int iNum, const char* pszLog)
{
	return m_sorenRand.get(iNum, pszLog);
}


int CvGame::calculateSyncChecksum()
{
	PROFILE_FUNC();

	CvUnit* pLoopUnit;
	int iMultiplier;
	int iValue;
	int iLoop;
	int iI, iJ;

	iValue = 0;

	iValue += getMapRand().getSeed();
	iValue += getSorenRand().getSeed();

	iValue += getNumCities();
	iValue += getTotalPopulation();
	iValue += getNumDeals();

	iValue += GC.getMapINLINE().getOwnedPlots();
	iValue += GC.getMapINLINE().getNumAreas();

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isEverAlive())
		{
			iMultiplier = getPlayerScore((PlayerTypes)iI);

			switch (getTurnSlice() % 4)
			{
			case 0:
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getTotalPopulation() * 543271);
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getTotalLand() * 327382);
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getGold() * 107564);
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getAssets() * 327455);
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getPower() * 135647);
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getNumCities() * 436432);
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getNumUnits() * 324111);
				iMultiplier += (GET_PLAYER((PlayerTypes)iI).getNumSelectionGroups() * 215356);
				break;

			case 1:
				for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
				{
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).calculateTotalYield((YieldTypes)iJ) * 432754);
				}

				for (iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
				{
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).getCommerceRate((CommerceTypes)iJ) * 432789);
				}
				break;

			case 2:
				for (iJ = 0; iJ < GC.getNumBonusInfos(); iJ++)
				{
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).getNumAvailableBonuses((BonusTypes)iJ) * 945732);
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).getBonusImport((BonusTypes)iJ) * 326443);
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).getBonusExport((BonusTypes)iJ) * 932211);
				}

				for (iJ = 0; iJ < GC.getNumImprovementInfos(); iJ++)
				{
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).getImprovementCount((ImprovementTypes)iJ) * 883422);
				}

				for (iJ = 0; iJ < GC.getNumBuildingClassInfos(); iJ++)
				{
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).getBuildingClassCountPlusMaking((BuildingClassTypes)iJ) * 954531);
				}

				for (iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++)
				{
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).getUnitClassCountPlusMaking((UnitClassTypes)iJ) * 754843);
				}

				for (iJ = 0; iJ < NUM_UNITAI_TYPES; iJ++)
				{
					iMultiplier += (GET_PLAYER((PlayerTypes)iI).AI_totalUnitAIs((UnitAITypes)iJ) * 643383);
				}
				break;

			case 3:
				for (pLoopUnit = GET_PLAYER((PlayerTypes)iI).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)iI).nextUnit(&iLoop))
				{
					iMultiplier += (pLoopUnit->getX_INLINE() * 876543);
					iMultiplier += (pLoopUnit->getY_INLINE() * 985310);
					iMultiplier += (pLoopUnit->getDamage() * 736373);
					iMultiplier += (pLoopUnit->getExperience() * 820622);
					iMultiplier += (pLoopUnit->getLevel() * 367291);
				}
				break;
			}

			if (iMultiplier != 0)
			{
				iValue *= iMultiplier;
			}
		}
	}

	return iValue;
}


int CvGame::calculateOptionsChecksum()
{
	PROFILE_FUNC();

	int iValue;
	int iI, iJ;

	iValue = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		for (iJ = 0; iJ < NUM_PLAYEROPTION_TYPES; iJ++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isOption((PlayerOptionTypes)iJ))
			{
				iValue += (iI * 943097);
				iValue += (iJ * 281541);
			}
		}
	}

	return iValue;
}


//Rhye - start (jdog) for Warlords
// Return success of changing properties of player
// playerIdx is index of player to be changed ... must have been alive at some point (otherwise use createNewPlayer)
// newCivType is index of new civ
// newLeader is index of new leader of that civ, currently has to be for the civ
// teamIdx is team civ should join, -1 for no change
// bIsHuman, true if player is to be human controlled
// bChangeGraphics, true to update player graphics to new civ type (leader head graphics always change)
bool CvGame::changePlayer( int playerIdx, int newCivType, int newLeader, int teamIdx, bool bIsHuman, bool bChangeGraphics )
{
	bool changedCivOrLeader = false;
	LeaderHeadTypes prevLeader = NO_LEADER;
	CvFlagEntity* newFlagSymbol = NULL;
	CvUnit* pLoopUnit;
	CvUnit* pNewUnit;
	int iLoop;
	TeamTypes prevTeam = GET_PLAYER((PlayerTypes)playerIdx).getTeam();

	if( playerIdx >= GC.getMAX_CIV_PLAYERS() )
	{
		//logMsg("Creating new player ... failed, invalid player index");
		return false;
	}
	if( !GET_PLAYER((PlayerTypes)playerIdx).isEverAlive() )
	{
		//logMsg("Changing player ... failed, player id never alive");
		return false;
	}
	if( newCivType >= GC.getNumCivilizationInfos() )
	{
		//logMsg("Creating new player ... failed, invalid civ type");
		return false;
	}
	if( newLeader >= GC.getNumLeaderHeadInfos() )
	{
		//logMsg("Creating new player ... failed, invalid leader type");
		return false;
	}
	if( teamIdx >= GC.getMAX_TEAMS() ) //( teamIdx >= GC.getMAX_CIV_TEAMS() )
	{
		//logMsg("Creating new player ... failed, invalid team index");
		return false;
	}

	//logMsg("Changing player ...");

	// Change whether this player is human
	if( bIsHuman )
	{
		if( GC.getInitCore().getSlotStatus( (PlayerTypes)playerIdx ) != SS_TAKEN )
			GC.getInitCore().setSlotStatus( (PlayerTypes)playerIdx, SS_TAKEN );
	}
	else
	{
		if( GC.getInitCore().getSlotStatus( (PlayerTypes)playerIdx ) == SS_TAKEN )
			GC.getInitCore().setSlotStatus( (PlayerTypes)playerIdx, SS_COMPUTER ); // or SS_OPEN?
	}

	// Change civ type
	if( (CivilizationTypes)newCivType != GC.getInitCore().getCiv((PlayerTypes)playerIdx) )
	{
		//logMsg("Changing civType");

		GC.getInitCore().setCiv((PlayerTypes)playerIdx, (CivilizationTypes)newCivType);

		changedCivOrLeader = true;
	}

	// Change Leader Head
	if( (LeaderHeadTypes)newLeader != GC.getInitCore().getLeader((PlayerTypes)playerIdx ) )
	{
		//logMsg("Changeing Leader");
		prevLeader = GC.getInitCore().getLeader((PlayerTypes)playerIdx );

		if( !GC.getCivilizationInfo( (CivilizationTypes)newCivType ).isLeaders( (LeaderHeadTypes)newLeader) )
		{
			//logMsg("WARNING: New leader not for this civ");
		}

		GC.getInitCore().setLeader((PlayerTypes)playerIdx, (LeaderHeadTypes)newLeader );
		GC.getInitCore().setLeaderName((PlayerTypes)playerIdx, GC.getLeaderHeadInfo((LeaderHeadTypes)newLeader).getDescription(0)); //Rhye

		changedCivOrLeader = true;
	}

	// Place on a different team?
	if( teamIdx >= 0 && (TeamTypes)teamIdx != prevTeam )
	{
		if( GET_TEAM(prevTeam).getNumMembers() == 1 )
		{
			GET_TEAM( (TeamTypes)teamIdx ).addTeam(prevTeam);
			gDLL->getInterfaceIFace()->setDirty(Fog_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		}
		else
		{
			// This handles both changes to prev team and new team
			GET_PLAYER((PlayerTypes)playerIdx).setTeam((TeamTypes)teamIdx);
			gDLL->getInterfaceIFace()->setDirty(Fog_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
			gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		}
	}

	// Update civs colors, artstyle, border colors, leader name on the score board, etc.
	// Current challenge is getting existing units to change their flag ...
	if( bChangeGraphics )
	{
		//logMsg("Changing player graphics");
		CivilizationTypes civType = GET_PLAYER((PlayerTypes)playerIdx).getCivilizationType();
		GC.getInitCore().setFlagDecal( (PlayerTypes)playerIdx, (CvWString)GC.getCivilizationInfo(civType).getFlagTexture() );
		GC.getInitCore().setColor( (PlayerTypes)playerIdx, (PlayerColorTypes)GC.getCivilizationInfo(civType).getDefaultPlayerColor() );
		GC.getInitCore().setArtStyle( (PlayerTypes)playerIdx, (ArtStyleTypes)GC.getCivilizationInfo(civType).getArtStyleType() );

		// Need to force redraw
		gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);

		gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(HighlightPlot_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(SelectionSound_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GlobeInfo_DIRTY_BIT, true);
/*
		//Change existing unit flags
		newFlagSymbol = gDLL->getFlagEntityIFace()->create((PlayerTypes)playerIdx);
		if( newFlagSymbol != NULL )
		{
			for(pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).nextUnit(&iLoop))
			{
				pLoopPlot = GC.getMapINLINE().plotINLINE(pLoopUnit->getX(),pLoopUnit->getY());
				//pLoopPlot->updateFlagSymbol();
				//gDLL->getFlagEntityIFace()->updateUnitInfo(newFlagSymbol, pLoopPlot);
			}
		}
		else
		{
			logMsg("New flag creation failed.");
		}
*/

		int numUnits = GET_PLAYER((PlayerTypes)playerIdx).getNumUnits();
		int i = 0;

		// Loop through players units, converting them
		for (pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).nextUnit(&iLoop))
		{
			// Concept borrowed from CvUnit::gift
			pNewUnit = GET_PLAYER((PlayerTypes)playerIdx).initUnit(pLoopUnit->getUnitType(), pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE(), pLoopUnit->AI_getUnitAIType());
			// Will kill pLoopUnit
			pNewUnit->convert(pLoopUnit);

			char cArray[99];
			sprintf(cArray, "Converting unit type: %d", pNewUnit->getUnitType());
			//logMsg(cArray);

			// Without this, is infinite loop ...
			i++;
			if( i >= numUnits )
				break;
		}

	}

	// If civ or leader changed, need to update traits/personality/civ data
	if( changedCivOrLeader )
	{
		GET_PLAYER((PlayerTypes)playerIdx).reinit((PlayerTypes)playerIdx, prevLeader, false);
	}

	//logMsg("Player change complete");

	return true;
}

void CvGame::convertUnits( int playerIdx )
{
	CvUnit* pLoopUnit;
	CvUnit* pNewUnit;
	int iLoop;
	int numUnits = GET_PLAYER((PlayerTypes)playerIdx).getNumUnits();
	int i = 0;

	// Loop through players units, converting them
	for (pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)playerIdx).nextUnit(&iLoop))
	{
		// Concept borrowed from CvUnit::gift
		pNewUnit = GET_PLAYER((PlayerTypes)playerIdx).initUnit(pLoopUnit->getUnitType(), pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE(), pLoopUnit->AI_getUnitAIType());
		// Will kill pLoopUnit
		pNewUnit->convert(pLoopUnit);

		char cArray[99];
		sprintf(cArray, "Converting unit type: %d", pNewUnit->getUnitType());
		//logMsg(cArray);

		// Without this, is infinite loop ...
		i++;
		if( i >= numUnits )
			break;
	}
}
// Rhye - end (jdog)



void CvGame::addReplayMessage(ReplayMessageTypes eType, PlayerTypes ePlayer, CvWString pszText, int iPlotX, int iPlotY, ColorTypes eColor)
{
	int iGameTurn = getGameTurn();
	CvReplayMessage* pMessage = new CvReplayMessage(iGameTurn, eType, ePlayer);
	if (NULL != pMessage)
	{
		pMessage->setPlot(iPlotX, iPlotY);
		pMessage->setText(pszText);
		if (NO_COLOR == eColor)
		{
			eColor = (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE");
		}
		pMessage->setColor(eColor);
		m_listReplayMessages.push_back(pMessage);
	}
}

void CvGame::clearReplayMessageMap()
{
	for (ReplayMessageList::const_iterator itList = m_listReplayMessages.begin(); itList != m_listReplayMessages.end(); itList++)
	{
		const CvReplayMessage* pMessage = *itList;
		if (NULL != pMessage)
		{
			delete pMessage;
		}
	}
	m_listReplayMessages.clear();
}

int CvGame::getReplayMessageTurn(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (-1);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (-1);
	}
	return pMessage->getTurn();
}

ReplayMessageTypes CvGame::getReplayMessageType(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NO_REPLAY_MESSAGE);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NO_REPLAY_MESSAGE);
	}
	return pMessage->getType();
}

int CvGame::getReplayMessagePlotX(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (-1);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (-1);
	}
	return pMessage->getPlotX();
}

int CvGame::getReplayMessagePlotY(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (-1);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (-1);
	}
	return pMessage->getPlotY();
}

PlayerTypes CvGame::getReplayMessagePlayer(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NO_PLAYER);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NO_PLAYER);
	}
	return pMessage->getPlayer();
}

LPCWSTR CvGame::getReplayMessageText(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NULL);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NULL);
	}
	return pMessage->getText().GetCString();
}

ColorTypes CvGame::getReplayMessageColor(uint i) const
{
	if (i >= m_listReplayMessages.size())
	{
		return (NO_COLOR);
	}
	const CvReplayMessage* pMessage =  m_listReplayMessages[i];
	if (NULL == pMessage)
	{
		return (NO_COLOR);
	}
	return pMessage->getColor();
}


uint CvGame::getNumReplayMessages() const
{
	return m_listReplayMessages.size();
}

// Private Functions...

void CvGame::read(FDataStreamBase* pStream)
{
	int iI;

	reset(NO_HANDICAP);

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	if (uiFlag < 1)
	{
		int iEndTurnMessagesSent;
		pStream->Read(&iEndTurnMessagesSent);
	}
	pStream->Read(&m_iElapsedGameTurns);
	pStream->Read(&m_iStartTurn);
	pStream->Read(&m_iStartYear);
	pStream->Read(&m_iEstimateEndTurn);
	pStream->Read(&m_iTurnSlice);
	pStream->Read(&m_iCutoffSlice);
	pStream->Read(&m_iNumGameTurnActive);
	pStream->Read(&m_iNumCities);
	pStream->Read(&m_iTotalPopulation);
	pStream->Read(&m_iTradeRoutes);
	pStream->Read(&m_iFreeTradeCount);
	pStream->Read(&m_iNoNukesCount);
	pStream->Read(&m_iNukesExploded);
	pStream->Read(&m_iMaxPopulation);
	pStream->Read(&m_iMaxLand);
	pStream->Read(&m_iMaxTech);
	pStream->Read(&m_iMaxWonders);
	pStream->Read(&m_iInitPopulation);
	pStream->Read(&m_iInitLand);
	pStream->Read(&m_iInitTech);
	pStream->Read(&m_iInitWonders);
	pStream->Read(&m_iAIAutoPlay);
	pStream->Read(&m_iCircumnavigated); //Rhye
	pStream->Read(&m_iMedianTechValue); // Leoreth

	// m_uiInitialTime not saved

	pStream->Read(&m_bScoreDirty);
	pStream->Read(&m_bCircumnavigated);
	// m_bDebugMode not saved
	pStream->Read(&m_bFinalInitialized);
	// m_bPbemTurnSent not saved
	pStream->Read(&m_bHotPbemBetweenTurns);
	// m_bPlayerOptionsSent not saved
	pStream->Read(&m_bNukesValid);

	pStream->Read((int*)&m_eHandicap);
	pStream->Read((int*)&m_ePausePlayer);
	pStream->Read((int*)&m_eBestLandUnit);
	pStream->Read((int*)&m_eWinner);
	pStream->Read((int*)&m_eVictory);
	pStream->Read((int*)&m_eGameState);
	pStream->Read((int*)&m_eCityScreenOwner); // Leoreth
	pStream->Read((int*)&m_eGreatPeopleNotifications);
	pStream->Read((int*)&m_eReligionSpreadNotifications);
	pStream->Read((int*)&m_eEventEffectNotifications);

	//Rhye - start bugfix (thanks Gyathaar)
	//pStream->ReadString(m_szScriptData);
	int charcount;
	char letter;
	pStream->Read(&charcount);
	m_szScriptData = "";
	for (iI=0;iI<charcount;iI++)
	{
		pStream->Read(&letter);
		m_szScriptData += letter;
	}
	//Rhye - end

	if (uiFlag < 1)
	{
		std::vector<int> aiEndTurnMessagesReceived(MAX_PLAYERS);
		pStream->Read(MAX_PLAYERS, &aiEndTurnMessagesReceived[0]);
	}
	pStream->Read(MAX_PLAYERS, m_aiRankPlayer);
	pStream->Read(MAX_PLAYERS, m_aiPlayerRank);
	pStream->Read(MAX_PLAYERS, m_aiPlayerScore);
	pStream->Read(MAX_TEAMS, m_aiRankTeam);
	pStream->Read(MAX_TEAMS, m_aiTeamRank);
	pStream->Read(MAX_TEAMS, m_aiTeamScore);

	// Leoreth
	pStream->Read(NUM_CIVS, m_aiCivPeriod);
	pStream->Read(MAX_TEAMS, m_aiTechRankTeam);

	pStream->Read(GC.getNumUnitInfos(), m_paiUnitCreatedCount);
	pStream->Read(GC.getNumUnitClassInfos(), m_paiUnitClassCreatedCount);
	pStream->Read(GC.getNumBuildingClassInfos(), m_paiBuildingClassCreatedCount);
	pStream->Read(GC.getNumProjectInfos(), m_paiProjectCreatedCount);
	pStream->Read(GC.getNumCivicInfos(), m_paiForceCivicCount);
	pStream->Read(GC.getNumVoteInfos(), (int*)m_paiVoteOutcome);
	pStream->Read(GC.getNumReligionInfos(), m_paiReligionGameTurnFounded);
	pStream->Read(GC.getNumCorporationInfos(), m_paiCorporationGameTurnFounded);
	pStream->Read(GC.getNumVoteSourceInfos(), m_aiSecretaryGeneralTimer);
	pStream->Read(GC.getNumVoteSourceInfos(), m_aiVoteTimer);
	pStream->Read(GC.getNumVoteSourceInfos(), m_aiDiploVote);

	pStream->Read(GC.getNumSpecialUnitInfos(), m_pabSpecialUnitValid);
	pStream->Read(GC.getNumSpecialBuildingInfos(), m_pabSpecialBuildingValid);
	pStream->Read(GC.getNumReligionInfos(), m_abReligionSlotTaken);

	// Leoreth
	pStream->Read(GC.getNumTechInfos(), m_aiFirstDiscovered);
	pStream->Read(GC.getNumTechInfos(), m_aiFirstDiscoveredTurn);

	for (iI=0;iI<GC.getNumReligionInfos();iI++)
	{
		pStream->Read((int*)&m_paHolyCity[iI].eOwner);
		pStream->Read(&m_paHolyCity[iI].iID);
	}

	for (iI=0;iI<GC.getNumCorporationInfos();iI++)
	{
		pStream->Read((int*)&m_paHeadquarters[iI].eOwner);
		pStream->Read(&m_paHeadquarters[iI].iID);
	}

	{
		CvWString szBuffer;
		uint iSize;

		m_aszDestroyedCities.clear();
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			pStream->ReadString(szBuffer);
			m_aszDestroyedCities.push_back(szBuffer);
		}

		m_aszGreatPeopleBorn.clear();
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			pStream->ReadString(szBuffer);
			m_aszGreatPeopleBorn.push_back(szBuffer);
		}
	}

	ReadStreamableFFreeListTrashArray(m_deals, pStream);
	ReadStreamableFFreeListTrashArray(m_voteSelections, pStream);
	ReadStreamableFFreeListTrashArray(m_votesTriggered, pStream);

	m_mapRand.read(pStream);
	m_sorenRand.read(pStream);

	{
		clearReplayMessageMap();
		ReplayMessageList::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (ReplayMessageList::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvReplayMessage* pMessage = new CvReplayMessage(0);
			if (NULL != pMessage)
			{
				pMessage->read(*pStream);
			}
			m_listReplayMessages.push_back(pMessage);
		}
	}
	// m_pReplayInfo not saved

	pStream->Read(&m_iNumSessions);
	if (!isNetworkMultiPlayer())
	{
		++m_iNumSessions;
	}

	{
		int iSize;
		m_aPlotExtraYields.clear();
		pStream->Read(&iSize);
		for (int i = 0; i < iSize; ++i)
		{
			PlotExtraYield kPlotYield;
			kPlotYield.read(pStream);
			m_aPlotExtraYields.push_back(kPlotYield);
		}
	}

	{
		int iSize;
		m_aPlotExtraCosts.clear();
		pStream->Read(&iSize);
		for (int i = 0; i < iSize; ++i)
		{
			PlotExtraCost kPlotCost;
			kPlotCost.read(pStream);
			m_aPlotExtraCosts.push_back(kPlotCost);
		}
	}

	{
		int iSize;
		m_mapVoteSourceReligions.clear();
		pStream->Read(&iSize);
		for (int i = 0; i < iSize; ++i)
		{
			VoteSourceTypes eVoteSource;
			ReligionTypes eReligion;
			pStream->Read((int*)&eVoteSource);
			pStream->Read((int*)&eReligion);
			m_mapVoteSourceReligions[eVoteSource] = eReligion;
		}
	}

	{
		int iSize;
		m_aeInactiveTriggers.clear();
		pStream->Read(&iSize);
		for (int i = 0; i < iSize; ++i)
		{
			int iTrigger;
			pStream->Read(&iTrigger);
			m_aeInactiveTriggers.push_back((EventTriggerTypes)iTrigger);
		}
	}

	// Get the active player information from the initialization structure
	if (!isGameMultiPlayer())
	{
		for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isHuman())
			{
				setActivePlayer((PlayerTypes)iI);
				break;
			}
		}
		addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getActivePlayer(), gDLL->getText("TXT_KEY_MISC_RELOAD", m_iNumSessions));
	}

	if (isOption(GAMEOPTION_NEW_RANDOM_SEED))
	{
		if (!isNetworkMultiPlayer())
		{
			m_sorenRand.reseed(timeGetTime());
		}
	}

	pStream->Read(&m_iShrineBuildingCount);
	pStream->Read(GC.getNumBuildingInfos(), m_aiShrineBuilding);
	pStream->Read(GC.getNumBuildingInfos(), m_aiShrineReligion);
	pStream->Read(&m_iNumCultureVictoryCities);
	pStream->Read(&m_eCultureVictoryCultureLevel);

	// Leoreth: read civ history entries
	for (iI = 0; iI < NUM_HISTORY_TYPES; iI++)
	{
		m_aiCivilizationHistory[iI].clear();

		int iNumHistoryEntries;
		pStream->Read(&iNumHistoryEntries);

		for (int iJ = 0; iJ < iNumHistoryEntries; iJ++)
		{
			int iCivilization;
			pStream->Read(&iCivilization);

			int iNumCivilizationEntries;
			pStream->Read(&iNumCivilizationEntries);

			for (int iK = 0; iK < iNumCivilizationEntries; iK++)
			{
				int iTurn;
				int iValue;
				pStream->Read(&iTurn);
				pStream->Read(&iValue);

				setCivilizationHistory((HistoryTypes)iI, (CivilizationTypes)iCivilization, iTurn, iValue);
			}
		}
	}
}


void CvGame::write(FDataStreamBase* pStream)
{
	int iI;

	uint uiFlag=1;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iElapsedGameTurns);
	pStream->Write(m_iStartTurn);
	pStream->Write(m_iStartYear);
	pStream->Write(m_iEstimateEndTurn);
	pStream->Write(m_iTurnSlice);
	pStream->Write(m_iCutoffSlice);
	pStream->Write(m_iNumGameTurnActive);
	pStream->Write(m_iNumCities);
	pStream->Write(m_iTotalPopulation);
	pStream->Write(m_iTradeRoutes);
	pStream->Write(m_iFreeTradeCount);
	pStream->Write(m_iNoNukesCount);
	pStream->Write(m_iNukesExploded);
	pStream->Write(m_iMaxPopulation);
	pStream->Write(m_iMaxLand);
	pStream->Write(m_iMaxTech);
	pStream->Write(m_iMaxWonders);
	pStream->Write(m_iInitPopulation);
	pStream->Write(m_iInitLand);
	pStream->Write(m_iInitTech);
	pStream->Write(m_iInitWonders);
	pStream->Write(m_iAIAutoPlay);
	pStream->Write(m_iCircumnavigated); //Rhye
	pStream->Write(m_iMedianTechValue);

	// m_uiInitialTime not saved

	pStream->Write(m_bScoreDirty);
	pStream->Write(m_bCircumnavigated);
	// m_bDebugMode not saved
	pStream->Write(m_bFinalInitialized);
	// m_bPbemTurnSent not saved
	pStream->Write(m_bHotPbemBetweenTurns);
	// m_bPlayerOptionsSent not saved
	pStream->Write(m_bNukesValid);

	pStream->Write(m_eHandicap);
	pStream->Write(m_ePausePlayer);
	pStream->Write(m_eBestLandUnit);
	pStream->Write(m_eWinner);
	pStream->Write(m_eVictory);
	pStream->Write(m_eGameState);
	pStream->Write(m_eCityScreenOwner); // Leoreth
	pStream->Write(m_eGreatPeopleNotifications);
	pStream->Write(m_eReligionSpreadNotifications);
	pStream->Write(m_eEventEffectNotifications);

	pStream->WriteString(m_szScriptData);

	pStream->Write(MAX_PLAYERS, m_aiRankPlayer);
	pStream->Write(MAX_PLAYERS, m_aiPlayerRank);
	pStream->Write(MAX_PLAYERS, m_aiPlayerScore);
	pStream->Write(MAX_TEAMS, m_aiRankTeam);
	pStream->Write(MAX_TEAMS, m_aiTeamRank);
	pStream->Write(MAX_TEAMS, m_aiTeamScore);
	pStream->Write(NUM_CIVS, m_aiCivPeriod);

	// Leoreth
	pStream->Write(MAX_TEAMS, m_aiTechRankTeam);

	pStream->Write(GC.getNumUnitInfos(), m_paiUnitCreatedCount);
	pStream->Write(GC.getNumUnitClassInfos(), m_paiUnitClassCreatedCount);
	pStream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingClassCreatedCount);
	pStream->Write(GC.getNumProjectInfos(), m_paiProjectCreatedCount);
	pStream->Write(GC.getNumCivicInfos(), m_paiForceCivicCount);
	pStream->Write(GC.getNumVoteInfos(), (int*)m_paiVoteOutcome);
	pStream->Write(GC.getNumReligionInfos(), m_paiReligionGameTurnFounded);
	pStream->Write(GC.getNumCorporationInfos(), m_paiCorporationGameTurnFounded);
	pStream->Write(GC.getNumVoteSourceInfos(), m_aiSecretaryGeneralTimer);
	pStream->Write(GC.getNumVoteSourceInfos(), m_aiVoteTimer);
	pStream->Write(GC.getNumVoteSourceInfos(), m_aiDiploVote);

	pStream->Write(GC.getNumSpecialUnitInfos(), m_pabSpecialUnitValid);
	pStream->Write(GC.getNumSpecialBuildingInfos(), m_pabSpecialBuildingValid);
	pStream->Write(GC.getNumReligionInfos(), m_abReligionSlotTaken);

	// Leoreth
	pStream->Write(GC.getNumTechInfos(), m_aiFirstDiscovered);
	pStream->Write(GC.getNumTechInfos(), m_aiFirstDiscoveredTurn);

	for (iI=0;iI<GC.getNumReligionInfos();iI++)
	{
		pStream->Write(m_paHolyCity[iI].eOwner);
		pStream->Write(m_paHolyCity[iI].iID);
	}

	for (iI=0;iI<GC.getNumCorporationInfos();iI++)
	{
		pStream->Write(m_paHeadquarters[iI].eOwner);
		pStream->Write(m_paHeadquarters[iI].iID);
	}

	{
		std::vector<CvWString>::iterator it;

		pStream->Write(m_aszDestroyedCities.size());
		for (it = m_aszDestroyedCities.begin(); it != m_aszDestroyedCities.end(); it++)
		{
			pStream->WriteString(*it);
		}

		pStream->Write(m_aszGreatPeopleBorn.size());
		for (it = m_aszGreatPeopleBorn.begin(); it != m_aszGreatPeopleBorn.end(); it++)
		{
			pStream->WriteString(*it);
		}
	}

	WriteStreamableFFreeListTrashArray(m_deals, pStream);
	WriteStreamableFFreeListTrashArray(m_voteSelections, pStream);
	WriteStreamableFFreeListTrashArray(m_votesTriggered, pStream);

	m_mapRand.write(pStream);
	m_sorenRand.write(pStream);

	ReplayMessageList::_Alloc::size_type iSize = m_listReplayMessages.size();
	pStream->Write(iSize);
	ReplayMessageList::const_iterator it;
	for (it = m_listReplayMessages.begin(); it != m_listReplayMessages.end(); it++)
	{
		const CvReplayMessage* pMessage = *it;
		if (NULL != pMessage)
		{
			pMessage->write(*pStream);
		}
	}
	// m_pReplayInfo not saved

	pStream->Write(m_iNumSessions);

	pStream->Write(m_aPlotExtraYields.size());
	for (std::vector<PlotExtraYield>::iterator it = m_aPlotExtraYields.begin(); it != m_aPlotExtraYields.end(); ++it)
	{
		(*it).write(pStream);
	}

	pStream->Write(m_aPlotExtraCosts.size());
	for (std::vector<PlotExtraCost>::iterator it = m_aPlotExtraCosts.begin(); it != m_aPlotExtraCosts.end(); ++it)
	{
		(*it).write(pStream);
	}

	pStream->Write(m_mapVoteSourceReligions.size());
	for (stdext::hash_map<VoteSourceTypes, ReligionTypes>::iterator it = m_mapVoteSourceReligions.begin(); it != m_mapVoteSourceReligions.end(); ++it)
	{
		pStream->Write(it->first);
		pStream->Write(it->second);
	}

	pStream->Write(m_aeInactiveTriggers.size());
	for (std::vector<EventTriggerTypes>::iterator it = m_aeInactiveTriggers.begin(); it != m_aeInactiveTriggers.end(); ++it)
	{
		pStream->Write(*it);
	}

	pStream->Write(m_iShrineBuildingCount);
	pStream->Write(GC.getNumBuildingInfos(), m_aiShrineBuilding);
	pStream->Write(GC.getNumBuildingInfos(), m_aiShrineReligion);
	pStream->Write(m_iNumCultureVictoryCities);
	pStream->Write(m_eCultureVictoryCultureLevel);

	// Leoreth: civ history graph
	for (iI = 0; iI < NUM_HISTORY_TYPES; iI++)
	{
		hash_map<int, hash_map<int, int> > history = m_aiCivilizationHistory[iI];
		
		int iNumHistoryEntries = history.size();
		pStream->Write(iNumHistoryEntries);

		hash_map<int, hash_map<int, int> >::iterator historyIt;
		for (historyIt = history.begin(); historyIt != history.end(); historyIt++)
		{
			hash_map<int, int> entries = historyIt->second;

			int iNumCivilizationEntries = entries.size();
			pStream->Write(historyIt->first);
			pStream->Write(iNumCivilizationEntries);

			hash_map<int, int>::iterator entriesIt;
			for (entriesIt = entries.begin(); entriesIt != entries.end(); entriesIt++)
			{
				pStream->Write(entriesIt->first);
				pStream->Write(entriesIt->second);
			}
		}
	}
}

void CvGame::writeReplay(FDataStreamBase& stream, PlayerTypes ePlayer)
{
	SAFE_DELETE(m_pReplayInfo);
	m_pReplayInfo = new CvReplayInfo();
	if (m_pReplayInfo)
	{
		m_pReplayInfo->createInfo(ePlayer);

		m_pReplayInfo->write(stream);
	}
}

void CvGame::saveReplay(PlayerTypes ePlayer)
{
	gDLL->getEngineIFace()->SaveReplay(ePlayer);
}


void CvGame::showEndGameSequence()
{
	CvPopupInfo* pInfo;
	CvWString szBuffer;
	int iI;

	long iHours = getMinutesPlayed() / 60;
	long iMinutes = getMinutesPlayed() % 60;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		CvPlayer& player = GET_PLAYER((PlayerTypes)iI);
		if (player.isHuman())
		{
			addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, (PlayerTypes)iI, gDLL->getText("TXT_KEY_MISC_TIME_SPENT", iHours, iMinutes));

			pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
			if (NULL != pInfo)
			{
				if ((getWinner() != NO_TEAM) && (getVictory() != NO_VICTORY))
				{
					//Rhye - start
					//pInfo->setText(gDLL->getText("TXT_KEY_GAME_WON", GET_TEAM(getWinner()).getName().GetCString(), GC.getVictoryInfo(getVictory()).getTextKeyWide()));
					pInfo->setText(gDLL->getText("TXT_KEY_GAME_WON", GET_PLAYER((PlayerTypes)getWinner()).getCivilizationShortDescription(), GC.getVictoryInfo(getVictory()).getTextKeyWide()));
					//Rhye - end
				}
				else
				{
					//pInfo->setText(gDLL->getText("TXT_KEY_MISC_DEFEAT")); //Rhye
					pInfo->setText(gDLL->getText("TXT_KEY_MISC_DEFEAT2")); //Rhye
				}
				player.addPopup(pInfo);
			}

			if (getWinner() == player.getTeam())
			{
				if (!CvString(GC.getVictoryInfo(getVictory()).getMovie()).empty())
				{
					// show movie
					pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
					if (NULL != pInfo)
					{
						pInfo->setText(L"showVictoryMovie");
						pInfo->setData1((int)getVictory());
						player.addPopup(pInfo);
					}
				}
				else if (GC.getVictoryInfo(getVictory()).isDiploVote())
				{
					pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
					if (NULL != pInfo)
					{
						pInfo->setText(L"showUnVictoryScreen");
						player.addPopup(pInfo);
					}
				}
			}

			// show replay
			pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
			if (NULL != pInfo)
			{
				pInfo->setText(L"showReplay");
				pInfo->setData1(iI);
				pInfo->setOption1(false); // don't go to HOF on exit
				player.addPopup(pInfo);
			}

			// show top cities / stats
			pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
			if (NULL != pInfo)
			{
				pInfo->setText(L"showInfoScreen");
				pInfo->setData1(0);
				pInfo->setData2(1);
				player.addPopup(pInfo);
			}

			// show Dan
			pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
			if (NULL != pInfo)
			{
				pInfo->setText(L"showDanQuayleScreen");
				player.addPopup(pInfo);
			}

			// show Hall of Fame
			pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
			if (NULL != pInfo)
			{
				pInfo->setText(L"showHallOfFame");
				player.addPopup(pInfo);
			}
		}
	}
}

CvReplayInfo* CvGame::getReplayInfo() const
{
	return m_pReplayInfo;
}

void CvGame::setReplayInfo(CvReplayInfo* pReplay)
{
	SAFE_DELETE(m_pReplayInfo);
	m_pReplayInfo = pReplay;
}

bool CvGame::hasSkippedSaveChecksum() const
{
	return gDLL->hasSkippedSaveChecksum();
}

void CvGame::addPlayer(PlayerTypes eNewPlayer, LeaderHeadTypes eLeader, CivilizationTypes eCiv, int iBirthTurn, bool bAlive, bool bMinor)
{
	// UNOFFICIAL_PATCH Start
	// * Fixed bug with colonies who occupy recycled player slots showing the old leader or civ names.
	CvWString szEmptyString = L"";
	LeaderHeadTypes eOldLeader = GET_PLAYER(eNewPlayer).getLeaderType();
	if ( (eOldLeader != NO_LEADER) && (eOldLeader != eLeader) ) 
	{
		GC.getInitCore().setLeaderName(eNewPlayer, szEmptyString);
	}
	CivilizationTypes eOldCiv = GET_PLAYER(eNewPlayer).getCivilizationType();
	if ( (eOldCiv != NO_CIVILIZATION) && (eOldCiv != eCiv) ) 
	{
		GC.getInitCore().setCivAdjective(eNewPlayer, szEmptyString);
		GC.getInitCore().setCivDescription(eNewPlayer, szEmptyString);
		GC.getInitCore().setCivShortDesc(eNewPlayer, szEmptyString);
	}
	// UNOFFICIAL_PATCH End
	PlayerColorTypes eColor = (PlayerColorTypes)GC.getCivilizationInfo(eCiv).getDefaultPlayerColor();

	/*for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/30/08                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/* original bts code
		if (eColor == NO_PLAYERCOLOR || GET_PLAYER((PlayerTypes)iI).getPlayerColor() == eColor)
*/
		// Don't invalidate color choice if it's taken by this player
/*		if (eColor == NO_PLAYERCOLOR || (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getPlayerColor() == eColor && (PlayerTypes)iI != eNewPlayer) )
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
/*		{
			for (int iK = 0; iK < GC.getNumPlayerColorInfos(); iK++)
			{
				if (iK != GC.getCivilizationInfo((CivilizationTypes)GC.getDefineINT("BARBARIAN_CIVILIZATION")).getDefaultPlayerColor())
				{
					bool bValid = true;

					for (int iL = 0; iL < MAX_CIV_PLAYERS; iL++)
					{
						if (GET_PLAYER((PlayerTypes)iL).getPlayerColor() == iK)
						{
							bValid = false;
							break;
						}
					}

					if (bValid)
					{
						eColor = (PlayerColorTypes)iK;
						iI = MAX_CIV_PLAYERS;
						break;
					}
				}
			}
		}
	}*/

	TeamTypes eTeam = GET_PLAYER(eNewPlayer).getTeam();
	GC.getInitCore().setLeader(eNewPlayer, eLeader);
	GC.getInitCore().setCiv(eNewPlayer, eCiv);
	GC.getInitCore().setSlotStatus(eNewPlayer, SS_COMPUTER);
	GC.getInitCore().setColor(eNewPlayer, eColor);
	GET_TEAM(eTeam).init(eTeam);
	GET_PLAYER(eNewPlayer).init(eNewPlayer);
	
	if (iBirthTurn >= 0)
	{
		GET_PLAYER(eNewPlayer).setInitialBirthTurn(iBirthTurn);
	}

	GET_PLAYER(eNewPlayer).setAlive(bAlive, false);
	GET_PLAYER(eNewPlayer).setMinorCiv(bMinor);

	if (eCiv != NO_CIVILIZATION)
	{
		CvEventReporter::getInstance().playerCivAssigned(eNewPlayer, eCiv);
		addReplayMessage(REPLAY_MESSAGE_CIV_ASSIGNED, eNewPlayer, (char*)NULL, eCiv);
	}
}

bool CvGame::isCompetingCorporation(CorporationTypes eCorporation1, CorporationTypes eCorporation2) const
{
	// edead: start comment
	// bool bShareResources = false;

	// for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES() && !bShareResources; ++i)
	// {
		// if (GC.getCorporationInfo(eCorporation1).getPrereqBonus(i) != NO_BONUS)
		// {
			// for (int j = 0; j < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++j)
			// {
				// if (GC.getCorporationInfo(eCorporation2).getPrereqBonus(j) != NO_BONUS)
				// {
					// if (GC.getCorporationInfo(eCorporation1).getPrereqBonus(i) == GC.getCorporationInfo(eCorporation2).getPrereqBonus(j))
					// {
						// return true;
					// }
				// }
			// }
		// }
	// }
	// edead: end comment

	return false;
}

int CvGame::getPlotExtraYield(int iX, int iY, YieldTypes eYield) const
{
	for (std::vector<PlotExtraYield>::const_iterator it = m_aPlotExtraYields.begin(); it != m_aPlotExtraYields.end(); ++it)
	{
		if ((*it).m_iX == iX && (*it).m_iY == iY)
		{
			return (*it).m_aeExtraYield[eYield];
		}
	}

	return 0;
}

void CvGame::setPlotExtraYield(int iX, int iY, YieldTypes eYield, int iExtraYield)
{
	bool bFound = false;

	for (std::vector<PlotExtraYield>::iterator it = m_aPlotExtraYields.begin(); it != m_aPlotExtraYields.end(); ++it)
	{
		if ((*it).m_iX == iX && (*it).m_iY == iY)
		{
			(*it).m_aeExtraYield[eYield] += iExtraYield;
			bFound = true;
			break;
		}
	}

	if (!bFound)
	{
		PlotExtraYield kExtraYield;
		kExtraYield.m_iX = iX;
		kExtraYield.m_iY = iY;
		for (int i = 0; i < NUM_YIELD_TYPES; ++i)
		{
			if (eYield == i)
			{
				kExtraYield.m_aeExtraYield.push_back(iExtraYield);
			}
			else
			{
				kExtraYield.m_aeExtraYield.push_back(0);
			}
		}
		m_aPlotExtraYields.push_back(kExtraYield);
	}

	CvPlot* pPlot = GC.getMapINLINE().plot(iX, iY);
	if (NULL != pPlot)
	{
		pPlot->updateYield();
	}
}

void CvGame::removePlotExtraYield(int iX, int iY)
{
	for (std::vector<PlotExtraYield>::iterator it = m_aPlotExtraYields.begin(); it != m_aPlotExtraYields.end(); ++it)
	{
		if ((*it).m_iX == iX && (*it).m_iY == iY)
		{
			m_aPlotExtraYields.erase(it);
			break;
		}
	}

	CvPlot* pPlot = GC.getMapINLINE().plot(iX, iY);
	if (NULL != pPlot)
	{
		pPlot->updateYield();
	}
}

int CvGame::getPlotExtraCost(int iX, int iY) const
{
	for (std::vector<PlotExtraCost>::const_iterator it = m_aPlotExtraCosts.begin(); it != m_aPlotExtraCosts.end(); ++it)
	{
		if ((*it).m_iX == iX && (*it).m_iY == iY)
		{
			return (*it).m_iCost;
		}
	}

	return 0;
}

void CvGame::changePlotExtraCost(int iX, int iY, int iCost)
{
	bool bFound = false;

	for (std::vector<PlotExtraCost>::iterator it = m_aPlotExtraCosts.begin(); it != m_aPlotExtraCosts.end(); ++it)
	{
		if ((*it).m_iX == iX && (*it).m_iY == iY)
		{
			(*it).m_iCost += iCost;
			bFound = true;
			break;
		}
	}

	if (!bFound)
	{
		PlotExtraCost kExtraCost;
		kExtraCost.m_iX = iX;
		kExtraCost.m_iY = iY;
		kExtraCost.m_iCost = iCost;
		m_aPlotExtraCosts.push_back(kExtraCost);
	}
}

void CvGame::removePlotExtraCost(int iX, int iY)
{
	for (std::vector<PlotExtraCost>::iterator it = m_aPlotExtraCosts.begin(); it != m_aPlotExtraCosts.end(); ++it)
	{
		if ((*it).m_iX == iX && (*it).m_iY == iY)
		{
			m_aPlotExtraCosts.erase(it);
			break;
		}
	}
}

ReligionTypes CvGame::getVoteSourceReligion(VoteSourceTypes eVoteSource) const
{
	stdext::hash_map<VoteSourceTypes, ReligionTypes>::const_iterator it;

	it = m_mapVoteSourceReligions.find(eVoteSource);
	if (it == m_mapVoteSourceReligions.end())
	{
		return NO_RELIGION;
	}

	return it->second;
}

void CvGame::setVoteSourceReligion(VoteSourceTypes eVoteSource, ReligionTypes eReligion, bool bAnnounce)
{
	m_mapVoteSourceReligions[eVoteSource] = eReligion;

	if (bAnnounce)
	{
		if (NO_RELIGION != eReligion)
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_VOTE_SOURCE_RELIGION", GC.getReligionInfo(eReligion).getTextKeyWide(), GC.getReligionInfo(eReligion).getAdjectiveKey(), GC.getVoteSourceInfo(eVoteSource).getTextKeyWide());

			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getReligionInfo(eReligion).getSound(), MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
				}
			}
		}
	}
}


// CACHE: cache frequently used values
///////////////////////////////////////


int CvGame::getShrineBuildingCount(ReligionTypes eReligion)
{
	int	iShrineBuildingCount = 0;

	if (eReligion == NO_RELIGION)
		iShrineBuildingCount = m_iShrineBuildingCount;
	else for (int iI = 0; iI < m_iShrineBuildingCount; iI++)
		if (m_aiShrineReligion[iI] == eReligion)
			iShrineBuildingCount++;

	return iShrineBuildingCount;
}

BuildingTypes CvGame::getShrineBuilding(int eIndex, ReligionTypes eReligion)
{
	FAssertMsg(eIndex >= 0 && eIndex < m_iShrineBuildingCount, "invalid index to CvGame::getShrineBuilding");

	BuildingTypes eBuilding = NO_BUILDING;

	if (eIndex >= 0 && eIndex < m_iShrineBuildingCount)
	{
		if (eReligion == NO_RELIGION)
			eBuilding = (BuildingTypes) m_aiShrineBuilding[eIndex];
		else for (int iI = 0, iReligiousBuilding = 0; iI < m_iShrineBuildingCount; iI++)
			if (m_aiShrineReligion[iI] == (int) eReligion)
			{
				if (iReligiousBuilding == eIndex)
				{
					// found it
					eBuilding = (BuildingTypes) m_aiShrineBuilding[iI];
					break;
				}

				iReligiousBuilding++;
			}
	}

	return eBuilding;
}

void CvGame::changeShrineBuilding(BuildingTypes eBuilding, ReligionTypes eReligion, bool bRemove)
{
	FAssertMsg(eBuilding >= 0 && eBuilding < GC.getNumBuildingInfos(), "invalid index to CvGame::changeShrineBuilding");
	FAssertMsg(bRemove || m_iShrineBuildingCount < GC.getNumBuildingInfos(), "trying to add too many buildings to CvGame::changeShrineBuilding");

	if (bRemove)
	{
		bool bFound = false;

		for (int iI = 0; iI < m_iShrineBuildingCount; iI++)
		{
			if (!bFound)
			{
				// note, eReligion is not important if we removing, since each building is always one religion
				if (m_aiShrineBuilding[iI] == (int) eBuilding)
					bFound = true;
			}

			if (bFound)
			{
				int iToMove = iI + 1;
				if (iToMove < m_iShrineBuildingCount)
				{
					m_aiShrineBuilding[iI] = m_aiShrineBuilding[iToMove];
					m_aiShrineReligion[iI] = m_aiShrineReligion[iToMove];
				}
				else
				{
					m_aiShrineBuilding[iI] = (int) NO_BUILDING;
					m_aiShrineReligion[iI] = (int) NO_RELIGION;
				}
			}

		if (bFound)
			m_iShrineBuildingCount--;

		}
	}
	else if (m_iShrineBuildingCount < GC.getNumBuildingInfos())
	{
		// add this item to the end
		m_aiShrineBuilding[m_iShrineBuildingCount] = eBuilding;
		m_aiShrineReligion[m_iShrineBuildingCount] = eReligion;
		m_iShrineBuildingCount++;
	}

}

bool CvGame::culturalVictoryValid()
{
	if (m_iNumCultureVictoryCities > 0)
	{
		return true;
	}

	return false;
}

int CvGame::culturalVictoryNumCultureCities()
{
	return m_iNumCultureVictoryCities;
}

CultureLevelTypes CvGame::culturalVictoryCultureLevel()
{
	if (m_iNumCultureVictoryCities > 0)
	{
		return (CultureLevelTypes) m_eCultureVictoryCultureLevel;
	}

	return NO_CULTURELEVEL;
}

int CvGame::getCultureThreshold(CultureLevelTypes eLevel) const
{
	int iThreshold = GC.getCultureLevelInfo(eLevel).getSpeedThreshold(getGameSpeedType());
	if (isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		iThreshold *= 100 + GC.getDefineINT("NO_ESPIONAGE_CULTURE_LEVEL_MODIFIER");
		iThreshold /= 100;
	}
	return iThreshold;
}

void CvGame::doUpdateCacheOnTurn()
{
	int	iI;

	// reset shrine count
	m_iShrineBuildingCount = 0;

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		CvBuildingInfo&	kBuildingInfo = GC.getBuildingInfo((BuildingTypes) iI);

		// if it is for holy city, then its a shrine-thing, add it
		if (kBuildingInfo.getHolyCity() != NO_RELIGION)
		{
			changeShrineBuilding((BuildingTypes) iI, (ReligionTypes) kBuildingInfo.getReligionType());
		}
	}

	// reset cultural victories
	m_iNumCultureVictoryCities = 0;
	for (iI = 0; iI < GC.getNumVictoryInfos(); iI++)
	{
		if (isVictoryValid((VictoryTypes) iI))
		{
			CvVictoryInfo& kVictoryInfo = GC.getVictoryInfo((VictoryTypes) iI);
			if (kVictoryInfo.getCityCulture() > 0)
			{
				int iNumCultureCities = kVictoryInfo.getNumCultureCities();
				if (iNumCultureCities > m_iNumCultureVictoryCities)
				{
					m_iNumCultureVictoryCities = iNumCultureCities;
					m_eCultureVictoryCultureLevel = kVictoryInfo.getCityCulture();
				}
			}
		}
	}
}

VoteSelectionData* CvGame::getVoteSelection(int iID) const
{
	return ((VoteSelectionData*)(m_voteSelections.getAt(iID)));
}

VoteSelectionData* CvGame::addVoteSelection(VoteSourceTypes eVoteSource)
{
	VoteSelectionData* pData = ((VoteSelectionData*)(m_voteSelections.add()));

	if  (NULL != pData)
	{
		pData->eVoteSource = eVoteSource;

		for (int iI = 0; iI < GC.getNumVoteInfos(); iI++)
		{
			if (GC.getVoteInfo((VoteTypes)iI).isVoteSourceType(eVoteSource))
			{
				if (isChooseElection((VoteTypes)iI))
				{
					VoteSelectionSubData kData;
					kData.eVote = (VoteTypes)iI;
					kData.iCityId = -1;
					kData.ePlayer = NO_PLAYER;
					kData.eOtherPlayer = NO_PLAYER;

					if (GC.getVoteInfo(kData.eVote).isOpenBorders())
					{
						if (isValidVoteSelection(eVoteSource, kData))
						{
							kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_OPEN_BORDERS", getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource));
							pData->aVoteOptions.push_back(kData);
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isDefensivePact())
					{
						if (isValidVoteSelection(eVoteSource, kData))
						{
							kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_DEFENSIVE_PACT", getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource));
							pData->aVoteOptions.push_back(kData);
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isForcePeace())
					{
						for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
						{
							CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);

							if (kTeam1.isAlive())
							{
								kData.ePlayer = kTeam1.getLeaderID();

								if (isValidVoteSelection(eVoteSource, kData))
								{
									//kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_PEACE", kTeam1.getName().GetCString(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_PEACE", GET_PLAYER((PlayerTypes)iTeam1).getCivilizationDescriptionKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									pData->aVoteOptions.push_back(kData);
								}
							}
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isForceNoTrade())
					{
						for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
						{
							CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);

							if (kTeam1.isAlive())
							{
								kData.ePlayer = kTeam1.getLeaderID();

								if (isValidVoteSelection(eVoteSource, kData))
								{
									//kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_NO_TRADE", kTeam1.getName().GetCString(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_NO_TRADE", GET_PLAYER((PlayerTypes)iTeam1).getCivilizationDescriptionKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									pData->aVoteOptions.push_back(kData);
								}
							}
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isForceWar())
					{
						for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
						{
							CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);

							if (kTeam1.isAlive())
							{
								kData.ePlayer = kTeam1.getLeaderID();

								if (isValidVoteSelection(eVoteSource, kData))
								{
									CvWString textKey = eVoteSource == 0 ? "TXT_KEY_POPUP_ELECTION_FORCE_WAR" : "TXT_KEY_POPUP_ELECTION_FORCE_WAR_RELIGIOUS";

									//kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_WAR", kTeam1.getName().GetCString(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									kData.szText = gDLL->getText(textKey, GET_PLAYER((PlayerTypes)iTeam1).getCivilizationDescriptionKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									pData->aVoteOptions.push_back(kData);
								}
							}
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isAssignCity())
					{
						for (int iPlayer1 = 0; iPlayer1 < MAX_CIV_PLAYERS; ++iPlayer1)
						{
							CvPlayer& kPlayer1 = GET_PLAYER((PlayerTypes)iPlayer1);

							int iLoop;
							for (CvCity* pLoopCity = kPlayer1.firstCity(&iLoop); NULL != pLoopCity; pLoopCity = kPlayer1.nextCity(&iLoop))
							{
								for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
								{
									if (GET_PLAYER((PlayerTypes)iI).isMinorCiv())
									{
										continue;
									}

									if (pLoopCity->plot()->isCore((PlayerTypes)iI))
									{
										kData.ePlayer = (PlayerTypes)iPlayer1;
										kData.iCityId = pLoopCity->getID();
										kData.eOtherPlayer = (PlayerTypes)iI;

										if (isValidVoteSelection(eVoteSource, kData))
										{
											kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_ASSIGN_CITY", kPlayer1.getCivilizationAdjectiveKey(), pLoopCity->getNameKey(), GET_PLAYER(kData.eOtherPlayer).getCivilizationDescriptionKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
											pData->aVoteOptions.push_back(kData);
											continue;
										}
									}
								}

								PlayerTypes eNewOwner = pLoopCity->plot()->findHighestCulturePlayer();
								if (NO_PLAYER != eNewOwner)
								{
									kData.ePlayer = (PlayerTypes)iPlayer1;
									kData.iCityId =	pLoopCity->getID();
									kData.eOtherPlayer = eNewOwner;

									if (isValidVoteSelection(eVoteSource, kData))
									{
										//kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_ASSIGN_CITY", kPlayer1.getCivilizationAdjectiveKey(), pLoopCity->getNameKey(), GET_PLAYER(eNewOwner).getNameKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
										kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_ASSIGN_CITY", kPlayer1.getCivilizationAdjectiveKey(), pLoopCity->getNameKey(), GET_PLAYER(eNewOwner).getCivilizationDescriptionKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
										pData->aVoteOptions.push_back(kData);
									}
								}
							}
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isRevokeMembership())
					{
						for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
						{
							CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);

							if (kTeam1.isAlive())
							{
								kData.ePlayer = kTeam1.getLeaderID();

								if (isValidVoteSelection(eVoteSource, kData))
								{
									//kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_FORCE_WAR", kTeam1.getName().GetCString(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_EXCOMMUNICATION", GET_PLAYER((PlayerTypes)iTeam1).getCivilizationDescriptionKey(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									pData->aVoteOptions.push_back(kData);
								}
							}
						}
					}
					else if (GC.getVoteInfo(kData.eVote).getGoldPercent() > 0)
					{
						kData.ePlayer = GET_TEAM(GC.getGame().getSecretaryGeneral(eVoteSource)).getLeaderID();

						if (isValidVoteSelection(eVoteSource, kData))
						{
							kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_COLLECT_TITHE", getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource));
							pData->aVoteOptions.push_back(kData);
						}
					}
					else if (GC.getVoteInfo(kData.eVote).getEspionage() > 0)
					{
						kData.ePlayer = GET_TEAM(GC.getGame().getSecretaryGeneral(eVoteSource)).getLeaderID();

						for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
						{
							CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);

							if (kLoopPlayer.isMinorCiv())
							{
								continue;
							}

							bool bValid = false;
							for (int iJ =  0; iJ < NUM_RELIGIONS; iJ++)
							{
								if (kLoopPlayer.getReligionPopulation((ReligionTypes)iJ) > 0)
								{
									bValid = true;
									break;
								}
							}

							if (bValid)
							{
								kData.eOtherPlayer = kLoopPlayer.getID();

								if (isValidVoteSelection(eVoteSource, kData))
								{
									kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_INQUISITION", kLoopPlayer.getCivilizationShortDescription(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource));
									pData->aVoteOptions.push_back(kData);
								}
							}
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isDecolonize())
					{
						for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
						{
							PlayerTypes ePlayer = (PlayerTypes)iI;
							CvPlayer& kPlayer = GET_PLAYER(ePlayer);

							if (kPlayer.isMinorCiv())
							{
								continue;
							}

							if (kPlayer.getTeam() == getSecretaryGeneral(eVoteSource))
							{
								continue;
							}

							if (!kPlayer.isAlive())
							{
								continue;
							}

							if (kPlayer.countColonies() == 0)
							{
								continue;
							}

							int iBestID = -1;
							int iBestValue = MAX_INT;
							int iCurrentValue;

							int iLoop;
							for (CvCity* pLoopCity = kPlayer.firstCity(&iLoop); NULL != pLoopCity; pLoopCity = kPlayer.nextCity(&iLoop))
							{
								if (pLoopCity->plot()->isCore(ePlayer)) continue;
								if (pLoopCity->plot()->isOverseas(kPlayer.getCapitalCity()->plot())) continue;

								if (NO_PLAYER == pLoopCity->getLiberationPlayer(false))
								{
									iCurrentValue = pLoopCity->plot()->getSettlerValue(ePlayer);
									if (iBestID == -1 || iCurrentValue < iBestValue)
									{
										iBestID = pLoopCity->getID();
										iBestValue = iCurrentValue;
									}
								}
							}

							if (iBestID != -1)
							{
								kData.ePlayer = ePlayer;
								kData.iCityId = iBestID;
								kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_DECOLONIZE", kPlayer.getCity(iBestID)->getNameKey(), kPlayer.getCivilizationShortDescription(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
								pData->aVoteOptions.push_back(kData);
							}
						}
					}
					else if (GC.getVoteInfo(kData.eVote).isReleaseCivilization())
					{
						PlayerTypes ePlayer;
						CivilizationTypes eReleasableCivilization;

						for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
						{
							ePlayer = (PlayerTypes)iI;

							if (GET_PLAYER(ePlayer).isMinorCiv())
							{
								continue;
							}

							if (GET_PLAYER(ePlayer).getTeam() == getSecretaryGeneral(eVoteSource))
							{
								continue;
							}

							if (!GET_PLAYER(ePlayer).isAlive())
							{
								continue;
							}

							for (int iJ = 0; iJ < NUM_CIVS; iJ++)
							{
								eReleasableCivilization = (CivilizationTypes)iJ;

								if (isCivAlive(eReleasableCivilization)) continue;
								if (!canRespawn(eReleasableCivilization)) continue;

								int iCityLoop;
								int iNumCities = 0;

								for (CvCity* pLoopCity = GET_PLAYER(ePlayer).firstCity(&iCityLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(ePlayer).nextCity(&iCityLoop))
								{
									if (pLoopCity->isCore(eReleasableCivilization) && !pLoopCity->isCore(ePlayer) && !pLoopCity->isCapital())
									{
										++iNumCities;
									}
								}

								if (iNumCities > 1)
								{
									kData.ePlayer = ePlayer;
									kData.eOtherPlayer = (PlayerTypes)eReleasableCivilization;
									kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_RELEASE", GC.getCivilizationInfo(eReleasableCivilization).getText(), GET_PLAYER(ePlayer).getCivilizationAdjective(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource)); //Rhye
									pData->aVoteOptions.push_back(kData);
								}
							}
						}
					}
					else
					{
						kData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_OPTION", GC.getVoteInfo(kData.eVote).getTextKeyWide(), getVoteRequired(kData.eVote, eVoteSource), countPossibleVote(kData.eVote, eVoteSource));
						if (isVotePassed(kData.eVote))
						{
							kData.szText += gDLL->getText("TXT_KEY_POPUP_PASSED");
						}

						if (canDoResolution(eVoteSource, kData))
						{
							pData->aVoteOptions.push_back(kData);
						}
					}
				}
			}
		}

		if (0 == pData->aVoteOptions.size())
		{
			deleteVoteSelection(pData->getID());
			pData = NULL;
		}
	}

	return pData;
}

void CvGame::deleteVoteSelection(int iID)
{
	m_voteSelections.removeAt(iID);
}

VoteTriggeredData* CvGame::getVoteTriggered(int iID) const
{
	return ((VoteTriggeredData*)(m_votesTriggered.getAt(iID)));
}

VoteTriggeredData* CvGame::addVoteTriggered(const VoteSelectionData& kData, int iChoice)
{
	if (-1 == iChoice || iChoice >= (int)kData.aVoteOptions.size())
	{
		return NULL;
	}

	return addVoteTriggered(kData.eVoteSource, kData.aVoteOptions[iChoice]);
}

VoteTriggeredData* CvGame::addVoteTriggered(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kOptionData)
{
	VoteTriggeredData* pData = ((VoteTriggeredData*)(m_votesTriggered.add()));

	if (NULL != pData)
	{
		pData->eVoteSource = eVoteSource;
		pData->kVoteOption = kOptionData;

		for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iI);
			if (kPlayer.isVotingMember(eVoteSource))
			{
				if (kPlayer.isHuman())
				{
					CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DIPLOVOTE);
					if (NULL != pInfo)
					{
						pInfo->setData1(pData->getID());
						gDLL->getInterfaceIFace()->addPopup(pInfo, (PlayerTypes)iI);
					}
				}
				else
				{
					castVote(((PlayerTypes)iI), pData->getID(), GET_PLAYER((PlayerTypes)iI).AI_diploVote(kOptionData, eVoteSource, false));
				}
			}
		}
	}

	return pData;
}

void CvGame::deleteVoteTriggered(int iID)
{
	m_votesTriggered.removeAt(iID);
}

void CvGame::doVoteResults()
{
	int iLoop;
	for (VoteTriggeredData* pVoteTriggered = m_votesTriggered.beginIter(&iLoop); NULL != pVoteTriggered; pVoteTriggered = m_votesTriggered.nextIter(&iLoop))
	{
		CvWString szBuffer;
		CvWString szMessage;
		VoteTypes eVote = pVoteTriggered->kVoteOption.eVote;
		VoteSourceTypes eVoteSource = pVoteTriggered->eVoteSource;
		bool bPassed = false;

		if (!canDoResolution(eVoteSource, pVoteTriggered->kVoteOption))
		{
			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				CvPlayer& kPlayer = GET_PLAYER((PlayerTypes) iPlayer);
				if (kPlayer.isVotingMember(eVoteSource))
				{
					CvWString szMessage;
					szMessage.Format(L"%s: %s", gDLL->getText("TXT_KEY_ELECTION_CANCELLED").GetCString(), GC.getVoteInfo(eVote).getDescription());
					gDLL->getInterfaceIFace()->addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), szMessage, "AS2D_NEW_ERA", MESSAGE_TYPE_INFO, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
				}
			}
		}
		else
		{
			bool bAllVoted = true;
			for (int iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
			{
				PlayerTypes ePlayer = (PlayerTypes) iJ;

				// Leoreth: player triggering the election and their capitulated vassals can't vote
				if (GC.getVoteInfo(eVote).isVictory())
				{
					if (pVoteTriggered->kVoteOption.ePlayer == ePlayer || (GET_TEAM((TeamTypes)ePlayer).isVassal((TeamTypes)pVoteTriggered->kVoteOption.ePlayer) && GET_TEAM((TeamTypes)ePlayer).isCapitulated()))
					{
						continue;
					}
				}

				if (GET_PLAYER(ePlayer).isVotingMember(eVoteSource))
				{
					if (getPlayerVote(ePlayer, pVoteTriggered->getID()) == NO_PLAYER_VOTE)
					{
						//give player one more turn to submit vote
						setPlayerVote(ePlayer, pVoteTriggered->getID(), NO_PLAYER_VOTE_CHECKED);
						bAllVoted = false;
						break;
					}
					else if (getPlayerVote(ePlayer, pVoteTriggered->getID()) == NO_PLAYER_VOTE_CHECKED)
					{
						//default player vote to abstain
						setPlayerVote(ePlayer, pVoteTriggered->getID(), PLAYER_VOTE_ABSTAIN);
					}
				}
			}

			if (!bAllVoted)
			{
				continue;
			}

			if (isTeamVote(eVote))
			{
				TeamTypes eTeam = findHighestVoteTeam(*pVoteTriggered);

				if (NO_TEAM != eTeam)
				{
					bPassed = countVote(*pVoteTriggered, (PlayerVoteTypes)eTeam) >= getVoteRequired(eVote, eVoteSource);
				}

				szBuffer = GC.getVoteInfo(eVote).getDescription();

				if (eTeam != NO_TEAM)
				{
					szBuffer += NEWLINE + gDLL->getText("TXT_KEY_POPUP_DIPLOMATIC_VOTING_VICTORY", GET_TEAM(eTeam).getName().GetCString(), countVote(*pVoteTriggered, (PlayerVoteTypes)eTeam), getVoteRequired(eVote, eVoteSource), countPossibleVote(eVote, eVoteSource));
				}

				for (int iI = MAX_CIV_TEAMS; iI >= 0; --iI)
				{
					for (int iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isVotingMember(eVoteSource))
						{
							if (getPlayerVote(((PlayerTypes)iJ), pVoteTriggered->getID()) == (PlayerVoteTypes)iI)
							{
								szBuffer += NEWLINE + gDLL->getText("TXT_KEY_POPUP_VOTES_FOR", GET_PLAYER((PlayerTypes)iJ).getNameKey(), GET_TEAM((TeamTypes)iI).getName().GetCString(), GET_PLAYER((PlayerTypes)iJ).getVotes(eVote, eVoteSource));
							}
						}
					}
				}

				for (int iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
				{
					if (GET_PLAYER((PlayerTypes)iJ).isVotingMember(eVoteSource))
					{
						if (getPlayerVote(((PlayerTypes)iJ), pVoteTriggered->getID()) == PLAYER_VOTE_ABSTAIN)
						{
							szBuffer += NEWLINE + gDLL->getText("TXT_KEY_POPUP_ABSTAINS", GET_PLAYER((PlayerTypes)iJ).getNameKey(), GET_PLAYER((PlayerTypes)iJ).getVotes(eVote, eVoteSource));
						}
					}
				}

				if (NO_TEAM != eTeam && bPassed)
				{
					setVoteOutcome(*pVoteTriggered, (PlayerVoteTypes)eTeam);
				}
				else
				{
					setVoteOutcome(*pVoteTriggered, PLAYER_VOTE_ABSTAIN);
				}
			}
			else
			{
				bPassed = countVote(*pVoteTriggered, PLAYER_VOTE_YES) >= getVoteRequired(eVote, eVoteSource);

				// Defying resolution
				if (bPassed)
				{
					for (int iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
					{
						if (getPlayerVote((PlayerTypes)iJ, pVoteTriggered->getID()) == PLAYER_VOTE_NEVER)
						{
							// Leoreth: AP resolutions still pass if defied - espionage is the only exception
							if (getVoteSourceReligion(eVoteSource) == NO_RELIGION || GC.getVoteInfo(eVote).getEspionage() > 0)
							{
								bPassed = false;
							}

							GET_PLAYER((PlayerTypes)iJ).setDefiedResolution(eVoteSource, pVoteTriggered->kVoteOption);
						}
					}
				}

				if (bPassed)
				{
					for (int iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isVotingMember(eVoteSource))
						{
							if (getPlayerVote(((PlayerTypes)iJ), pVoteTriggered->getID()) == PLAYER_VOTE_YES)
							{
								GET_PLAYER((PlayerTypes)iJ).setEndorsedResolution(eVoteSource, pVoteTriggered->kVoteOption);
							}
						}
					}
				}

				szBuffer += NEWLINE + gDLL->getText((bPassed ? "TXT_KEY_POPUP_DIPLOMATIC_VOTING_SUCCEEDS" : "TXT_KEY_POPUP_DIPLOMATIC_VOTING_FAILURE"), GC.getVoteInfo(eVote).getTextKeyWide(), countVote(*pVoteTriggered, PLAYER_VOTE_YES), getVoteRequired(eVote, eVoteSource), countPossibleVote(eVote, eVoteSource));

				for (int iI = PLAYER_VOTE_NEVER; iI <= PLAYER_VOTE_YES; ++iI)
				{
					for (int iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isVotingMember(eVoteSource))
						{
							if (getPlayerVote(((PlayerTypes)iJ), pVoteTriggered->getID()) == (PlayerVoteTypes)iI)
							{
								switch ((PlayerVoteTypes)iI)
								{
								case PLAYER_VOTE_ABSTAIN:
									szBuffer += NEWLINE + gDLL->getText("TXT_KEY_POPUP_ABSTAINS", GET_PLAYER((PlayerTypes)iJ).getNameKey(), GET_PLAYER((PlayerTypes)iJ).getVotes(eVote, eVoteSource));
									break;
								case PLAYER_VOTE_NEVER:
									szBuffer += NEWLINE + gDLL->getText("TXT_KEY_POPUP_VOTES_YES_NO", GET_PLAYER((PlayerTypes)iJ).getNameKey(), L"TXT_KEY_POPUP_VOTE_NEVER", GET_PLAYER((PlayerTypes)iJ).getVotes(eVote, eVoteSource));
									break;
								case PLAYER_VOTE_NO:
									szBuffer += NEWLINE + gDLL->getText("TXT_KEY_POPUP_VOTES_YES_NO", GET_PLAYER((PlayerTypes)iJ).getNameKey(), L"TXT_KEY_POPUP_NO", GET_PLAYER((PlayerTypes)iJ).getVotes(eVote, eVoteSource));
									break;
								case PLAYER_VOTE_YES:
									szBuffer += NEWLINE + gDLL->getText("TXT_KEY_POPUP_VOTES_YES_NO", GET_PLAYER((PlayerTypes)iJ).getNameKey(), L"TXT_KEY_POPUP_YES", GET_PLAYER((PlayerTypes)iJ).getVotes(eVote, eVoteSource));
									break;
								default:
									FAssert(false);
									break;
								}
							}
						}
					}
				}

				setVoteOutcome(*pVoteTriggered, bPassed ? PLAYER_VOTE_YES : PLAYER_VOTE_NO);
			}

			for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iI);
				if (kPlayer.isHuman())
				{
					bool bShow = kPlayer.isVotingMember(pVoteTriggered->eVoteSource);

					if (bShow)
					{
						CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
						if (NULL != pInfo)
						{
							pInfo->setText(szBuffer);
							gDLL->getInterfaceIFace()->addPopup(pInfo, (PlayerTypes)iI);
						}
					}

					if (!bShow)
					{
						if (iI == pVoteTriggered->kVoteOption.ePlayer && GET_PLAYER(pVoteTriggered->kVoteOption.ePlayer).isVotingMember(pVoteTriggered->eVoteSource))
						{
							bShow = true;
						}
					}

					if (!bShow)
					{
						if (iI == pVoteTriggered->kVoteOption.eOtherPlayer && GET_PLAYER(pVoteTriggered->kVoteOption.eOtherPlayer).isVotingMember(pVoteTriggered->eVoteSource))
						{
							bShow = true;
						}
					}

					if (bShow && bPassed)
					{
						CvWString szMessage = gDLL->getText("TXT_KEY_VOTE_RESULTS", GC.getVoteSourceInfo(eVoteSource).getTextKeyWide(), pVoteTriggered->kVoteOption.szText.GetCString());
						gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szMessage, "AS2D_NEW_ERA", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
					}

				}
			}
		}

		if (!bPassed && GC.getVoteInfo(eVote).isSecretaryGeneral())
		{
			setSecretaryGeneralTimer(eVoteSource, 0);
		}

		deleteVoteTriggered(pVoteTriggered->getID());
	}
}

void CvGame::doVoteSelection()
{
	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
		VoteSourceTypes eVoteSource = (VoteSourceTypes)iI;

		if (isDiploVote(eVoteSource))
		{
			if (getVoteTimer(eVoteSource) > 0)
			{
				changeVoteTimer(eVoteSource, -1);
			}
			else
			{
				setVoteTimer(eVoteSource, (GC.getVoteSourceInfo(eVoteSource).getVoteInterval() * GC.getGameSpeedInfo(getGameSpeedType()).getVictoryDelayPercent()) / 100);

				for (int iTeam1 = 0; iTeam1 < MAX_CIV_TEAMS; ++iTeam1)
				{
					CvTeam& kTeam1 = GET_TEAM((TeamTypes)iTeam1);

					if (kTeam1.isAlive() && kTeam1.isVotingMember(eVoteSource))
					{
						for (int iTeam2 = iTeam1 + 1; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
						{
							CvTeam& kTeam2 = GET_TEAM((TeamTypes)iTeam2);

							if (kTeam2.isAlive() && kTeam2.isVotingMember(eVoteSource))
							{
								kTeam1.meet((TeamTypes)iTeam2, true);
							}
						}
					}
				}

				TeamTypes eSecretaryGeneral = getSecretaryGeneral(eVoteSource);
				PlayerTypes eSecretaryPlayer;

				if (eSecretaryGeneral != NO_TEAM)
				{
					eSecretaryPlayer = GET_TEAM(eSecretaryGeneral).getSecretaryID();
				}
				else
				{
					eSecretaryPlayer = NO_PLAYER;
				}

				bool bSecretaryGeneralVote = false;
				if (canHaveSecretaryGeneral(eVoteSource))
				{
					if (getSecretaryGeneralTimer(eVoteSource) > 0)
					{
						changeSecretaryGeneralTimer(eVoteSource, -1);
					}
					else
					{
						setSecretaryGeneralTimer(eVoteSource, GC.getDefineINT("DIPLO_VOTE_SECRETARY_GENERAL_INTERVAL"));

						for (int iJ = 0; iJ < GC.getNumVoteInfos(); iJ++)
						{
							if (GC.getVoteInfo((VoteTypes)iJ).isSecretaryGeneral() && GC.getVoteInfo((VoteTypes)iJ).isVoteSourceType(iI))
							{
								VoteSelectionSubData kOptionData;
								kOptionData.iCityId = -1;
								kOptionData.ePlayer = NO_PLAYER;
								kOptionData.eVote = (VoteTypes)iJ;
								kOptionData.szText = gDLL->getText("TXT_KEY_POPUP_ELECTION_OPTION", GC.getVoteInfo((VoteTypes)iJ).getTextKeyWide(), getVoteRequired((VoteTypes)iJ, eVoteSource), countPossibleVote((VoteTypes)iJ, eVoteSource));
								addVoteTriggered(eVoteSource, kOptionData);
								bSecretaryGeneralVote = true;
								break;
							}
						}
					}
				}

				if (!bSecretaryGeneralVote && eSecretaryGeneral != NO_TEAM && eSecretaryPlayer != NO_PLAYER)
				{
					VoteSelectionData* pData = addVoteSelection(eVoteSource);
					if (NULL != pData)
					{
						if (GET_PLAYER(eSecretaryPlayer).isHuman())
						{
							CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHOOSEELECTION);
							if (NULL != pInfo)
							{
								pInfo->setData1(pData->getID());
								gDLL->getInterfaceIFace()->addPopup(pInfo, eSecretaryPlayer);
							}
						}
						else
						{
							setVoteChosen(GET_TEAM(eSecretaryGeneral).AI_chooseElection(*pData), pData->getID());
						}
					}
					else
					{
						setVoteTimer(eVoteSource, 0);
					}
				}
			}
		}
	}
}

bool CvGame::isEventActive(EventTriggerTypes eTrigger) const
{
	for (std::vector<EventTriggerTypes>::const_iterator it = m_aeInactiveTriggers.begin(); it != m_aeInactiveTriggers.end(); ++it)
	{
		if (*it == eTrigger)
		{
			return false;
		}
	}

	return true;
}

void CvGame::initEvents()
{
	for (int iTrigger = 0; iTrigger < GC.getNumEventTriggerInfos(); ++iTrigger)
	{
		if (isOption(GAMEOPTION_NO_EVENTS) || getSorenRandNum(100, "Event Active?") >= GC.getEventTriggerInfo((EventTriggerTypes)iTrigger).getPercentGamesActive())
		{
			m_aeInactiveTriggers.push_back((EventTriggerTypes)iTrigger);
		}
	}
}

bool CvGame::isCivEverActive(CivilizationTypes eCivilization) const
{
	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.isEverAlive())
		{
			if (kLoopPlayer.getCivilizationType() == eCivilization)
			{
				return true;
			}
		}
	}

	return false;
}

bool CvGame::isLeaderEverActive(LeaderHeadTypes eLeader) const
{
	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.isEverAlive())
		{
			if (kLoopPlayer.getLeaderType() == eLeader)
			{
				return true;
			}
		}
	}

	return false;
}

bool CvGame::isUnitEverActive(UnitTypes eUnit) const
{
	for (int iCiv = 0; iCiv < GC.getNumCivilizationInfos(); ++iCiv)
	{
		if (isCivEverActive((CivilizationTypes)iCiv))
		{
			if (eUnit == GC.getCivilizationInfo((CivilizationTypes)iCiv).getCivilizationUnits(GC.getUnitInfo(eUnit).getUnitClassType()))
			{
				return true;
			}
		}
	}

	return false;
}

bool CvGame::isBuildingEverActive(BuildingTypes eBuilding) const
{
	for (int iCiv = 0; iCiv < GC.getNumCivilizationInfos(); ++iCiv)
	{
		if (isCivEverActive((CivilizationTypes)iCiv))
		{
			if (eBuilding == GC.getCivilizationInfo((CivilizationTypes)iCiv).getCivilizationBuildings(GC.getBuildingInfo(eBuilding).getBuildingClassType()))
			{
				return true;
			}
		}
	}

	return false;
}

void CvGame::processBuilding(BuildingTypes eBuilding, int iChange)
{
	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
		if (GC.getBuildingInfo(eBuilding).getVoteSourceType() == (VoteSourceTypes)iI)
		{
			changeDiploVote((VoteSourceTypes)iI, iChange);
		}
	}
}

bool CvGame::pythonIsBonusIgnoreLatitudes() const
{
	long lResult = -1;
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "isBonusIgnoreLatitude", NULL, &lResult))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl() && lResult != -1)
		{
			return (lResult != 0);
		}
	}

	return false;
}


// BUFFY - Security Checks - start
#ifdef _BUFFY
// from HOF Mod - Dianthus
int CvGame::checkCRCs(std::string fileName_, std::string expectedModCRC_, std::string expectedDLLCRC_, std::string expectedShaderCRC_, std::string expectedPythonCRC_, std::string expectedXMLCRC_) const
{
	return 0;
}

// from HOF Mod - Denniz 3.17
int CvGame::getWarningStatus() const
{
	return 0;
}
#endif
// BUFFY - Security Checks - end

// Leoreth
bool CvGame::isNeighbors(PlayerTypes ePlayer1, PlayerTypes ePlayer2) const
{
	return (GET_PLAYER(ePlayer1).AI_calculateStolenCityRadiusPlots(ePlayer2) > 0 || GET_PLAYER(ePlayer2).AI_calculateStolenCityRadiusPlots(ePlayer1) > 0);
}

// Leoreth
TeamTypes CvGame::determineWinner(TeamTypes eTeam1, TeamTypes eTeam2) const
{
	return (GET_TEAM(eTeam1).AI_endWarVal(eTeam2) < GET_TEAM(eTeam2).AI_endWarVal(eTeam1)) ? eTeam1 : eTeam2;
}

// Leoreth: graphics paging

int CvGame::getXResolution() const
{
	return m_iXResolution;
}

void CvGame::setXResolution(int iNewValue)
{
	m_iXResolution = iNewValue;
}

void CvGame::changeXResolution(int iChange)
{
	setXResolution(getXResolution() + iChange);
}

int CvGame::getYResolution() const
{
	return m_iYResolution;
}

void CvGame::setYResolution(int iNewValue)
{
	m_iYResolution = iNewValue;
}

void CvGame::changeYResolution(int iChange)
{
	setYResolution(getYResolution() + iChange);
}

void CvGame::autosave(bool bInitial)
{
	gDLL->getEngineIFace()->AutoSave(bInitial);
}

bool CvGame::isPlayerAutoplay(PlayerTypes ePlayer)
{
	if (ePlayer == NO_PLAYER)
	{
		ePlayer = getActivePlayer();
	}

	return getGameTurnYear() < GC.getCivilizationInfo(GET_PLAYER(ePlayer).getCivilizationType()).getStartingYear();
}

void CvGame::setCityScreenOwner(PlayerTypes ePlayer)
{
	m_eCityScreenOwner = ePlayer;
}

void CvGame::resetCityScreenOwner()
{
	setCityScreenOwner(NO_PLAYER);
}

PlayerTypes CvGame::getCityScreenOwner() const
{
	return m_eCityScreenOwner;
}

bool CvGame::isNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer, NotificationLevels eNotificationLevel) const
{
	switch (eNotificationLevel)
	{
	case NOTIFICATIONS_ALL:
		return true;
	case NOTIFICATIONS_KNOWN:
		return eNotifiedPlayer == eCausingPlayer || GET_PLAYER(eNotifiedPlayer).canContact(eCausingPlayer);
	case NOTIFICATIONS_NEARBY:
		return isNeighbors(eNotifiedPlayer, eCausingPlayer);
	case NOTIFICATIONS_OURS:
		return eNotifiedPlayer == eCausingPlayer;
	}

	return true;
}

NotificationLevels CvGame::getGreatPeopleNotifications() const
{
	return m_eGreatPeopleNotifications;
}

void CvGame::setGreatPeopleNotifications(NotificationLevels eNotificationLevel)
{
	m_eGreatPeopleNotifications = eNotificationLevel;
}

bool CvGame::isGreatPeopleNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const
{
	return isNotification(eNotifiedPlayer, eCausingPlayer, getGreatPeopleNotifications());
}

NotificationLevels CvGame::getReligionSpreadNotifications() const
{
	return m_eReligionSpreadNotifications;
}

void CvGame::setReligionSpreadNotifications(NotificationLevels eNotificationLevel)
{
	m_eReligionSpreadNotifications = eNotificationLevel;
}

bool CvGame::isReligionSpreadNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const
{
	return isNotification(eNotifiedPlayer, eCausingPlayer, getReligionSpreadNotifications());
}

NotificationLevels CvGame::getEventEffectNotifications() const
{
	return m_eEventEffectNotifications;
}

void CvGame::setEventEffectNotifications(NotificationLevels eNotificationLevel)
{
	m_eEventEffectNotifications = eNotificationLevel;
}

bool CvGame::isEventEffectNotification(PlayerTypes eNotifiedPlayer, PlayerTypes eCausingPlayer) const
{
	return isNotification(eNotifiedPlayer, eCausingPlayer, getEventEffectNotifications());
}

PeriodTypes CvGame::getPeriod(CivilizationTypes eCivilization) const
{
	if (eCivilization < NUM_CIVS)
	{
		return (PeriodTypes)m_aiCivPeriod[eCivilization];
	}

	return NO_PERIOD;
}

void CvGame::setPeriod(CivilizationTypes eCivilization, PeriodTypes ePeriod)
{
	if (getPeriod(eCivilization) != ePeriod)
	{
		m_aiCivPeriod[eCivilization] = ePeriod;

		// Leoreth: update for Inca UP
		if (isFinalInitialized() && eCivilization == INCA)
		{
			for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
			{
				CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

				pLoopPlot->updateYield();
				pLoopPlot->setLayoutDirty(true);
			}
		}
	}
}

void CvGame::setCivilizationHistory(HistoryTypes eHistory, CivilizationTypes eCivilization, int iTurn, int iValue)
{
	if (eCivilization == NO_CIVILIZATION)
	{
		return;
	}

	hash_map<int, hash_map<int, int> >::iterator it = m_aiCivilizationHistory[eHistory].find(eCivilization);
	if (it == m_aiCivilizationHistory[eHistory].end())
	{
		hash_map<int, int> civilizationHistory;
		civilizationHistory.insert(pair<int, int>(iTurn, iValue));
		m_aiCivilizationHistory[eHistory].insert(std::pair<int, hash_map<int, int> >(eCivilization, civilizationHistory));
	} 
	else
	{
		it->second.insert(pair<int, int>(iTurn, iValue));
	}
}

int CvGame::getCivilizationHistory(HistoryTypes eHistory, CivilizationTypes eCivilization, int iTurn) const
{
	hash_map<int, hash_map<int, int> >::iterator it = m_aiCivilizationHistory[eHistory].find(eCivilization);
	if (it != m_aiCivilizationHistory[eHistory].end())
	{
		hash_map<int, int>::iterator entryIt = it->second.find(iTurn);

		if (entryIt != it->second.end())
		{
			return entryIt->second;
		}
	}

	return 0;
}

CivilizationTypes CvGame::getFirstDiscovered(TechTypes eTech) const
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());

	return (CivilizationTypes)m_aiFirstDiscovered[eTech];
}

void CvGame::setFirstDiscovered(TechTypes eTech, CivilizationTypes eCiv)
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());
	FAssert(eCiv > NO_CIVILIZATION);
	FAssert(eCiv < NUM_CIVS);

	m_aiFirstDiscovered[eTech] = eCiv;
}

int CvGame::getFirstDiscoveredTurn(TechTypes eTech) const
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());

	return m_aiFirstDiscoveredTurn[eTech];
}

void CvGame::setFirstDiscoveredTurn(TechTypes eTech, int iTurn)
{
	FAssert(eTech > NO_TECH);
	FAssert(eTech < GC.getNumTechInfos());

	m_aiFirstDiscoveredTurn[eTech] = iTurn;
}