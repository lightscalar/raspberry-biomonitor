<template>
  <v-layout>
    <v-flex xs4 class='pr-4'>
      <v-layout>
      <v-flex xs4>
        <h3 class='blue--text text--darken-3'>{{channelName}}</h3>
      </v-flex>
        <v-flex>
          <v-checkbox
            @change='setConfig'
            color='primary'
            v-model='autoScale'
            label='Autoscale'>
          </v-checkbox>
        </v-flex>
      </v-layout>
        <v-layout>
          <v-flex xs4 class='input-group'>
            <label>Smoothing</label>
          </v-flex>
          <v-flex xs6>
            <v-slider
              @input='setConfig'
               max='300'
               min='0'
               :disabled='!autoScale'
               step="1"
               v-model='scaleSensitivity'>
            </v-slider>
          </v-flex>
          <v-flex xs2 class='mt-3'>
            {{alphaDecay | formatNumber('%0.3f')}}
          </v-flex>
        </v-layout>
        <v-layout>
          <v-flex xs4 class='input-group'>
            <label>Deviations Above</label>
          </v-flex>
          <v-flex xs6>
            <v-slider
               @input='setConfig'
               max='1000'
               min='10'
               :disabled='!autoScale'
               step="1"
               v-model='stdAbove'>
            </v-slider>
          </v-flex>
          <v-flex xs2 class='mt-3'>
            {{ (stdAbove/100) | formatNumber('%0.2f')}}
          </v-flex>
        </v-layout>
        <v-layout>
          <v-flex xs4 class='input-group'>
            <label>Deviations Below</label>
          </v-flex>
          <v-flex xs6>
            <v-slider
               :disabled='!autoScale'
               @input='setConfig'
               max='1000'
               min='10'
               step="1"
               v-model='stdBelow'>
          </v-slider>
          </v-flex>
          <v-flex xs2 class='mt-3'>
            {{ (stdBelow/100) | formatNumber('%0.2f')}}
          </v-flex>
        </v-layout>

        <v-layout>
          <v-flex xs4 class='input-group'>
            <label>Time Scale</label>
          </v-flex>
          <v-flex xs6>
            <v-slider
               @input='setConfig'
               max='25'
               min='0'
               step="1"
               v-model='speedScale'>
            </v-slider>
          </v-flex>
          <v-flex xs2 class='mt-3'>
            {{speedScale | formatNumber('%0.3f')}}
          </v-flex>
        </v-layout>

    </v-flex>

    <v-flex xs8 v-bind:id='chartID'>
      <canvas v-bind:id='canvasID' height="350"></canvas>
    </v-flex>
  </v-layout>
