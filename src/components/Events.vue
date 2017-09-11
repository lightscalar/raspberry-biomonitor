<template>

  <v-container fluid>
    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-breadcrumbs  icons divider="forward" class='pa-0 ma-0'>
              <v-breadcrumbs-item href='#/'>
                Home
              </v-breadcrumbs-item>
              <v-breadcrumbs-item :href="'#/session/' + session._id">
                <span class='upper'>{{session.hid}}</span>
              </v-breadcrumbs-item>
              <v-breadcrumbs-item>
                Events
              </v-breadcrumbs-item>
            </v-breadcrumbs>
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
    <br/>

    <v-layout v-if='session.events.length>0' v-for='(event,k) in session.events' :key='k'>
    <v-flex xs12 lg8 offset-lg2>
      <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-subheader class='red--text text--darken-3'>
              {{event.name}}
            </v-subheader>
          </v-card-title>
          <v-divider></v-divider>

          <!-- DATE -->
          <v-card-text>
            <v-layout>
              <v-flex xs10 lg4>
                <v-subheader>{{event.timestamp}}</v-subheader>
              </v-flex>
            </v-layout>

            <field-table :fields='event.fields'>
            </field-table>

          </v-card-text>
          <v-divider></v-divider>

          <!-- CARD ACTIONS -->
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn small flat error @click.native='showDelete=true; index=k'>Delete</v-btn>
            <v-btn small flat primary @click.native='editEvent(k)'>Edit</v-btn>
          </v-card-actions>
        </v-card>
        <br/>
      </v-flex>
    </v-layout>

    <v-layout v-if='session.events.length==0'>
      <v-flex lg6 offset-lg3 xs12>
        <h4 class='text-xs-center white--text'>
          No Snapshots for this Session.
        </h4>
      </v-flex>
    </v-layout>

    <!-- EDIT EVENT -->
    <report-modal
      @close='isReportDialogOpen=false'
      @submit='saveReport'
      :report='currentReport'
      :isOpen='isReportDialogOpen'>
    </report-modal>

  <!-- DELETE DIALOG -->
    <confirm-modal
      @confirm='deleteEvent'
      :isOpen='showDelete'
      @cancel='showDelete=false'
      :message='deleteMessage'>
    </confirm-modal>

  </v-container>

</template>

<script>

  import ReportModal from "./ReportModal"
  import ConfirmModal from "./ConfirmModal"
  import FieldTable from "./FieldTable"

  export default {

    components: {ReportModal, ConfirmModal, FieldTable},

    props: ['id'],

    data () {
      return {
        isReportDialogOpen: false,
        fields: [],
        timestamp: null,
        currentReport: {},
        deleteMessage: 'Deleting this snapshot cannot be undone.',
        index: null,
        showDelete: false
      }
    },

    methods: {

      deleteEvent () {
        this.session.events.splice(this.index, 1)
        this.$store.dispatch('updateSession', this.session)
        this.showDelete = false
      },

      editEvent (k) {
        this.index = k
        this.currentReport = this.session.events[k]
        this.isReportDialogOpen = true
      },

      saveReport (report) {
        this.session.events.splice(this.index,1,report)
        this.saveSession()
      },

      saveSession () {
        this.$store.dispatch('updateSession', this.session)
        this.isReportDialogOpen = false
      }

    },

    computed: {

      session () {
        return this.$store.state.session
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
  margin-top: 15px;
}
.upper {
  text-transform: uppercase;
}
</style>
