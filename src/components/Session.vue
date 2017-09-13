<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        <span class='human-id'>{{session.hid}}</span>

        <v-spacer></v-spacer>
        <v-btn primary flat download :to="{name:'Download', params:{id:id}}">
          <v-icon left>file_download</v-icon>
          Download Data
        </v-btn>

        <v-btn
          @click.native='annotate'
          primary large
          class='white--text primary'>
          <v-icon class='white--text' left >
            comment
          </v-icon>
          Add Annotation
        </v-btn>

        <v-btn
          v-if='!isRecording'
          @click.native='toggleRecord'
          primary large
          class='white--text primary'>
          <v-icon class='white--text' left>fiber_manual_record</v-icon>
          Record
        </v-btn>
        <v-btn
          v-else
          @click.native='toggleRecord'
          primary large
          class='white--text red darken-3'>
          <v-icon class='white--text' left>pause</v-icon>
          Pause
        </v-btn>
      </v-card-title>
    </v-card>
    <br/>

    <div v-for='channel in availableChannels' :key='channel'>
    <v-card>
      <v-card-text >
        <smart-chart :channelNumber='channel'>
        </smart-chart>
      </v-card-text>
    </v-card>
    </br>
    </div>

  </v-container>
</template>

<script>

import Chart from "./Chart.vue"
import ChartX from "./ChartX.vue"
import SmartChart from "./SmartChart.vue"

export default {

  components: {Chart, ChartX, SmartChart},

  props: ['id'],

  data () {

    return {
      availableChannels: [0, 1],
      isRecording: false,
      activeChannel: '0'
    }
  },

  methods: {

    annotate () {
      this.$router.push({'name': 'Annotate', params: {id: this.id}})
    },

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
    },

    updateControls (status) {
      this.isRecording = status.isRecording
    },

    getStatus () {
      this.$store.state.socket.emit('requestStatus')
    }

  },

  computed: {

    session () {
      return this.$store.state.session
    },

  },

  mounted () {
    this.$store.dispatch('getSession', this.id)
    this.$store.state.socket.on('status', this.updateControls)
    setTimeout(this.getStatus, 800)
  }
}

</script>

<style scoped>
html, body, main, .container {
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
