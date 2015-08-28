var _ = require('lodash')
var Class = require('uberclass')
var arkUtil = require('arkutil')

module.exports = Class.extend({

init: function(searchpaths, modes)
{
	_.bindAll(this)
	searchpaths = arkUtil.ensureArray(searchpaths)
	modes = arkUtil.ensureArray(modes)
	this.settings = {}

	var self = this

	_.each(modes, function(mode)
	{
		_.each(searchpaths, function(searchpath)
		{
			try
			{
				var settings = require(searchpath+'/'+ mode)
				_.merge(self, settings)
				_.merge(self.settings, settings)
			}
			catch (err)
			{
				//The filepath does not exist; no problem
			}
		})
	})
}
})