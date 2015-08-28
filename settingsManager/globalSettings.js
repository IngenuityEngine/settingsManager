var _ = require('lodash')
var Class = require('uberclass')
var arkUtil = require('arkutil')
var fs = require('fs')

var globalSettings = module.exports = Class.extend({

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
				_.each(_.keys(settings), function(key)
				{
					if (!self[key])
					{
						self[key] = settings[key]
						self.settings[key] = settings[key]
					}
					else
						self[key] = _.merge(self[key], settings[key])
						self.settings[key] = _.merge(self.settings[key], settings[key])
				})
			}
			catch (err)
			{
				//The filepath does not exist; no problem
			}
		})
	})
}
})