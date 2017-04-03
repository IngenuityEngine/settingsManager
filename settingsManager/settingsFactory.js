var globalSettings = require('./globalSettings')
var settingsManager = require('./settingsManager')

var settingsManager = module.exports = {

init: function(context, callback)
{
	settingsManager.database = context.database
	context.settingsManager = settingsManager
	callback()
},

globalSettings: function(paths, modes)
{
	return new globalSettings(paths, modes)
},

settingsManager: function(token, user)
{
	return new settingsManager(settingsManager.database, token, user)
}

//end of module
}
