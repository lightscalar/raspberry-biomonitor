import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'
import Session from '@/components/Session'
import Sessions from '@/components/Sessions'

Vue.use(Router)

var landingPageRoute = {path: '/', name: 'LandingPage', component: LandingPage}
var sessionRoute = {path: '/session/:id', name: 'Session', component: Session,
  props: true}
var sessionsRoute = {path: '/sessions', name: 'Sessions', component: Sessions}

export default new Router({
  routes: [
    landingPageRoute,
    sessionRoute,
    sessionsRoute
  ]
})
