// Vendor Modules
/////////////////////////
// var _ = require('lodash')
var async = require('async')
var it = global.it
var describe = global.describe
var chai = require('chai')
var expect = chai.expect



//Our Modules
///////////////////////
// var helpers = require('arkutil')
var it = global.it
var before = global.before
var after = global.after
var Database = require('c:/ie/database/')
var SettingsManager = require('c:/ie/settingsManager/settingsManager/settingsManager')


describe('test/test_settingsManager', function()
{

before(function(done)
{
	var self = this


	function createDatabase(callback)
	{
		self.database = new Database(
							{
								coren:
								{
									apiRoot: 'http://127.0.0.1:2160/api/',
									authenticate: false
								}
							}, callback)
	}
	function createBasicSettings(callback)
	{
		self.database
			.create('settings',
					{
						'key': 'testApp',
						'settings': JSON.stringify(
						{
							profile: 'randomUser',
							otherThing: 'someOtherSetting'
						 })
					},
					null,
					callback)
	}
	function createUser(callback)
	{
		self.database
			.create('user',
					{
						'name': 'settingsTestUser',
						'username': 'settingsTestUser',
						'password': 'sfacvsdf',
						'email': 'settings@user.com'
					}, null, function(err, resp)
					{
						self.userID = resp[0]._id
						callback()
					})
	}
	function createUserSettings(callback)
	{
		self.database
			.create('settings',
			{
				'user': self.userID,
				'key': 'testApp',
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
		createUser,
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
			.where('key', 'is', 'testApp')
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
	var settingsManager = new SettingsManager(this.database, 'testApp', function()
	{
		expect(settingsManager).to.not.equal(undefined)
		done()
	})
})

it('should load in the default settings for a generic app', function(done)
{
	var settingsManager = new SettingsManager(this.database, 'testApp', function()
	{
		expect(settingsManager.profile).to.equal('randomUser')
		expect(settingsManager.otherThing).to.equal('someOtherSetting')
		done()
	})
})

it('should load in the default settings for a user app', function(done)
{
	var settingsManager = new SettingsManager(this.database, 'testApp', 'settingsTestUser', function()
	{
		expect(settingsManager.profile).to.equal('otherUser')
		expect(settingsManager.otherThing).to.equal('someOtherSetting')
		expect(settingsManager.newSetting).to.equal('a personalized setting')
		done()
	})
})

it('should load in the default settings for a user app', function(done)
{
	var settingsManager = new SettingsManager(this.database, 'testApp', this.userID, function()
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
	var settingsManager = new SettingsManager(this.database, 'testApp', this.userID, function()
	{
		expect(settingsManager.profile).to.equal('otherUser')
		expect(settingsManager.otherThing).to.equal('someOtherSetting')
		expect(settingsManager.newSetting).to.equal('a personalized setting')

		settingsManager.newSetting = 'repersonalizedSetting'
		settingsManager.otherThing = 'aModifiedSetting'
		settingsManager.brandNew  = 'superNew'

		settingsManager.save(function()
		{
			var updatedSettings = new SettingsManager(self.database, 'testApp', self.userID, function()
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


