from globalSettings import globalSettings
import os
os.environ['ARK_MODE'] = 'test'

globalst = globalSettings()


print(globalst.get('NETWORK_TOOLSETS'))
print(globalst.get('USERROOT'))
print(globalst.get('SHEEPSTATUS'))
print(globalst.get('ADDITIONAL_TOOLS'))