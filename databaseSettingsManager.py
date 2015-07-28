import json
import sys

sys.path.append('c:\dev\coren\python')
from settingsInterface import SettingsInterface


class DatabaseSettingsManager(SettingsInterface):

	def __init__(self, coren):
		self.coren = coren
		self.user = ""
		self.key =""

	def create(self, key, user=None):
		if self.user or self.key:
			self.saveSettings()
		self.key = key
		self.user = user
		self.currentSettings = {}
		if self.user:
			print(self.coren.find('_user').execute())
			userId = self.coren.find('_user').where('name','is', self.user).execute().json()[0]['_id']
			createQuery = self.coren.create('settings', {'key': key, 'user': userId, 'settings': json.dumps({})})
		else:
			createQuery = self.coren.create('settings', {'key': key, 'settings': json.dumps({})})
		createQuery.execute()

		return self


	def load(self, key, user=""):
		#Key stores the key of what settings we are now looking at

		if self.user or self.key:
			self.saveSettings()
		#User if there is a particular user is a name
		self.key = key
		self.user = user
		#A local cache of what the settings are currently
		self.currentSettings = self.getSettingsForQuery()
		if user:
			self.currentSettings.update(self.getSettingsForQuery(user))

		return self

	def save(self, toSave):
		defaultSettings = self.getSettingsForQuery()
		changedSettings = {}
		for key in self.currentSettings:
			if key not in defaultSettings or (key in defaultSettings and \
					self.currentSettings[key] != defaultSettings):
				changedSettings[key] = self.currentSettings[key]

		query = self.coren.update('settings', {'settings': json.dumps(changedSettings)})\
					.where('key', 'is', self.key)
		if self.user:
			userId = self.coren.find('_user')\
								.where('name','is', self.user)\
								.execute()\
								.json()[0]['_id']
			query = query.where('user','is',userId)
		else:
			query = query.where('user', 'notexists')
		query.execute()


	def set(self, key, value=None):
		if value:
			self.currentSettings[key] = value
		else:
			self.currentSettings.update(key)


	def getSettingsForQuery(self, queryKey = ""):
		try:
			if queryKey:
				userId = self.coren.find('_user').where('name','is',queryKey).execute().json()[0]['_id']
				resp = self.coren.find('settings').where('key','is',self.key).where('user','is',userId).execute().json()
			else:
				resp = self.coren.find('settings').where('key', 'is', self.key).where('user', 'notexists').execute().json()

			responseSettings = json.loads(resp[0]['settings'])
			return responseSettings
		except:
			print ('Nothing was found for the query of %s with user potentially %s' % (self.key, queryKey))
			return {}

	def get(self, key=None):
		if key is None:
			return self.currentSettings
		try:
			return self.currentSettings[key]
		except:
			raise KeyError('This setting for ' + key + ' has not been defined yet!')

