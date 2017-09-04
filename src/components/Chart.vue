<template>
  <v-layout>
    <v-flex xs5>

      <v-layout>
        <v-flex>
          <v-slider
            :disabled='autoScale'
            label="Max"
            max="25000"
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
            max="25000"
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
        <v-flex xs7>
          <!-- <v-btn -->
          <!--   primary -->
          <!--   @click.native='autoScale=true; autoScaleIterations=0'> -->
          <!--   AutoScale -->
          <!-- </v-btn> -->
          <v-checkbox
            color='primary'
            v-model='autoScale'
            label='Autoscale'>
          </v-checkbox>
       </v-flex>
       <v-flex xs4>
         <v-btn icon class='mt-3' @click.native='openConfig = true'>
           <v-icon>settings</v-icon>
         </v-btn>
       </v-flex>
      </v-layout>

    </v-flex>
  <v-flex xs12 id='data'>
    <canvas id='chart' height="275"></canvas>
  </v-flex>


  <v-dialog
    width='500px'
    v-model='openConfig'
    persistent>
    <v-card>
      <v-card-title>
        <v-subheader>
        AutoScale Options
        </v-subheader>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-layout>
          <v-flex xs4 class='input-group'>
            <label>Smoothing</label>
          </v-flex>
          <v-flex xs6>
            <v-slider
              max='300'
              min='0'
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
              max='1000'
              min='10'
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
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn flat primary @click.native='openConfig=false'>
          Close
        </v-btn>
      </v-card-actions>j
    </v-card>

  </v-dialog>


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
        autoScale: false,
        autoScaleIterations: 0,
        boardTime: 0,
        leaveTime: 0,
        maxTime: 0,
        plotFiltered: true,
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
        var currentTime = new Date().getTime()
        var sample = dataPackage[1]
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
            if ( (currentTime - this.autoScaleTime) > this.autoScaleInterval) {
              this.topScale = 10000*maxVal
              this.botScale = 10000*minVal
              this.autoScaleTime = new Date().getTime()
            }
          }
        }
      },
    },

    watch: {

      topScale () {
        this.chart.options.maxValue = this.topScale / 10000
      },

      botScale () {
        this.chart.options.minValue = this.botScale / 10000
      },

      speedScale () {
        this.chart.options.millisPerPixel = this.speedScale
      }

    },

    computed: {

        alphaDecay () {
            return Math.pow(10, -this.scaleSensitivity/100)
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
      this.chart.streamTo(document.getElementById('chart'), 1000)

      // Let's update the size of the graph if windows resize...
      $( window ).resize(function() {
        var y = $('#data').width()
        $('#chart').attr('width',y)
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
      this.$store.state.socket.on('data_package', this.updateBuffer)
    }
  }

</script>

<style>
html, body, main {
  overflow: hidden
}
</style>
