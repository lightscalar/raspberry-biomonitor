import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'
import Session from '@/components/Session'

Vue.use(Router)

var landingPageRoute = {path: '/', name: 'LandingPage', component: LandingPage}
var sessionRoute = {path: '/session/:id', name: 'Session', component: Session,
  props: true}

export default new Router({
  routes: [
    landingPageRoute,
    sessionRoute
  ]
})
