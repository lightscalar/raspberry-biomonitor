<template>

  <v-container>

    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-breadcrumbs  icons divider="forward" class='pa-0 ma-0'>
              <v-breadcrumbs-item href='/#'>
                Home
              </v-breadcrumbs-item>
              <v-breadcrumbs-item :to="{name: 'Cohorts'}" class='white--text'>
                Cohort List
              </v-breadcrumbs-item>
              <v-breadcrumbs-item :href='cohortUrl'>
                {{cohort.name}} Cohort
              </v-breadcrumbs-item>
              <v-breadcrumbs-item class='brighten'>
                {{report.name}} Report
              </v-breadcrumbs-item>
            </v-breadcrumbs>
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
    <br/>

    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>

          <v-card-title class=''>
            <v-subheader>
              Report Details
            </v-subheader>
          </v-card-title>

          <v-divider></v-divider>
          <v-card-text class="elevation-0">
            <v-layout row wrap>
              <v-flex lg6 xs12>
                <v-text-field
                  @submit='updateDetails'
                  @keyup = 'submit'
                  label='Report Name'
                  v-model='report.name'>
                </v-text-field>
              </v-flex>
              <v-radio-group v-model='report.type'>
                <v-layout row wrap>
                  <v-flex xs-6>
                <v-radio
                       color='primary'
                       @change = 'updateDetails'
                       label="Snapshot"
                       value="snapshot">
                </v-radio>
                  </v-flex>
                  <v-flex xs-6>
                <v-radio
                       @change = 'updateDetails'
                       color='primary'
                       label="History"
                       value="history">
                </v-radio>
                  </v-flex>
                </v-layout>
              </v-radio-group>
            </v-layout>
            <v-layout row wrap>
              <v-flex lg6 xs12>
                <v-text-field
                   @keyup = 'submit'
                   label='Report Description'
                   v-model='report.description'>
                </v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions class='actions-panel'>
            <v-spacer></v-spacer>
            <v-btn small error flat @click.native='confirmDelete=true'>
              Delete
            </v-btn>
            <v-btn flat small primary @click.native='updateDetails'>
              Update
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    <br/>


    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card>
          <v-card-title class=''>
            <v-subheader>
              Fields
            </v-subheader>
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text v-if='report.fields.length>0'>
            <v-list two-line>
              <template v-for='(field,k) in report.fields'>
                <v-list-tile
                       @drop='onDrag'
                       avatar v-bind:key="field.name"
                       @click.native='openField(field)'>
                  <v-list-tile-avatar>
                    <v-icon small class='blue--text text--darken-3'
                      v-if="field.type=='boolean'">
                      check_box
                    </v-icon>
                    <v-icon class='blue--text text--darken-3'
                      v-if="field.type=='numeric'">
                      fa-calculator
                    </v-icon>
                    <v-icon class='blue--text text--darken-3'
                      v-if="field.type=='text'">
                      fa-comment
                    </v-icon>
                  </v-list-tile-avatar>
                  <v-list-tile-content>
                    <v-list-tile-title
                      v-html="field.name">
                    </v-list-tile-title>
                    <v-list-tile-sub-title
                      v-html='field.description'>
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
                <v-divider v-if='k<report.fields.length-1'></v-divider>
              </template>
            </v-list>

          </v-card-text>
          <v-card-text v-else>
            <h6 class='blue--text text--darken-2'>
              Report contains no fields.
            </h6>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions class='actions-panel'>
            <v-spacer></v-spacer>
            <v-btn primary @click.native='addField'>Add Field</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>


    <v-snackbar v-model='showMessage' :top=true primary>{{message}}</v-snackbar>

    <v-dialog v-model='editField' persistent width='450px'>
      <v-card>
        <v-card-text>

          <v-text-field
            v-model='field.name'
            label='Field Name'>
          </v-text-field>
          <v-text-field
            v-model='field.description'
            label='Field Description'>
          </v-text-field>
          <v-radio-group v-model='field.type'>
          <v-layout row wrap>
            <v-flex lg4>
              <v-radio
                 value='numeric'
                 color='primary'
                 label='Numeric'>
              </v-radio>
            </v-flex>
            <v-flex lg4>
              <v-radio
                value='text'
                color='primary'
                label='Text'>
              </v-radio>
            </v-flex>
            <v-flex lg4>
              <v-radio
               value='boolean'
               color='primary'
               label='Boolean'>
              </v-radio>
            </v-flex>
          </v-layout>
          </v-radio-group>
          <v-layout row wrap>

          </v-layout>
          <v-layout row wrap>

            <v-flex lg6>
              <v-text-field
                       label='Define Units'
                       v-model='field.units'
                       :disabled="field.type != 'numeric'">
              </v-text-field>
            </v-flex>

            <v-flex lg6>
              <v-checkbox
                       label='Allow Details?'
                       color='primary'
                       v-model='field.includeDetails'
                       :disabled="field.type != 'boolean'">
              </v-checkbox>
            </v-flex>

          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-btn error flat
                       @click.native='editField=!editField;deleteCurrentField()'>
            Delete
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn flat small @click.native='editField=!editField'>Cancel</v-btn>
          <v-btn primary
                       @click.native='editField=!editField; updateDetails()'>Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model='confirmDelete' persistent>
      <v-card>
        <v-card-title class='red white--text text--lighten-2'>
          Are You Certain?
        </v-card-title>
        <v-card-text>
          Are you are sure you want to delete this report? This cannot be
          undone.
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn @click.native='confirmDelete=false'>Cancel</v-btn>
          <v-spacer></v-spacer>
          <v-btn error flat @click.native='deleteReport'>Delete</v-btn>
        </v-card-actions>
      </v-card>
  </v-dialog>

  </v-container>

