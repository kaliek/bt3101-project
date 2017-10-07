// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable no-unused-vars */
import Vue from 'vue'
import App from './App'
import router from './router'
import '../semantic/dist/semantic.css'
import semantic from 'semantic'
import {createClass} from 'asteroid'
import Vuex from 'vuex'
import $ from 'jquery'

Vue.config.productionTip = false
Vue.use(Vuex)
const Asteroid = createClass()

/* eslint-disable no-new */
const store = new Vuex.Store({
  state: {
    conn: new Asteroid({
      endpoint: 'ws://115.66.242.122:3100/websocket'
      // endpoint: 'ws://localhost:3000/websocket'
    }),
    msgModalProps: {
      title: '',
      msg: '',
      icon: ''
    },
    uIds: [],
    fId: '',
    dbSearchResults: [],
    cruIds: [],
    crfId: ''
  },
  mutations: {
    added: function (s, o) {
      var obj = o.fields
      obj._id = o.id
      Vue.set(s, o.collection, s[o.collection] || {}) // If the collection doesn't yet exist in the s, create it.
      Vue.set(s, o.collection + 'List', s[o.collection + 'List'] || [])
      if (!(o.id in s[o.collection])) {
        Vue.set(s[o.collection], obj._id, obj)
        s[o.collection + 'List'].push(obj)
        console.log(obj._id + ' added to ' + o.collection)
      } else {
        Vue.set(s[o.collection], obj._id, obj)
        s[o.collection + 'List'].splice(s[o.collection + 'List'].findIndex(function (e) {
          return e['_id'] === o.id
        }, 1))
        s[o.collection + 'List'].push(obj)
        console.log(obj._id + ' re-added to ' + o.collection)
      }
    },
    changed: function (s, o) {
      if ('cleared' in o) {
        o.cleared.forEach(function (field) {
          Vue.delete(s[o.collection][o.id], field)
        })
      }
      if ('fields' in o) {
        Object.keys(o.fields).forEach(function (field) {
          Vue.set(s[o.collection][o.id], field, o.fields[field])
        })
      }
      Vue.set(s[o.collection + 'List'], 0, s[o.collection + 'List'][0]) // Just to trigger computed value updates
      console.log(o.id + ' from ' + o.collection + ' changed')
    },
    removed: function (s, o) {
      Vue.delete(s[o.collection], o.id)
      s[o.collection + 'List'].splice(s[o.collection + 'List'].findIndex(function (e) {
        return e._id === o.id
      }), 1)
      console.log(o.id + ' from ' + o.collection + ' removed')
    },
    showMessageModal: function (s, payload) {
      s.msgModalProps = payload
      $('#message-modal').modal('show')
    },
    setDbSearchResults: function (s, p) {
      s.dbSearchResults = p
    },
    setSelectedIds: function (s, {uIds, fId}) {
      s.uIds = uIds
      s.fId = fId
    },
    setCrawlRequest: function (s, {uIds, fId, router}) {
      s.cruIds = uIds
      s.crfId = fId
      router.push('crawlrequest')
    }
  },
  actions: {
    callMethod: function ({ commit, state }, params) {
      state.conn.call(...params).catch(function (e) {
        commit('showMessageModal', {msg: e.reason, title: e.error, icon: 'fa-exclamation-triangle'})
      })
    },
    callMethodAndCallback: function ({ commit, state }, {callback, params}) {
      state.conn.call(...params).then(callback).catch(function (e) {
        commit('showMessageModal', {msg: e.reason, title: e.error, icon: 'fa-exclamation-triangle'})
      })
    },
    loginWithPassword: function ({ commit, state }, {email, password, router}) {
      state.conn.loginWithPassword({email: email, password: password}).then(function (r) {
      }).catch(function (e) {
        commit('showMessageModal', {msg: 'Incorrect login information', title: 'Login Failed', icon: 'fa-exclamation-triangle'})
      })
    },
    logout: function ({ commit, state }, router) {
      state.conn.logout()
      router.push('/')
    },
    searchProfessors: function ({ commit, state }, {uIds, fId, router}) {
      commit('setSelectedIds', {uIds: uIds, fId: fId})
      state.conn.call('searchProfessors', uIds, fId).then(function (r) {
        commit('setDbSearchResults', r)
        router.push('database')
      }).catch(function (e) {
        commit('showMessageModal', {msg: e.reason, title: e.error, icon: 'fa-exclamation-triangle'})
      })
    }
  },
  getters: {
  }
})

const app = new Vue({
  el: '#app',
  router: router,
  store,
  template: '<App/>',
  components: { App },
  beforeCreate: function () {
    this.$store.state.conn.connect()
    this.$store.state.conn.on('connected', function () {
      console.log('Connected to Server!')
      this.$store.state.conn.loginWithPassword({email: 'admin@admin.com', password: 'admin'})
    }.bind(this))
    this.$store.state.conn.on('disconnected', function () {
      console.log('Disconnected!')
    })
    this.$store.state.conn.on('loggedIn', function () {
      console.log('Logged In!')
      this.$store.state.conn.subscribe('allUniversities')
      this.$store.state.conn.subscribe('allFaculties')
      this.$store.state.conn.subscribe('allProfessors')
      this.$store.state.conn.subscribe('allCrawlRequests')
    }.bind(this))
    this.$store.state.conn.on('loggedOut', function () {
      this.$router.push('/')
      console.log('Logged Out!')
    }.bind(this))
    this.$store.state.conn.ddp.on('added', function (item) {
      this.$store.commit('added', item)
    }.bind(this))
    this.$store.state.conn.ddp.on('changed', function (item) {
      this.$store.commit('changed', item)
    }.bind(this))
    this.$store.state.conn.ddp.on('removed', function (item) {
      this.$store.commit('removed', item)
    }.bind(this))
    this.$store.state.conn.ddp.on('ready', function () {
      console.log('Ready!')
    })
  },
  destroyed: function () {
    this.$store.state.conn.disconnect()
  }
})
