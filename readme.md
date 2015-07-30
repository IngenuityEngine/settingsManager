# settingsManager
Save and load settings files

## How it works

Global settings
- arkConfig: path to settings
	- default: c:/ie/config
- arkMode: which settings to load
	- default: default
	- other: developer, test, node

SettingsManager
- name and optional user
- merges user overtop of name
- storage:
	- arkConfig environment variable
- filenames:
	config/someProgram.json
	config/someProgram.grantmiller.json

