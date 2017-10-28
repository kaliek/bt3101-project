const HeadlessChrome = require('simple-headless-chrome')
const config = require('./config.json')

const browser = new HeadlessChrome({
    headless: false // set to true for production; to false to view actual browser action
})
function getInfo(name, uni, professor_id, request_id, original_status) {
    var result = {
        name: name,
        currPos: null,
        uni: uni,
        promYear: null,
        sch: null,
        gradYear: null,
        phdField: null,
        success: false,
        profId: professor_id,
        requestId: request_id,
        originalStatus: original_status
    }
    console.log(result.value)
    try {
        const eduHtml = document.querySelector('.workspace-accordion-item.workspace-accordion-active.ng-scope')
        var phds = eduHtml.querySelectorAll('.ng-binding.ng-scope')
        console.log(phds)
        var guess = phds[0].innerText
        console.log(guess)
        if (!isNaN(guess)) { // this means the user did not give year data
            result['gradYear'] = eduHtml.querySelectorAll('span[ng-if="group.getActive().endDate.year"]')[0].innerText
        }
        result['sch'] = eduHtml.querySelectorAll('span[ng-bind="group.getActive().affiliationName.value"]')[0].innerText
        result['phdField'] = eduHtml.querySelectorAll('span[ng-if="group.getActive().roleTitle.value"]')[0].innerText
        result['success'] = true

        const expHtml = document.querySelector('#workspace-employment')
        var unis = expHtml.querySelectorAll('span[ng-bind="group.getActive().affiliationName.value"]')
        var workIndex = unis.length - 1 // assume the list is in order
        result['uni'] = expHtml.querySelectorAll('span[ng-bind="group.getActive().affiliationName.value"]')[workIndex].innerText
        result['promYear'] = expHtml.querySelectorAll('span[ng-if="group.getActive().startDate.year"]')[workIndex].innerText
        result['currPos'] = expHtml.querySelectorAll('span[ng-if="group.getActive().roleTitle.value"]')[workIndex].innerText

        return result
    } catch (err) {
        result['error'] = 'Exception in querySelector ' + err
        return result
    }
}

async function search(item) {
    try {
        await browser.init()
        const tab = await browser.newTab({ privateTab: false })
        await tab.goTo('http://orcid.org/0000-0003-2463-7842')
        await tab.wait(2000)
        await tab.click('#search-box input')
        await tab.type('#search-box input', item[0] + ' ' + item[1])
        await tab.click('.search-button')
        await tab.wait(2000)
        await tab.waitForSelectorToLoad('td.search-result-orcid-id:first-child a')
        await tab.click('td.search-result-orcid-id:first-child a')
        await tab.wait(2000)

        const info = await tab.evaluate(getInfo, item[0], item[1], item[2], item[3], item[4])
        await console.log(info["result"])
        if (info.result.value.error) {
            throw info.error
        } node
        await tab.wait(1000)
        await tab.close()
        console.log(info['result'])
        return info['result']
    } catch (err) {
        console.log('ERROR!', err)
        console.log('Cannot get ', item)
        console.log('-------------------')
    }
}

async function crawl(item) {
    var a = await search(item)
    await browser.close()
    return a
}

var fs = require('fs');
var parse = require('csv-parse');

var inputFile = 'crawler_inputs.csv';
console.log("Processing input file");
var csvWriter = require('csv-write-stream')
var writer = csvWriter()
writer.pipe(fs.createWriteStream('crawler_outputs.csv'))

var parser = parse({ delimiter: ',' }, async function (err, data) {
    data.forEach(async function (line) {
        var prof = {
            "professor_name": line[0],
            "university_name": line[1],
            "professor_id": line[2],
            "request_id": line[3],
            "original_status": line[4]
        };
        var output = await crawl([prof["professor_name"], prof["university_name"], prof["professor_id"], prof["request_id"], prof["original_status"]])
        if (output.value.success) {
            writer.write(output.value)
        }
    })
})

// read the inputFile, feed the contents to the parser
fs.createReadStream(inputFile).pipe(parser)

