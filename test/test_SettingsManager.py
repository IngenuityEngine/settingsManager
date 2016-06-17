# Standard modules
import os

# Ark modules
import arkInit
arkInit.init()
from settingsManager import SettingsManager
import tryout
import cOS

class test(tryout.TestSuite):
	title = 'test/test_SettingsManager.py'

	def setUp(self):
		self.ogConfig = os.environ.get('ARK_CONFIG')
		configPath = cOS.getDirName(__file__) + 'testSettings'
		os.environ['ARK_CONFIG'] = configPath

	def tearDown(self):
		os.environ['ARK_CONFIG'] = self.ogConfig

	def shouldRetrieveLiteralString(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.firstTest, 'testOne')

	def shouldRetrieveLiteralList(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.listTest,
			[
				'apples',
				'pears'
			])

	def shouldRetrieveLiteralDict(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.dictTest,
			{'other': 'test'})

	def shouldRetrieveSubstitutedString(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.subTest,
			'testOne/testTwo')

	def shouldAcceptDotAndGetNotation(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.firstTest,
			settings.get('firstTest'))

	def shouldBeAbleToOverrideSettings(self):
		settings = SettingsManager('testMode')
		self.assertEqual(
			settings.firstTest,
			'testModeOne')
		self.assertEqual(
			settings.listTest,
			'variable overwrite')
		self.assertEqual(
			settings.dictTest,
			{
				# fix: merge if we need it later
				# "other": "test",
				"more": "variables"
			})

	def handle_urls(self):
		settings = SettingsManager()
		self.assertEqual(
			settings.urlTest,
			'http://192.168.0.75/api')

	# def shouldBeAbleToOverrideSettingsWithUser(self):
	# 	settings = SettingsManager('testMode',
	# 		'testuser')
	# 	self.assertEqual(
	# 		settings.NETWORK_TOOLSETS,
	# 		'networktools')


if __name__ == '__main__':
	tryout.run(test)
