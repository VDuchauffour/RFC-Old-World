from Core import *
from unittest import *


def assertType(test, obj, expected_type):
	test.assertEqual(type(obj), expected_type)


class TestTurn(TestCase):

	def test_equals(self):
		self.assertEqual(Turn(10), Turn(10))

	def test_equals_int(self):
		self.assertEqual(Turn(10), 10)
		
	def test_add_turns(self):
		# given
		turn = Turn(10)
		
		# when
		added_turn = turn + Turn(10)
		
		# then
		self.assert_(isinstance(added_turn, Turn))
		self.assertEqual(added_turn, Turn(20))
		
	def test_add_int_to_turn(self):
		# given
		turn = Turn(10)
		
		# when
		added_turn = turn + 10
		
		# then
		self.assert_(isinstance(added_turn, Turn))
		self.assertEqual(added_turn, Turn(20))
		
	def test_subtract_turns(self):
		# given
		turn = Turn(20)
		
		# when
		subtracted_turn = turn - Turn(10)
		
		# then
		self.assert_(isinstance(subtracted_turn, Turn))
		self.assertEqual(subtracted_turn, Turn(10))
		
	def test_between(self):
		# given
		start = -3000
		end = -2000
		turn = Turn(2)
		
		# when/then
		self.assert_(turn.between(start, end))
		
	def test_not_between(self):
		# given
		start = -3000
		end = -2000
		turn = Turn(100)
		
		# when/then
		self.assert_(not turn.between(start, end))
		
	def test_between_at_border(self):
		# given
		start = -3000
		end = -2000
		turn = Turn(0) # 3000 BC
		
		# when/then
		self.assert_(turn.between(start, end))
		
	def test_between_inverse(self):
		# given
		start = -2000
		end = -3000
		turn = Turn(2)
		
		# when/then
		self.assert_(not turn.between(start, end))
		
	def test_deviate(self):
		# given
		turn = Turn(100)
		
		# when
		bExceeded = False
		for _ in range(1000):
			if not (90 <= turn.deviate(10) <= 110):
				bExceeded = True
				
		# then
		self.assert_(not bExceeded)
		
	def test_deviate_seed(self):
		# given
		turn = Turn(100)
		iSeed = 25
		
		# when
		new_turn = turn.deviate(10, 25)
		
		# then
		self.assertEqual(new_turn, 95)
		
		
class TestInfos(TestCase):

	def setUp(self):
		self.infos = Infos()
		
	def test_type(self):
		# given
		string = 'CIVILIZATION_EGYPT'
		expected_type = iCivEgypt
		
		# when
		actual_type = self.infos.type(string)
		
		# then
		self.assert_(isinstance(actual_type, int))
		self.assertEqual(actual_type, expected_type)
		
	def test_nonexistent_type(self):
		self.assertRaises(ValueError, self.infos.type, 'ABCDEF')
		
	def test_constant(self):
		# given
		string = 'CIV4_VERSION'
		expected_value = 319
		
		# when
		actual_value = self.infos.constant(string)
		
		# then
		self.assert_(isinstance(actual_value, int))
		self.assertEqual(actual_value, expected_value)
		
	def test_civ(self):
		# given
		iCiv = 0
		expected_civinfo = gc.getCivilizationInfo(iCiv)
		
		# when
		actual_civinfo = self.infos.civ(iCiv)
	
		# then
		self.assert_(isinstance(actual_civinfo, CvCivilizationInfo))
		self.assertEqual(actual_civinfo.getText(), expected_civinfo.getText())
		
	def test_civ_player(self):
		# given
		player = gc.getPlayer(0)
		expected_civinfo = gc.getCivilizationInfo(iCivEgypt)
		
		# when
		actual_civinfo = self.infos.civ(player)
		
		# then
		self.assert_(isinstance(actual_civinfo, CvCivilizationInfo))
		self.assertEqual(actual_civinfo.getText(), expected_civinfo.getText())
		
	def test_religion(self):
		# given
		iReligion = 0
		expected_religioninfo = gc.getReligionInfo(iReligion)
		
		# when
		actual_religioninfo = self.infos.religion(iReligion)
		
		# then
		self.assert_(isinstance(actual_religioninfo, CvReligionInfo))
		self.assertEqual(actual_religioninfo.getText(), expected_religioninfo.getText())
		
	def test_gameSpeed(self):
		# given
		iGameSpeed = 0
		expected_gamespeedinfo = gc.getGameSpeedInfo(iGameSpeed)
		
		# when
		actual_gamespeedinfo = self.infos.gameSpeed(iGameSpeed)
		
		# then
		self.assert_(isinstance(actual_gamespeedinfo, CvGameSpeedInfo))
		self.assertEqual(actual_gamespeedinfo.getText(), expected_gamespeedinfo.getText())
		
	def test_gameSpeed_inferred(self):
		# given
		expected_gamespeedinfo = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType())
		
		# then
		actual_gamespeedinfo = self.infos.gameSpeed()
		
		# then
		self.assert_(isinstance(actual_gamespeedinfo, CvGameSpeedInfo))
		self.assertEqual(actual_gamespeedinfo.getText(), expected_gamespeedinfo.getText())
		
	def test_unit(self):
		# given
		iUnit = iSettler
		expected_unitinfo = gc.getUnitInfo(iSettler)
		
		# when
		actual_unitinfo = self.infos.unit(iUnit)
		
		# then
		self.assert_(isinstance(actual_unitinfo, CvUnitInfo))
		self.assertEqual(actual_unitinfo.getText(), expected_unitinfo.getText())
		
	def test_unit_instance(self):
		# given
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		expected_unitinfo = gc.getUnitInfo(4)
		
		# when
		actual_unitinfo = self.infos.unit(unit)
		
		# then
		self.assert_(isinstance(actual_unitinfo, CvUnitInfo))
		self.assertEqual(actual_unitinfo.getText(), expected_unitinfo.getText())
		
		# cleanup
		unit.kill(False, 0)
		
	def test_unit_invalid(self):
		self.assertRaises(TypeError, self.infos.unit, gc.getMap().plot(0, 0))
		
	def test_feature(self):
		# given
		iFeature = iRainforest
		expected_featureinfo = gc.getFeatureInfo(iRainforest)
		
		# when
		actual_featureinfo = self.infos.feature(iFeature)
		
		# then
		self.assert_(isinstance(actual_featureinfo, CvFeatureInfo))
		self.assertEqual(actual_featureinfo.getText(), expected_featureinfo.getText())
		
	def test_feature_plot(self):
		# given
		plot = gc.getMap().plot(0, 0)
		plot.setFeatureType(iRainforest, 0)
		expected_featureinfo = gc.getFeatureInfo(iRainforest)
		
		# when
		actual_featureinfo = self.infos.feature(plot)
		
		# then
		self.assert_(isinstance(actual_featureinfo, CvFeatureInfo))
		
		# cleanup
		plot.setFeatureType(-1, -1)
		
	def test_feature_invalid(self):
		self.assertRaises(TypeError, self.infos.feature, gc.getMap())
		
	def test_tech(self):
		# given
		iTech = 0
		expected_techinfo = gc.getTechInfo(0)
		
		# when
		actual_techinfo = self.infos.tech(iTech)
		
		# then
		self.assert_(isinstance(actual_techinfo, CvTechInfo))
		self.assertEqual(actual_techinfo.getText(), expected_techinfo.getText())
		
	def test_bonus(self):
		# given
		iBonus = 0
		expected_bonusinfo = gc.getBonusInfo(0)
		
		# when
		actual_bonusinfo = self.infos.bonus(iBonus)
		
		# then
		self.assert_(isinstance(actual_bonusinfo, CvBonusInfo))
		self.assertEqual(actual_bonusinfo.getText(), expected_bonusinfo.getText())
		
	def test_bonus_plot(self):
		# given
		plot = gc.getMap().plot(0, 0)
		plot.setBonusType(iIron)
		expected_bonusinfo = gc.getBonusInfo(iIron)
		
		# when
		actual_bonusinfo = self.infos.bonus(plot)
		
		# then
		self.assert_(isinstance(actual_bonusinfo, CvBonusInfo))
		self.assertEqual(actual_bonusinfo.getText(), expected_bonusinfo.getText())
		
		# cleanup
		plot.setBonusType(-1)
		
	def test_bonus_invalid(self):
		self.assertRaises(TypeError, self.infos.bonus, gc.getMap())
		
	def test_handicap(self):
		# given
		expected_handicapinfo = gc.getHandicapInfo(gc.getGame().getHandicapType())
		
		# when
		actual_handicapinfo = self.infos.handicap()
		
		# then
		self.assert_(isinstance(actual_handicapinfo, CvHandicapInfo))
		self.assertEqual(actual_handicapinfo.getText(), expected_handicapinfo.getText())
		
	def test_corporation(self):
		# given
		iCorporation = 0
		expected_corporationinfo = gc.getCorporationInfo(0)
		
		# when
		actual_corporationinfo = self.infos.corporation(iCorporation)
		
		# then
		self.assert_(isinstance(actual_corporationinfo, CvCorporationInfo))
		self.assertEqual(actual_corporationinfo.getText(), expected_corporationinfo.getText())
		
	def test_building(self):
		# given
		iBuilding = 0
		expected_buildinginfo = gc.getBuildingInfo(0)
		
		# when
		actual_buildinginfo = self.infos.building(iBuilding)
		
		# then
		self.assert_(isinstance(actual_buildinginfo, CvBuildingInfo))
		self.assertEqual(actual_buildinginfo.getText(), expected_buildinginfo.getText())
		
	def test_art(self):
		# given
		string = 'INTERFACE_EVENT_BULLET'
		expected_path = ',Art/Interface/Buttons/Process/Blank.dds,Art/Interface/Buttons/Beyond_the_Sword_Atlas.dds,8,5'
		
		# when
		actual_path = self.infos.art(string)
		
		# then
		self.assertEqual(actual_path, expected_path)
		
	def test_art_nonexistent(self):
		self.assertRaises(ValueError, self.infos.art, 'ABCDEF')
		
	def test_commerce(self):
		# given
		iCommerce = 0
		expected_commerceinfo = gc.getCommerceInfo(0)
		
		# when
		actual_commerceinfo = self.infos.commerce(iCommerce)
		
		# then
		self.assert_(isinstance(actual_commerceinfo, CvCommerceInfo))
		self.assertEqual(actual_commerceinfo.getText(), expected_commerceinfo.getText())
		
	def test_promotions(self):
		self.assertEqual(self.infos.promotions(), range(gc.getNumPromotionInfos()))
		
	def test_promotion(self):
		# given
		iPromotion = 0
		expected_promotioninfo = gc.getPromotionInfo(0)
		
		# when
		actual_promotioninfo = self.infos.promotion(iPromotion)
		
		# then
		self.assert_(isinstance(actual_promotioninfo, CvPromotionInfo))
		self.assertEqual(actual_promotioninfo.getText(), expected_promotioninfo.getText())
	
	def test_project(self):
		# given
		iProject = 0
		expected_projectinfo = gc.getProjectInfo(0)
		
		# when
		actual_projectinfo = self.infos.project(iProject)
		
		# then
		self.assert_(isinstance(actual_projectinfo, CvProjectInfo))
		self.assertEqual(actual_projectinfo.getText(), expected_projectinfo.getText())
	
	def test_leader(self):
		# given
		iLeader = 0
		expected_leaderheadinfo = gc.getLeaderHeadInfo(0)
		
		# when
		actual_leaderheadinfo = self.infos.leader(iLeader)
		
		# then
		self.assert_(isinstance(actual_leaderheadinfo, CvLeaderHeadInfo))
		self.assertEqual(actual_leaderheadinfo.getText(), expected_leaderheadinfo.getText())
	
	def test_leader_player(self):
		# given
		player = gc.getPlayer(0)
		expected_leaderheadinfo = gc.getLeaderHeadInfo(iRamesses)
		
		# then
		actual_leaderheadinfo = self.infos.leader(player)
		
		# then
		self.assert_(isinstance(actual_leaderheadinfo, CvLeaderHeadInfo))
		self.assertEqual(actual_leaderheadinfo.getText(), expected_leaderheadinfo.getText())
	
	def test_leader_invalid(self):
		self.assertRaises(TypeError, self.infos.leader, gc.getMap())
	
	def test_improvement(self):
		# given
		iImprovement = 0
		expected_improvementinfo = gc.getImprovementInfo(0)
		
		# when
		actual_improvementinfo = self.infos.improvement(iImprovement)
		
		# then
		self.assert_(isinstance(actual_improvementinfo, CvImprovementInfo))
		self.assertEqual(actual_improvementinfo.getText(), expected_improvementinfo.getText())
	
	def test_buildingClass(self):
		# given
		iBuildingClass = 0
		expected_buildingclassinfo = gc.getBuildingClassInfo(0)
		
		# when
		actual_buildingclassinfo = self.infos.buildingClass(iBuildingClass)
		
		# then
		self.assert_(isinstance(actual_buildingclassinfo, CvBuildingClassInfo))
		self.assertEqual(actual_buildingclassinfo.getText(), expected_buildingclassinfo.getText())
	
	def test_culture(self):
		# given
		iCultureLevel = 0
		expected_culturelevelinfo = gc.getCultureLevelInfo(0)
		
		# when
		actual_culturelevelinfo = self.infos.culture(iCultureLevel)
		
		# then
		self.assert_(isinstance(actual_culturelevelinfo, CvCultureLevelInfo))
		self.assertEqual(actual_culturelevelinfo.getText(), expected_culturelevelinfo.getText())
	
	def test_era(self):
		# given
		iEra = 0
		expected_erainfo = gc.getEraInfo(0)
		
		# when
		actual_erainfo = self.infos.era(iEra)
		
		# then
		self.assert_(isinstance(actual_erainfo, CvEraInfo))
		self.assertEqual(actual_erainfo.getText(), expected_erainfo.getText())
		
		
