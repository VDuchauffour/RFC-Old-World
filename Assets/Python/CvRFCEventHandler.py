from CvPythonExtensions import *
import CvUtil
import PyHelpers 
import Popup as PyPopup 

from StoredData import sd # edead
import RiseAndFall        
import Barbs                
import Religions        
import Resources        
import CityNameManager as cnm
import UniquePowers     
import AIWars           
import Congresses as cong
import Consts as con 
import RFCUtils
utils = RFCUtils.RFCUtils()
import CvScreenEnums #Rhye
import Victory as vic
import Stability as sta
import Plague
import Communications
import Companies
import DynamicCivs
        

gc = CyGlobalContext()        
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()

#Rhye - start
iEgypt = con.iEgypt
iIndia = con.iIndia
iChina = con.iChina
iBabylonia = con.iBabylonia
iGreece = con.iGreece
iPersia = con.iPersia
iCarthage = con.iCarthage
iRome = con.iRome
iTamils = con.iTamils
iJapan = con.iJapan
iEthiopia = con.iEthiopia
iKorea = con.iKorea
iMaya = con.iMaya
iByzantium = con.iByzantium
iVikings = con.iVikings
iArabia = con.iArabia
iTibet = con.iTibet
iKhmer = con.iKhmer
iIndonesia = con.iIndonesia
iMoors = con.iMoors
iSpain = con.iSpain
iFrance = con.iFrance
iEngland = con.iEngland
iHolyRome = con.iHolyRome
iRussia = con.iRussia
iNetherlands = con.iNetherlands
iHolland = con.iHolland
iMali = con.iMali
iPoland = con.iPoland
iPortugal = con.iPortugal
iInca = con.iInca
iItaly = con.iItaly
iMongolia = con.iMongolia
iAztecs = con.iAztecs
iMughals = con.iMughals
iTurkey = con.iTurkey
iThailand = con.iThailand
iCongo = con.iCongo
iGermany = con.iGermany
iAmerica = con.iAmerica
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNative = con.iNative
iCeltia = con.iCeltia
iSeljuks = con.iSeljuks
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers
#Rhye - end

