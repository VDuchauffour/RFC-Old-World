from Events import handler
from Core import *


tCarthage = (58, 39)
tConstantinople = (68, 45)
tBeijing = (102, 47)
tMecca = (75, 33)
tCopenhagen = (60, 56)

dRelocatedCapitals = CivDict({
	iPhoenicia : tCarthage,
	iMongols : tBeijing,
	iOttomans : tConstantinople
})

dCapitalInfrastructure = CivDict({
	iPhoenicia : (3, [], []),
	iByzantium : (5, [iBarracks, iWalls, iLibrary, iMarket, iGranary, iHarbor, iForge], [temple]),
	iPortugal : (5, [iLibrary, iMarket, iHarbor, iLighthouse, iForge, iWalls], [temple]),
	iItaly : (7, [iLibrary, iPharmacy, iMarket, iArtStudio, iAqueduct, iCourthouse, iWalls], [temple]),
	iNetherlands : (9, [iLibrary, iMarket, iWharf, iLighthouse, iBarracks, iPharmacy, iBank, iArena, iTheatre], [temple]),
})


### CITY ACQUIRED ###


@handler("cityAcquired")
def relocateAcquiredCapital(iOwner, iPlayer, city):
	relocateCapitals(iPlayer, city)


@handler("cityAcquired")
def buildAcquiredCapitalInfrastructure(iOwner, iPlayer, city):
	buildCapitalInfrastructure(iPlayer, city)


### CITY ACQUIRED AND KEPT ###


# TODO: maybe new event capitalfounded?
@handler("cityAcquiredAndKept")
def createAdditionalPolishSettler(iPlayer, city):
	if city.isCapital() and civ(iPlayer) == iPoland and not player(iPlayer).isHuman():
		# TODO: move to Locations
		locations = {
			(65, 55): 1, # Memel
			(65, 54): 1, # Koenigsberg
			(64, 54): 3, # Gdansk
		}
		
		location = weighted_random_entry(locations)
		
		makeUnit(iPlayer, iSettler, location)
		makeUnit(iPlayer, iCrossbowman, location)


### CITY BUILT ###


@handler("cityBuilt")
def relocateFoundedCapital(city):
	relocateCapitals(city.getOwner(), city)


@handler("cityBuilt")
def buildFoundedCapitalInfrastructure(city):
	buildCapitalInfrastructure(city.getOwner(), city)
	
	
@handler("cityBuilt")
def createCarthaginianDefenses(city):
	if at(city, tCarthage) and not player(city).isHuman():					
		makeUnit(iPhoenicia, iWorkboat, tCarthage, UnitAITypes.UNITAI_WORKER_SEA)
		makeUnit(iPhoenicia, iGalley, direction(tCarthage, DirectionTypes.DIRECTION_NORTHWEST), UnitAITypes.UNITAI_SETTLER_SEA)
		makeUnit(iPhoenicia, iSettler, direction(tCarthage, DirectionTypes.DIRECTION_NORTHWEST), UnitAITypes.UNITAI_SETTLE)
		
		if player(iRome).isHuman():
			city.setHasRealBuilding(iWalls, True)
			
			makeUnits(iPhoenicia, iArcher, tCarthage, 2, UnitAITypes.UNITAI_CITY_DEFENSE)
			makeUnits(iPhoenicia, iNumidianCavalry, tCarthage, 3)
			makeUnits(iPhoenicia, iWarElephant, tCarthage, 2, UnitAITypes.UNITAI_CITY_COUNTER)


@handler("cityBuilt")
def foundIslam(city):
	if civ(city) == iArabia:
		if not game.isReligionFounded(iIslam):
			if at(city, tMecca):
				rel.foundReligion(location(city), iIslam)


# TODO: use capital founded/acquired event OR hook up into new rnf code
@handler("cityBuilt")
def clearDanishCulture(city):
	if civ(city) == iHolyRome and player(city).getNumCities() == 1:
		copenhagen = city(tCopenhagen)
		if copenhagen and civ(copenhagen) == iVikings:
			city.setCulture(city.getOwner(), 5, True)
			
			