class TestDefaultDict(TestCase):

	def setUp(self):
		self.normaldict = {1: 'one', 2: 'two', 3: 'three'}
		self.defaultdict = DefaultDict(self.normaldict, 'other')
	
	def test_equals_dict(self):
		self.assertEqual(self.normaldict, self.defaultdict)
		
	def test_immutable_under_base_dictionary(self):
		self.normaldict[4] = 'four'
		
		self.assert_(4 not in self.defaultdict)
		
	def test_does_not_contain_missing(self):
		self.assert_(4 not in self.defaultdict)
		
	def test_returns_default_if_missing(self):
		self.assertEqual(self.defaultdict[4], 'other')
		
	def test_can_append_to_default_list(self):
		# given
		defaultdict = DefaultDict({1: ['one'], 2: ['two']}, [])
		
		# when
		defaultdict[3].append('three')
		
		# then
		self.assertEqual(defaultdict[3], ['three'])
		
	def test_defaultdict(self):
		test_dict = defaultdict(self.normaldict, 0)
		assertType(self, test_dict, DefaultDict)
		self.assertEqual(test_dict[0], 0)
		
	def test_deepdict(self):
		deep_dict = deepdict(self.normaldict)
		assertType(self, deep_dict, DefaultDict)
		assertType(self, deep_dict[0], dict)
		self.assertEqual(deep_dict[0], {})
		
	def test_appenddict(self):
		append_dict = appenddict(self.normaldict)
		assertType(self, append_dict, DefaultDict)
		assertType(self, append_dict[0], list)
		self.assertEqual(append_dict[0], [])
		
		
