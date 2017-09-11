<template>

  <v-dialog v-model='openDialog' persistent width='500px'>

    <!-- TITLE CARD -->
    <v-card>
      <v-card-title>
        <v-icon
          v-if="report.type=='snapshot'"
          small
          class='red--text text--darken-4'>
          fa-line-chart
        </v-icon>
        <v-subheader>
          {{report.name}}
        </v-subheader>
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click.native='openDialog=false'>
          <v-icon>cancel</v-icon>
        </v-btn>
      </v-card-title>
    </v-card>
    </br>

    <!-- DATE/TIME CARD -->
    <v-card>
      <v-card-title>
        <v-subheader>
          {{timestamp}}
        </v-subheader>
        <v-spacer></v-spacer>
        <v-btn primary flat @click.native='resetTime'>
          <v-icon small primary class='no-shift'>timer</v-icon>
        </v-btn>
      </v-card-title>
    </v-card>
    <br/>

    <!-- FIELDS CARD -->
    <v-card>
      <v-card-text>
        <v-layout v-for='(field, k) in report.fields' row :key='k'>
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
          <template v-else>
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
        <v-btn primary @click.native='submitReport'>
          Submit {{report.name}}</v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>

</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: ['report'],

    data () {
      return {
        openDialog: false,
      }
    },

    methods: {

    },

    computed: {

    },

    mounted () {

    }
  }

</script>

<style>

</style>
