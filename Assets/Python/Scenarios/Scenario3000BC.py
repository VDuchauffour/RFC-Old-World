from Scenario import *
from Core import *


lCivilizations = [
	Civilization(
		iEgypt,
		lCivics=[iMonarchy, iRedistribution, iDeification],
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
	Civilization(
		iBabylonia,
		techs=techs.of(iPottery, iPastoralism, iAgriculture)
	),
	Civilization(
		iHarappa,
		techs=techs.of(iMining, iPottery, iAgriculture)
	),
	Civilization(
		iCelts
	),
	Civilization(
		iNative,
		techs=techs.of(iTanning, iMythology)
	),
	Civilization(
		iIndependent
	),
	Civilization(
		iIndependent2
	),
]


scenario3000BC = Scenario(
	iStartYear = -3000,
	fileName = "RFC_3000BC",
	
	lCivilizations = lCivilizations,
)
