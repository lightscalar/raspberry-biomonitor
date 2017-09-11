import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/index'
Vue.use(Vuex)

export default new Vuex.Store ({

  state: {

    session: {hid: null, cohortId: null, events: [], histories: [], reports: []},
    sessions: [],
    monitorStatus: {
      status: false,
      connected: false,
      streaming: false,
      message: 'Board Not Detected'
    },
    socket: {},

    histories: [],
    history: {},

    sessions: [],
    snapshot: {},

    cohorts: [],
    cohort: {name: '', description: '', reports: [], histories: []},
    report: {name: '', description: '', fields: [], type: 'history'},
    field: {name:'', description: '', type: 'numeric', includeUnits: false,
             units: '', includeDetails: false, isTextOnly: false}
  },

  mutations: {

    setSocket (state) {
      state.socket = io.connect('http://localhost:5200')
    },

    setStatus (state, monitorStatus) {
      state.monitorStatus = monitorStatus
    },

    setSession (state, session) {
      state.session = session
    },

    setSessions (state, sessions) {
      state.sessions = sessions
    },

    setSnapshot(state, snapshot) {
      state.snapshot = snapshot
    },

    setCohort(state, cohort) {
      state.cohort = cohort
    },

    setCohorts(state, cohorts) {
      state.cohorts = cohorts
    },

    resetField(state) {
      state.field = {name:'', description: '', isBoolean: false, type: 'numeric',
                     includeUnits: false, units: '', includeDetails: false}
    },

    reset(state) {
      state.cohort = {name:'', description: '', reports: []}
      state.report = {name: '', description: '', fields: [], type: 'history'}
      state.session = {hid: null, cohortId: null, events:[], histories:[]}
      state.snapshot = {}
    }

  },

  actions: {

    establishSocketConnection (context) {
      context.commit('setSocket')
      context.state.socket.emit('request_status')
    },

    createSession (context) {
      var session = context.state.session
      api.postResource ('sessions', session).then(function (resp) {
        context.commit('setSession', resp.data)
        router.push({name: 'Session', params: {id: resp.data._id}})
      })
    },

    getSession (context, id) {
      api.getResource('session', id).then( function (resp) {
        context.commit('setSession', resp.data)
      })
    },

    getSessions (context) {
      api.listResource('sessions').then( function (resp) {
        context.commit('setSessions', resp.data)
      })
    },

    createCohort(context, cohort) {
      api.postResource('cohorts', cohort).then(function(resp) {
        context.commit('setCohort', resp.data)
        router.push({name: 'Cohort', params: {id: resp.data._id}})
      })
    },

    getCohort(context, cohortId) {
      api.getResource('cohort', cohortId).then(function(resp) {
        context.commit('setCohort', resp.data)
      })
    },

    getCohorts(context) {
      api.listResource('cohorts').then(function(resp) {
        context.commit('setCohorts', resp.data)
      })
    },

    deleteCohort(context, id) {
      api.deleteResource('cohort', id).then(function(resp) {
       router.push({name: 'LandingPage'})
      })
    },

    deleteSession(context, id) {
      api.deleteResource('session', id).then(function(resp) {
       router.push({name: 'LandingPage'})
      })
    },

    updateCohort(context, cohort) {
      api.putResource('cohort', cohort).then(function(resp) {
        context.dispatch('getCohort', resp.data._id)
      })
    },

    listSessions(context) {
      api.listResource('sessions').then( function (resp) {
        context.commit('setSessions', resp.data)
      })
    },

    updateSession(context, session) {
      api.putResource('session', session).then(function (resp) {
        context.commit('setSession', resp.data)
      })
    },

  },

})


