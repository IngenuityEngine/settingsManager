from SettingsManager import SettingsManager
from globalSettings import globalSettings
from databaseSettingsManager import DatabaseSettingsManager
from Settings import Settings

def getSettings(appName='default', user=None):
	return SettingsManager(appName, user)
