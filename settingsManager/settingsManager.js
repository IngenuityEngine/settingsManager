var _ = require('lodash')
var _s = require('underscore.string')
var async = require('async')
var Class = require('uberclass')
var arkUtil = require('arkutil')

module.exports = Class.extend({

init: function(database, settingsKeys, user, callback)
{
	_.bindAll(this)
	this._database = database
	this._user = user
	this._save = this.save
	this._settingsKey = settingsKeys

	// user is an optional parameter
	if (!callback)
	{
		callback = _.noop
		if (_.isFunction(user))
		{
			callback = user
			user = null
		}
	}
	settingsKeys = arkUtil.ensureArray(settingsKeys)
	var self = this

	function loadBasicSettings(cb)
	{
		self._database
			.find('settings')
			.where('key', 'in', settingsKeys)
			.where('user', 'notexists')
			.execute(function(err, resp)
			{
				if (err)
					return cb(err)
				_.each(resp, function(setting)
					{
						setting = JSON.parse(setting.settings)
						_.merge(self, setting)
					})
				cb()
			})
	}

	function loadUserSettings(cb)
	{
		if (!user)
			return cb()
		self._database
			.find('settings')
			.where('key', 'in', settingsKeys)
			.where('user', 'is', user)
			.execute(function(err, resp)
			{
				if (err)
					return cb(err)
				if (resp)
				{
					_.each(resp, function(setting)
					{
						setting = JSON.parse(setting.settings)
						_.merge(self, setting)
					})
				}
				return cb()
			})
	}

	function setSave(cb)
	{
		self.save = self._save
		cb()
	}

	async.series([
		loadBasicSettings,
		loadUserSettings,
		setSave],
		callback)
},

save: function(callback)
{
	var self = this
	var settingsToSave = {}
	_.forOwn(this, function(value, key)
	{
		if (!_s.startsWith(key, '_') && !_.isFunction(value))
			settingsToSave[key] = value
	})
	var query = this._database
		.update('settings')
		.where('key', 'is', this._settingsKey)
		.set('settings', JSON.stringify(settingsToSave))

	if (self._user)
		query = query.where('user', 'is', self._user)
	query.execute(callback)

}

// end of module
})