class TestCreatedUnits(TestCase):

	def setUp(self):
		units = []
		for x, y in [(0, 0), (0, 1), (0, 2)]:
			unit = gc.getPlayer(0).initUnit(0, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			units.append(unit)
			
		self.created_units = CreatedUnits(units)
		
	def tearDown(self):
		for unit in self.created_units:
			unit.kill(False, 0)
			
	def test_adjective(self):
		# given
		expected_names = ["Egyptian %s" % unit.getName() for unit in self.created_units]
		
		# when
		created_units = self.created_units.adjective('Egyptian')
		actual_names = [unit.getName() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_names, expected_names)
		
	def test_adjective_text_key(self):
		# given
		expected_names = ["Egyptian %s" % unit.getName() for unit in self.created_units]
		
		# when
		created_units = self.created_units.adjective('TXT_KEY_CIV_EGYPT_ADJECTIVE')
		actual_names = [unit.getName() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_names, expected_names)
		
	def test_adjective_empty(self):
		# given
		expected_names = [unit.getName() for unit in self.created_units]
		
		# when
		created_units = self.created_units.adjective('')
		actual_names = [unit.getName() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_names, expected_names)
	
	def test_experience(self):
		# given
		expected_experiences = [5, 5, 5]
		
		# when
		created_units = self.created_units.experience(5)
		actual_experiences = [unit.getExperience() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_experiences, expected_experiences)
		
	def test_experiences_invalid(self):
		# given
		expected_experiences = [0, 0, 0]
		
		# when
		created_units = self.created_units.experience(-5)
		actual_experiences = [unit.getExperience() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_experiences, expected_experiences)
	
	def test_one(self):
		# given
		unit = gc.getPlayer(0).initUnit(0, 1, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		created_units = CreatedUnits([unit])
		
		# when
		single_unit = created_units.one()
		
		# then
		self.assertEqual(unit.getID(), single_unit.getID())
		
		# cleanup
		single_unit.kill(False, 0)
	
	def test_one_many_units(self):
		# when
		self.assertRaises(Exception, self.created_units.one)
		
		
class TestPlayers(TestCase):

	def setUp(self):
		self.players = Players([0, 1, 2])

	def test_contains_player(self):
		self.assert_(gc.getPlayer(0) in self.players)
		
	def test_contains_civ_id(self):
		self.assert_(iCivEgypt in self.players)
		
	def test_iterate(self):
		for element in self.players:
			self.assert_(isinstance(element, int))
			self.assertEqual(gc.getPlayer(element).getID(), element)
			
	def test_string(self):
		expected_names = ','.join(['Egypt', 'Babylonia', 'Harappa'])
		actual_names = str(self.players)
		self.assertEqual(actual_names, expected_names)
		
	def test_players(self):
		expected_ids = [0, 1, 2]
		actual_ids = [player.getID() for player in self.players.players()]
		self.assertEqual(actual_ids, expected_ids)
		
	def test_alive(self):
		players = Players([0, 1, 2, 3])
		self.assert_(gc.getPlayer(3) in players)
		
		players = players.alive()
		assertType(self, players, Players)
		self.assert_(gc.getPlayer(3) not in players)
		
	def test_ai(self):
		players = self.players.ai()
		assertType(self, players, Players)
		self.assertEqual(len(players), 2)
		self.assert_(gc.getPlayer(0) not in players)
		
	def test_without_player_id(self):
		players = self.players.without(0)
		assertType(self, players, Players)
		self.assertEqual(len(players), 2)
		self.assert_(gc.getPlayer(0) not in players)
		
	def test_without_list(self):
		players = self.players.without([0, 1])
		assertType(self, players, Players)
		self.assertEqual(len(players), 1)
		self.assert_(gc.getPlayer(2) in players)
		
	def test_without_set(self):
		players = self.players.without(set([0, 1]))
		assertType(self, players, Players)
		self.assertEqual(len(players), 1)
		self.assert_(gc.getPlayer(2) in players)
		
	def test_cities_none(self):
		cities = self.players.cities()
		assertType(self, cities, Cities)
		self.assertEqual(len(cities), 0)
		
	def test_cities(self):
		# given
		expected_locations = [(66, 0), (68, 0), (70, 0)]
		for i, (x, y) in enumerate(expected_locations):
			gc.getPlayer(i).initCity(x, y)
			
		# when
		cities = self.players.cities()
		assertType(self, cities, Cities)
		actual_locations = [(city.getX(), city.getY()) for city in cities]
		
		# then
		self.assertEqual(set(actual_locations), set(expected_locations))
		
		# cleanup
		for x, y in expected_locations:
			gc.getMap().plot(x, y).getPlotCity().kill()
			
			
class TestPlayerFactory(TestCase):

	def setUp(self):
		self.factory = PlayerFactory()
		
	def test_all(self):
		players = self.factory.all()
		assertType(self, players, Players)
		self.assertEqual(len(players), iNumTotalPlayers)
		
	def test_major(self):
		players = self.factory.major()
		assertType(self, players, Players)
		self.assertEqual(len(players), iNumPlayers)
		
	def test_with_barbarian(self):
		players = self.factory.withBarbarian()
		assertType(self, players, Players)
		self.assertEqual(len(players), iNumTotalPlayersB)
		
	def test_minor(self):
		players = self.factory.minor()
		assertType(self, players, Players)
		for p in players:
			self.assert_(gc.getPlayer(p).isMinorCiv() or gc.getPlayer(p).isBarbarian())
	
	def test_vassals(self):
		# given
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, True, False)
		
		# when
		vassals = self.factory.vassals(2)
		
		# then
		assertType(self, vassals, Players)
		self.assertEqual(len(vassals), 1)
		self.assert_(gc.getPlayer(1) in vassals)
		
		# cleanup
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, False, False)
	
	def test_none(self):
		players = self.factory.none()
		assertType(self, players, Players)
		self.assertEqual(len(players), 0)
		
		
