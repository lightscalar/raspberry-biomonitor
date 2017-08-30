// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import('../node_modules/vuetify/dist/vuetify.min.css')
import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import store from './store'

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(Vuetify)

/* eslint-disable no-new */
var app = new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})

window.router = app.$router
