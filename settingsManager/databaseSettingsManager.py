import json
import arkInit
arkInit.init()
import arkUtil
# import cOS

from SettingsManager import SettingsManager


class DatabaseSettingsManager(SettingsManager):

	def __init__(self, database, appName, user=None):
		self.database = database
		self.user = user
		self.appName = appName
		self.settings = {}
		self.customSettings = {}

		basicSettings = self.database\
			.find('settings')\
			.where('key', 'is', self.appName)\
			.where('user','notexists')\
			.execute()

		if basicSettings:
			for setting in basicSettings:
				convertedSettings = arkUtil.parseJSON(setting['settings'])
				self.updateSettings(convertedSettings)

		if self.user:
			extraSettings = self.database\
				.find('settings')\
				.where('key', 'is', self.appName)\
				.where('user', 'is', self.user)\
				.execute()
			if extraSettings:
				for setting in extraSettings:
					convertedSettings = arkUtil.parseJSON(setting['settings'])
					self.updateSettings(convertedSettings)

					# keep the user's settings around
					# the idea here is to only save the things the user
					# has changed, thus attempting to preserve
					# the defaults whenever possible
					self.customSettings = arkUtil\
						.mergeDict(self.customSettings, convertedSettings)

		for setting in self.settings:
			setattr(self, setting, self.get(setting))

	def save(self):
		allSettings = json.dumps(self.settings)
		query = self.database\
			.update('settings')\
			.where('key', 'is', self.appName)\
			.set('settings', allSettings)

		if self.user:
			query = query.where('user', 'is', self.user)
		else:
			query = query.where('user', 'notexists')

		result = query.execute()
		if result['modified'] == 0:
			data = {'key': self.appName, 'settings': allSettings}
			if self.user:
				data['user'] = self.user
			query = self.database\
						.create('settings', data)\
						.execute()
