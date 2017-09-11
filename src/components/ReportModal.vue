<template>
  <v-container>
    <v-dialog v-model='isOpen' persistent width='500px'>

      <!-- TITLE CARD -->
      <v-card>
        <v-card-title>
          <v-icon
            v-if="localReport.type=='snapshot'"
            class='red--text text--darken-4'
            small>
            fa-line-chart
          </v-icon>
          <v-icon
            v-else
            class='blue--text text--darken-4'>
            fa-history
          </v-icon>
          <v-subheader>
            {{localReport.name}}
          </v-subheader>
          <v-spacer></v-spacer>
          <v-btn
            icon
            @click.native='$emit("close")'>
            <v-icon>
              cancel
            </v-icon>
          </v-btn>
        </v-card-title>
      </v-card>
      </br>

      <!-- DATE/TIME CARD -->
      <v-card v-if="localReport.type=='snapshot'">
        <v-card-title>
          <v-subheader>
            {{localReport.timestamp}}
          </v-subheader>
          <v-spacer></v-spacer>
          <v-btn primary flat @click.native='setTime'>
            <v-icon small primary class='no-shift'>timer</v-icon>
          </v-btn>
        </v-card-title>
      </v-card>
      <br v-if='localReport.type=="snapshot"'/>

      <!-- FIELDS CARD -->
      <v-card>
        <v-card-text>
          <v-layout v-for='(field, k) in localReport.fields' row :key='k'>
            <!-- Boolean Input -->
            <template v-if='field.type=="boolean"'>
              <v-flex xs5 v-if='field.type=="boolean"'>
                <v-checkbox
                  color='primary' v-bind:label='field.name'
                  v-model='field.value'
                  :hint='field.description' persistent-hint>
                </v-checkbox>
              </v-flex>
              <v-flex xs7 v-if='field.includeDetails'>
                <v-text-field
                  v-model='field.details'
                  label='Details'
                  :disabled='!field.value'>
                </v-text-field>
              </v-flex>
            </template>

            <!-- NUMERIC Input -->
            <template v-if="field.type=='numeric'">
              <v-flex xs12>
                <v-text-field
                  v-model='field.value'
                  v-bind:label='field.name'
                  :hint='field.description + " [" + field.units + "]"'
                  persistent-hint>
                </v-text-field>
              </v-flex>
            </template>

            <!-- TEXT Input -->
            <template v-if="field.type=='text'">
              <v-flex xs12>
                <v-text-field
                  v-model='field.value'
                  v-bind:label='field.name'
                  :hint='field.description'
                  persistent-hint>
                </v-text-field>
              </v-flex>
            </template>
          </v-layout>
        </v-card-text>
        <v-divider></v-divider>

        <!-- ACTIONS -->
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn small flat @click.native='$emit("close")'>Cancel</v-btn>
          <v-btn primary
            @click.native="$emit('submit', localReport); $emit('close')">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>

    </v-dialog>

  </v-container>
</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: ['report', 'isOpen'],

    watch: {
      isOpen () {
        this.setReport()
      }
    },

    data () {
      return {
        localReport: {}
      }
    },

    methods: {

      setTime () {
        this.localReport.timestamp = moment().format('YYYY MMMM D | h:mm:ss a')
        this.localReport.unixTime = moment.now()
      },

      setReport () {
        if (!this.report.timestamp) {
          this.report.timestamp = ''
          this.report.unixTime = ''
        }
        this.localReport = JSON.parse(JSON.stringify(this.report))
        if (this.report.timestamp == '') {
          this.setTime()
        }
      }

    },

    computed: {
    },

    mounted () {

    }

  }

</script>

<style>

</style>
