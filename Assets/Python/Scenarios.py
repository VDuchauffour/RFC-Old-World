from Core import *

from Scenario500AD import scenario500AD


SCENARIOS = {
	i500AD: scenario500AD,
}


def getScenario(iScenario=None):
	if iScenario is None:
		iScenario = scenario()
	
	return SCENARIOS[iScenario]
