import sys
import json

sys.path.append('c:/dev/coren/python')

sys.path.append('c:ie/ark/tools/settingsManager')

from coren import Coren
from settingsManager import SettingsManager

currentUser = 'Grant Miller'

coren = Coren('http://localhost:2020/api/')
settingsManager = SettingsManager('database', coren)

print('getting ehre')

appSettings = settingsManager.create('PublishManager', currentUser)

appSettings.set('fields', ['one', 'two', 'three'])

appSettings.save()

otherSettings = SettingsManager('database', coren)
otherSettings.create('MultiPublish', currentUser)
otherSettings.set(appSettings.get())
otherSettings.save()