import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/login'
import search from '@/components/search'
import database from '@/components/database'
import crawlrequest from '@/components/crawlrequest'
import crawlmonitor from '@/components/crawlmonitor'
import manualcrawl from '@/components/manualcrawl'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: main
    },
    {
      path: '/search',
      name: 'search',
      component: search
    },
    {
      path: '/database',
      name: 'database',
      component: database
    },
    {
      path: '/crawlrequest',
      name: 'crawlrequest',
      component: crawlrequest
    },
    {
      path: '/crawlmonitor',
      name: 'crawlmonitor',
      component: crawlmonitor
    },
    {
      path: '/manualcrawl',
      name: 'manualcrawl',
      component: manualcrawl
    }
  ]
})
