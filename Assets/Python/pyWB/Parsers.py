from MapParser import *

PATH_TEMPLATE = "Mods/RFC Old World/PrivateMaps/%s.txt"


def parseBaseMap():
	mapName = "RFC_Old_World"
	parser = MapParser()
	parser.read(PATH_TEMPLATE % mapName)
	return parser

def parseScenarioMap(scenario):
	parser = parseBaseMap()
	parser.read(PATH_TEMPLATE % scenario.fileName)
	return parser