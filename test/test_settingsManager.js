// Vendor Modules
/////////////////////////
// var _ = require('lodash')
var async = require('async')
var debug = require('debug')('settingsManager:test')
var it = global.it
var describe = global.describe
var expect = require('expect.js')


// Our Modules
///////////////////////
// var helpers = require('arkutil')
var config = require('../config/test')
var it = global.it
var before = global.before
var after = global.after
var Database = require(config.databasePath)
var SettingsManager = require('../settingsManager/settingsManager')


describe('test/test_settingsManager', function()
{

// bail after the first error
this.bail(true)
// 5 second timeout
this.timeout(10000)

before(function(done)
{
	var self = this

	function createDatabase(callback)
	{
		self.database = new Database(
							{
								coren:
								{
									apiRoot: config.apiRoot,
									authenticate: false
								}
							}, callback)
	}
	function createBasicSettings(callback)
	{
		self.database
			.create('settings',
					{
						'key': 'testKey',
						'settings': JSON.stringify(
						{
							profile: 'randomUser',
							otherThing: 'someOtherSetting'
						 })
					},
					null,
					callback)
	}
	function findOrCreateUser(callback)
	{
		self.database
			.find('user')
			.where('name','is','settingsTestUser')
			.execute(function(err, resp)
			{
				if (err)
					return callback(err)
				if (resp.length)
				{
					self.userID = resp[0]._id
					callback()
				}
				else
				{
					self.database.create('user',
					{
						'name': 'settingsTestUser',
						'username': 'settingsTestUser',
						'password': 'sfacvsdf',
						'email': 'settings@user.com'
					}, null, function(err, resp)
					{
						debug('err:', err)
						debug('resp:', resp)
						self.userID = resp[0]._id
						callback()
					})
				}
			})
	}
	function createUserSettings(callback)
	{
		self.database
			.create('settings',
			{
				'user': self.userID,
				'key': 'testKey',
				'settings': JSON.stringify(
				{
					profile: 'otherUser',
					newSetting: 'a personalized setting'
				})
			},
			null,
			callback)

	}

	async.series([
		createDatabase,
		createBasicSettings,
		findOrCreateUser,
		createUserSettings
		], done)
})

after(function(done)
{
	var self = this

	function removeSettings(callback)
	{
		var query = self.database
			.remove('settings')
			.where('key', 'is', 'testKey')
			.multiple(true)
			query.execute(callback)
	}

	function removeTestUser(callback)
	{
		var query = self.database
			.remove('user')
			.where('name', 'is', 'settingsTestUser')
			.multiple(true)
			query.execute(callback)
	}
	async.series([
		removeSettings,
		removeTestUser
		], done)
})

it('should initialize a settingsManager', function(done)
{
	var settingsManager = new SettingsManager(this.database, 'testKey', function()
	{
		expect(settingsManager).to.not.equal(undefined)
		done()
	})
})

it('should load in the default settings for a generic app', function(done)
{
	var settingsManager = new SettingsManager(this.database, 'testKey', function()
	{
		expect(settingsManager.profile).to.equal('randomUser')
		expect(settingsManager.otherThing).to.equal('someOtherSetting')
		done()
	})
})

it('should load in the default settings for a user app', function(done)
{
	var settingsManager = new SettingsManager(this.database, 'testKey', 'settingsTestUser', function()
	{
		expect(settingsManager.profile).to.equal('otherUser')
		expect(settingsManager.otherThing).to.equal('someOtherSetting')
		expect(settingsManager.newSetting).to.equal('a personalized setting')
		done()
	})
})

it('should load in the default settings for a user app', function(done)
{
	var settingsManager = new SettingsManager(this.database, 'testKey', this.userID, function()
	{
		expect(settingsManager.profile).to.equal('otherUser')
		expect(settingsManager.otherThing).to.equal('someOtherSetting')
		expect(settingsManager.newSetting).to.equal('a personalized setting')
		done()
	})
})

it('should load save settings for a user app', function(done)
{
	var self = this
	var settingsManager = new SettingsManager(this.database, 'testKey', this.userID, function()
	{
		expect(settingsManager.profile).to.equal('otherUser')
		expect(settingsManager.otherThing).to.equal('someOtherSetting')
		expect(settingsManager.newSetting).to.equal('a personalized setting')

		settingsManager.newSetting = 'repersonalizedSetting'
		settingsManager.otherThing = 'aModifiedSetting'
		settingsManager.brandNew  = 'superNew'

		settingsManager.save(function()
		{
			var updatedSettings = new SettingsManager(self.database, 'testKey', self.userID, function()
			{
				expect(updatedSettings.profile).to.equal('otherUser')
				expect(updatedSettings.otherThing).to.equal('aModifiedSetting')
				expect(updatedSettings.newSetting).to.equal('repersonalizedSetting')
				expect(updatedSettings.brandNew).to.equal('superNew')
				updatedSettings.otherThing = 'someOtherSetting'
				updatedSettings.newSetting = 'a personalized setting'
				updatedSettings.save(done)
			})
		})

	})
})


})


