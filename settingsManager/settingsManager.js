var _ = require('lodash')
var async = require('async')
var Class = require('uberclass')
var arkUtil = require('arkutil')

module.exports = Class.extend({

init: function(database, settingsKeys, user, callback)
{
	_.bindAll(this)
	this.database = database
	this.user = user
	this._save = this.save
	this._settingsList = []

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
		self.database
			.find('settings')
			.where('key', 'in', settingsKeys)
			.where('user', 'notexists')
			.execute(function(err, resp)
			{
				if (err)
					return cb(err)
				_.each(resp, function(setting)
					{
						self[setting.key] = JSON.parse(setting.settings)
						self._settingsList.push(setting.key)
					})
				cb()
			})
	}

	function loadUserSettings(cb)
	{
		if (!user)
			return cb()
		self.database
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
						if (!_.isUndefined(self[setting.key]))
							_.extend(self[setting.key], JSON.parse(setting.settings))
						else
							self[setting.key] = JSON.parse(setting.settings)
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
	var funcs = _.collect(this._settingsList, function(key)
	{
		return function updateKey(cb)
		{
			var query = self.database
							.update('settings')
							.where('key', 'is', key)
							.set('settings', JSON.stringify(self[key]))
			if (self.user)
				query = query.where('user','is', self.user)
			else
				query = query.where('user', 'notexists')
			query.execute(function(err, resp)
			{
				if (resp.modified === 0)
					self.database
						.create('setting',
						{
							'key': key,
							'settings': JSON.stringify(self[key])
						}, cb)
				else
					cb()
			})
		}
	})

	async.series(funcs, callback)
}
})