import jsonParser as json
import sendToWeb as web
import fileTimeStamp as fts
import liveParameter as param

# initialisation des parametres
parameter = param.ParameterClass()

dateFile = open('dayfile.day','r')
today = '02-17'

NbofDays = 7
TimePrecision = 10 
print('-I- Calcul de la moyenne hebdomadaire')
fts.NdaysDataMean(NbofDays,today+'_meteo.bet',TimePrecision)
avgFileNameBet = 'dossierMeteo//{}DaysAvg_meteo.abet'.format(NbofDays)
avgFileNameJson= '{}DaysAvg_meteo.json'.format(NbofDays)
print('-I- Conversion en json')
json.parseData(avgFileNameBet,avgFileNameJson,parameter)		
print('-I- Envoi sur raspi.sarno')
web.sendToWeb(avgFileNameJson)
print('-I- Fini')