<template>
  <v-container>
    <v-card>
      <v-card-title>
        <span class='human-id'>{{session.hid}}</span>
        <v-spacer></v-spacer>
        <v-btn
          v-if='!isRecording'
          @click.native='toggleRecord'
          icon error large
          v-tooltip:top="{html: 'Start Recording'}"
          class='white--text red darken-3'>
          <!-- <v-icon>fiber_manual_record</v-icon> -->
        </v-btn>
        <v-btn
          v-else
          @click.native='toggleRecord'
          v-tooltip:top="{html: 'Pause Recording'}"
          icon primary large
          class='white--text'>
          <v-icon>pause</v-icon>
        </v-btn>
      </v-card-title>
    </v-card>
    <br/>

    <v-card>
      <v-card-text>
        <!-- <div id='data' style='display: block: height:400px'> -->
          <chart v-bind:max-scale='maxScale' @update-rate='updateRate'></chart>
        <!-- </div> -->
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
      samplingRate: 0,
      maxScale: 0.75

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
        this.$store.state.socket.emit('start_record')
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

.container {
  padding-top: 85px;
}
.human-id {
  text-transform: uppercase;
  font-size: 40px;
  color: #c62828;
}

</style>
