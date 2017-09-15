from SettingsManager import SettingsManager
from globalSettings import globalSettings
from databaseSettingsManager import DatabaseSettingsManager
from Settings import Settings

def getSettings(appName='default', user=None):
	return SettingsManager(appName, user)

def databaseSettings(appName='default', user=None):
	from database import Database
	database = Database(keepTrying=True)
	return DatabaseSettingsManager(database, appName, user)