class CvRFCEventHandler:

	def __init__(self, eventManager):

                self.EventKeyDown=6

                # initialize base class
                eventManager.addEventHandler("GameStart", self.onGameStart) #Stability
                eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn) #Stability
                eventManager.addEventHandler("cityAcquired", self.onCityAcquired) #Stability
                eventManager.addEventHandler("cityRazed", self.onCityRazed) #Stability
                eventManager.addEventHandler("cityBuilt", self.onCityBuilt) #Stability
                eventManager.addEventHandler("combatResult", self.onCombatResult) #Stability
                eventManager.addEventHandler("changeWar", self.onChangeWar)
                eventManager.addEventHandler("religionFounded",self.onReligionFounded) #Victory
                eventManager.addEventHandler("buildingBuilt",self.onBuildingBuilt) #Victory
                eventManager.addEventHandler("projectBuilt",self.onProjectBuilt) #Victory
                eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
                eventManager.addEventHandler("kbdEvent",self.onKbdEvent)
                eventManager.addEventHandler("OnLoad",self.onLoadGame) #edead: StoredData
                eventManager.addEventHandler("techAcquired",self.onTechAcquired) #Stability
                eventManager.addEventHandler("religionSpread",self.onReligionSpread) #Stability
                eventManager.addEventHandler("firstContact",self.onFirstContact)
                eventManager.addEventHandler("OnPreSave",self.onPreSave) #edead: StoredData
		eventManager.addEventHandler("vassalState", self.onVassalState)
		eventManager.addEventHandler("revolution", self.onRevolution)
		eventManager.addEventHandler("cityGrowth", self.onCityGrowth)
		eventManager.addEventHandler("unitPillage", self.onUnitPillage)
		eventManager.addEventHandler("cityCaptureGold", self.onCityCaptureGold)
		eventManager.addEventHandler("playerGoldTrade", self.onPlayerGoldTrade)
		eventManager.addEventHandler("tradeMission", self.onTradeMission)
		eventManager.addEventHandler("playerSlaveTrade", self.onPlayerSlaveTrade)
		eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)
		                
		#Leoreth
		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
		eventManager.addEventHandler("unitCreated", self.onUnitCreated)
		eventManager.addEventHandler("unitBuilt", self.onUnitBuilt)
		eventManager.addEventHandler("plotFeatureRemoved", self.onPlotFeatureRemoved)
		eventManager.addEventHandler("goldenAge", self.onGoldenAge)
		eventManager.addEventHandler("releasedPlayer", self.onReleasedPlayer)
		eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept)
		eventManager.addEventHandler("blockade", self.onBlockade)
		eventManager.addEventHandler("peaceBrokered", self.onPeaceBrokered)
		eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
               
                self.eventManager = eventManager

                self.rnf = RiseAndFall.RiseAndFall()
                self.barb = Barbs.Barbs()
                self.rel = Religions.Religions()
                self.res = Resources.Resources()
                self.up = UniquePowers.UniquePowers()
                self.aiw = AIWars.AIWars()
                self.pla = Plague.Plague()
                self.com = Communications.Communications()
                self.corp = Companies.Companies()

		self.dc = DynamicCivs.DynamicCivs()

        def onGameStart(self, argsList):
                'Called at the start of the game'
		
		sd.setup() # edead
                self.rnf.setup()
                self.rel.setup()
                self.pla.setup()
		self.dc.setup()
                self.aiw.setup()
		
		vic.setup()
		cong.setup()
		
		# area debug
		#sContinentDebug = ""
		#for y in range(con.iWorldY-1, 0, -1):
		#	for x in range(con.iWorldX):
		#		sContinentDebug += str(gc.getMap().plot(x, y).getArea()) + ", "
		#	sContinentDebug += "\n"
		##print sContinentDebug
		
		

		for i in range(con.iNumUnits):
			print gc.getUnitInfo(i).getText()
			
		for i in range(con.iNumBuildings):
			print gc.getBuildingInfo(i).getText()
		
		# Leoreth: set DLL core values
		for x in range(124):
			for y in range(68):
				plot = gc.getMap().plot(x, y)
				if plot.isWater(): continue
				for iPlayer in range(con.iNumPlayers):
					if utils.isPlotInArea((x, y), con.tCoreAreasTL[0][iPlayer], con.tCoreAreasBR[0][iPlayer], con.tExceptions[0][iPlayer]):
						plot.setCore(iPlayer, False, True)
					if utils.isPlotInArea((x, y), con.tCoreAreasTL[1][iPlayer], con.tCoreAreasBR[1][iPlayer], con.tExceptions[1][iPlayer]):
						plot.setCore(iPlayer, True, True)
                
                return 0


        def onCityAcquired(self, argsList):
		iOwner, iPlayer, city, bConquest, bTrade = argsList
                
		cnm.onCityAcquired(city, iPlayer)
		
		if bConquest:
			sta.onCityAcquired(city, iOwner, iPlayer)
			
		if iPlayer == con.iArabia:
			self.up.arabianUP(city)
		elif iPlayer == con.iMughals and utils.getHumanID() != con.iMughals:
			self.up.mughalUP(city)
		elif iPlayer == con.iSeljuks:
			self.up.seljukUP(city)
			
		if iPlayer == con.iMongolia and bConquest and utils.getHumanID() != iPlayer:
			self.up.mongolUP(city)
			
                if iPlayer < iNumMajorPlayers:
			utils.spreadMajorCulture(iPlayer, city.getX(), city.getY())
		
		# relocate capitals
		if utils.getHumanID() != iPlayer:
			if iPlayer == con.iTurkey and (city.getX(), city.getY()) == (68, 45):
				utils.moveCapital(con.iTurkey, (68, 45)) # Kostantiniyye
			elif iPlayer == con.iMongolia and (city.getX(), city.getY()) == (102, 47):
				utils.moveCapital(con.iMongolia, (102, 47)) # Khanbaliq
				
		# remove slaves if unable to practice slavery
		if gc.getPlayer(iPlayer).getCivics(1) == con.iCivicEgalitarianism:
			utils.removeSlaves(city)
		else:
			utils.freeSlaves(city, iPlayer)
					
							
		# kill Seljuks
		#if iOwner == iSeljuks and gc.getPlayer(iSeljuks).isAlive() and gc.getGame().getGameTurnYear() >= 1250:
		#	if city.isCapital() or gc.getPlayer(iSeljuks).getNumCities() <= 2:
		#		sta.completeCollapse(iSeljuks)
				#utils.killAndFragmentCiv(iSeljuks, iIndependent, iIndependent2, -1, False)
				
		# Leoreth: relocate capital for AI if reacquired:
		if utils.getHumanID() != iPlayer and iPlayer < con.iNumPlayers:
			tCity = (city.getX(), city.getY())
			if sd.scriptDict['lResurrections'][iPlayer] == 0:
				if tCity == con.tCapitals[utils.getReborn(iPlayer)][iPlayer]:
					utils.relocateCapital(iPlayer, city)
			else:
				if tCity == con.tRespawnCapitals[iPlayer]:
					utils.relocateCapital(iPlayer, city)
					
		# Leoreth: conquering Constantinople adds it to the Turkish core + Rumelia
		if iPlayer == con.iTurkey and (city.getX(), city.getY()) == (68, 45):
			if not utils.isReborn(con.iTurkey): gc.getPlayer(con.iTurkey).setReborn(True)
					
		# Leoreth: help Byzantium/Constantinople
		if iPlayer == con.iByzantium and (city.getX(), city.getY()) == con.tCapitals[0][con.iByzantium] and gc.getGame().getGameTurn() <= getTurnForYear(330)+3:
			if city.getPopulation() < 5:
				city.setPopulation(5)
				
			city.setHasRealBuilding(con.iBarracks, True)
			city.setHasRealBuilding(con.iWalls, True)
			city.setHasRealBuilding(con.iLibrary, True)
			city.setHasRealBuilding(con.iMarket, True)
			city.setHasRealBuilding(con.iGranary, True)
			city.setHasRealBuilding(con.iHarbor, True)
			city.setHasRealBuilding(con.iForge, True)
			
			city.setName("Konstantinoupolis", False)
			
			city.setHasRealBuilding(con.iJewishTemple + 4*gc.getPlayer(iPlayer).getStateReligion(), True)
			
		if bConquest:

			# Colombian UP: no resistance in conquered cities in Latin America
			if iPlayer == con.iMaya and utils.isReborn(con.iMaya):
				if utils.isPlotInArea((city.getX(), city.getY()), con.tSouthCentralAmericaTL, con.tSouthCentralAmericaBR):
					city.setOccupationTimer(0)
					
			# Statue of Zeus effect: no city resistance on conquest
			if gc.getPlayer(iPlayer).countNumBuildings(con.iStatueOfZeus) > 0 and not gc.getTeam(iPlayer).isHasTech(con.iTheology):
				city.setOccupationTimer(0)
				
			# Byzantium reduced to four cities: core shrinks to Constantinople
			if iOwner == con.iByzantium and gc.getPlayer(con.iByzantium).getNumCities <= 4:
				gc.getPlayer(con.iByzantium).setReborn(True)
					
		if bTrade:
			for i in range(con.iNumBuildings):
				iNationalWonder = i
				if isNationalWonderClass(gc.getBuildingInfo(iNationalWonder).getBuildingClassType()) and city.hasBuilding(iNationalWonder):
					city.setHasRealBuilding(iNationalWonder, False)
					
		self.pla.onCityAcquired(iOwner, iPlayer, city) # Plague
		self.com.onCityAcquired(city) # Communications
		self.corp.onCityAcquired(argsList) # Companies
		self.dc.onCityAcquired(argsList) # DynamicCivs
		
		vic.onCityAcquired(iPlayer, iOwner, city, bConquest)
                
                return 0
		
	def onCityAcquiredAndKept(self, argsList):
		iPlayer, city = argsList
		iOwner = city.getPreviousOwner()
		
		#utils.debugTextPopup('City acquired and kept: ' + city.getName() + '\nPlayer: ' + gc.getPlayer(iPlayer).getCivilizationShortDescription(0) + '\nOwner: ' + gc.getPlayer(iOwner).getCivilizationShortDescription(0))
		
		lTradingCompanyList = [con.iSpain, con.iFrance, con.iEngland, con.iPortugal, con.iNetherlands]
			
		if iPlayer == con.iSeljuks or gc.getPlayer(iPlayer).isHasBuildingEffect(con.iTopkapiPalace):
			self.up.turkishUP(city, iPlayer, iOwner)
		elif iPlayer in lTradingCompanyList and (city.getX(), city.getY()) in con.tTradingCompanyPlotLists[lTradingCompanyList.index(iPlayer)]:
			self.up.tradingCompanyCulture(city, iPlayer, iOwner)
		else:
			utils.cityConquestCulture(city, iPlayer, iOwner)

        def onCityRazed(self, argsList):
                city, iPlayer = argsList

                self.dc.onCityRazed(argsList)
		self.pla.onCityRazed(city,iPlayer) #Plague
                        
                vic.onCityRazed(iPlayer, city)	
		sta.onCityRazed(iPlayer, city)

        def onCityBuilt(self, argsList):
                city = argsList[0]
                iOwner = city.getOwner()
                
                if iOwner < con.iNumActivePlayers: 
                        cnm.onCityBuilt(city)
			
		# starting workers
		if gc.getPlayer(iOwner).getNumCities() == 1:
			self.rnf.createStartingWorkers(iOwner, (city.getX(), city.getY()))

		#Rhye - delete culture of barbs and minor civs to prevent weird unhappiness
                pCurrent = gc.getMap().plot( city.getX(), city.getY() )
                for i in range(con.iNumTotalPlayers - con.iNumActivePlayers):
                        iMinorCiv = i + con.iNumActivePlayers
                        pCurrent.setCulture(iMinorCiv, 0, True)
                pCurrent.setCulture(con.iBarbarian, 0, True)

                if iOwner < iNumMajorPlayers:
                        utils.spreadMajorCulture(iOwner, city.getX(), city.getY())
			if gc.getPlayer(iOwner).getNumCities() < 2:
				gc.getPlayer(iOwner).AI_updateFoundValues(False); # fix for settler maps not updating after 1st city is founded

		if iOwner == con.iTurkey:
                        self.up.turkishUP(city, iOwner, -1)
			
		if iOwner == con.iCarthage:
			if city.getX() == 58 and city.getY() == 39:
				if not gc.getPlayer(con.iCarthage).isHuman():
					x = gc.getPlayer(con.iCarthage).getCapitalCity().getX()
					y = gc.getPlayer(con.iCarthage).getCapitalCity().getY()
					carthage = gc.getMap().plot(58,39).getPlotCity()
					carthage.setHasRealBuilding(con.iPalace, True)
					gc.getMap().plot(x,y).getPlotCity().setHasRealBuilding(con.iPalace, False)
					
					carthage.setPopulation(3)
					
					utils.makeUnitAI(con.iWorkboat, con.iCarthage, (58, 39), UnitAITypes.UNITAI_WORKER_SEA, 1)
					utils.makeUnitAI(con.iGalley, con.iCarthage, (57, 40), UnitAITypes.UNITAI_SETTLER_SEA, 1)
					utils.makeUnitAI(con.iSettler, con.iCarthage, (57, 40), UnitAITypes.UNITAI_SETTLE, 1)
					
				if not utils.isReborn(iOwner): gc.getPlayer(con.iCarthage).setReborn(True)
					
				self.dc.setCivAdjective(iOwner, "TXT_KEY_CIV_CARTHAGE_ADJECTIVE")
				self.dc.setCivShortDesc(iOwner, "TXT_KEY_CIV_CARTHAGE_SHORT_DESC")
				
		if iOwner == con.iByzantium and (city.getX(), city.getY()) == con.tCapitals[0][con.iByzantium] and gc.getGame().getGameTurn() <= getTurnForYear(330)+3:
			if city.getPopulation() < 5:
				city.setPopulation(5)
				
			city.setHasRealBuilding(con.iBarracks, True)
			city.setHasRealBuilding(con.iWalls, True)
			city.setHasRealBuilding(con.iLibrary, True)
			city.setHasRealBuilding(con.iMarket, True)
			city.setHasRealBuilding(con.iGranary, True)
			city.setHasRealBuilding(con.iHarbor, True)
			city.setHasRealBuilding(con.iForge, True)
			
			city.setHasRealBuilding(con.iJewishTemple + 4*gc.getPlayer(iOwner).getStateReligion(), True)
			
		if iOwner == con.iNetherlands and (city.getX(), city.getY()) == con.tCapitals[0][con.iNetherlands] and gc.getGame().getGameTurn() <= getTurnForYear(1580)+3:
			city.setPopulation(9)
			
			for iBuilding in [con.iLibrary, con.iBarracks, con.iGrocer, con.iBank, con.iColosseum, con.iTheatre, con.iJewishTemple+4*gc.getPlayer(con.iNetherlands).getStateReligion()]:
				city.setHasRealBuilding(iBuilding, True)
				
			gc.getPlayer(con.iNetherlands).AI_updateFoundValues(False)
			
		if iOwner == con.iItaly and (city.getX(), city.getY()) == con.tCapitals[0][con.iItaly] and gc.getGame().getGameTurn() <= getTurnForYear(con.tBirth[con.iItaly])+3:
			city.setPopulation(7)
			
			for iBuilding in [con.iLibrary, con.iGrocer, con.iTemple+4*gc.getPlayer(con.iItaly).getStateReligion(), con.iMarket, con.iItalianArtStudio, con.iAqueduct, con.iCourthouse, con.iWalls]:
				city.setHasRealBuilding(iBuilding, True)
				
			gc.getPlayer(con.iItaly).AI_updateFoundValues(False)

		vic.onCityBuilt(iOwner, city)
			
                if iOwner < con.iNumPlayers:
			self.dc.onCityBuilt(iOwner)

		if iOwner == con.iArabia:
			if not gc.getGame().isReligionFounded(con.iIslam):
				if (city.getX(), city.getY()) == (75, 33):
					self.rel.foundReligion((75, 33), con.iIslam)
				
		# Leoreth: free defender and worker for AI colonies
		if iOwner in con.lCivGroups[0]:
			if city.getRegionID() not in con.mercRegions[con.iArea_Europe]:
				if utils.getHumanID() != iOwner:
					x = city.getX()
					y = city.getY()
					utils.createGarrisons((x,y), iOwner, 1)
					utils.makeUnit(con.iWorker, iOwner, (x,y), 1)
					
		# Holy Rome founds its capital
		if iOwner == con.iHolyRome:
			if gc.getPlayer(con.iHolyRome).getNumCities() == 1:
				self.rnf.holyRomanSpawn()

        def onPlayerChangeStateReligion(self, argsList):
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		
		if iPlayer < iNumPlayers:
			self.dc.onPlayerChangeStateReligion(argsList)
			
		sta.onPlayerChangeStateReligion(iPlayer)

        def onCombatResult(self, argsList):
                self.up.aztecUP(argsList)
                self.rnf.immuneMode(argsList)
		self.up.vikingUP(argsList) # includes Moorish Corsairs
		
		pWinningUnit, pLosingUnit = argsList
		
		vic.onCombatResult(pWinningUnit, pLosingUnit)
		
		iUnitPower = 0
		pLosingUnitInfo = gc.getUnitInfo(pLosingUnit.getUnitType())
		
		if pLosingUnitInfo.getUnitCombatType() != gc.getInfoTypeForString("UNITCOMBAT_SIEGE"):
			iUnitPower = pLosingUnitInfo.getPowerValue()
		
		sta.onCombatResult(pWinningUnit.getOwner(), pLosingUnit.getOwner(), iUnitPower)
		
		# catch slaves by defeating native and barbarian Pombos or Impis
		if pLosingUnit.getOwner() in [con.iBarbarian, con.iNative] and pLosingUnit.getUnitType() in [con.iZuluImpi, con.iKongoPombos]:
			if gc.getMap().plot(pLosingUnit.getX(), pLosingUnit.getY()).getOwner() == pWinningUnit.getOwner():
				if gc.getPlayer(pWinningUnit.getOwner()).getCivics(2) == con.iCivicSlavery:
					iRand = gc.getGame().getSorenRandNum(5, "Caught slaves?")
					if iRand == 1:
						iNewUnit = utils.getUniqueUnitType(pWinningUnit.getOwner(), gc.getUnitInfo(con.iSlave).getUnitClassType())
						utils.makeUnit(iNewUnit, pWinningUnit.getOwner(), (pWinningUnit.getX(), pWinningUnit.getY()), 1)
						CyInterface().addMessage(pWinningUnit.getOwner(),True,15,CyTranslator().getText("TXT_KEY_UP_ENSLAVE_WIN", ()),'SND_REVOLTEND',1,'Art/Units/slave/button_slave.dds',ColorTypes(8),pWinningUnit.getX(),pWinningUnit.getY(),True,True)

		# Maya Holkans give food to closest city on victory
		if pWinningUnit.getUnitType() == con.iMayaHolkan:
			iOwner = pWinningUnit.getOwner()
			city = gc.getMap().findCity(pWinningUnit.getX(), pWinningUnit.getY(), iOwner, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
			if city: 
				city.changeFood(5)
				sAdjective = gc.getPlayer(pLosingUnit.getOwner()).getCivilizationAdjectiveKey()
				CyInterface().addMessage(iOwner, False, con.iDuration, CyTranslator().getText("TXT_KEY_MAYA_HOLKAN_EFFECT", (sAdjective, pLosingUnit.getNameKey(), 5, city.getName())), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
		
        def onReligionFounded(self, argsList):
                'Religion Founded'
                iReligion, iFounder = argsList
		
		if gc.getGame().getGameTurn() == utils.getScenarioStartTurn():
			return
        
                vic.onReligionFounded(iFounder, iReligion)
		self.rel.onReligionFounded(iReligion, iFounder)

        def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal, bCapitulated = argsList
		
		if bCapitulated:
			sta.onVassalState(iMaster, iVassal)
		
		if iVassal == con.iInca:
			gc.getPlayer(con.iInca).setReborn(True)
			
		# move Mongolia's core south in case they vassalize China
		if bCapitulated and iVassal == con.iChina and iMaster == con.iMongolia:
			gc.getPlayer(con.iMongolia).setReborn(True)
		
		self.dc.onVassalState(argsList)

	def onRevolution(self, argsList):
		'Called at the start of a revolution'
		iPlayer = argsList[0]
		
		sta.onRevolution(iPlayer)
		
		if iPlayer < iNumPlayers:
			self.dc.onRevolution(iPlayer)
			
		if gc.getPlayer(iPlayer).getCivics(1) == con.iCivicEgalitarianism:
			utils.clearSlaves(iPlayer)
			
		if iPlayer in [con.iEgypt]:
			cnm.onRevolution(iPlayer)
			
	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity, iPlayer = argsList
		
		# Leoreth/Voyhkah: Empire State Building effect
		if pCity.isHasRealBuilding(con.iEmpireState):
                        iPop = pCity.getPopulation()
                        pCity.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_EMPIRE_STATE"), 0, iPop)
			
	def onUnitPillage(self, argsList):
		unit, iImprovement, iRoute, iPlayer, iGold = argsList
		
		if iPlayer == con.iVikings and iGold > 0 and iImprovement != -1 and iGold < 1000:
			vic.onUnitPillage(iPlayer, iGold)
			
	def onCityCaptureGold(self, argsList):
		city, iPlayer, iGold = argsList
		
		if iPlayer == con.iVikings and iGold > 0:
			vic.onCityCaptureGold(iPlayer, iGold)
			
	def onPlayerGoldTrade(self, argsList):
		iFromPlayer, iToPlayer, iGold = argsList
		
		if iToPlayer == con.iTamils:
			vic.onPlayerGoldTrade(iToPlayer, iGold)
			
	def onTradeMission(self, argsList):
		iUnitType, iPlayer, iX, iY, iGold = argsList
		
		if iPlayer in [con.iTamils, con.iMali]:
			vic.onTradeMission(iPlayer, iX, iY, iGold)
		
	def onPlayerSlaveTrade(self, argsList):
		iPlayer, iGold = argsList
		
		if iPlayer == con.iCongo:
			vic.onPlayerSlaveTrade(iPlayer, iGold)
			
	def onUnitGifted(self, argsList):
		pUnit, iOwner, pPlot = argsList
			
	def onUnitCreated(self, argsList):
		utils.debugTextPopup("Unit created")
		pUnit = argsList
			
	def onUnitBuilt(self, argsList):
		city, unit = argsList
		
		if unit.getUnitType() == con.iSettler and city.getOwner() == iChina and utils.getHumanID() != iChina:
			utils.handleChineseCities(unit)
			
		# Leoreth: help AI by moving new slaves to the new world
		if unit.getUnitType() == con.iSlave and city.getRegionID() in [con.rIberia, con.rBritain, con.rEurope, con.rScandinavia, con.rRussia, con.rItaly, con.rBalkans, con.rMaghreb, con.rAnatolia] and utils.getHumanID() != city.getOwner():
			utils.moveSlaveToNewWorld(city.getOwner(), unit)
			
	
		
        def onBuildingBuilt(self, argsList):
                city, iBuildingType = argsList
                iOwner = city.getOwner()
                vic.onBuildingBuilt(iOwner, iBuildingType)
                if iOwner < con.iNumPlayers:
                        self.com.onBuildingBuilt(iOwner, iBuildingType, city)
		
		if isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType()):
			sta.onWonderBuilt(iOwner, iBuildingType)
			
		if iBuildingType == con.iPalace:
			sta.onPalaceMoved(iOwner)
			
			if city.isHasRealBuilding(con.iSummerPalace): city.setHasRealBuilding(con.iSummerPalace, False)

		# Leoreth: Apostolic Palace moves holy city
		if iBuildingType == con.iApostolicPalace:
			self.rel.foundOrthodoxy(iOwner)
			
			# Leoreth: build shrine in 3000 BC scenario during HRE autoplay to provide a challenge
			if utils.getScenario() == con.i3000BC and utils.getHumanID() == con.iHolyRome and gc.getGame().getGameTurnYear() < 840:
				gc.getGame().getHolyCity().setHasRealBuilding(con.iChristianShrine, True)
			
			gc.getGame().setHolyCity(con.iChristianity, city, False)

		# Leoreth: update trade routes when Porcelain Tower is built to start its effect
		if iBuildingType == con.iPorcelainTower:
			gc.getPlayer(iOwner).updateTradeRoutes()

		# Leoreth/Voyhkah: Empire State Building
		if iBuildingType == con.iEmpireState:
			iPop = city.getPopulation()
			city.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_EMPIRE_STATE"), 0, iPop)
			
		# Leoreth: Machu Picchu
		if iBuildingType == con.iMachuPicchu:
			iNumPeaks = 0
			for i in range(21):
				if city.getCityIndexPlot(i).isPeak():
					iNumPeaks += 1
			city.setBuildingCommerceChange(gc.getInfoTypeForString("BUILDINGCLASS_MACHU_PICCHU"), 0, iNumPeaks * 2)
			
		# Leoreth: Great Wall
		if iBuildingType == con.iGreatWall:
			for iPlot in range(gc.getMap().numPlots()):
				plot = gc.getMap().plotByIndex(iPlot)
				if plot.getOwner() == iOwner and not plot.isWater():
					plot.setWithinGreatWall(True)
					
		# Leoreth: La Mezquita
		if iBuildingType == con.iMezquita:
			lGPList = [0, 0, 0, 0, 0, 0, 0]
			for city in utils.getCityList(iOwner):
				for i in range(7):
					iSpecialistUnit = utils.getUniqueUnit(iOwner, con.iProphet + i)
					lGPList[i] += city.getGreatPeopleUnitProgress(iSpecialistUnit)
			iGPType = utils.getUniqueUnit(iOwner, con.iProphet + utils.getHighestIndex(lGPList))
			utils.makeUnit(iGPType, iOwner, (city.getX(), city.getY()), 1)
			CyInterface().addMessage(iOwner, False, con.iDuration, CyTranslator().getText("TXT_KEY_MEZQUITA_FREE_GP", (gc.getUnitInfo(iGPType).getText(), city.getName())), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getUnitInfo(iGPType).getButton(), ColorTypes(con.iWhite), city.getX(), city.getY(), True, True)

		# Leoreth: found Buddhism when a Hindu temple is built
		if iBuildingType == con.iHinduTemple:
			self.rel.foundBuddhism(city)
			
		# Leoreth: in case human Phoenicia moves palace to Carthage
		if iBuildingType == con.iPalace:
			if iOwner == con.iCarthage and city.getX() == 58 and city.getY() == 39:
				if not utils.isReborn(iOwner): gc.getPlayer(con.iCarthage).setReborn(True)
			
	def onPlotFeatureRemoved(self, argsList):
		plot, city, iFeature = argsList
		
		if plot.getOwner() == con.iBrazil:
			iGold = 0
			
			if iFeature == con.iForest: iGold = 15
			elif iFeature == con.iJungle: iGold = 20
			
			if iGold > 0:
				gc.getPlayer(con.iBrazil).changeGold(iGold)
				
				if utils.getHumanID() == con.iBrazil:
					CyInterface().addMessage(con.iBrazil, False, con.iDuration, CyTranslator().getText("TXT_KEY_DEFORESTATION_EVENT", (gc.getFeatureInfo(iFeature).getText(), city.getName(), iGold)), "", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCommerceInfo(0).getButton(), ColorTypes(con.iWhite), plot.getX(), plot.getY(), True, True)

        def onProjectBuilt(self, argsList):
                city, iProjectType = argsList
                vic.onProjectBuilt(city.getOwner(), iProjectType)

        def onImprovementDestroyed(self, argsList):
		pass
                
        def onBeginGameTurn(self, argsList):
                iGameTurn = argsList[0]
                
                self.rnf.checkTurn(iGameTurn)
                self.barb.checkTurn(iGameTurn)
                self.rel.checkTurn(iGameTurn)
                self.res.checkTurn(iGameTurn)
                self.up.checkTurn(iGameTurn)
                self.aiw.checkTurn(iGameTurn)
                self.pla.checkTurn(iGameTurn)
                self.com.checkTurn(iGameTurn)
		self.corp.checkTurn(iGameTurn)
		
		sta.checkTurn(iGameTurn)
		cong.checkTurn(iGameTurn)
		
		if iGameTurn % 10 == 0:
                        self.dc.checkTurn(iGameTurn)
			
                return 0

        def onBeginPlayerTurn(self, argsList):        
                iGameTurn, iPlayer = argsList
		
		#if utils.getHumanID() == iPlayer:
		#	utils.debugTextPopup('Can contact: ' + str([gc.getPlayer(i).getCivilizationShortDescription(0) for i in range(con.iNumPlayers) if gc.getTeam(iPlayer).canContact(i)]))

		if (self.rnf.getDeleteMode(0) != -1):
                        self.rnf.deleteMode(iPlayer)
			
		self.pla.checkPlayerTurn(iGameTurn, iPlayer)
		
		if (gc.getPlayer(iPlayer).isAlive()):
                        vic.checkTurn(iGameTurn, iPlayer)
			
		if (gc.getPlayer(iPlayer).isAlive() and iPlayer < con.iNumPlayers and not gc.getPlayer(iPlayer).isHuman()):
                        self.rnf.checkPlayerTurn(iGameTurn, iPlayer) #for leaders switch

	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		player = PyPlayer(iPlayer)
		iUnitType = pUnit.getUnitType()
		iUnitClassType = pUnit.getUnitClassType()
		sName = pUnit.getName()
		
		# Leoreth: replace graphics for female GP names
		if sName[0] == "f":
			pUnit.setName(sName[1:])
			pUnit = utils.replace(pUnit, con.dFemaleGreatPeople[utils.getBaseUnit(iUnitType)])
		
		# Leoreth: display notification
		if iPlayer not in [con.iIndependent, con.iIndependent2, con.iBarbarian]:
			pDisplayCity = pCity
			if pDisplayCity.isNone(): pDisplayCity = gc.getMap().findCity(pUnit.getX(), pUnit.getY(), PlayerTypes.NO_PLAYER, TeamTypes.NO_TEAM, False, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				
			sCity = "%s (%s)" % (pDisplayCity.getName(), gc.getPlayer(pDisplayCity.getOwner()).getCivilizationShortDescription(0))
			sMessage = localText.getText("TXT_KEY_MISC_GP_BORN", (pUnit.getName(), sCity))
			sUnrevealedMessage = localText.getText("TXT_KEY_MISC_GP_BORN_SOMEWHERE", (pUnit.getName(),))
			
			if pCity.isNone(): sMessage = localText.getText("TXT_KEY_MISC_GP_BORN_OUTSIDE", (pUnit.getName(), sCity))
		
			for iLoopPlayer in range(con.iNumPlayers):
				if gc.getPlayer(iLoopPlayer).isAlive():
					if pUnit.plot().isRevealed(gc.getPlayer(iLoopPlayer).getTeam(), False):
						CyInterface().addMessage(iLoopPlayer, False, con.iDuration, sMessage, "AS2D_UNIT_GREATPEOPLE", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, pUnit.getButton(), ColorTypes(gc.getInfoTypeForString("COLOR_UNIT_TEXT")), pUnit.getX(), pUnit.getY(), True, True)
					else:
						CyInterface().addMessage(iLoopPlayer, False, con.iDuration, sUnrevealedMessage, "AS2D_UNIT_GREATPEOPLE", InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT, "", ColorTypes(gc.getInfoTypeForString("COLOR_UNIT_TEXT")), -1, -1, False, False)

		vic.onGreatPersonBorn(iPlayer, pUnit)
		sta.onGreatPersonBorn(iPlayer)

        def onReligionSpread(self, argsList):
            
                iReligion, iOwner, pSpreadCity = argsList
		
		cnm.onReligionSpread(iReligion, iOwner, pSpreadCity)

		#Leoreth: if state religion spreads, pagan temples are replaced with its temple. For other religions, they're simply removed.         
		if pSpreadCity.isHasBuilding(con.iObelisk):
			pSpreadCity.setHasRealBuilding(con.iObelisk, False)
			if gc.getPlayer(iOwner).getCivics(4) != con.iCivicPantheon and gc.getPlayer(iOwner).getStateReligion() == iReligion and gc.getTeam(iOwner).isHasTech(con.iPriesthood):
				pSpreadCity.setHasRealBuilding(con.iJewishTemple+4*iReligion, True)
                                CyInterface().addMessage(iOwner, True, con.iDuration, CyTranslator().getText("TXT_KEY_PAGAN_TEMPLE_REPLACED", (str(gc.getReligionInfo(iReligion).getText()), str(pSpreadCity.getName()), str(gc.getBuildingInfo(con.iJewishTemple+4*iReligion).getText()))), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)
			else:
				CyInterface().addMessage(iOwner, True, con.iDuration, CyTranslator().getText("TXT_KEY_PAGAN_TEMPLE_REMOVED", (str(gc.getReligionInfo(iReligion).getText()), str(pSpreadCity.getName()))), "", 0, "", ColorTypes(con.iWhite), -1, -1, True, True)

        def onFirstContact(self, argsList):
            
                iTeamX,iHasMetTeamY = argsList
		if iTeamX < con.iNumPlayers:
			self.rnf.onFirstContact(iTeamX, iHasMetTeamY)
                self.pla.onFirstContact(iTeamX, iHasMetTeamY)
		
		vic.onFirstContact(iTeamX, iHasMetTeamY)

        #Rhye - start
        def onTechAcquired(self, argsList):
		iTech, iTeam, iPlayer, bAnnounce = argsList

                iHuman = utils.getHumanID()
		
		iEra = gc.getTechInfo(iTech).getEra()
                
                if (utils.getScenario() == con.i600AD and gc.getGame().getGameTurn() == getTurnForYear(600)): #late start condition
                        return
			
		if utils.getScenario() == con.i1700AD and gc.getGame().getGameTurn() == getTurnForYear(1700):
			return
			
		sta.onTechAcquired(iPlayer, iTech)
		
                if (gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer])):
                	vic.onTechAcquired(iPlayer, iTech)
                        cnm.onTechAcquired(argsList[2])

                if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer]) and iPlayer < con.iNumPlayers):
                        self.rel.onTechAcquired(argsList[0], argsList[2])
                
                if (gc.getPlayer(iPlayer).isAlive() and gc.getGame().getGameTurn() > getTurnForYear(con.tBirth[iPlayer]) and iPlayer < con.iNumPlayers):
                        if (gc.getGame().getGameTurn() > getTurnForYear(1700)):
                                self.aiw.forgetMemory(argsList[0], argsList[2])

                if (argsList[0] == con.iAstronomy):
			if iPlayer in [con.iSpain, con.iFrance, con.iEngland, con.iGermany, con.iVikings, con.iNetherlands, con.iPortugal]:
				self.rnf.setAstronomyTurn(iPlayer, gc.getGame().getGameTurn())
				
                if (argsList[0] == con.iCompass):
                        if (iPlayer == con.iVikings):
                                gc.getMap().plot(49, 62).setTerrainType(con.iCoast, True, True)
				
                if (argsList[0] == con.iMedicine):
                        self.pla.onTechAcquired(argsList[0], argsList[2])

		if argsList[0] == con.iRailroad:
			self.rnf.onRailroadDiscovered(argsList[2])
			
		if iTech in [con.iAstronomy, con.iGunpowder]:
			teamPlayer = gc.getTeam(iPlayer)
			if teamPlayer.isHasTech(con.iAstronomy) and teamPlayer.isHasTech(con.iGunpowder):
				self.rnf.earlyTradingCompany(iPlayer)
			
		if iTech in [con.iEconomics, con.iRifling]:
			teamPlayer = gc.getTeam(iPlayer)
			if teamPlayer.isHasTech(con.iEconomics) and teamPlayer.isHasTech(con.iRifling):
				self.rnf.lateTradingCompany(iPlayer)
	
		if utils.getHumanID() != iPlayer:
			if iPlayer == con.iJapan and iEra == con.iIndustrial:
				utils.moveCapital(iPlayer, (116, 47)) # Toukyou
			elif iPlayer == con.iItaly and iEra == con.iIndustrial:
				utils.moveCapital(iPlayer, (60, 44)) # Roma
			elif iPlayer == con.iVikings and iEra == con.iRenaissance:
				utils.moveCapital(iPlayer, (63, 59)) # Stockholm
			elif iPlayer == con.iHolyRome and iEra == con.iRenaissance:
				utils.moveCapital(iPlayer, (62, 49)) # Wien
				
		# Spain's core extends when reaching the Renaissance and there are no Moors in Iberia
		# at the same time, the Moorish core relocates to Africa
		if iPlayer == con.iSpain and iEra == con.iRenaissance:
			bNoMoors = True
			if gc.getPlayer(con.iMoors).isAlive():
				for city in utils.getCityList(iMoors):
					if city.plot().getRegionID() == con.rIberia:
						bNoMoors = False
			if bNoMoors:
				gc.getPlayer(con.iSpain).setReborn(True)
				gc.getPlayer(con.iMoors).setReborn(True)
				
		# Italy's core extends when reaching the Industrial era
		if iPlayer == con.iItaly and iEra == con.iIndustrial:
			gc.getPlayer(con.iItaly).setReborn(True)
			
		# Arabia's core moves to Iraq when Philosophy is discovered
		if iPlayer == con.iArabia and iTech == con.iPhilosophy:
			gc.getPlayer(con.iArabia).setReborn(True)
			
		# Japan's core extends when reaching the Industrial era
		if iPlayer == con.iJapan and iEra == con.iIndustrial:
			gc.getPlayer(con.iJapan).setReborn(True)
			
		# Germany's core shrinks when reaching the Modern era
		if iPlayer == con.iGermany and iEra == con.iModern:
			gc.getPlayer(con.iGermany).setReborn(True)
                

        def onPreSave(self, argsList):
                'called before a game is actually saved'
		
		sd.save() # edead: pickle & save script data

        def onLoadGame(self, argsList):
		sd.load() # edead: load & unpickle script data
		
	def onChangeWar(self, argsList):
		bWar, iTeam, iOtherTeam, bGlobalWar = argsList
		
		sta.onChangeWar(bWar, iTeam, iOtherTeam)
		self.up.onChangeWar(bWar, iTeam, iOtherTeam)
		
		if iTeam < con.iNumPlayers and iOtherTeam < con.iNumPlayers:
			cong.onChangeWar(argsList)
		
		# don't start AIWars if they get involved in natural wars
		if bWar and iTeam < con.iNumPlayers and iOtherTeam < con.iNumPlayers:
			sd.setAggressionLevel(iTeam, 0)
			sd.setAggressionLevel(iOtherTeam, 0)
			
	def onGoldenAge(self, argsList):
		iPlayer = argsList[0]
		
		sta.onGoldenAge(iPlayer)
		
	def onReleasedPlayer(self, argsList):
		iPlayer, iReleasedPlayer = argsList
		
		lCities = []
		for city in utils.getCityList(iPlayer):
			if city.plot().isCore(iReleasedPlayer) and not city.plot().isCore(iPlayer) and not city.isCapital():
				lCities.append(city)
				
		sta.doResurrection(iReleasedPlayer, lCities, False)
		
		gc.getPlayer(iReleasedPlayer).AI_changeAttitudeExtra(iPlayer, 2)
		
	def onBlockade(self, argsList):
		iPlayer, iGold = argsList
		
		vic.onBlockade(iPlayer, iGold)
		
	def onPeaceBrokered(self, argsList):
		iBroker, iPlayer1, iPlayer2 = argsList
		
		vic.onPeaceBrokered(iBroker, iPlayer1, iPlayer2)
		
	def onEndPlayerTurn(self, argsList):
		iGameTurn, iPlayer = argsList
		
		self.rnf.endTurn(iPlayer)
		sta.endTurn(iPlayer)

        def onKbdEvent(self, argsList):
                'keypress handler - return 1 if the event was consumed'
                eventType,key,mx,my,px,py = argsList
                        
                theKey=int(key)
		
		if ( eventType == self.EventKeyDown and theKey == int(InputTypes.KB_Q) and self.eventManager.bAlt and self.eventManager.bShift):
                        print("SHIFT-ALT-Q") #enables squatting
                        self.rnf.setCheatMode(True);
                        CyInterface().addMessage(utils.getHumanID(), True, con.iDuration, "EXPLOITER!!! ;)", "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)

                #Stability Cheat
                if self.rnf.getCheatMode() and theKey == int(InputTypes.KB_S) and self.eventManager.bAlt and self.eventManager.bShift:
                        print("SHIFT-ALT-S") #increases stability by one level
			utils.setStabilityLevel(utils.getHumanID(), min(5, utils.getStabilityLevel(utils.getHumanID()) + 1))