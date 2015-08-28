import json
import sys

sys.path.append('c:\dev\database\python')
from SettingsManager import SettingsManager


class DatabaseSettingsManager(SettingsManager):

	def __init__(self, database, token, user=None):
		self._database = database
		self._user = user
		self._token = token
		self._settings = {}

		basicSettings = self._database\
					.find('settings')\
					.where('key', 'is', token)\
					.where('user','notexists')\
					.execute()

		if basicSettings:
			for setting in basicSettings:
				self._settings.update(setting.settings)

		if (self._user):
			extraSettings = self._database\
								.find('settings')\
								.where('key', 'is', token)\
								.where('user', 'is', self._user)\
								.execute()
			if extraSettings:
				for setting in extraSettings:
					self._settings.update(setting.settings)

		for setting in self._settings:
			setattr(self, key, self._get(key))

		self.set = self._set

		self.save = self._save

	def _set(self, key, value=None):
		if value = None:
			self._settings.update(key)
			for setting in key:
				setattr(self, key, self._get(key))
		else:
			self._settings[key] = value
			setattr(self, key, self._get(value))

	def _save(self):
		allSettings = json.dumps(self._settings)
		query = self._database\
			.update('settings')\
			.where('key', 'is', token)\
			.set('settings', allSettings)
		if self._user:
			query = query.where('user', 'is', self._user)
		else:
			query = query.where('user', 'notexists')

		query.execute()







