# Standard modules
import os

# Ark modules
import arkInit
arkInit.init()
import settingsManager
import tryout
import cOS

class test(tryout.TestSuite):
	title = 'test/test_SettingsManager.py'

	def setUpClass(self):
		sourcePath = cOS.getDirName(os.path.realpath(__file__)) + 'testSettings'
		self.configPath = cOS.getDirName(os.path.realpath(__file__)) + 'config'
		cOS.copyTree(sourcePath, self.configPath)

	def setUp(self):
		self.ogConfig = os.environ.get('USER_CONFIG')
		self.ogMode = os.environ.get('mode')
		configPath = cOS.getDirName(os.path.realpath(__file__)) + 'config'
		os.environ['USER_CONFIG'] = configPath
		os.environ['mode'] = 'default'

	def tearDown(self):
		if self.ogConfig:
			os.environ['USER_CONFIG'] = self.ogConfig
		if self.ogMode:
			os.environ['mode'] = self.ogMode

	def retrieveLiteralString(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.get('firstTest'), 'testOne')

	def retrieveLiteralList(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.get('listTest'),
			[
				'apples',
				'pears'
			])

	def retrieveLiteralDict(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.get('dictTest'),
			{'other': 'test'})

	def retrieveSubstitutedString(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.get('subTest'),
			'testOne/testTwo')

	# def dotAndGetNotation(self):
	# 	settings = settingsManager.getSettings()
	# 	self.assertEqual(
	# 		settings.firstTest,
	# 		settings.get('firstTest'))

	def loadAppSettings(self):
		settings = settingsManager.getSettings('sweetApp')
		self.assertEqual(
			settings.get('firstTest'),
			'testModeOne')
		self.assertEqual(
			settings.get('listTest'),
			'variable overwrite')
		self.assertEqual(
			settings.get('dictTest'),
			{
				"more": "variables"
			})

	def handle_urls(self):
		settings = settingsManager.getSettings()
		self.assertEqual(
			settings.get('urlTest'),
			'http://127.0.0.1/api')

	def overrideSettingsWithUser(self):
		settings = settingsManager.getSettings('sweetApp',
			'blented')
		self.assertEqual(
			settings.get('firstTest'),
			'blented is awesome')
		self.assertEqual(
			settings.get('listTest'),
			'variable overwrite')
		self.assertEqual(
			settings.get('dictTest'),
			{
				"more": "variables",
				"such": "dict",
				"so": "overwrite"
			})

	def setASettingAndSaveForANewUser(self):
		settings = settingsManager.getSettings('sweetApp',
			'newUser')
		settings.set('autoRun', False).save()

		settings = settingsManager.getSettings('sweetApp',
			'newUser')
		self.assertEqual(settings.get('autoRun'), False)
		self.assertTrue(os.path.isfile(settings.filename))

	def setASettingAndSaveForExistingUser(self):
		settings = settingsManager.getSettings('sweetApp',
			'blented')
		settings.set('awesome', True).save()

		settings = settingsManager.getSettings('sweetApp',
			'blented')
		self.assertEqual(settings.get('awesome'), True)
		self.assertTrue(os.path.isfile(settings.filename))

	def make_new_settings_for_non_existant_app(self):
		settings = settingsManager.getSettings('whatever')
		settings.set('awesome', True).save()
		settings = settingsManager.getSettings('whatever')
		self.assertEqual(settings.get('awesome'), True)
		self.assertTrue(os.path.isfile(settings.filename))

if __name__ == '__main__':
	tryout.run(test)
