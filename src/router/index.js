import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'
import Session from '@/components/Session'
import Sessions from '@/components/Sessions'
import CreateCohort from '@/components/CreateCohort'
import Cohort from '@/components/Cohort'
import Cohorts from '@/components/Cohorts'
import Report from '@/components/Report'
import Annotate from '@/components/Annotate'
import Events from '@/components/Events'
import Histories from '@/components/Histories'
import Download from '@/components/Download'

Vue.use(Router)

var landingPageRoute = {path: '/', name: 'LandingPage', component: LandingPage}
var sessionRoute = {path: '/session/:id', name: 'Session', component: Session,
  props: true}
var sessionsRoute = {path: '/sessions', name: 'Sessions', component: Sessions}

var createCohortRoute = {path: '/cohorts/create', name: 'CreateCohort', component: CreateCohort}
var cohortRoute = {path: '/cohort/:id', name: 'Cohort', component: Cohort, props: true}
var cohortsRoute = {path: '/cohorts', name: 'Cohorts', component: Cohorts}
var reportRoute = {path: '/cohort/:id/report/:reportId', name: 'Report',
  component: Report, props: true}
var annotateRoute = {path: '/session/:id/annotate', name: 'Annotate',
  component: Annotate, props: true}
var eventsRoute = {path: '/session/:id/events', name: 'Events', component: Events, props: true}
var historiesRoute = {path: '/session/:id/histories', name: 'Histories',
  component: Histories, props: true}
var downloadRoute = {path: '/session/:id/download', name: 'Download',
  component: Download, props: true}

export default new Router({
  routes: [
    landingPageRoute,
    sessionRoute,
    sessionsRoute,
    createCohortRoute,
    cohortRoute,
    cohortsRoute,
    reportRoute,
    annotateRoute,
    eventsRoute,
    historiesRoute,
    downloadRoute
  ]
})
