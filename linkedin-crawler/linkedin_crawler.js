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
        const expHtml = document.querySelector('.pv-profile-section.experience-section')
        var unis = document.querySelectorAll('.pv-entity__secondary-title')
        for (var i = 0; i < unis.length; i++) {
            var u = unis[i].innerText
            if (u == uni) {
                result['currPos'] = expHtml.querySelectorAll('.pv-entity__summary-info h3')[i].innerText
                var p = expHtml.querySelectorAll('.pv-entity__date-range span:not(.visually-hidden)')[i].innerText
                result['promYear'] = p.split("–")[0].trim()
                break
            }
        }

        const eduHtml = document.querySelector('.pv-profile-section.education-section')
        var phds = eduHtml.querySelectorAll('.pv-entity__degree-name .pv-entity__comma-item')
        for (var i = 0; i < phds.length; i++) {
            var d = phds[i].innerText
            if (d == 'PhD') {
                result['sch'] = eduHtml.querySelectorAll('.pv-entity__school-name')[i].innerText
                result['gradYear'] = eduHtml.querySelectorAll('.pv-entity__dates span:not(.visually-hidden) time')[i + 1].innerText
                result['phdField'] = eduHtml.querySelectorAll('.pv-entity__fos .pv-entity__comma-item')[i].innerText
            }
        }
        result['success'] = true
        return result
    } catch (err) {
        result['error'] = 'Exception in querySelector ' + err
        return result
    }
}
async function authenticate() {
    await browser.init()
    const tab = await browser.newTab({ privateTab: false })

    await tab.goTo('https://www.linkedin.com/')
    await tab.fill('#login-email', config.username)
    await tab.type('#login-password', config.password)
    await tab.click('#login-submit')
    await tab.wait(3500)
    await tab.log('Finish logging in')
}

async function search(item) {
    try {
        const tab = await browser.newTab({ privateTab: false })
        await tab.goTo('https://www.linkedin.com/')
        await tab.wait(2000)
        await tab.click('.nav-search-bar input')
        await tab.type('.nav-search-bar input', item[0] + ' ' + item[1])
        await tab.click('button.nav-search-button')
        await tab.wait(2000)
        await tab.click('.search-result__wrapper a')
        await tab.wait(2000)

        const info = await tab.evaluate(getInfo, item[0], item[1], item[2], item[3], item[4])
        // await console.log(info["result"])
        if (info.result.value.error) {
            throw info.error
        }
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
    await authenticate()
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
            "professor_name": line[0]
            , "university_name": line[1]
            , "professor_id": line[2]
            , "request_id": line[3]
            , "original_status": line[4]
        };
        var output = await crawl([prof["professor_name"], prof["university_name"], prof["professor_id"], prof["request_id"], prof["original_status"]])
        if (output.value.success) {
            writer.write(output.value)
        }
    })
})

// read the inputFile, feed the contents to the parser
fs.createReadStream(inputFile).pipe(parser)

