import os

import arkInit
arkInit.init()
import cOS
import tryout
import time

import settingsManager

class test(tryout.TestSuite):

	def setUp(self):
		self.ogConfig = os.environ.get('ARK_CONFIG')
		self.ogMode = os.environ.get('ARK_MODE')
		configPath = cOS.getDirName(__file__) + 'config'
		os.environ['ARK_CONFIG'] = configPath
		os.environ['ARK_MODE'] = 'default'

	def tearDown(self):
		if self.ogConfig:
			os.environ['ARK_CONFIG'] = self.ogConfig
		if self.ogMode:
			os.environ['ARK_MODE'] = self.ogMode


	def shouldRetrieveLiteralString(self):
		settings = settingsManager.globalSettings()
		self.assertEqual(
			settings.firstTest, 'testOne')

	def shouldRetrieveLiteralList(self):
		settings = settingsManager.globalSettings()
		self.assertEqual(
			settings.listTest,
			[
				'apples',
				'pears'
			])

	def shouldRetrieveLiteralDict(self):
		settings = settingsManager.globalSettings()
		self.assertEqual(
			settings.dictTest,
			{'other': 'test'})

	def shouldRetrieveSubstitutedString(self):
		settings = settingsManager.globalSettings()
		self.assertEqual(
			settings.subTest,
			'testOne/testTwo')

	def shouldAcceptDotAndGetNotation(self):
		settings = settingsManager.globalSettings()
		self.assertEqual(
			settings.firstTest,
			settings.get('firstTest'))

	def shouldBeAbleToOverrideSettings(self):
		os.environ['ARK_MODE'] = 'sweetApp'
		settings = settingsManager.globalSettings()

		self.assertEqual(
			settings.firstTest,
			'testModeOne')
		self.assertEqual(
			settings.listTest,
			'variable overwrite')
		self.assertEqual(
			settings.dictTest,
			{
				"other": "test",
				"more": "variables"
			})

	def handle_urls(self):
		settings = settingsManager.globalSettings()
		self.assertEqual(
			settings.urlTest,
			'http://192.168.0.75/api')

if __name__ == '__main__':
	# fix: tryout should have startTest and endTest methods
	sourcePath = cOS.getDirName(__file__) + 'testSettings'
	configPath = cOS.getDirName(__file__) + 'config'
	cOS.copyTree(sourcePath, configPath)

	error = None
	try:
		tryout.run(test)
	except Exception as err:
		error = err

	cOS.removeDir(configPath)
	if error:
		raise error



