<template>

  <v-container>

    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-breadcrumbs  icons divider="forward" class='pa-0 ma-0'>
              <v-breadcrumbs-item href="/#" class='white--text'>
                Home
              </v-breadcrumbs-item>
              <v-breadcrumbs-item :href="'#/session/'+session._id">
                {{session.hid}}
              </v-breadcrumbs-item>
              <v-breadcrumbs-item>
                Annotation
              </v-breadcrumbs-item>
            </v-breadcrumbs>
            <v-spacer></v-spacer>
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
    <br/>

    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card>
          <v-card-title>
            <v-subheader>
              Details
            </v-subheader>
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text>
            <v-layout row wrap>
              <v-flex xs12 lg6>
                <v-text-field
                  @blur='saveSession'
                  label='Description'
                  v-model='session.description'>
                </v-text-field>
              </v-flex>

              <v-flex xs12 lg4 offset-lg1>
                <v-select
                  v-bind:items="cohorts"
                  label="Cohort"
                  item-value='_id'
                  item-text='name'
                  v-model="session.cohortId"
                  persistent-hint
                  @change='saveSession'
                  bottom>
                </v-select>
              </v-flex>
            </v-layout>

          </v-card-text>

          <v-divider></v-divider>

          <!-- UPDATE OR DELETE -->
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn error flat @click.native='showDelete=true'>
              Delete
            </v-btn>
            <v-btn primary flat @click.native='saveSession'>
              Update
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-flex>
    </v-layout>
    <br/>

    <v-layout v-if='snapshots.length>0'>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-subheader>
              Add Snapshots
            </v-subheader>
            <v-spacer></v-spacer>
            <v-btn
              primary
              flat
              :to="{name: 'Events', params: {id: this.id}}">
              <v-icon class='blue--text text--darken-3'>
                view_list
              </v-icon>
              View
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>

            <v-list two-line>
              <template v-for='(report, k) in snapshots'>
                <v-list-tile
                  avatar
                  v-bind:key="report.name"
                  @click.native='openReportDialog(report)'>
                  <v-list-tile-avatar>
                    <v-icon
                      v-if="report.type=='snapshot'"
                      class='red--text text--darken-4'>
                      fa-line-chart
                    </v-icon>
                  </v-list-tile-avatar>
                  <v-list-tile-content>
                    <v-list-tile-title v-html="report.name">
                    </v-list-tile-title>
                    <v-list-tile-sub-title v-html='report.description'>
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider v-if='k < snapshots.length-1'></v-divider>
              </template>
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <br v-if='snapshots.length>0'/>

    <v-layout v-if='histories.length>0'>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-subheader>
              Edit Histories
           </v-subheader>
            <v-spacer></v-spacer>
            <v-btn
              primary
              flat
              :to="{name: 'Histories', params: {id: this.id}}">
              <v-icon class='blue--text text--darken-3'>
                view_list
              </v-icon>
              View
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>

            <v-list two-line>
              <template v-for='(report, k) in histories'>
                <v-list-tile
                  avatar
                  v-bind:key="report.name"
                  @click.native='openReportDialog(report)'>
                  <v-list-tile-avatar>
                    <v-icon
                      v-if="report.type=='snapshot'"
                      class='red--text darken-3--text'>
                      fa-line-chart
                    </v-icon>
                    <v-icon
                      v-else="report.type=='snapshot'"
                      class='blue--text text--darken-4'>
                      fa-history
                    </v-icon>
                  </v-list-tile-avatar>
                  <v-list-tile-content>
                    <v-list-tile-title
                      v-html="report.name">
                    </v-list-tile-title>
                    <v-list-tile-sub-title
                      v-html='report.description'>
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider
                  v-if='k < histories.length-1'>
                </v-divider>
              </template>
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <report-modal
      @close='isReportDialogOpen=false'
      @submit='saveReport'
      :report='currentReport'
      :isOpen='isReportDialogOpen'>
    </report-modal>

    <confirm-modal
      @confirm='deleteSession'
      :isOpen='showDelete'
      @cancel='showDelete=false'
      :message='deleteMessage'>
    </confirm-modal>

    <messenger
      :isOpen='showMessage'
      :message='message'
      :type='messageType'>
    </messenger>

  </v-container>
</template>

<script>

import ReportModal from "./ReportModal"
import ConfirmModal from "./ConfirmModal"
import Messenger from "./Messenger"

  export default {

    components: {ReportModal, ConfirmModal, Messenger},

    props: ['id'],

    data () {
      return {
        isReportDialogOpen: false,
        showDelete: false,
        deleteMessage: 'Are you are sure you want to delete this session?',
        message: '',
        showMessage: false,
        messageType: 'info',
        currentReport: {},
        update: true,
        selectedSession: null,
        active: false
      }
    },

    watch: {

      $route () {
        this.$store.dispatch('getSession', this.id)
      },

    },

    methods: {

      saveReport (report) {
        if (report.type == 'history') {
          this.session.histories.push(report)
        } else {
          this.session.events.push(report)
        }
        this.saveSession()
      },

      deleteSession () {
        this.showDelete = false
        this.$store.dispatch('deleteSession', this.session._id)
      },

      selectedActiveSession () {
        this.$router.replace({name: 'Session',
          params: {id: this.selectedSession}})
      },

      openEvents () {
        this.$router.push({name: 'Events', params: {id: this.id}})
      },

      openReportDialog(report) {
        if (report.type == 'history') {
          var latestHistory = report
          for (var k=0; k<this.session.histories.length; k++) {
            if (report.uid == this.session.histories[k].uid) {
              latestHistory = this.session.histories[k]
            }
            report = latestHistory
          }
        }
        this.currentReport = report
        this.isReportDialogOpen = true
      },

      showInfo(message) {
        this.message = message
        this.showMessage = !this.showMessage
      },

      saveSession () {
        this.$store.dispatch('updateSession', this.session)
        this.showInfo('Session successfully updated.')
      },

    },

    computed: {

      session() {
        return this.$store.state.session
      },

      snapshots () {
        var shots = []
        for (var k=0; k<this.cohort.reports.length; k++) {
          if (this.cohort.reports[k].type == 'snapshot') {
            shots.push(this.cohort.reports[k])
          }
        }
        return shots
      },

      histories () {
        var hists = []
        for (var k=0; k<this.cohort.reports.length; k++) {
          if (this.cohort.reports[k].type == 'history') {
            hists.push(this.cohort.reports[k])
          }
        }
        return hists
      },

      snapshot () {
        return this.$store.state.snapshot
      },

      cohorts () {
        return this.$store.state.cohorts
      },

      cohort () {
        if (this.session.cohortId) {
          for (var k=0; k<this.cohorts.length; k++) {
            if (this.session.cohortId == this.cohorts[k]._id) {
              return this.cohorts[k]
            }
          }
        }
        return {reports:[]}
      },
    },

    mounted() {
      this.$store.dispatch('getSession', this.id)
      this.$store.dispatch('getCohorts')
    }
  }

</script>

<style scoped>
.container {
  padding-top: 85px;
}
.icon {
  margin-right: 15px
}
.list__tile:hover {
    background-color: #efefef !important;
}
</style>
