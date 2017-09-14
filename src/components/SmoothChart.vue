<template>
<div v-bind:id='canvasID'>
    Hello
</div>
</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: ['channelNumber'],

    data () {
      return {

        sampleBuffer: [],
        streaming: false,
        bufferLength: 0,

      }
    },

    methods: {

      dataReceived (samples) {
        console.log(this.sampleBuffer.length)
        this.sampleBuffer = this.sampleBuffer.concat(samples)
        if (!this.streaming) {
          this.buildChart([])
          this.streaming = true
          this.flowChart()
        }
      },

      flowChart () {
        var chunkSize = Math.min(2, this.sampleBuffer.length)
        var dt = 40 * chunkSize
        var chunks = []
        if (chunkSize > 0) {
          for (var k=0; k<chunkSize; k++) {
            var d = this.sampleBuffer.shift()
            chunks.push(d)
          }
          this.bufferLength += chunks.length
          if (this.bufferLength > 50) {
            var shift = 1
          } else {
            var shift = 0
          }
          this.chart.flow({
              json: chunks,
              keys: {
                value: ['y']
              },
              duration: 10,
              length: shift,
              done: this.flowChart
          })
        }
      },

      buildChart (samples) {
        this.chart = c3.generate({
          bindto: '#canvas-0',
          data: {
            json: samples,
            keys: {
              value: ['y']
            },
            type: 'area-spline'
          },
        })
      },

      channelName () {
        if (this.channelNumber == 0) {
          return 'PZT'
        } else {
          return 'PPG'
        }
      },

      registerListeners () {
        if (this.channelName == 'PPG') {
          this.$store.state.socket.on('ppg', this.dataReceived)
        } else {
          this.$store.state.socket.on('pzt', this.dataReceived)
        }
      }

    },

    computed: {

      canvasID () {
        return ('canvas-' + this.channelNumber)
      },

    },

    mounted () {

      setTimeout(this.registerListeners, 2000)

    }
  }

</script>

<style>

</style>
