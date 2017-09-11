<template>
  <v-container>

    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card>
          <v-card-title>
            <v-breadcrumbs  icons divider="forward" class='pa-0 ma-0'>
              <v-breadcrumbs-item href='#/'>
                Home
              </v-breadcrumbs-item>
              <v-breadcrumbs-item href='/#/cohorts'>
                Cohort List
              </v-breadcrumbs-item>
              <v-breadcrumbs-item href='/#' class='brighten'>
                {{cohort.name}} Cohort
              </v-breadcrumbs-item>
            </v-breadcrumbs>
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
    <br/>

    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-1'>
          <v-card-title class=''>
            <v-subheader>
              Cohort Details
            </v-subheader>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="elevation-0">
            <v-layout row wrap>
              <v-flex lg6 xs12>
                <v-text-field
                  @keyup='submit'
                  label='Name' v-model='cohort.name'></v-text-field>
                <v-text-field
                       @keyup='submit'
                       label='Description'
                       v-model='cohort.description'>
                </v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions class='actions-panel'>
            <v-spacer></v-spacer>
            <v-btn error flat @click.native='showDelete=true'>Delete</v-btn>
            <v-btn flat primary @click.native='updateDetails'>Update</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    <br/>

    <v-layout>
    <v-flex xs12 lg8 offset-lg2>
      <v-card class='elevation-1'>
        <v-card>
          <v-card-title class=''>
            <v-subheader>
            Reports
            </v-subheader>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text v-if='this.cohort.reports.length>0'>

            <v-list two-line>
              <template v-for='(report,k) in cohort.reports'>
                <v-list-tile avatar v-bind:key="report.name"
                       :to="{name: 'Report', params:{id: id, reportId: k}}">
                  <v-list-tile-avatar>
                    <v-icon
                       v-if="report.type=='snapshot'"
                       class='red--text text--darken-3'>fa-line-chart</v-icon>
                     <v-icon
                       v-else
                       class='blue--text text--darken-3'>fa-history</v-icon>
                  </v-list-tile-avatar>
                  <v-list-tile-content>
                    <v-list-tile-title v-html="report.name"></v-list-tile-title>
                    <v-list-tile-sub-title v-html='report.description'>
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider v-if='k<cohort.reports.length-1'></v-divider>
              </template>
            </v-list>
          </v-card-text>
          <v-card-text v-else>
            <h6 class='blue--text text--darken-2'>
              No Reports Available.
            </h6>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions class='actions-panel'>
            <v-spacer></v-spacer>
            <v-btn primary @click.native='createReport'>Create Report</v-btn>
          </v-card-actions>
        </v-card>

      </v-card>
    </v-flex>
  </v-layout>
  <v-snackbar v-model='showMessage' :top=true primary>{{message}}</v-snackbar>
  <v-dialog v-model='showDelete' persistent>
    <v-card>
      <v-card-title class='red white--text text--lighten-2'>
        Are You Certain?
      </v-card-title>
      <v-card-text>
        Are you are sure you want to delete this cohort? This will delete all
        reports and fields; it cannot be undone.
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn @click.native='showDelete=false'>Cancel</v-btn>
        <v-spacer></v-spacer>
        <v-btn error flat @click.native='deleteCohort'>Delete</v-btn>
      </v-card-actions>
    </v-card>

  </v-dialog>
  </v-container>

</template>

<script>
// import Component from "../component_location"

  export default {
    components: {},
    props: ['id'],

    data () {
      return {
        showDelete: false,
        reportHeaders: [{text: 'Report', value:'name', align: 'left'}],
        showMessage: false,
        message: '',
        showDetails: true
      }
    },

    methods: {

      submit (keyEvent) {
        if (keyEvent.keyCode == 13) {
          this.updateDetails()
        }
      },

      deleteCohort() {
        this.$store.dispatch('deleteCohort', this.id)
      },

      updateDetails () {
        var cohort = {name: this.cohort.name,
          description: this.cohort.description,
          _id: this.cohort._id}
        var self = this
        this.$store.dispatch('updateCohort', cohort).then(function(){
          self.message = 'Cohort successfully updated.'
          self.showMessage = true
        })
      },

      createReport() {
        var self = this
        var newReport = this.$store.state.report
        newReport.uid = guid()
        this.cohort.reports.push(newReport)
        this.$store.dispatch('updateCohort', this.cohort).then(function() {
          self.$router.push({name: 'Report',
            params: {id: self.cohort._id, reportId: self.cohort.reports.length-1}})
        })
      }

    },

    computed: {

      cohort() {
        return this.$store.state.cohort
      }

    },

    mounted() {
      this.$store.dispatch('getCohort', this.id)
    }
  }

</script>

<style scoped>

.container {
  padding-top: 85px;;
}
.header {
  background-color: #305580;
  font-size: 16px;
}
.actions-panel {
}
.icon {
  margin-right: 15px;
}
</style>
