import os

import arkInit
arkInit.init()
import cOS
import tryout
# import time

import settingsManager

class test(tryout.TestSuite):

	title = 'test/test_globalSettings.py'

	def setUpClass(self):
		sourcePath = cOS.getDirName(os.path.realpath(__file__)) + 'testSettings'
		self.configPath = cOS.getDirName(os.path.realpath(__file__)) + 'config'
		cOS.copyTree(sourcePath, self.configPath)

	def setUp(self):
		self.ogConfig = os.environ.get('ARK_CONFIG')
		self.ogMode = os.environ.get('mode')
		configPath = cOS.getDirName(os.path.realpath(__file__)) + 'config'
		os.environ['ARK_CONFIG'] = configPath
		os.environ['mode'] = 'default'

	def tearDown(self):
		if self.ogConfig:
			os.environ['ARK_CONFIG'] = self.ogConfig
		if self.ogMode:
			os.environ['mode'] = self.ogMode

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
		os.environ['mode'] = 'sweetApp'
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
			'http://127.0.0.1/api')

	def actual_settings(self):
		os.environ['ARK_CONFIG'] = self.ogConfig
		os.environ['mode'] = 'default'
		settings = settingsManager.globalSettings()

		self.assertTrue(
			settings.DATABASE is not False)
		self.assertTrue(
			'http' in settings.DATABASE)
		self.assertTrue(
			settings.ARK_ROOT is not False)
		self.assertTrue(
			settings.COMPUTER_TYPE is not False)
		self.assertTrue(
			settings.SHARED_ROOT is not False)
		self.assertTrue(
			settings.USER_ROOT is not False)
		self.assertTrue(
			settings.OS_USERNAME is not False)
		self.assertTrue(
			settings.TEMP is not False)
		self.assertTrue(
			settings.ARK_CONFIG is not None)
		self.assertTrue(
			settings.ARK_PYTHON is not None)
		self.assertTrue(
			settings.ARK_PYTHONLIB is not None)

	# Should get 'normal' program vars
	def program_vars(self):
		os.environ['ARK_CONFIG'] = self.ogConfig
		os.environ['mode'] = 'default'
		settings = settingsManager.globalSettings()

		self.assertTrue(
			settings.THIRDPARTY is not None)
		self.assertTrue(
			settings.VRAY_EXE is not None)
		self.assertTrue(
			settings.MAX_ROOT is not None)

	def shouldResolveWindowsProgramVars(self):
		os.environ['ARK_CONFIG'] = self.ogConfig
		os.environ['mode'] = 'default'
		settings = settingsManager.globalSettings()

		if cOS.isWindows():
			self.assertTrue(
				settings.THIRDPARTY is not None)
			self.assertTrue(
				settings.VRAY_EXE is not None)
			self.assertTrue(
				settings.MAX_ROOT is not None)
			self.assertTrue(
				settings.MAYA_ROOT is not False)
			self.assertEqual(
				settings.MAYA_ROOT, settings.MAYA_ROOT_WIN)
			self.assertNotEqual(
				settings.MAYA_ROOT, settings.MAYA_ROOT_LINUX)
			self.assertTrue(
				settings.MODO_ROOT is not False)
			self.assertEqual(
				settings.MODO_ROOT, settings.MODO_ROOT_WIN)
			self.assertNotEqual(
				settings.MODO_ROOT, settings.MODO_ROOT_LINUX)

			self.assertEqual(
				settings.VRAY_EXE, 'C:/Program Files/Autodesk/Maya2016/vray/bin/vray.exe')

		if cOS.isLinux():
			self.assertTrue(
				settings.THIRDPARTY is not None)
			self.assertTrue(
				settings.VRAY_EXE is not None)
			self.assertTrue(
				settings.MAX_ROOT is not None)
			self.assertTrue(
				settings.MAYA_ROOT is not False)
			self.assertEqual(
				settings.MAYA_ROOT, settings.MAYA_ROOT_LINUX)
			self.assertNotEqual(
				settings.MAYA_ROOT, settings.MAYA_ROOT_LINUX)
			self.assertTrue(
				settings.MODO_ROOT is not False)
			self.assertEqual(
				settings.MODO_ROOT, settings.MODO_ROOT_LINUX)
			self.assertNotEqual(
				settings.MODO_ROOT, settings.MODO_ROOT_LINUX)

			self.assertEqual(
				settings.VRAY_EXE, '/usr/local/Autodesk/Maya2016/vray/bin/vray.exe')

if __name__ == '__main__':
	tryout.run(test)