### UNIT BUILT ###
	

@handler("unitBuilt")
def foundChineseCity(city, unit):
	if unit.isFound() and civ(unit) == iChina and not player(unit).isHuman():
		plot = plots.of(lChineseCities).where(lambda plot: isFree(unit.getOwner(), plot, True, True, True)).random()
	
		if plot:
			player(unit).found(plot.getX(), plot.getY())
			unit.kill(False, -1)


### BEGIN GAME TURN ###


@handler("BeginGameTurn")
def placeGoodyHuts(iGameTurn):
	if iGameTurn == scenarioStartTurn() + 3:
			
		if scenario() == i3000BC:
			placeHut((101, 38), (107, 41)) # Southern China
			placeHut((62, 45), (67, 50)) # Balkans
			placeHut((69, 42), (76, 46)) # Asia Minor
		
		if scenario() <= i600AD:
			placeHut((49, 40), (54, 46)) # Iberia
			placeHut((57, 51), (61, 56)) # Denmark / Northern Germany
			placeHut((48, 55), (49, 58)) # Ireland
			placeHut((50, 53), (54, 60)) # Britain
			placeHut((57, 57), (65, 65)) # Scandinavia
			placeHut((73, 53), (81, 58)) # Russia
			placeHut((81, 43), (86, 47)) # Transoxania
			placeHut((88, 30), (94, 36)) # Deccan
			placeHut((110, 40), (113, 43)) # Shikoku
			placeHut((114, 49), (116, 52)) # Hokkaido
			placeHut((85, 53), (99, 59)) # Siberia
			placeHut((103, 24), (109, 29)) # Indonesia
			placeHut((68, 17), (72, 23)) # East Africa
			placeHut((65, 10), (70, 16)) # South Africa
			placeHut((22, 48), (29, 51)) # Great Lakes
			placeHut((18, 44), (22, 52)) # Great Plains
			placeHut((34, 25), (39, 29)) # Amazonas Delta
			placeHut((33, 9), (37, 15)) # Parana Delta
			placeHut((25, 36), (32, 39)) # Caribbean
		
		placeHut((107, 19), (116, 22)) # Northern Australia
		placeHut((114, 10), (118, 17)) # Western Australia
		placeHut((120, 5), (123, 11)) # New Zealand
		placeHut((59, 25), (67, 28)) # Central Africa


@handler("BeginGameTurn")
def clearMassilianCulture(iGameTurn):		
	if iGameTurn == year(dBirth[iSpain])-1:
		if scenario() == i600AD:
			pMassilia = city_(56, 46)
			if pMassilia:
				pMassilia.setCulture(pMassilia.getOwner(), 1, True)


@handler("BeginGameTurn")
def ottomansFlipIndependents(iGameTurn):
	if iGameTurn == data.iOttomanSpawnTurn + 1:
		for city in cities.birth(iOttomans):
			iOwner = city.getOwner()
			if is_minor(iOwner):
				# TODO: this should be better but is not covered by completeCityFlip
				flipCity(city, False, True, slot(iOttomans), ())
				cultureManager(city, 100, slot(iOttomans), iOwner, True, False, False)
				self.convertSurroundingPlotCulture(slot(iOttomans), plots.surrounding(city))
				makeUnit(iOttomans, iCrossbowman, city)


@handler("BeginGameTurn")
def createCarthaginianSettler(iGameTurn):
	if not player(iPhoenicia).isHuman() and iGameTurn == year(-820) - (data.iSeed % 10):
		makeUnit(iPhoenicia, iSettler, tCarthage)
		makeUnits(iPhoenicia, iArcher, tCarthage, 2)
		makeUnits(iPhoenicia, iWorker, tCarthage, 2)
		makeUnits(iPhoenicia, iWarElephant, tCarthage, 2)


