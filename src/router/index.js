import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'

Vue.use(Router)

var landingPageRoute = {path: '/', name: 'LandingPage', component: LandingPage} 

export default new Router({
  routes: [
    landingPageRoute
  ]
})
