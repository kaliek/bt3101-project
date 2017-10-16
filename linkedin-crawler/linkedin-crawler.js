const HeadlessChrome = require('simple-headless-chrome')
const config = require('./config.json')

const browser = new HeadlessChrome({
    headless: false // set to true for production; to false to view actual browser action
})
function getInfo(name, uni) {
    var result = {
        name: name,
        currPos: null,
        uni: uni,
        promYear: null,
        sch: [],
        gradYear: [],
        phdField: []
    }

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
                result['sch'].push(eduHtml.querySelectorAll('.pv-entity__school-name')[i].innerText)
                result['gradYear'].push(eduHtml.querySelectorAll('.pv-entity__dates span:not(.visually-hidden) time')[i + 1].innerText)
                result['phdField'].push(eduHtml.querySelectorAll('.pv-entity__fos .pv-entity__comma-item')[i].innerText)
            }
        }
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

        const info = await tab.evaluate(getInfo, item[0], item[1])
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
    await search(item)
}
var output = crawl(['Ben Leong', 'National University of Singapore'])
