import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/index'
Vue.use(Vuex)

export default new Vuex.Store ({

  state: {

    session: {},
    sessions: [],
    monitorStatus: {
      status: false,
      connected: false,
      streaming: false,
      message: 'Board Not Detected'
    },
    socket: {}

  },

  mutations: {

    setSocket (state) {
      state.socket = io.connect('http://localhost')
    },

    setStatus (state, monitorStatus) {
      state.monitorStatus = monitorStatus
    },

    setSession (state, session) {
      state.session = session
    },

    setSessions (state, sessions) {
      state.sessions = sessions
    }

  },

  actions: {

    establishSocketConnection (context) {
      context.commit('setSocket')
      context.state.socket.emit('request_status')
    },

    createSession (context) {
      api.postResource ('sessions', {}).then(function (resp) {
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
    }

  },

})


