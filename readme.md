# settingsManager
A class that eases the getting and setting of settings through json config files.

## Basic usage

SettingsManager has two main classes currently:
 - SettingsManager
 - globalSettings

globalSettings is meant for GLOBAL configurations. Once you initialize it, you should be able to get the global settings through dot notation. EG:
```
   import settingsManager
   globalSettings = settingsManager.globalSettings()

   ark_root = globalSettings.ARK_ROOT
```
settingsManager.SettingsManager works exactly the same, but is intended to give you application-specific, and if needs be, user-specific settings.
```
import settingsManager
nukeSettings = settingsManager.SettingsManager('Nuke')
last_project = settingsManager.LAST_PROJECT

randoNukeSettings = settingsManager.SettingsManager('Nuke', 'Rando')
RandosLast_Project = settingsManager.LAST_PROJECT
```
(Here, Rando may have a different setting for last project.)

## Config files

The config files are usual json files(which allow commenting by double slashes).
By default, the settingsManagers will search for this file in the path given by the environment
variable 'USER_CONFIG', or, failing to find such a variable, c:/ie/config.

globalSettings will by default load in the file 'default.json' that is stored in this location. It will then load in any additional settings (or update already existing settings) as determined by the mode specified by the environment variable 'mode'. If there is no mode, or if mode is listed as 'default', you're pretty much stuck with the default settings. However, if mode is, for example, 'test', globalSettings will load in 'test.json' (again, in the default config path) and fill in those settings.

settingsManager works similarly. If USER_CONFIG is set to 'c:/ie/config', and we invoke SettingsManager('Nuke'), the settings in the file 'c:/ie/config/Nuke.json' will be loaded by the settingsManager. SettingsManager also allows user specifications; if I initialize SettingsManager('Nuke', 'Rando'), it will first load in 'c:/ie/config/Nuke.json' and then overwrite and augment settings with the settings in 'c:/ie/config/Nuke.Rando.json'.


Config files can support strings that are shaped like 'somePath/{OTHER_CONFIG}/otherPart'. The settingsManager will fill in the '{OTHER_CONFIG}' bracketed part with OTHER_CONFIG, the setting.


## Setting user settings

Given a settingsManager (not globalSettings), a call to set(key, value) will write this setting to the settings file. These settings are deliberate in only writing newer, user-specific settings so should probably not be called if you're simply on the default settings level.

## Setup scripts
globalSettings inherits from SettingsManager and implements a setup script. This setup method defines a whole set of computer-specific settings that are machine-dependent. If a specific application requires highly specific settings, which cannot be gleaned just from literal strings or string substitutions, it's possible to just inherit a new SettingsManager from settingsManager and implement the setup method.

