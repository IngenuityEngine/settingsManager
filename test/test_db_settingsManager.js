// Vendor Modules
/////////////////////////
var _ = require('lodash')
var it = global.it
var describe = global.describe
var chai = require('chai')
var expect = chai.expect



//Our Modules
///////////////////////
var helpers = require('arkutil')
var it = global.it
var Database = require('c:/ie/database/database')


// var SettingsManager = require('../settingsManager/settingsManager')

// var urlPrefix = ''
// if (helpers.isServer)
// {
// 	urlPrefix = 'http://127.0.0.1'
// 	if (coren.options.basics.port)
// 		urlPrefix += ':' + coren.options.basics.port
// }

// // Mocha globals
// /////////////////////////
// var describe = helpers.getGlobal('describe')

// // Tests
// /////////////////////////
// describe('test/test_settingsManager.js', function()
// {
// it('should init', function()
// {
// 	var settingsManager = new SettingsManager()
// 	expect(settingsManager).to.not.equal(undefined)
// })

// var firstPath = 'c:/ie/settingsManager/test/testSettings'
// var secondPath = 'c:/ie/settingsManager/test/moreTestSettings'

// it('should load in config from one path, one mode', function()
// {
// 	var settingsManager = new SettingsManager(firstPath, 'default')
// 	expect(settingsManager.firstTest).to.equal('testOne')

// })

// it('should load in config from several paths, several modes', function()
// {
// 	var settingsManager = new SettingsManager([firstPath, secondPath], ['default', 'more'])
// 	expect(settingsManager.firstTest).to.equal('testOne')
// 	expect(settingsManager.otherSetting).to.equal('othersetting')

// })
// })

var Database = require('c:/ie/database/database')

var db = new Database({coren: {apiRoot: 'http://127.0.0.1:2160/api/', authenticate: false}}, function()
{
	console.log('yatta')
	var user
db.find('user').execute(function(err, resp)
{
	user = resp
	console.log('user is', user)
})
})

