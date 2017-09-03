<template>
  <v-layout>
    <v-flex xs3>
      {{Math.round(samplingRate)}} | {{Math.round(boardTime)}}

      <v-layout>
        <v-flex>
          <v-slider
            :disabled='autoScale'
            label="Max"
            max="2500"
            min='0'
            v-model="topScale">
          </v-slider>
        </v-flex>
      </v-layout>

      <v-layout>
        <v-flex>
          <v-slider
            :disabled='autoScale'
            label="MIN"
            max="2500"
            min='0'
            v-model="botScale">
          </v-slider>
        </v-flex>
      </v-layout>

      <v-layout>
        <v-flex>
          <v-slider
            label="TIME"
            max="20"
            min='0'
            v-model="speedScale">
          </v-slider>
        </v-flex>
      </v-layout>

      <v-layout>
        <v-flex>
          <v-checkbox
            color='primary'
            v-model='autoScale'
            label='Autoscale'>
          </v-checkbox>
       </v-flex>
      </v-layout>

    </v-flex>
  <v-flex xs12 id='data'>
    <canvas id='chart' height="300"></canvas>
  </v-flex>
  </v-layout>
</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: {
    },

    data () {
      return {
        intervalId: null,
        chart: null,
        sampleBuffer: [],
        timeBuffer: [],
        samplingRate: 0,
        timeSeries: null,
        topScale: 750,
        botScale: 0,
        speedScale: 4,
        weightedMean: 0,
        weightedVar: 0,
        alphaDecay: 0.005,
        autoScale: true,
        boardTime: 0,
        leaveTime: 0,
        maxTime: 0
      }
    },

    methods: {

      resize () {
        // What a hack! Need slight delay to find correct width of chart.
        var y = $('#data').width()
        $('#chart').attr('width', y)
      },

      updateBuffer (dataPackage) {
        // Update sampling rate.
        dataPackage = JSON.parse(dataPackage)
        this.timeSeries.append(new Date().getTime(), dataPackage[3])
      },

      simpleUpdate () {
        var sample = this.sampleBuffer.shift()
        if (sample) {
          this.timeSeries.append(new Date().getTime(), sample)
        }
        setTimeout(this.simpleUpdate, 20)
      },

      updateChart () {
        var elapsedTime = new Date().getTime() - this.startTime
        var ratio = Math.round(elapsedTime/this.deltaT)
        console.log(elapsedTime)
        var sample
        for (var k=0; k<Math.ceil(ratio); k++) {
          sample = this.sampleBuffer.shift()
        }
        this.startTime = new Date().getTime()
        if (sample) {
          this.timeSeries.append(new Date().getTime(), sample)
          this.boardTime = this.timeBuffer.shift()
          this.weightedMean = (1 - this.alphaDecay) * this.weightedMean
            + this.alphaDecay * sample
          this.weightedVar = (1 - this.alphaDecay) * (this.weightedVar
            + this.alphaDecay * (sample - this.weightedMean)**2)
          var std = Math.sqrt(this.weightedVar)
          var minVal = this.weightedMean - 2*std
          var maxVal = this.weightedMean + 6*std
          if (this.autoScale) {
            this.topScale = 1000*maxVal
            this.botScale = 1000*minVal
          }
          setTimeout(this.updateChart, 20)
        }
      }
    },

    watch: {

      topScale () {
        this.chart.options.maxValue = this.maxScale
      },

      botScale () {
        this.chart.options.minValue = this.minScale
      },

      speedScale () {
        this.chart.options.millisPerPixel = this.pixScale
      }

    },

    computed: {

      maxScale () {
        return this.topScale / 1000
      },

      minScale () {
        return this.botScale / 1000
      },

      pixScale () {
        return this.speedScale
      }

    },

    mounted () {

      // CREATE THE SMOOTHIE-CHART!
      var options = {}
      options.interpolation = 'linear'
      options.scaleSmoothing = 0.040
      options.maxValue = this.maxScale
      options.minValue = this.minScale
      options.millisPerPixel = this.pixScale
      options.grid = {
        linewidth: 1,
        verticalSections: 4,
        fillStyle: '#fefefe',
      }
      options.labels = {
        fillStyle: '#000000',
        fontSize: 18}
      this.chart = new SmoothieChart(options)
      this.chart.streamTo(document.getElementById('chart'), 1000)

      // Let's update the size of the graph if windows resize...
      $( window ).resize(function() {
        var y = $('#data').width()
        $('#chart').attr('width',y)
      })
      setTimeout(this.resize, 200)

      // Define series options.
      var seriesOptions = {}
      seriesOptions.strokeStyle = '#c62828'
      seriesOptions.lineWidth = 3
      seriesOptions.fillStyle = 'rgba(0,0,35,0.1)'
      seriesOptions.opacity = 0.2

      this.timeSeries = new TimeSeries()
      this.chart.addTimeSeries(this.timeSeries, seriesOptions)
      this.$store.dispatch('establishSocketConnection')
      this.$store.state.socket.on('data_package', this.updateBuffer)
    }
  }

</script>

<style>

</style>
