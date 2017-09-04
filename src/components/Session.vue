<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        <span class='human-id'>{{session.hid}}</span>
        <v-spacer></v-spacer>
        <v-btn
          v-if='!isRecording'
          @click.native='toggleRecord'
          error large
          class='white--text red darken-3'>
          <v-icon class='white--text' left>fiber_manual_record</v-icon>
          Record
        </v-btn>
        <v-btn
          v-else
          @click.native='toggleRecord'
          primary large
          class='white--text'>
          <v-icon class='white--text' left>pause</v-icon>
          Pause
        </v-btn>
      </v-card-title>
    </v-card>
    <br/>

    <v-card>
      <v-card-text>
        <chart></chart>
      </v-card-text>
    </v-card>

  </v-container>
</template>

<script>

import Chart from "./Chart.vue"

export default {

  components: {Chart},

  props: ['id'],

  data () {

    return {

      isRecording: false,

    }
  },

  methods: {

    updateRate (rate) {
      this.samplingRate = rate
    },

    toggleRecord () {
      if (this.isRecording) {
        this.$store.state.socket.emit('stop_record')
      } else {
        this.$store.state.socket.emit('start_record', this.session._id)
      }
      this.isRecording = !this.isRecording
    }

  },

  computed: {

    session () {
      return this.$store.state.session
    }

  },

  mounted () {
    console.log('Mounted!')
    this.$store.dispatch('getSession', this.id)

  }
}

</script>

<style scoped>
html, body, main {
  overflow: hidden !important;
}

.container {
  padding-top: 85px;
}
.human-id {
  text-transform: uppercase;
  font-size: 40px;
  color: #c62828;
}

</style>
