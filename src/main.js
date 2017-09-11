// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import('../node_modules/vuetify/dist/vuetify.min.css')
import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import store from './store'
import moment from 'moment'
window.moment = moment

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
// Implement an SPRINTF filter! So nice to have.
//
Vue.filter('formatNumber', function(value, formatString) {
  return sprintf(formatString, value)
})

// Quick GUID generator.
function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
    .toString(16)
    .substring(1);
}

window.guid = function () {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

// Modify local storage!
Storage.prototype.setObj = function(key, obj) {
    return this.setItem(key, JSON.stringify(obj))
}
Storage.prototype.getObj = function(key) {
    return JSON.parse(this.getItem(key))
}
