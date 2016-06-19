// Vendor Modules
/////////////////////////
var _ = require('lodash')
var Class = require('uberclass')

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
}
})
