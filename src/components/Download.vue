<template>
  <v-container fluid>

    <v-layout>
      <v-flex xs12 lg8 offset-lg2>
        <v-card class='elevation-0 banner'>
          <v-card-title>
            <v-breadcrumbs  icons divider="forward" class='pa-0 ma-0'>
              <v-breadcrumbs-item href="/#" class='white--text'>
                Home
              </v-breadcrumbs-item>
              <v-breadcrumbs-item
                :href="'#/session/'+session._id">
                <span class='upper'>{{session.hid}}</span>
              </v-breadcrumbs-item>
              <v-breadcrumbs-item>
                Data Download
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
          <v-card-text>

            <v-layout v-if='!isDataReady'>
              <v-flex xs1>
                <v-progress-circular
                  indeterminate
                  v-bind:size="50"
                  class="primary--text">
                </v-progress-circular>
              </v-flex>
              <v-flex xs8>
                <v-subheader>
                  Please wait. Compiling data.
                </v-subheader>
              </v-flex>
            </v-layout>

            <v-layout v-else>
              <v-flex xs8 offset-xs1>
                <v-btn primary :href='fileLocation'>
                  <v-icon left>file_download</v-icon>
                  Download Data
                </v-btn>
              </v-flex>
            </v-layout>

          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

  </v-container>

</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: ['id'],

    data () {
      return {
        isDataReady: false,
        fileLocation: null
      }
    },

    methods: {

      dataReady (fileLocation) {
        this.isDataReady=true
        this.fileLocation = fileLocation
      }

    },

    computed: {

      session () {
        return this.$store.state.session
      }

    },

    mounted () {
      this.$store.dispatch('getSession', this.id)
      this.$store.dispatch('establishSocketConnection')
      this.$store.state.socket.emit('downloadData', this.id)
      this.$store.state.socket.on('dataReady', this.dataReady)
    }
  }

</script>

<style scoped>
.container {
  padding-top: 85px;
}
.upper {
  text-transform: uppercase;
}

</style>