# TODO: revisit how this works
@handler("BeginGameTurn")
def checkEarlyColonists():
	dEarlyColonistYears = {
		-850 : iGreece,
		-700 : iCarthage,
		-600 : iRome,
		-400 : iRome,
	}
	
	iYear = game.getGameTurnYear()
	if iYear in dEarlyColonistYears:
		iCiv = dEarlyColonistYears[iYear]
		giveEarlyColonists(iCiv)
		
		
@handler("BeginGameTurn")
def checkLateColonists():
	if year().between(1350, 1918):
		for iCiv in dTradingCompanyPlots:
			if player(iCiv).isAlive():
				iPlayer = slot(iCiv)
				if turn() == data.players[iPlayer].iExplorationTurn + 1 + data.players[iPlayer].iColonistsAlreadyGiven * 8:
					giveColonists(iPlayer)


@handler("BeginGameTurn")
def checkRaiders():
	if year().between(860, 1250):
		if turn() % turns(10) == 9:
			giveRaiders(iVikings)
	

@handler("BeginGameTurn")
def moorishSpawnInMorocoo():
	if year() == year(710)-1:
		marrakesh = city_(51, 37)
		if marrakesh:
			marrakesh.setHasReligion(iIslam, True, False, False)
			
			makeUnit(marrakesh.getOwner(), iSettler, marrakesh)
			makeUnit(marrakesh.getOwner(), iWorker, marrakesh)


@handler("BeginGameTurn")
def flipChineseStartingCities():
	if scenario() == i600AD and year() == scenarioStartTurn():
		tTL, tBR = dBirthArea[iChina]
		if not player(iChina).isHuman(): 
			tTL = (99, 39) # 4 tiles further north
		
		china = plots.start(tTL).end(tBR)
		iNumAICitiesConverted, iNumHumanCitiesToConvert = self.convertSurroundingCities(slot(iChina), china)
		self.convertSurroundingPlotCulture(slot(iChina), china)
		
		for iMinor in players.independent().barbarian():
			flipUnitsInArea(china, slot(iChina), iMinor, False, player(iMinor).isBarbarian())


### FIRST CONTACT ###


