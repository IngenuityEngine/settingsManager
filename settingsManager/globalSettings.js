// Vendor Modules
/////////////////////////
var _ = require('lodash')
var Class = require('uberclass')
var args = require('optimist').argv

// Our Modules
///////////////////////
var arkUtil = require('arkutil')

module.exports = Class.extend({

init: function(searchPaths, modes)
{
	_.bindAll(this, _.functionsIn(this))
	searchPaths = arkUtil.ensureArray(searchPaths)
	modes = arkUtil.ensureArray(modes)
	this.settings = {}

	var self = this

	_.each(modes, function(mode)
	{
		_.each(searchPaths, function(searchpath)
		{
			try
			{
				var settings = require(searchpath + '/' + mode)
				_.merge(self, settings)
				_.merge(self.settings, settings)
			}
			catch (err)
			{
				// The filepath does not exist, no problem
			}
		})
	})

	// this bit of magic allows for 'basics.port': 2000
	// to become basics: {port: 2000}
	var parsedEnvArgs = {}
	_.each(process.env, function(val, key)
	{
		_.merge(parsedEnvArgs, _.zipObjectDeep([key], [val]))
	})

	delete args._
	delete args.$0

	// finally merge the args and process.env in overtop of everything
	_.merge(self, parsedEnvArgs)
	_.merge(self, args)
	_.merge(self.settings, parsedEnvArgs)
	_.merge(self.settings, args)
}

// end of module
})

// if (!module.parent)
// {
// 	process.env = {'basics.port': 2000, 'some.big.dumb.param': 12}
// 	var gs = new globalSettings()
// 	console.log(gs.settings)
// 	console.log(gs.basics.port)
// 	console.log(gs.some.big.dumb.param)
// }