class TestUnits(TestCase):

	def setUp(self):
		units = []
		for x, y in [(0, 0), (0, 1), (0, 2), (0, 3)]:
			unit = gc.getPlayer(3).initUnit(4, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			units.append(unit)
		self.units = Units(units)
		self.unit = units[0]
			
	def tearDown(self):
		for unit in self.units:
			unit.kill(False, 3)
			
	def test_basic(self):
		assertType(self, self.units, Units)
		self.assertEqual(len(self.units), 4)
			
	def test_contains(self):
		self.assert_(self.unit in self.units)
		
	def test_contains_int(self):
		self.assertRaises(TypeError, self.units.__contains__, 0)
		
	def test_string(self):
		expected_string = "Settler (Chinese) at (0, 0), Settler (Chinese) at (0, 1), Settler (Chinese) at (0, 2), Settler (Chinese) at (0, 3)"
		self.assertEqual(str(self.units), expected_string)
		
	def test_owner(self):
		# given
		indian_unit = gc.getPlayer(4).initUnit(4, 0, 4, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		units = self.units + Units([indian_unit])
		
		# when
		indian_units = units.owner(4)
		
		# then
		assertType(self, indian_units, Units)
		self.assertEqual(len(indian_units), 1)
		self.assert_(indian_unit in indian_units)
		
		# cleanup
		indian_unit.kill(False, 4)
		
	def test_type(self):
		# given
		worker = gc.getPlayer(3).initUnit(7, 0, 4, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		units = self.units + Units([worker])
		
		# when
		workers = units.type(7)
		
		# then
		assertType(self, workers, Units)
		self.assertEqual(len(workers), 1)
		self.assert_(worker in workers)

		# cleanup
		worker.kill(False, 3)
		
	def test_by_type(self):
		# given
		worker = gc.getPlayer(3).initUnit(7, 0, 4, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		units = self.units + Units([worker])
		
		# when
		grouped = units.by_type()
		
		# then
		assertType(self, grouped, dict)
		self.assertEqual(len(grouped), 2)
		self.assert_(4 in grouped)
		self.assertEqual(len(grouped[4]), 4)
		self.assert_(7 in grouped)
		self.assertEqual(len(grouped[7]), 1)
		
		# cleanup
		worker.kill(False, 3)
		
		
class TestUnitFactory(TestCase):

	def setUp(self):
		self.factory = UnitFactory()
		self.units = []
		for _ in range(4):
			unit = gc.getPlayer(3).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			self.units.append(unit)
			
		for _ in range(3):
			unit = gc.getPlayer(4).initUnit(4, 0, 2, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			self.units.append(unit)

	def tearDown(self):
		for unit in self.units:
			unit.kill(False, unit.getOwner())

	def test_owner_id(self):
		# when
		chinese_units = self.factory.owner(3)
		
		# then
		assertType(self, chinese_units, Units)
		self.assertEqual(len(chinese_units), 4)
		
	def test_owner_player(self):
		# when
		chinese_units = self.factory.owner(gc.getPlayer(3))
		
		# then
		assertType(self, chinese_units, Units)
		self.assertEqual(len(chinese_units), 4)
		
	def test_at_coordinates(self):
		# when
		indian_units = self.factory.at(0, 2)
		
		# then
		assertType(self, indian_units, Units)
		self.assertEqual(len(indian_units), 3)
		
	def test_at_plot(self):
		# when
		indian_units = self.factory.at(gc.getMap().plot(0, 2))
		
		# then
		assertType(self, indian_units, Units)
		self.assertEqual(len(indian_units), 3)
		

class TestPlots(TestCase):

	def setUp(self):
		self.tiles = [(x, y) for x in range(3) for y in range(3)]
		self.plots = Plots(self.tiles)

	def test_basic(self):
		assertType(self, self.plots, Plots)
		self.assertEqual(len(self.plots), 9)
		
	def test_contains_tile(self):
		self.assert_((1, 1) in self.plots)
		
	def test_does_not_contain_tile(self):
		self.assert_((4, 4) not in self.plots)
		
	def test_contains_plot(self):
		self.assert_(gc.getMap().plot(1, 1) in self.plots)
		
	def test_contains_unit(self):
		unit = gc.getPlayer(3).initUnit(4, 1, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		self.assert_(unit in self.plots)
		unit.kill(False, 3)
		
	def test_contains_city(self):
		city = gc.getPlayer(3).initCity(1, 1)
		self.assert_(city in self.plots)
		city.kill()
		
	def test_string(self):
		self.assertEqual(str(self.plots), str(self.tiles))
		
	def test_cities(self):
		# given
		first_city = gc.getPlayer(3).initCity(0, 0)
		second_city = gc.getPlayer(3).initCity(2, 2)
		
		# when
		cities = self.plots.cities()
		
		# then
		assertType(self, cities, Cities)
		self.assertEqual(len(cities), 2)
		self.assert_(first_city in cities)
		self.assert_(second_city in cities)
		
		# cleanup
		first_city.kill()
		second_city.kill()
		
	def test_units(self):
		# given
		tile_units = []
		for x, y in [(0, 0), (0, 2), (2, 0), (2, 2)]:
			unit = gc.getPlayer(3).initUnit(4, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			tile_units.append(unit)
		
		# when
		units = self.plots.units()
		
		# then
		assertType(self, units, Units)
		self.assertEqual(len(units), 4)
		for unit in tile_units:
			self.assert_(unit in units)
			
		# cleanup
		for unit in tile_units:
			unit.kill(False, 3)
			
	def test_without_tile(self):
		plots = self.plots.without((1, 1))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((1, 1) not in plots)
		
	def test_without_plot(self):
		plots = self.plots.without(gc.getMap().plot(1, 1))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((1, 1) not in plots)
		
	def test_without_city(self):
		city = gc.getPlayer(3).initCity(1, 1)
		plots = self.plots.without(city)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((1, 1) not in plots)
		
		city.kill()
		
	def test_without_unit(self):
		unit = gc.getPlayer(3).initUnit(4, 1, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		plots = self.plots.without(unit)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((1, 1) not in plots)
		
		unit.kill(False, 3)
		
	def test_without_list(self):
		tiles = [(0, 0), (1, 0), (2, 0)]
		plots = self.plots.without(tiles)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 6)
		for tile in tiles:
			self.assert_(tile not in plots)
			
	def test_without_set(self):
		tiles = [(0, 0), (1, 0), (2, 0)]
		plots = self.plots.without(set(tiles))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 6)
		for tile in tiles:
			self.assert_(tile not in plots)
			
	def test_closest(self):
		closest = self.plots.closest(3, 3)
		
		assertType(self, closest, CyPlot)
		self.assertEqual((closest.getX(), closest.getY()), (2, 2))
		
	def test_closest_distance(self):
		distance = self.plots.closest_distance(3, 3)
		
		assertType(self, distance, int)
		self.assertEqual(distance, 1)
		
	def test_notowner(self):
		# given
		gc.getMap().plot(1, 1).setOwner(1)
		
		# when
		plots = self.plots.notowner(1)
		
		# then
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((1, 1) not in plots)
		
		# cleanup
		gc.getMap().plot(1, 1).setOwner(-1)
		
	def test_where_surrounding(self):
		# given
		unit = gc.getPlayer(3).initUnit(4, 3, 3, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		# when
		plots = self.plots.where_surrounding(lambda p: p.getNumUnits() == 0)
		
		# then
		print "units: %s" % Plots([(x, y) for x in range(5) for y in range(5)]).units()
		print "test_where_surrounding: %s" % plots 
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((2, 2) not in plots)
		
		# cleanup
		unit.kill(False, 3)
		
	def test_land(self):
		plots = Plots([(64+x, 10+y) for x in range(3) for y in range(3)])
		self.assertEqual(len(plots.land()), 9)
		
	def test_no_land(self):
		self.assertEqual(len(self.plots.land()), 0)
		
	def test_water(self):
		self.assertEqual(len(self.plots.water()), 9)
		
	def test_no_water(self):
		plots = Plots([(64+x, 10+y) for x in range(3) for y in range(3)])
		self.assertEqual(len(plots.water()), 0)
		
	def test_core(self):
		plots = Plots([(67+x, 33+y) for x in range(3) for y in range(3)])
		self.assertEqual(len(plots.core(0)), 9)
		
	def test_no_core(self):
		self.assertEqual(len(self.plots.core(0)), 0)
		
	def test_any(self):
		self.assert_(self.plots.any(lambda p: p.getX() == 0))
		
	def test_not_any(self):
		self.assert_(not self.plots.any(lambda p: p.getX() == 3))
		
	def test_all(self):
		self.assert_(self.plots.all(lambda p: p.getX() < 3))
		
	def test_not_all(self):
		self.assert_(not self.plots.all(lambda p: p.getX() < 2))
		
	def test_none(self):
		self.assert_(self.plots.none(lambda p: p.getX() > 2))
		
	def test_not_none(self):
		self.assert_(not self.plots.none(lambda p: p.getX() > 1))
		
	def test_first(self):
		plot = self.plots.first()
		self.assertEqual((plot.getX(), plot.getY()), (0, 0))
		
	def test_sample(self):
		plots = self.plots.sample(3)
		assertType(self, plots, list)
		self.assertEqual(len(plots), 3)
		self.assertEqual(len(set(plots)), 3)
		
	def test_sample_invalid_size(self):
		plots = self.plots.sample(0)
		self.assertEqual(plots, None)
		
	def test_sample_empty(self):
		plots = self.plots.where(lambda p: False).sample(3)
		assertType(self, plots, list)
		self.assertEqual(len(plots), 0)
		
	def test_buckets(self):
		x_one, y_one, rest = self.plots.buckets(lambda p: p.getX() == 1, lambda p: p.getY() == 1)
		
		assertType(self, x_one, Plots)
		assertType(self, y_one, Plots)
		assertType(self, rest, Plots)
		
		self.assertEqual(len(x_one), 3)
		self.assertEqual(len(y_one), 3)
		self.assertEqual(len(rest), 4)
		
		self.assert_(x_one.all(lambda p: p.getX() == 1))
		self.assert_(y_one.all(lambda p: p.getY() == 1))
		self.assert_(rest.all(lambda p: p.getX() != 1 and p.getY() != 1))
		
	def test_split(self):
		even, odd = self.plots.split(lambda p: (p.getX() + p.getY()) % 2 == 0)
		
		assertType(self, even, Plots)
		assertType(self, odd, Plots)
		
		self.assertEqual(len(even), 5)
		self.assertEqual(len(odd), 4)
		
		self.assert_(even.all(lambda p: (p.getX() + p.getY()) % 2 == 0))
		self.assert_(odd.all(lambda p: (p.getX() + p.getY()) % 2 == 1))
		
	def test_sort(self):
		expected_tiles = [(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (1, 2), (2, 1), (2, 2)]
		
		plots = self.plots.sort(lambda p: p.getX() + p.getY())
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		assertType(self, plots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_highest(self):
		expected_tiles = [(2, 2), (1, 2), (2, 1)]
		
		plots = self.plots.highest(3, lambda p: p.getX() + p.getY())
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		assertType(self, plots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_lowest(self):
		expected_tiles = [(0, 0), (0, 1), (1, 0)]
		
		plots = self.plots.lowest(3, lambda p: p.getX() + p.getY())
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		assertType(self, plots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_including_tile(self):
		plots = self.plots.including((3, 3))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 10)
		self.assert_((3, 3) in plots)
		
	def test_including_tiles(self):
		plots = self.plots.including((3, 3), (4, 4), (5, 5))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 12)
		for tile in [(3, 3), (4, 4), (5, 5)]:
			self.assert_(tile in plots)
			
	def test_including_plots(self):
		included = Plots([(3, 3), (4, 4), (5, 5)])
		plots = self.plots.including(included)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 12)
		for tile in [(3, 3), (4, 4), (5, 5)]:
			self.assert_(tile in plots)
			
	def test_limit(self):
		plots = self.plots.limit(3)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 3)
		for tile in [(0, 0), (0, 1), (0, 2)]:
			self.assert_(tile in plots)
			
	def test_count(self):
		self.assertEqual(self.plots.count(), 9)
		
	def test_maximum(self):
		max = self.plots.maximum(lambda p: p.getX() + p.getY())
		
		assertType(self, max, CyPlot)
		self.assertEqual((max.getX(), max.getY()), (2, 2))
		
	def test_rank(self):
		rank = self.plots.rank((2, 2), lambda p: p.getX() * p.getY())
		
		assertType(self, rank, int)
		self.assertEqual(rank, 0)
		
	def test_shuffle(self):
		plots = self.plots.shuffle()
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 9)
		self.assert_(plots != self.plots)
		
	def test_fraction(self):
		plots = self.plots.fraction(3)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 3)
		self.assertEqual(plots, self.plots.limit(3))
		
	def test_sum(self):
		sum = self.plots.sum(lambda p: p.getX() + p.getY())
		
		assertType(self, sum, int)
		self.assertEqual(sum, 18)
		
	def test_accessor(self):
		plot = self.plots[0]
		
		assertType(self, plot, CyPlot)
		self.assertEqual((plot.getX(), plot.getY()), (0, 0))
		
	def test_add(self):
		added = Plots([(0, 3), (1, 3), (2, 3)])
		plots = self.plots + added
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 12)
		for tile in [(x, y) for x in range(3) for y in range(4)]:
			self.assert_(tile in plots)
			
	def test_add_other_class(self):
		added = Cities([(0, 3), (1, 3), (2, 3)])
		
		self.assertRaises(TypeError, self.plots.__add__, added)
		
	def test_string(self):
		expected_string = str(self.tiles)
		actual_string = str(self.plots)
		self.assertEqual(actual_string, expected_string)
		
	def test_same(self):
		self.assert_(self.plots.same(self.plots.shuffle()))
		
	def test_equal(self):
		plots = Plots(self.tiles)
		self.assertEqual(self.plots, plots)
		
	def test_unequal_with_different_order(self):
		plots = self.plots.sort(lambda p: p.getY())
		self.assert_(self.plots != plots)
		
	def test_equal_other_class(self):
		cities = Cities(self.tiles)
		self.assertRaises(TypeError, self.plots.__eq__, cities)
		
	def test_greater_than_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(plots > self.plots)
		
	def test_greater_than_int(self):
		self.assert_(self.plots > 8)
		
	def test_greater_than_other_class(self):
		cities = Cities(self.tiles)
		self.assertRaises(TypeError, self.plots.__gt__, cities)
		
	def test_greater_equal_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(plots >= self.plots)
		
	def test_greater_equal_int(self):
		self.assert_(self.plots >= 9)
		self.assert_(self.plots >= 8)
		
	def test_greater_equal_other_class(self):
		cities = Cities(self.tiles)
		self.assertRaises(TypeError, self.plots.__ge__, cities)
		
	def test_less_than_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(self.plots < plots)
		
	def test_less_than_int(self):
		self.assert_(self.plots < 10)
		
	def test_less_than_other_class(self):
		cities = Cities(self.tiles)
		self.assertRaises(TypeError, self.plots.__lt__, cities)
		
	def test_less_equal_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(self.plots <= plots)
		
	def test_less_equal_int(self):
		self.assert_(self.plots <= 9)
		self.assert_(self.plots <= 10)
		
	def test_less_equal_other_class(self):
		cities = Cities(self.tiles)
		self.assertRaises(TypeError, self.plots.__le__, cities)
		
	def test_iterate_all_does_not_contain_invalid(self):
		for plot in plots.all():
			self.assert_((plot.getX(), plot.getY()) != (-1, -1))
			
	def test_regions(self):
		tiles = [(23, 37), (26, 38), (26, 40)] # mesoamerica, caribbean, usa
		plots = Plots(tiles)
		
		expected_tiles = [(23, 37), (26, 38)]
		actual_plots = plots.regions(rCaribbean, rMesoamerica)
		actual_tiles = [(plot.getX(), plot.getY()) for plot in actual_plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
		
class TestPlotFactory(TestCase):

	def setUp(self):
		self.factory = PlotFactory()
		
	def test_of(self):
		tiles = [(0, 0), (0, 1), (0, 2)]
		self.assertEqual(self.factory.of(tiles), Plots(tiles))
		
	def test_rectangle(self):
		plots = self.factory.rectangle((0, 0), (2, 2))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_rectangle_inverted(self):
		plots = self.factory.rectangle((2, 2), (0, 0))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_rectangle_diagonal(self):
		plots = self.factory.rectangle((0, 2), (2, 0))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_rectangle_plots(self):
		plots = self.factory.rectangle(gc.getMap().plot(0, 0), gc.getMap().plot(2, 2))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_all(self):
		plots = self.factory.all()
		self.assertEqual(len(plots), iWorldX * iWorldY)
		
	def test_region(self):
		expected_tiles = [(25, 38), (26, 38), (27, 38), (27, 36), (29, 37), (30, 37), (30, 39), (32, 37), (33, 33), (33, 35)]
		region = Plots(expected_tiles)
		plots = self.factory.region(rCaribbean)
		self.assertEqual(len(region), len(plots))
		self.assert_(plots.same(region))
		
	def test_regions_single(self):
		self.assert_(self.factory.region(rCaribbean).same(self.factory.regions(rCaribbean)))
	
	def test_regions_multiple(self):
		self.assert_(self.factory.regions(rEgypt, rMesopotamia).same(self.factory.region(rEgypt) + self.factory.region(rMesopotamia)))
	
	def test_surrounding(self):
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		plots = self.factory.surrounding((1, 1))
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_surrounding_wrap(self):
		expected_tiles = [(0, 0), (1, 0), (0, 1), (1, 1), (123, 0), (123, 1)]
		plots = self.factory.surrounding((0, 0))
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_surrounding_radius(self):
		expected_tiles = [(x, y) for x in range(5) for y in range(5)]
		plots = self.factory.surrounding((2, 2), radius=2)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_surrounding_zero(self):
		expected_tiles = [(1, 1)]
		plots = self.factory.surrounding((1, 1), radius=0)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_surrounding_negative(self):
		self.assertRaises(ValueError, self.factory.surrounding, (1, 1), -1)
		
	def test_ring(self):
		expected_tiles = [(x, y) for x in range(3) for y in range(3) if (x, y) != (1, 1)]
		plots = self.factory.ring((1, 1), 1)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_ring_large(self):
		expected_tiles = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (1, 4), (2, 4), (3, 4)]
		plots = self.factory.ring((2, 2), 2)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_owner(self):
		gc.getMap().plot(0, 0).setOwner(0)
		gc.getMap().plot(1, 0).setOwner(0)
		
		expected_tiles = [(0, 0), (1, 0)]
		plots = self.factory.owner(0)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
		gc.getMap().plot(0, 0).setOwner(-1)
		gc.getMap().plot(1, 0).setOwner(-1)


class TestCities(TestCase):

	def setUp(self):
		gc.getPlayer(3).initCity(0, 0)
		gc.getPlayer(3).initCity(0, 2)
		gc.getPlayer(4).initCity(2, 0)
		
		self.cities = Cities([(0, 0), (0, 2), (2, 0)])
		
	def tearDown(self):
		for city in self.cities:
			city.kill()
			
	def test_basic(self):
		assertType(self, self.cities, Cities)
		self.assertEqual(len(self.cities), 3)
		
	def test_contains_tile(self):
		self.assert_((0, 0) in self.cities)
		
	def test_contains_plot(self):
		self.assert_(gc.getMap().plot(0, 0) in self.cities)
		
	def test_contains_city(self):
		self.assert_(gc.getMap().plot(0, 0).getPlotCity() in self.cities)
		
	def test_contains_unit(self):
		unit = gc.getPlayer(3).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		self.assert_(unit in self.cities)
		unit.kill(False, 3)
		
	def test_contains_other(self):
		self.assertRaises(TypeError, self.cities.__contains__, 0)
		
	def test_without_tile(self):
		cities = self.cities.without((0, 0))
		expected_tiles = [(0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_plot(self):
		cities = self.cities.without(gc.getMap().plot(0, 0))
		expected_tiles = [(0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_city(self):
		cities = self.cities.without(gc.getMap().plot(0, 0).getPlotCity())
		expected_tiles = [(0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_list(self):
		cities = self.cities.without([(0, 2), (2, 0)])
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_cities(self):
		subtracted = Cities([(0, 2), (2, 0)])
		cities = self.cities.without(subtracted)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_plots(self):
		subtracted = plots.rectangle((0, 0), (1, 2))
		cities = self.cities.without(subtracted)
		expected_tiles = [(2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_religion(self):
		self.cities[0].setHasReligion(0, True, False, False)
		cities = self.cities.religion(0)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_owner(self):
		cities = self.cities.owner(3)
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_building(self):
		self.cities[0].setHasRealBuilding(iFactory, True)
		cities = self.cities.building(iFactory)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_building_effect(self):
		self.cities[0].setHasRealBuilding(iFactory, True)
		cities = self.cities.building_effect(iFactory)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_core(self):
		city = gc.getPlayer(0).initCity(69, 33)
		cities = self.cities.including(city)
		self.assertEqual(len(cities), 4)
		actual_cities = cities.core(0)
		expected_tiles = [(69, 33)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in actual_cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
		city.kill()
		
	def test_coastal(self):
		city = gc.getPlayer(0).initCity(63, 10)
		cities = self.cities.including(city)
		actual_cities = cities.coastal()
		expected_tiles = [(63, 10)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in actual_cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
		city.kill()
		
	def test_regions(self):
		tiles = [(23, 37), (26, 38), (26, 40)] # mesoamerica, caribbean, usa
		created_cities = []
		for x, y in tiles:
			city = gc.getPlayer(0).initCity(x, y)
			created_cities.append(city)
		
		cities = Cities(tiles)
		
		expected_tiles = [(23, 37), (26, 38)]
		actual_cities = cities.regions(rCaribbean, rMesoamerica)
		actual_tiles = [(city.getX(), city.getY()) for city in actual_cities]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
		for city in created_cities:
			city.kill()
			
	def test_notowner(self):
		expected_tiles = [(2, 0)]
		
		cities = self.cities.notowner(3)
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		self.assertEqual(actual_tiles, expected_tiles)
		
		
class TestCityFactory(TestCase):

	def setUp(self):
		gc.getPlayer(3).initCity(0, 0)
		gc.getPlayer(3).initCity(0, 2)
		gc.getPlayer(4).initCity(2, 0)
		
		self.factory = CityFactory()
		
	def tearDown(self):
		for x, y in [(0, 0), (0, 2), (2, 0)]:
			gc.getMap().plot(x, y).getPlotCity().kill()
			
	def test_owner(self):
		cities = self.factory.owner(3)
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_all(self):
		cities = self.factory.all()
		expected_tiles = [(0, 0), (0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_rectangle(self):
		cities = self.factory.rectangle((0, 0), (1, 2))
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_region(self):
		caribbean = plots.region(rCaribbean).random()
		city = gc.getPlayer(3).initCity(caribbean.getX(), caribbean.getY())
		
		cities = self.factory.region(rCaribbean)
		
		assertType(self, cities, Cities)
		self.assertEqual(len(cities), 1)
		self.assert_(city in cities)
		
		city.kill()
		
	def test_of(self):
		cities = self.factory.of([(0, 0), (0, 1), (0, 2)])
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_surrounding(self):
		cities = self.factory.surrounding((0, 1))
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
		
class TestMove(TestCase):

	def setUp(self):
		self.unit = gc.getPlayer(3).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
	def tearDown(self):
		if self.unit.getX() >= 0:
			self.unit.kill(False, 3)

	def test_move_tile(self):
		move(self.unit, (0, 2))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 2))
		
	def test_move_plot(self):
		move(self.unit, gc.getMap().plot(0, 2))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 2))
		
	def test_move_city(self):
		city = gc.getPlayer(3).initCity(0, 2)
		move(self.unit, city)
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 2))
		
		city.kill()
		
	def test_move_no_destination(self):
		move(self.unit, None)
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 0))
		
	def test_move_invalid_location(self):
		self.unit.kill(False, 3)
		move(self.unit, (0, 2))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (-2147483647, -2147483647))
		
	def test_move_same_destination(self):
		move(self.unit, (0, 0))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 0))
	

class TestHasCivic(TestCase):

	def test_has_civic(self):
		self.assert_(has_civic(1, 0))
		
	def test_not_has_civic(self):
		self.assert_(not has_civic(1, 1))
		
	def test_has_civic_player(self):
		self.assert_(has_civic(gc.getPlayer(1), 0))
		
		
class TestScenarioUtils(TestCase):

	def test_scenario(self):
		self.assertEqual(scenario(), i3000BC)
		
	def test_scenario_start_turn(self):
		self.assertEqual(scenarioStartTurn(), 0)
		
	def test_scenario_start_year(self):
		self.assertEqual(scenarioStartYear(), -3000)
		
		
class TestUniqueUnitsAndBuildings(TestCase):

	def test_base_building_for_base(self):
		self.assertEqual(base_building(iMonument), iMonument)
		
	def test_base_building_for_unique(self):
		self.assertEqual(base_building(iObelisk), iMonument)
		
	def test_unique_building_for_base(self):
		self.assertEqual(unique_building(iEgypt, iMonument), iObelisk)
		
	def test_unique_building_for_unique(self):
		self.assertEqual(unique_building(iEgypt, iObelisk), iObelisk)
		
	def test_unique_building_no_player(self):
		self.assertEqual(unique_building(-1, iObelisk), iMonument)
		
	def test_base_unit_for_base(self):
		self.assertEqual(base_unit(iChariot), iChariot)
		
	def test_base_unit_for_unique(self):
		self.assertEqual(base_unit(iWarChariot), iChariot)
		
	def test_unique_unit_for_base(self):
		self.assertEqual(unique_unit(iEgypt, iChariot), iWarChariot)
		
	def test_unique_unit_for_unique(self):
		self.assertEqual(unique_unit(iEgypt, iWarChariot), iWarChariot)
		
	def test_unique_unit_no_player(self):
		self.assertEqual(unique_unit(-1, iWarChariot), iChariot)
		

class TestMasterAndVassal(TestCase):
	
	def test_master(self):
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, True, False)
		
		self.assertEqual(master(1), 2)
		
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, False, False)
		
	def test_master_no_vassal(self):
		self.assertEqual(master(1), None)
		
	def test_vassals(self):
		gc.getTeam(gc.getPlayer(0).getTeam()).setVassal(1, True, False)
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, True, False)
		gc.getTeam(gc.getPlayer(2).getTeam()).setVassal(1, True, False)
		
		vassal = vassals()
		
		assertType(self, vassal, DefaultDict)
		self.assertEqual(vassal[1], [0, 2])
		self.assertEqual(vassal[2], [1])
		self.assertEqual(vassal[0], [])
		
		gc.getTeam(gc.getPlayer(0).getTeam()).setVassal(1, False, False)
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, False, False)
		gc.getTeam(gc.getPlayer(2).getTeam()).setVassal(1, False, False)
		
	def test_vassals_no_vassals(self):
		vassal = vassals()
		assertType(self, vassal, DefaultDict)
		self.assertEqual(vassal[0], [])
		self.assertEqual(vassal[1], [])
		self.assertEqual(vassal[2], [])


class TestMinor(TestCase):

	def test_is_minor_independent(self):
		self.assert_(is_minor(iIndependent))
		
	def test_is_minor_barbarian(self):
		self.assert_(is_minor(iBarbarian))
		
	def test_is_minor_player(self):
		self.assert_(is_minor(gc.getPlayer(iIndependent)))
		
	def test_not_is_minor(self):
		self.assert_(not is_minor(0))
		

class TestEstimateDirection(TestCase):

	def test_estimate_directions(self):
		plot_directions = {
			(0, 1): DirectionTypes.DIRECTION_WEST,
			(1, 0): DirectionTypes.DIRECTION_SOUTH,
			(2, 1): DirectionTypes.DIRECTION_EAST,
			(1, 2): DirectionTypes.DIRECTION_NORTH,
		}
		
		for (x, y), direction in plot_directions.items():
			self.assertEqual(estimate_direction((1, 1), (x, y)), direction)
			
	def test_estimate_direction_plots(self):
		fromPlot = gc.getMap().plot(1, 1)
		toPlot = gc.getMap().plot(1, 0)
		self.assertEqual(estimate_direction(fromPlot, toPlot), DirectionTypes.DIRECTION_SOUTH)
		
	def test_estimate_direction_same(self):
		self.assertEqual(estimate_direction((0, 0), (0, 0)), DirectionTypes.NO_DIRECTION)


class TestYear(TestCase):

	def test_year(self):
		test_year = year(-3000)
		assertType(self, test_year, Turn)
		self.assertEqual(test_year, 0)
		
	def test_current_year(self):
		test_year = year()
		assertType(self, test_year, Turn)
		self.assertEqual(test_year, 0)
		

class TestMakeUnit(TestCase):

	def test_missionary(self):
		self.assertEqual(missionary(iJudaism), iJewishMissionary)
		
	def test_missionary_invalid(self):
		self.assertEqual(missionary(-1), None)
		
	def test_make_unit(self):
		unit = makeUnit(0, 4, (0, 0))
		assertType(self, unit, CyUnit)
		self.assertEqual(unit.getOwner(), 0)
		self.assertEqual(unit.getUnitType(), 4)
		self.assertEqual((unit.getX(), unit.getY()), (0, 0))
	
	def test_make_unit_plot(self):
		unit = makeUnit(0, 4, gc.getMap().plot(0, 0))
		assertType(self, unit, CyUnit)
		self.assertEqual(unit.getOwner(), 0)
		self.assertEqual(unit.getUnitType(), 4)
		self.assertEqual((unit.getX(), unit.getY()), (0, 0))
		
	def test_make_unit_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		unit = makeUnit(0, 4, city)
		assertType(self, unit, CyUnit)
		self.assertEqual(unit.getOwner(), 0)
		self.assertEqual(unit.getUnitType(), 4)
		self.assertEqual((unit.getX(), unit.getY()), (0, 0))
		
		city.kill()
		
	def test_make_units(self):
		units = makeUnits(0, 4, (0, 0), 3)
		assertType(self, units, CreatedUnits)
		self.assertEqual(len(units), 3)
		for unit in units:
			self.assertEqual(unit.getOwner(), 0)
			self.assertEqual(unit.getUnitType(), 4)
			self.assertEqual((unit.getX(), unit.getY()), (0, 0))
			
			
class TestText(TestCase):

	def test_text(self):
		self.assertEqual(text("TXT_KEY_CIV_EGYPT_ADJECTIVE"), "Egyptian")
		
	def test_text_format(self):
		self.assertEqual(text("TXT_KEY_INTERFACE_CITY_CORE_POPULATION", 5), "Core Population: 5")
	
	def test_text_undefined(self):
		self.assertEqual(text("ABCDEF"), "ABCDEF")
		
	def test_text_if_exists(self):
		self.assertEqual(text_if_exists("TXT_KEY_CIV_EGYPT_ADJECTIVE"), "Egyptian")
		
	def test_text_if_exists_undefined(self):
		self.assertEqual(text_if_exists("ABDCDEF"), "")
		
	def test_text_if_exists_otherwise(self):
		self.assertEqual(text_if_exists("TXT_KEY_CIV_EGYPT_ADJECTIVE", otherwise="TXT_KEY_CIV_ENGLAND_ADJECTIVE"), "Egyptian")
		
	def test_text_if_exists_undefined_otherwise(self):
		self.assertEqual(text_if_exists("ABCDEF", otherwise="TXT_KEY_CIV_ENGLAND_ADJECTIVE"), "English")
		
	def test_text_if_exists_otherwise_format(self):
		self.assertEqual(text_if_exists("TXT_KEY_INTERFACE_CITY_CORE_POPULATION", 5, otherwise="TXT_KEY_CIV_ENGLAND_ADJECTIVE"), "Core Population: 5")
		
	def test_text_if_exists_undefined_otherwise_format(self):
		self.assertEqual(text_if_exists("ABDCDEF", 5, otherwise="TXT_KEY_INTERFACE_CITY_CORE_POPULATION"), "Core Population: 5")
		

class TestDistance(TestCase):

	def test_distance(self):
		self.assertEqual(distance((0, 0), (0, 2)), 2)
		
	def test_distance_plots(self):
		self.assertEqual(distance(gc.getMap().plot(0, 0), gc.getMap().plot(0, 2)), 2)
		
	def test_distance_cities(self):
		city1 = gc.getPlayer(0).initCity(0, 0)
		city2 = gc.getPlayer(0).initCity(0, 2)
		self.assertEqual(distance(city1, city2), 2)
		

class TestFind(TestCase):

	def setUp(self):
		self.numbers = [0, 4, 5, -1, 12, 3]

	def test_find_min(self):
		found = find_min(self.numbers)
		assertType(self, found, FindResult)
		self.assertEqual(found.result, -1)
		self.assertEqual(found.index, 3)
		self.assertEqual(found.value, -1)
		
	def test_find_max(self):
		found = find_max(self.numbers)
		assertType(self, found, FindResult)
		self.assertEqual(found.result, 12)
		self.assertEqual(found.index, 4)
		self.assertEqual(found.value, 12)
		
	def test_find_max_custom(self):
		found = find_max(self.numbers, lambda x: x % 3)
		assertType(self, found, FindResult)
		self.assertEqual(found.result, 5)
		self.assertEqual(found.index, 2)
		self.assertEqual(found.value, 2)
		
		
class TestRandom(TestCase):

	def run_random(self, random, min, max):
		bFoundMin = False
		bOutside = False
		for _ in range(10000):
			iRand = random()
			if iRand == min: bFoundMin = True
			if not min <= iRand < max: bOutside = True
		self.assert_(bFoundMin)
		self.assert_(not bOutside)
		
	def test_random(self):
		self.run_random(lambda: rand(10), 0, 10)
		
	def test_random_min(self):
		self.run_random(lambda: rand(10, 20), 10, 20)
		
	def test_random_entry(self):
		list = [0, 1, 2, 3, 4]
		self.assert_(random_entry(list) in list)
		
	def test_random_entry_empty(self):
		self.assertEqual(random_entry([]), None)
		

class TestNames(TestCase):

	def test_name(self):
		self.assertEqual(name(0), "Egypt")
		
	def test_name_player(self):
		self.assertEqual(name(gc.getPlayer(0)), "Egypt")
		
	def test_adjective(self):
		self.assertEqual(adjective(0), "Egyptian")
		
	def test_adjective_player(self):
		self.assertEqual(adjective(gc.getPlayer(0)), "Egyptian")
		
	def test_full_name(self):
		self.assertEqual(fullname(iEngland), "Anglo-Saxon Peoples")
		
	def test_full_name_player(self):
		self.assertEqual(fullname(pEngland), "Anglo-Saxon Peoples")
		
		
class TestWrap(TestCase):

	def test_wrap_x(self):
		self.assertEqual(wrap(124, 0), (0, 0))
		
	def test_wrap_x_negative(self):
		self.assertEqual(wrap(-1, 0), (123, 0))
		
	def test_wrap_y(self):
		self.assertEqual(wrap(0, 68), (0, 67))
		
	def test_wrap_y_negative(self):
		self.assertEqual(wrap(0, -1), (0, 0))
		
	def test_wrap_noop(self):
		self.assertEqual(wrap(0, 0), (0, 0))
		
	def test_wrap_plots(self):
		self.assertEqual(wrap(gc.getMap().plot(0, 0)), (0, 0))
		
	def test_wrap_invalid_plot(self):
		self.assertEqual(wrap(gc.getMap().plot(124, 68)), None)
		
		
class TestLocation(TestCase):

	def base_test(self, expected_class, expected_value, func, *args):
		obj = func(*args)
		assertType(self, obj, expected_class)
		self.assertEqual((obj.getX(), obj.getY()), expected_value)


class TestPlot(TestLocation):

	def test_coords(self):
		self.base_test(CyPlot, (0, 0), plot, 0, 0)
		
	def test_tile(self):
		self.base_test(CyPlot, (0, 0), plot, (0, 0))
		
	def test_plot(self):
		self.base_test(CyPlot, (0, 0), plot, gc.getMap().plot(0, 0))
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		self.base_test(CyPlot, (0, 0), plot, city)
		city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		self.base_test(CyPlot, (0, 0), plot, unit)
		unit.kill(False, 0)
		
	def test_invalid(self):
		self.assertRaises(TypeError, plot, 0, 0, 0)
		

class TestCity(TestLocation):

	def setUp(self):
		self.city = gc.getPlayer(0).initCity(0, 0)
		
	def tearDown(self):
		self.city.kill()
		
	def test_coords(self):
		self.base_test(CyCity, (0, 0), city, 0, 0)
		
	def test_tile(self):
		self.base_test(CyCity, (0, 0), city, (0, 0))
		
	def test_plot(self):
		self.base_test(CyCity, (0, 0), city, gc.getMap().plot(0, 0))
	
	def test_city(self):
		self.base_test(CyCity, (0, 0), city, self.city)
		
	def test_invalid(self):
		self.assertRaises(TypeError, city, 0, 0, 0)
		
	def test_no_city(self):
		self.assertEqual(city(0, 1), None)
		
	
class TestUnit(TestCase):
		
	def setUp(self):
		self.unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
	def tearDown(self):
		if self.unit.getX() >= 0:
			self.unit.kill(False, 0)
			
	def test_create_unit_key(self):
		key = unit_key(self.unit)
		self.assertEqual(key.owner, self.unit.getOwner())
		self.assertEqual(key.id, self.unit.getID())
		
	def test_unit(self):
		u = unit(unit_key(self.unit))
		self.assertEqual(u.getOwner(), self.unit.getOwner())
		self.assertEqual(u.getID(), self.unit.getID())
		
	def test_unit_invalid(self):
		self.assertRaises(TypeError, unit, self.unit)
		
		
class TestLocationFunction(TestCase):

	def test_plot(self):
		self.assertEqual(location(gc.getMap().plot(0, 0)), (0, 0))
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		self.assertEqual(location(city), (0, 0))
		city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		self.assertEqual(location(unit), (0, 0))
		unit.kill(False, 0)
		
		
class TestTeam(TestCase):

	def test_current(self):
		self.assertEqual(team().getID(), 0)

	def test_team(self):
		t = gc.getTeam(0)
		self.assertEqual(team(t).getID(), t.getID())
		
	def test_player(self):
		p = gc.getPlayer(0)
		self.assertEqual(team(p).getID(), p.getTeam())
		
	def test_id(self):
		self.assertEqual(team(0).getID(), gc.getTeam(0).getID())
		
	def test_plot(self):
		plot = gc.getMap().plot(0, 0)
		plot.setOwner(0)
		
		self.assertEqual(team(plot).getID(), plot.getTeam())
		
		plot.setOwner(-1)
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		
		self.assertEqual(team(city).getID(), city.getTeam())
		
		city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		self.assertEqual(team(unit).getID(), unit.getTeam())
		
		unit.kill(False, 0)
		
	def test_invalid(self):
		self.assertRaises(TypeError, team, gc.getCivilizationInfo(0))
		
	def test_teamtype(self):
		self.assertEqual(teamtype(0).getID(), gc.getTeam(0).getID())
		

class TestPlayer(TestCase):

	def test_current(self):
		self.assertEqual(player().getID(), 0)

	def test_player(self):
		p = gc.getPlayer(0)
		self.assertEqual(player(p).getID(), p.getID())
		
	def test_team(self):
		t = gc.getTeam(0)
		self.assertEqual(player(t).getID(), t.getLeaderID())
		
	def test_id(self):
		self.assertEqual(player(0).getID(), gc.getPlayer(0).getID())
		
	def test_negative_id(self):
		self.assertEqual(player(-1), None)
		
	def test_plot(self):
		plot = gc.getMap().plot(0, 0)
		plot.setOwner(0)
		self.assertEqual(player(plot).getID(), plot.getOwner())
		plot.setOwner(-1)
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		
		self.assertEqual(city.getOwner(), 0)
		self.assertEqual(player(city).getID(), city.getOwner())
		
		city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		self.assertEqual(player(unit).getID(), unit.getOwner())
		
		unit.kill(False, 0)
		
	def test_invalid(self):
		self.assertRaises(TypeError, player, gc.getCivilizationInfo(0))
		
		
class TestCiv(TestCase):
	
	def test_id(self):
		self.assertEqual(civ(0), iCivEgypt)
		
	def test_player(self):
		self.assertEqual(civ(gc.getPlayer(0)), iCivEgypt)
		
	def test_team(self):
		self.assertEqual(civ(gc.getTeam(gc.getPlayer(0).getTeam())), iCivEgypt)
		
		
class TestHuman(TestCase):

	def test_human(self):
		self.assertEqual(human(), gc.getGame().getActivePlayer())


class TestIterableHelpers(TestCase):

	def setUp(self):
		self.iterable = [1, 2, 3, 4, 5]
		
	def test_any_with_one(self):
		self.assert_(any([x >= 5 for x in self.iterable]))
		
	def test_any_with_all(self):
		self.assert_(any([x >= 1 for x in self.iterable]))
		
	def test_any_with_none(self):
		self.assert_(not any([x < 0 for x in self.iterable]))
		
	def test_all_with_one(self):
		self.assert_(not all([x >= 5 for x in self.iterable]))
		
	def test_all_with_all(self):
		self.assert_(all([x >= 1 for x in self.iterable]))
		
	def test_all_with_none(self):
		self.assert_(not all([x < 0 for x in self.iterable]))
		
	def test_next_once(self):
		first = next(self.iterable)
		self.assertEqual(first, 1)
		
	def test_next_twice(self):
		iterator = iter(self.iterable)
		first = next(iterator)
		second = next(iterator)
		self.assertEqual(first, 1)
		self.assertEqual(second, 2)
		
	def test_next_default(self):
		first = next([], -1)
		self.assertEqual(first, -1)
		
		
class TestClosestCity(TestCase):

	def test_closest_city(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		closest_city = gc.getPlayer(0).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(original_city)
		
		self.assertEqual((closest.getX(), closest.getY()), (closest_city.getX(), closest_city.getY()))
		
		original_city.kill()
		closest_city.kill()
		farther_city.kill()
	
	def test_closest_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 63, 10, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		closest_city = gc.getPlayer(0).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(unit)
		
		self.assertEqual((closest.getX(), closest.getY()), (closest_city.getX(), closest_city.getY()))
		
		unit.kill(False, -1)
		closest_city.kill()
		farther_city.kill()
	
	def test_closest_owner(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		closest_city = gc.getPlayer(1).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(original_city, 0)
		
		self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		
		original_city.kill()
		closest_city.kill()
		farther_city.kill()
	
	def test_closest_continents(self):
		original_city = gc.getPlayer(0).initCity(49, 35)
		closest_city = gc.getPlayer(0).initCity(47, 36)
		farther_city = gc.getPlayer(0).initCity(57, 27)
		
		closest = closestCity(original_city, same_continent=True)
		
		self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		
		original_city.kill()
		closest_city.kill()
		farther_city.kill()
	
	def test_coastal(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		closest_city = gc.getPlayer(0).initCity(65, 11)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(original_city, coastal_only=True)
		
		self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		
		original_city.kill()
		closest_city.kill()
		farther_city.kill()
	
	def test_no_result(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		
		closest = closestCity(original_city, owner=1)
		
		self.assert_(closest is None)
		
		original_city.kill()
	
	def test_skip_city(self):
		unit = gc.getPlayer(0).initUnit(4, 63, 10, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		closest_city = gc.getPlayer(0).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(unit, skip_city=closest_city)
		
		self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		
		unit.kill(False, -1)
		closest_city.kill()
		farther_city.kill()


class TestSpecialbuilding(TestCase):

	def test_temple(self):
		building = temple(iJudaism)
		
		self.assertEqual(building, iJewishTemple)
		
	def test_monastery(self):
		building = monastery(iIslam)
		
		self.assertEqual(building, iIslamicMonastery)
		
	def test_cathedral(self):
		building = cathedral(iBuddhism)
		
		self.assertEqual(building, iBuddhistCathedral)


class TestMap(TestCase):

	def setUp(self):
		self.tiles = [[1, 2, 3],
					  [4, 5, 6],
					  [7, 8, 9]]
		self.map = Map(self.tiles)
	
	def test_init_no_list(self):
		self.assertRaises(ValueError, Map, 1)
	
	def test_init_not_empty(self):
		self.assertRaises(ValueError, Map, [])
	
	def test_init_different_widths(self):
		self.assertRaises(ValueError, Map, [[1], [2, 3]])
	
	def test_getitem(self):
		self.assertEqual(self.map[0, 0], 7)
		self.assertEqual(self.map[1, 0], 8)
		self.assertEqual(self.map[2, 0], 9)
		self.assertEqual(self.map[0, 1], 4)
		self.assertEqual(self.map[1, 1], 5)
		self.assertEqual(self.map[2, 1], 6)
		self.assertEqual(self.map[0, 2], 1)
		self.assertEqual(self.map[1, 2], 2)
		self.assertEqual(self.map[2, 2], 3)
		
	def test_setitem(self):
		self.map[1, 1] = 0
		self.assertEqual(self.map[1, 1], 0)
		
	def test_iter(self):
		expected_items = [((0, 0), 7), ((1, 0), 8), ((2, 0), 9), ((0, 1), 4), ((1, 1), 5), ((2, 1), 6), ((0, 2), 1), ((1, 2), 2), ((2, 2), 3)]
		actual_items = [item for item in self.map]
		
		self.assertEqual(set(actual_items), set(expected_items))
	
	def test_apply(self):
		otherMap = Map([[0, 0], [0, 0]])
		
		self.map.apply(otherMap)
		
		self.assertEqual(self.map[0, 0], 0)
		self.assertEqual(self.map[0, 1], 0)
		self.assertEqual(self.map[2, 2], 3)
		
	def test_apply_offset(self):
		otherMap = Map([[0, 0], [0, 0]])
		
		self.map.apply(otherMap, (1, 1))
		
		self.assertEqual(self.map[0, 0], 7)
		self.assertEqual(self.map[1, 1], 0)
		self.assertEqual(self.map[2, 2], 0)


class TestDeepList(TestCase):

	def test_list(self):
		result = deeplist([1, 2, 3])
		self.assertEqual(result, [1, 2, 3])
		
	def test_tuple(self):
		result = deeplist((1, 2, 3))
		self.assertEqual(result, [1, 2, 3])
		
	def test_deep_tuple(self):
		result = deeplist(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
		self.assertEqual(result, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])


test_cases = [
	TestTurn, 
	TestInfos, 
	TestDefaultDict, 
	TestCreatedUnits, 
	TestPlayers, 
	TestPlayerFactory,
	TestUnits,
	TestUnitFactory,
	TestPlots,
	TestPlotFactory,
	TestCities,
	TestCityFactory,
	TestMove,
	TestHasCivic,
	TestScenarioUtils,
	TestUniqueUnitsAndBuildings,
	TestMasterAndVassal,
	TestMinor,
	TestEstimateDirection,
	TestYear,
	TestMakeUnit,
	TestText,
	TestFind,
	TestRandom,
	TestNames,
	TestWrap,
	TestPlot,
	TestCity,
	TestUnit,
	TestLocationFunction,
	TestTeam,
	TestPlayer,
	TestCiv,
	TestHuman,
	TestIterableHelpers,
	TestClosestCity,
	TestMap,
]
		
suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)