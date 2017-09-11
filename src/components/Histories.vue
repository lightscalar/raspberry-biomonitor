<template>

  <v-container>

    <!-- NAV CARD -->
    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-breadcrumbs  icons divider="forward" class='pa-0 ma-0'>
              <v-breadcrumbs-item href="#/">
                Home
              </v-breadcrumbs-item>
              <v-breadcrumbs-item :href="'#/session/' + session._id">
                {{session.hid}}
              </v-breadcrumbs-item>
              <v-breadcrumbs-item>
                Histories
              </v-breadcrumbs-item>
            </v-breadcrumbs>
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
    <br/>

    <v-layout
      v-if='session.histories.length>0'
      v-for='(history, k) in histories'
      :key='k'>

      <!-- HISTORY CARD -->
      <v-flex xs12 lg8 offset-lg2>
        <v-card>
          <v-card-title>
            <v-subheader class='blue--text text--darken-3'>
              {{history.name}}
            </v-subheader>
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text>
            <field-table :fields='history.fields'>
            </field-table>
          </v-card-text>

          <!-- CARD ACTIONS -->
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              small flat error
              @click.native='showDelete=true; index=k'>
              Delete
            </v-btn>
            <v-btn
              small flat primary
              @click.native='editEvent(k)'>
              Edit
            </v-btn>
          </v-card-actions>
        </v-card>
        <br/>
      </v-flex>
    </v-layout>

    <v-layout v-if='histories.length==0'>
      <v-flex lg6 offset-lg3 xs12>
        <h4
          class='text-xs-center white--text'>
          No Patient Histories for this Session.
        </h4>
      </v-flex>
    </v-layout>

    <report-modal
      @close='isReportDialogOpen=false'
      @submit='saveReport'
      :report='currentReport'
      :isOpen='isReportDialogOpen'>
    </report-modal>

    <confirm-modal
      @confirm='deleteHistory'
      :isOpen='showDelete'
      @cancel='showDelete=false'
      :message='deleteMessage'>
    </confirm-modal>

  </v-container>

</template>

<script>
  import ReportModal from "./ReportModal"
  import ConfirmModal from "./ConfirmModal"
  import Messenger from "./Messenger"
  import FieldTable from "./FieldTable"

  export default {

    components: {ReportModal, ConfirmModal, Messenger, FieldTable},

    props: ['id'],

    data () {
      return {
        index: null,
        isReportDialogOpen: false,
        currentReport: {},
        showDelete: false,
        deleteMessage: 'Do you want to delete this patient history?'
      }
    },

    methods: {

      editEvent (k) {
        this.index = k
        this.currentReport = this.histories[k]
        this.isReportDialogOpen = true
      },

      addHistory (history, histories) {
        for (var k=0; k< histories.length; k++) {
          if (history.uid == histories[k].uid) {
            histories.splice(k, 1, history)
            return histories
          }
        }
        histories.push(history)
        return histories
      },

      saveReport (report) {
        this.session.histories[report.index] = report
        this.saveSession()
      },

      saveSession () {
        this.$store.dispatch('updateSession', this.session)
      },

      deleteHistory () {
        var histories = []
        var targetUid = this.histories[this.index].uid
        for (var k=0; k<this.session.histories.length; k++) {
          var history = this.session.histories.shift()
          if (history.uid != targetUid) {
            history.push(history)
          }
          for (var k=0; k<histories.length; k++) {
            this.session.histories.push(histories[k])
          }
        }
        this.showDelete = false
        this.saveSession()
      }

    },

    computed: {

      session () {
        return this.$store.state.session
      },

      histories () {
        var histories = []
        for (var k=0; k<this.session.histories.length; k++) {
          var history = this.session.histories[k]
          history.index = k
          this.addHistory(history, histories)
        }
        return histories
      }

    },

    mounted () {
      this.$store.dispatch('getSession', this.id)
    }
  }

</script>

<style scoped>

.container {
  padding-top: 85px;
}
.icon {
  margin-right: 15px;
}
.subheader {
  color: #305580 !important;
}
p {
  margin-top: 8px;
  border: 1px solid #cfcfcf;;
  padding: 5px;
  background-color: white;
}
.boolbar {
}
</style>
