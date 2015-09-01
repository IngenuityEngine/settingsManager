import json
# import arkInit
# arkInit.init()
# import cOS

from SettingsManager import SettingsManager


class DatabaseSettingsManager(SettingsManager):

	def __init__(self, database, token, user=None):
		self._database = database
		self._user = user
		self._token = token
		self.settings = {}

		basicSettings = self._database\
					.find('settings')\
					.where('key', 'is', token)\
					.where('user','notexists')\
					.execute()

		if basicSettings:
			for setting in basicSettings:
				convertedSettings = json.loads(setting['settings'])
				self.settings.update(convertedSettings)

		if (self._user):
			extraSettings = self._database\
								.find('settings')\
								.where('key', 'is', self._token)\
								.where('user', 'is', self._user)\
								.execute()
			if extraSettings:
				for setting in extraSettings:
					convertedSettings = json.loads(setting['settings'])
					self.settings.update(convertedSettings)

		for setting in self.settings:
			setattr(self, setting, self.get(setting))

		self.set = self._set
		self.save = self._save

	def _set(self, key, value=None):
		if value == None:
			self.settings.update(key)
			for setting in key:
				setattr(self, key, self._get(key))
		else:
			self.settings[key] = value
			setattr(self, key, self.get(key))

	def _save(self):
		allSettings = json.dumps(self.settings)
		query = self._database\
			.update('settings')\
			.where('key', 'is', self._token)\
			.set('settings', allSettings)
		if self._user:
			query = query.where('user', 'is', self._user)
		else:
			query = query.where('user', 'notexists')

		result = query.execute()
		if result['modified'] == 0:
			data = {'key': self._token, 'settings': allSettings}
			if self._user:
				data['user'] = self._user
			query = self._database\
						.create('settings', data)\
						.execute()