</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: ['id', 'reportId'],

    data () {
      return {
        confirmDelete: false,
        open: true,
        message: '',
        showMessage: false,
        editField: false,
        field: {name: '', isBoolean: true, includeDetails: false,
          includeUnits: false, units:''}
      }
    },

    methods: {

      onDrag (dragEvent) {
        console.log(dragEvent)
      },

      submit (keyEvent) {
        if (keyEvent.keyCode == 13) {
          this.updateDetails()
        }
      },

      deleteReport() {
        var self = this
        this.cohort.reports.splice(this.reportId,1)
        this.$store.dispatch('updateCohort', this.cohort).then(function() {
          self.$router.push({name: 'Cohort', params: {'id': self.cohort._id}})
        })
      },

      updateDetails() {
        var self = this
        this.$store.dispatch('updateCohort', this.cohort).then(function(){
          self.message = 'Report successfully updated.'
          self.showMessage = true
        })
      },

      deleteCurrentField() {
        for (var k=0; k<this.report.fields.length; k++) {
          if (this.field.name == this.report.fields[k].name) {
            this.report.fields.splice(k,1)
          }
        }
        this.updateDetails()
      },

      addField() {
        var field = this.$store.state.field
        field.value = ''
        field.details = ''
        field.uid = guid()
        this.report.fields.push(field)
        this.field = field
        this.editField = true
        this.$store.commit('resetField')
      },

      openField(field) {
        console.log('Opening Dialog.')
        this.editField = true
        this.field = field
      }
    },

    computed: {

      cohortUrl () {
        return '#/cohort/' + this.id
      },

      cohort () {
        return this.$store.state.cohort
      },

      report () {
        var reports = this.$store.state.cohort.reports
        if (!reports) {return {fields:[]}}
        if (reports.length>0) {
          return reports[this.reportId]
        } else {
          return {fields: []}
        }
      }

    },

    mounted() {
      this.$store.dispatch('getCohort', this.id)
    }
  }

</script>

<style scoped>

.container {
  padding-top: 85px;
}
.header {
  background-color: #305580 !important;
  font-size: 16px;
}
.icon {
  margin-right: 15px
}
.side-icon {
  color: #305580 !important
}
</style>
