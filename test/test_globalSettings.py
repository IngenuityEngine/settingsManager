import os

import arkInit
arkInit.init()
import cOS
import tryout

import settingsManager

class test(tryout.TestSuite):

	def setUp(self):
		self.ogConfig = os.environ.get('ARK_CONFIG')
		self.ogMode = os.environ.get('ARK_MODE')
		configPath = cOS.getDirName(__file__) + 'testSettings'
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
		os.environ['ARK_MODE'] = 'testMode'
		settings = settingsManager.globalSettings()

		self.assertEqual(
			settings.firstTest,
			'testModeOne')
		self.assertEqual(
			settings.listTest,
			'variable overwrite')
		print 'settings.dictTest:', settings.dictTest
		print 'settings.listTest:', settings.listTest
		self.assertEqual(
			settings.dictTest,
			{
				# fix: merge if we need it later
				"other": "test",
				"more": "variables"
			})

	def handle_urls(self):
		settings = settingsManager.globalSettings()
		self.assertEqual(
			settings.urlTest,
			'http://192.168.0.75/api')


	# def test_shouldRetrieveLiteralString(self):
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(arkGlobals.TEMP, 'C:/ie/temp/')

	# def test_shouldRetrieveLiteralList(self):
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(
	# 		arkGlobals.ADDITIONAL_TOOLS, ['arkHelpers', 'shepherd', 'cOS', 'translators', 'weaver', 'settingsManager'])

	# def test_shouldRetrieveLiteralDict(self):
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(arkGlobals.JOB_LIST_TYPE, {'blacklist': 1, 'whitelist': 2})

	# def test_shouldRetrieveSubstitutedString(self):
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(arkGlobals.MANTRA_EXE, 'C:/Program Files/Side Effects Software/Houdini 13.0.547/bin/mantra.exe')

	# def test_shouldRetrieveProgrammaticKey(self):
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(arkGlobals.ARK_ROOT, os.environ.get('ARK_ROOT'))

	# def test_shouldAcceptDotAndGetNotation(self):
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(arkGlobals.ARK_ROOT, arkGlobals.get('ARK_ROOT'))
	# 	self.assertEqual(arkGlobals.get('ARK_ROOT'), os.environ.get('ARK_ROOT'))

	# def test_shouldBeAbleToOverrideSettings(self):
	# 	os.environ['ARK_MODE'] = 'overridetest'
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(arkGlobals.NETWORK_TOOLSETS, 'networktools')

	# def test_shouldBeAbleToOverrideSettings(self):
	# 	os.environ['ARK_MODE'] = 'overridetest'
	# 	arkGlobals = globalSettings()
	# 	self.assertEqual(arkGlobals.DUMMY_ATTR, 'dummy')

if __name__ == '__main__':
	tryout.run(test)