</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: ['channelNumber'],

    data () {
      return {
        lastTime: 0,
        config: {},
        autoScaleTime: 0,
        autoScaleInterval: 500,
        stdAbove: 600,
        stdBelow: 200,
        openConfig: false,
        intervalId: null,
        chart: null,
        sampleBuffer: [],
        timeBuffer: [],
        samplingRate: 0,
        timeSeries: null,
        topScale: 7500,
        botScale: 0,
        speedScale: 4,
        weightedMean: 0,
        weightedVar: 0,
        scaleSensitivity: 200,
        autoScale: true,
        autoScaleIterations: 0,
        boardTime: 0,
        leaveTime: 0,
        maxTime: 0,
      }
    },

    methods: {

      retrieveConfig () {
        // HACK! Noat
        if (this.channelNumber == 0) {
          this.config = localStorage.getObj('pztConfig')
        } else {
          this.config = localStorage.getObj('ppgConfig')
        }
        if (this.config) {
          this.autoScale = this.config.autoScale
          this.scaleSensitivity = this.config.scaleSensitivity
          this.stdAbove = this.config.stdAbove
          this.stdBelow = this.config.stdBelow
          this.speedScale = this.config.speedScale
          this.topScale = this.config.topScale
          this.botScale = this.config.botScale
        }
      },

      setConfig () {
        if (this.channelNumber == 0) {
          var configName = 'pztConfig'
        } else {
          var configName = 'ppgConfig'
        }
        this.config.autoScale = this.autoScale
        this.config.scaleSensitivity = this.scaleSensitivity
        this.config.stdAbove = this.stdAbove
        this.config.stdBelow = this.stdBelow
        this.config.speedScale = this.speedScale
        this.config.topScale = this.topScale
        this.config.botScale = this.botScale
        localStorage.setObj(configName, this.config)
      },

      resize () {
        // What a hack! Need slight delay to find correct width of chart.
        var y = $('#' + this.chartID).width()
        $('#' +  this.canvasID).attr('width', y)
      },

      dataReceived (samples) {
        this.sampleBuffer = this.sampleBuffer.concat(samples)
        console.log(this.sampleBuffer.length)
      },

      updateBuffer () {
        // Update sampling rate.
        var now =  new Date().getTime()
        var deltaTime = (now - this.lastTime)
        console.log(deltaTime/10)
        var ratio = parseInt(Math.round(deltaTime/10))
        ratio = Math.max(ratio,5)
        var sample = this.sampleBuffer.shift()
        if (ratio == 2) {
          var sample = this.sampleBuffer.shift()
        }

        if (sample) {
          this.timeSeries.append(new Date().getTime(), sample)
          if (this.autoScale) {
            this.weightedMean = (1 - this.alphaDecay) * this.weightedMean
              + this.alphaDecay * sample
            this.weightedVar = (1 - this.alphaDecay) * (this.weightedVar
              + this.alphaDecay * (sample - this.weightedMean)**2)
            var std = Math.sqrt(this.weightedVar)
            var minVal = this.weightedMean - (this.stdBelow/100)*std
            var maxVal = this.weightedMean + (this.stdAbove/100)*std
            if ( (now - this.autoScaleTime) > this.autoScaleInterval) {
              this.topScale = maxVal
              this.botScale = minVal
              this.autoScaleTime = new Date().getTime()
              this.setConfig()
            }
          }
        }
        this.lastTime = new Date().getTime()
        setTimeout(this.updateBuffer, 10)
      },
    },

    watch: {

      topScale () {
        this.chart.options.maxValue = this.topScale
      },

      botScale () {
        this.chart.options.minValue = this.botScale
      },

      speedScale () {
        this.chart.options.millisPerPixel = this.speedScale
      }

    },

    computed: {

      alphaDecay () {
        return Math.pow(10, -this.scaleSensitivity/100)
      },

      chartID () {
        return ('channel-' + this.channelNumber)
      },

      canvasID () {
        return ('canvas-' + this.channelNumber)
      },

      channelName () {
        if (this.channelNumber == 0) {
          return 'PZT'
        } else {
          return 'PPG'
        }
      }
    },

    mounted () {

      // CREATE THE SMOOTHIE-CHART!
      var options = {}
      options.interpolation = 'linear'
      options.scaleSmoothing = 0.040
      options.maxValue = 2.5
      options.minValue = 0.0
      this.topScale = 2500
      this.botScale = 0
      options.millisPerPixel = this.speedScale
      options.grid = {
        linewidth: 1,
        verticalSections: 4,
        fillStyle: '#fefefe',
      }
      options.labels = {
        fillStyle: '#000000',
        fontSize: 18}
      this.chart = new SmoothieChart(options)
      this.chart.streamTo(document.getElementById(this.canvasID), 1000)

      // Let's update the size of the graph if windows resize...
      $( window ).resize(function() {
        var y = $('#' + this.chartID).width()
        $('#' +  this.canvasID).attr('width',y)
      })
      setTimeout(this.resize, 500)

      // Define series options.
      var seriesOptions = {}
      seriesOptions.strokeStyle = '#c62828'
      seriesOptions.lineWidth = 3
      seriesOptions.fillStyle = 'rgba(0,0,35,0.1)'
      seriesOptions.opacity = 0.2

      this.timeSeries = new TimeSeries()
      this.chart.addTimeSeries(this.timeSeries, seriesOptions)
      this.$store.dispatch('establishSocketConnection')
      this.$store.state.socket.on('disconnect', function() {console.log('Disconnected')})
      this.retrieveConfig()
      if (this.channelName == 'PPG') {
        this.$store.state.socket.on('ppg', this.dataReceived)
      } else {
        this.$store.state.socket.on('pzt', this.dataReceived)
      }
      this.updateBuffer()
      window.addEventListener('visibilityChange', function () {
        console.log('CHANGING VISIBILITY')
      })
    }
  }

</script>

<style scoped>
html, body, main, .container {
  overflow: hidden !important;
}
</style>
