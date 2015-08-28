// Vendor Modules
/////////////////////////
var _ = require('lodash')
var it = global.it
var describe = global.describe
var chai = require('chai')
var expect = chai.expect

var GlobalSettings = require('../settingsManager/globalSettings')



describe('test/test_globalSettings.js', function()
{
this.timeout(1000000)

it('should init', function()
{
	var globalSettings = new GlobalSettings()
	expect(globalSettings).to.not.equal(undefined)
})

var firstPath = 'c:/ie/settingsManager/test/testSettings'
var secondPath = 'c:/ie/settingsManager/test/moreTestSettings'

it('should load in config from one path, one mode', function()
{
	var globalSettings = new GlobalSettings(firstPath, 'default')
	expect(globalSettings.firstTest).to.equal('testOne')

})

it('should load in config from several paths, several modes', function()
{
	var globalSettings = new GlobalSettings([firstPath, secondPath], ['default', 'more'])
	expect(globalSettings.firstTest).to.equal('testOne')
	expect(globalSettings.otherSetting).to.equal('othersetting')

})

it('should handle lists, strings and objects', function()
{
	var globalSettings = new GlobalSettings(firstPath, 'default')
	expect(globalSettings.firstTest).to.equal('testOne')
	expect(_.isEqual(globalSettings.listTest, ['apples', 'pears'])).to.equal(true)
	expect(_.isEqual(globalSettings.dictTest, {other: 'test'})).to.equal(true)
})

it('should overwrite settings from left to right in the modes', function()
{
	var globalSettings = new GlobalSettings(firstPath, ['default', 'newMode'])
	expect(globalSettings.firstTest).to.equal('newTestOne')
	expect(globalSettings.listTest).to.equal('overwrittenTest')
	expect(_.isEqual(globalSettings.dictTest, {other: 'test'})).to.equal(true)
})

it('should overwrite settings from left to right in the filepaths', function()
{
	var globalSettings = new GlobalSettings([firstPath, secondPath], 'newMode')
	expect(globalSettings.secondPathTest).to.equal('secondPathOnly')
	expect(globalSettings.firstTest).to.equal('newTestTwo')
	expect(globalSettings.listTest).to.equal('overwrittenTest')
})

})