@handler("firstContact")
def conquistadors(iTeamX, iHasMetTeamY):
		if is_minor(iTeamX) or is_minor(iHasMetTeamY):
			return
		
		if year().between(600, 1800):
			if civ(iTeamX) in lBioNewWorld and civ(iHasMetTeamY) not in lBioNewWorld:
				iNewWorldPlayer = iTeamX
				iOldWorldPlayer = iHasMetTeamY
				
				iNewWorldCiv = civ(iNewWorldPlayer)
				
				iIndex = lBioNewWorld.index(civ(iNewWorldPlayer))
				
				# TODO: use dict for first contact conquerors to avoid using index
				bAlreadyContacted = data.lFirstContactConquerors[iIndex]
				
				# avoid "return later" exploit
				if year() <= year(dBirth[iAztecs]) + turns(10):
					data.lFirstContactConquerors[iIndex] = True
					return
					
				if not bAlreadyContacted:
					if iNewWorldCiv == iMaya:
						tContactZoneTL = (15, 30)
						tContactZoneBR = (34, 42)
					elif iNewWorldCiv == iAztecs:
						tContactZoneTL = (11, 31)
						tContactZoneBR = (34, 43)
					elif iNewWorldCiv == iInca:
						tContactZoneTL = (21, 11)
						tContactZoneBR = (36, 40)
						
					lArrivalExceptions = [(25, 32), (26, 40), (25, 42), (23, 42), (21, 42)]
						
					data.lFirstContactConquerors[iIndex] = True
					
					# change some terrain to end isolation
					if iNewWorldCiv == iInca:
						plot(27, 30).setFeatureType(-1, 0)
						plot(28, 31).setFeatureType(-1, 0)
						plot(29, 23).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						plot(31, 13).setPlotType(PlotTypes.PLOT_HILLS, True, True) 
						plot(32, 19).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						plot(27, 29).setPlotType(PlotTypes.PLOT_HILLS, True, True) #Bogota
						
					elif iNewWorldCiv == iAztecs:
						plot(40, 66).setPlotType(PlotTypes.PLOT_HILLS, True, True)
						
					newWorldPlots = plots.start(tContactZoneTL).end(tContactZoneBR).without(lArrivalExceptions)
					contactPlots = newWorldPlots.where(lambda p: p.isVisible(iNewWorldPlayer, False) and p.isVisible(iOldWorldPlayer, False))
					arrivalPlots = newWorldPlots.owner(iNewWorldPlayer).where(lambda p: not p.isCity() and isFree(iOldWorldPlayer, p, bCanEnter=True) and not isIsland(p))
					
					if contactPlots and arrivalPlots:
						contactPlot = contactPlots.random()
						arrivalPlot = arrivalPlots.closest(contactPlot)
						
						iModifier1 = 0
						iModifier2 = 0
						
						if player(iNewWorldPlayer).isHuman() and player(iNewWorldPlayer).getNumCities() > 6:
							iModifier1 = 1
						else:
							if iNewWorldCiv == iInca or player(iNewWorldPlayer).getNumCities() > 4:
								iModifier1 = 1
							if not player(iNewWorldPlayer).isHuman():
								iModifier2 = 1
								
						if year() < year(dBirth[active()]):
							iModifier1 += 1
							iModifier2 += 1
							
						team(iOldWorldPlayer).declareWar(iNewWorldPlayer, True, WarPlanTypes.WARPLAN_TOTAL)
						
						iInfantry = getBestInfantry(iOldWorldPlayer)
						iCounter = getBestCounter(iOldWorldPlayer)
						iCavalry = getBestCavalry(iOldWorldPlayer)
						iSiege = getBestSiege(iOldWorldPlayer)
						
						iStateReligion = player(iOldWorldPlayer).getStateReligion()
						iMissionary = missionary(iStateReligion)
						
						if iInfantry:
							makeUnits(iOldWorldPlayer, iInfantry, arrivalPlot, 1 + iModifier2, UnitAITypes.UNITAI_ATTACK_CITY)
						
						if iCounter:
							makeUnits(iOldWorldPlayer, iCounter, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iSiege:
							makeUnits(iOldWorldPlayer, iSiege, arrivalPlot, 1 + iModifier1 + iModifier2, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iCavalry:
							makeUnits(iOldWorldPlayer, iCavalry, arrivalPlot, 2 + iModifier1, UnitAITypes.UNITAI_ATTACK_CITY)
							
						if iMissionary:
							makeUnit(iOldWorldPlayer, iMissionary, arrivalPlot)
							
						if iNewWorldCiv == iInca:
							makeUnits(iOldWorldPlayer, iAucac, arrivalPlot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iAztecs:
							makeUnits(iOldWorldPlayer, iJaguar, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iHolkan, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
						elif iNewWorldCiv == iMaya:
							makeUnits(iOldWorldPlayer, iHolkan, arrivalPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
							makeUnit(iOldWorldPlayer, iJaguar, arrivalPlot, UnitAITypes.UNITAI_ATTACK_CITY)
							
						message(iNewWorldPlayer, 'TXT_KEY_FIRST_CONTACT_NEWWORLD')
						message(iOldWorldPlayer, 'TXT_KEY_FIRST_CONTACT_OLDWORLD')


@handler("firstContact")
def mongolConquerors(iTeamX, iHasMetTeamY):
	if civ(iHasMetTeamY) == iMongols and not player(iMongols).isHuman():
		iCivX = civ(iTeamX)
	
		if iCivX in lMongolCivs:
			if year() < year(1500) and data.isFirstContactMongols(iCivX):

				data.setFirstContactMongols(iCivX, False)
	
				teamTarget = team(iTeamX)
					
				if iCivX == iArabia:
					tTL = (73, 31)
					tBR = (84, 43)
					iDirection = DirectionTypes.DIRECTION_EAST
				elif iCivX == iPersia:
					tTL = (73, 37)
					tBR = (86, 48)
					iDirection = DirectionTypes.DIRECTION_NORTH
				elif iCivX == iByzantium:
					tTL = (68, 41)
					tBR = (77, 46)
					iDirection = DirectionTypes.DIRECTION_EAST
				elif iCivX == iRussia:
					tTL = (68, 48)
					tBR = (81, 62)
					iDirection = DirectionTypes.DIRECTION_EAST

				lTargetList = getBorderPlots(iTeamX, tTL, tBR, iDirection, 3)
				
				if not lTargetList: return

				team(iMongols).declareWar(iTeamX, True, WarPlanTypes.WARPLAN_TOTAL)
				
				iHandicap = 0
				if teamtype(iTeamX).isHuman():
					iHandicap = game.getHandicapType() / 2

				for tPlot in lTargetList:
					makeUnits(iMongols, iKeshik, tPlot, 2 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
					makeUnits(iMongols, iMangudai, tPlot, 1 + 2 * iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
					makeUnits(iMongols, iTrebuchet, tPlot, 1 + iHandicap, UnitAITypes.UNITAI_ATTACK_CITY)
					
				message(iTeamX, 'TXT_KEY_MONGOL_HORDE_HUMAN')
				if team().canContact(iTeamX):
					message(active(), 'TXT_KEY_MONGOL_HORDE', adjective(iTeamX))


### TECH ACQUIRED ###


@handler("techAcquired")
def recordExplorationTurn(iTech, iTeam, iPlayer):
	if iTech == iExploration:
		data.players[iPlayer].iExplorationTurn = game.getGameTurn()


@handler("techAcquired")
def openIcelandRoute(iTech):		
	if iTech == iCompass:
		plot(49, 62).setTerrainType(iCoast, True, True)


@handler("techAcquired")
def americanWestCoastSettlement(iTech, iTeam, iPlayer):
	if iTech == iRailroad and civ(iPlayer) == iAmerica and not player(iPlayer).isHuman():
		lWestCoast = [(11, 50), (11, 49), (11, 48), (11, 47), (11, 46), (12, 45)]
				
		enemyCities = cities.of(lWestCoast).notowner(iAmerica)
		
		for iEnemy in enemyCities.owners():
			team(iPlayer).declareWar(iEnemy, True, WarPlanTypes.WARPLAN_LIMITED)
		
		for city in enemyCities:
			plot = plots.surrounding(city).random()
			makeUnits(iPlayer, iMinuteman, plot, 3, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iCannon, plot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
				
		if enemyCities.count() < 2:
			for plot in plots.of(lWestCoast).without(enemyCities).sample(2 - enemyCities.count()):
				makeUnit(iPlayer, iSettler, plot)
				makeUnit(iPlayer, iMinuteman, plot)


@handler("techAcquired")
def russianSiberianSettlement(iTech, iTeam, iPlayer):
	if iTech == iRailroad and civ(iPlayer) == iRussia and not player(iPlayer).isHuman():
		tVladivostok = (111, 51)
		
		vladivostok = city(tVladivostok)
		
		convertPlotCulture(plot(tVladivostok), iPlayer, 100, True)
		
		if vladivostok and vladivostok.getOwner() != iPlayer:
			spawnPlot = plots.surrounding(tVladivostok).land().passable().where(lambda plot: not city_(plot)).random()
			
			team(iTeam).declareWar(vladivostok.getTeam(), True, WarPlanTypes.WARPLAN_LIMITED)
			
			makeUnits(iPlayer, iRifleman, spawnPlot, 4, UnitAITypes.UNITAI_ATTACK_CITY)
			makeUnits(iPlayer, iCannon, spawnPlot, 2, UnitAITypes.UNITAI_ATTACK_CITY)
			
		elif isFree(iPlayer, tVladivostok, True):
			player(iPlayer).found(*tVladivostok)
			makeUnits(iPlayer, iRifleman, tVladivostok, 2)
			
			for plot in plots.surrounding(tVladivostok):
				convertPlotCulture(plot, iPlayer, 80, True)


@handler("techAcquired")
def earlyTradingCompany(iTech, iTeam, iPlayer):
	lCivs = [iSpain, iPortugal]
	lTechs = [iExploration, iFirearms]
	
	if civ(iPlayer) in lCivs:
		if iTech in lTechs and all(team(iTeam).isHasTech(iTech) for iTech in lTechs):
			if not player(iPlayer).isHuman() and not team(iTeam).isAVassal():
				handleColonialAcquisition(iPlayer)


@handler("techAcquired")
def lateTradingCompany(iTech, iTeam, iPlayer):
	lCivs = [iFrance, iEngland, iNetherlands]
	lTechs = [iEconomics, iReplaceableParts]
	
	if civ(iPlayer) in lCivs:
		if iTech in lTechs and all(team(iTeam).isHasTech(iTech) for iTech in lTechs):
			if not player(iPlayer).isHuman() and not team(iTeam).isAVassal():
				handleColonialConquest(iPlayer)


### IMPLEMENTATION ###


def relocateCapitals(iPlayer, city):
	if player(iPlayer).isHuman():
		return
	
	if iPlayer in dRelocatedCapitals:
		tCapital = dRelocatedCapitals[iPlayer]
		
		if location(city) == tCapital:
			moveCapital(iPlayer, tCapital)
			
	if civ(iPlayer) == iTurks and isAreaControlled(iPlayer, dCoreArea[iPersia][0], dCoreArea[iPersia][1]):
		capital = player(iPlayer).getCapitalCity()
		if capital not in plots.core(iPersia):
			newCapital = cities.core(iPersia).owner(iPlayer).random()
			if newCapital:
				moveCapital(iPlayer, location(newCapital))


def buildCapitalInfrastructure(iPlayer, city):
	if iPlayer in dCapitalInfrastructure:
		if at(city, plots.capital(iPlayer)) and year() <= year(dSpawn[iPlayer]) + turns(5):
			iPopulation, lBuildings, lReligiousBuildings = dCapitalInfrastructure
			
			if city.getPopulation() < iPopulation:
				city.setPopulation(iPopulation)
			
			for iBuilding in lBuildings:
				city.setHasRealBuilding(iBuilding, True)
			
			iStateReligion = player(iPlayer).getStateReligion()
			if iStateReligion >= 0:
				for religiosBuilding in lReligiousBuildings:
					city.setHasRealBuilding(religiosBuilding(iStateReligion), True)
					
					
def giveEarlyColonists(iCiv):
	pPlayer = player(iCiv)
	
	if pPlayer.isAlive() and not pPlayer.isHuman():
		capital = pPlayer.getCapitalCity()

		if iCiv == iRome:
			capital = cities.owner(iCiv).region(rIberia).random()
			
		if capital:
			tSeaPlot = self.findSeaPlots(capital, 1, iCiv)
			if tSeaPlot:
				makeUnit(iCiv, iGalley, tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iCiv, iSettler, tSeaPlot)
				makeUnit(iCiv, iArcher, tSeaPlot)


def giveColonists(iPlayer):
	pPlayer = player(iPlayer)
	pTeam = team(iPlayer)
	iCiv = civ(iPlayer)
	
	if pPlayer.isAlive() and not pPlayer.isHuman() and iCiv in dMaxColonists:
		if pTeam.isHasTech(iExploration) and data.players[iPlayer].iColonistsAlreadyGiven < dMaxColonists[iCiv]:
			sourceCities = cities.core(iCiv).owner(iPlayer)
			
			# help England with settling Canada and Australia
			if iCiv == iEngland:
				colonialCities = cities.start(tCanadaTL).end(tCanadaBR).owner(iPlayer)
				colonialCities += cities.start(tAustraliaTL).end(tAustraliaBR).owner(iPlayer)
				
				if colonialCities:
					sourceCities = colonialCities
					
			city = sourceCities.coastal().random()
			if city:
				tSeaPlot = self.findSeaPlots(city, 1, iCiv)
				if not tSeaPlot: tSeaPlot = city
				
				makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), tSeaPlot, UnitAITypes.UNITAI_SETTLER_SEA)
				makeUnit(iPlayer, iSettler, tSeaPlot, UnitAITypes.UNITAI_SETTLE)
				makeUnit(iPlayer, getBestDefender(iPlayer), tSeaPlot)
				makeUnit(iPlayer, iWorker, tSeaPlot)
				
				data.players[iPlayer].iColonistsAlreadyGiven += 1


def giveRaiders(iCiv):
	pPlayer = player(iCiv)
	pTeam = team(iCiv)
	
	if pPlayer.isAlive() and not pPlayer.isHuman():
		city = cities.owner(iCiv).coastal().random()
		if city:
			seaPlot = self.findSeaPlots(location(city), 1, iCiv)
			if seaPlot:
				makeUnit(iCiv, unique_unit(iCiv, iGalley), seaPlot, UnitAITypes.UNITAI_ASSAULT_SEA)
				if pTeam.isHasTech(iSteel):
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iHeavySwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)
				else:
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK)
					makeUnit(iCiv, unique_unit(iCiv, iSwordsman), seaPlot, UnitAITypes.UNITAI_ATTACK_CITY)


def handleColonialAcquisition(iPlayer):
	pPlayer = player(iPlayer)
	iCiv = civ(iPlayer)
	
	targets = getColonialTargets(iPlayer, bEmpty=True)
	if not targets:
		return
		
	iGold = targets.count() * 200
	
	targetPlayers = targets.cities().owners()
	freePlots = targets.where(lambda plot: not city(plot))
	
	for plot in freePlots:
		colonialAcquisition(iPlayer, plot)

	for iTarget in targetPlayers:
		if player(iTarget).isHuman():
			askedCities = [(x, y) for x, y in targets if city_(x, y).getOwner() == iTarget]
			message = format_separators(askedCities, ',', text("TXT_KEY_AND"), lambda tile: city_(tile).getName())
					
			iAskGold = len(askedCities) * 200
					
			popup = Popup.PyPopup(7625, EventContextTypes.EVENTCONTEXT_ALL)
			popup.setHeaderString(text("TXT_KEY_ASKCOLONIALCITY_TITLE", adjective(iPlayer)))
			popup.setBodyString(text("TXT_KEY_ASKCOLONIALCITY_MESSAGE", adjective(iPlayer), iAskGold, message))
			popup.addButton(text("TXT_KEY_POPUP_YES"))
			popup.addButton(text("TXT_KEY_POPUP_NO"))
			data.lTempEventList = (iPlayer, askedCities)
			popup.launch(False)
			
		else:
			bAccepted = is_minor(iTarget) or (rand(100) >= dPatienceThreshold[iTarget] and not team(iPlayer).isAtWar(iTarget))
			iNumCities = targets.cities().owner(iTarget).count()
					
			if iNumCities >= player(iTarget).getNumCities():
				bAccepted = False
			
			for plot in targets.cities().owner(iTarget):
				if bAccepted:
					colonialAcquisition(iPlayer, plot)
					player(iTarget).changeGold(200)
				else:
					data.timedConquest(iPlayer, location(plot))

	iNewGold = pPlayer.getGold() - iGold
	pPlayer.setGold(max(0, iNewGold))


def handleColonialConquest(iPlayer):
	targets = getColonialTargets(iPlayer)
	
	if not targets:
		handleColonialAcquisition(iPlayer)
		return

	for plot in targets:
		data.timedConquest(iPlayer, location(plot))
		
	seaPlot = plots.surrounding(targetList[0]).water().random()

	if seaPlot:
		makeUnit(iPlayer, unique_unit(iPlayer, iGalleon), seaPlot)


def placeHut(tTL, tBR):
	plotList = []
	
	for plot in plots.start(tTL).end(tBR):
		if plot.isFlatlands() or plot.isHills():
			if plot.getFeatureType() != iMud:
				if plot.getOwner() < 0:
					plotList.append(location(plot))
	
	if not plotList:
		return
	
	tPlot = random_entry(plotList)
	plot_(tPlot).setImprovementType(iHut)