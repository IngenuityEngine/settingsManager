var globalSettings = require('./globalSettings')
var settingsManager = require('./settingsManager')


module.exports = {

globalSettings: function(paths, modes)
{
	return new globalSettings(paths, modes)
},

settingsManager: function(database, token, user)
{
	return new settingsManager(database, token, user)
}

//end of module
}
