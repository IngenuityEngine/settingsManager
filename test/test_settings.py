
# Standard modules
from expects import *

# Our modules
import arkInit
arkInit.init()

import tryout
import settingsManager

class test(tryout.TestSuite):
	title = 'test/test_settings.py'

	def set_settings(self):
		settings = settingsManager.Settings(
			some='thing',
			x=12,
			options={'yea':False})

		self.assertEqual(settings.some, 'thing')
		self.assertEqual(settings.x, 12)
		self.assertEqual(settings.options['yea'], False)

if __name__ == '__main__':
	tryout.run(test)
