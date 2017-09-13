<template>
  <v-card class='elevation-0'>
    <v-card-text style='height:330px'>
      <v-layout>
        <v-flex xs4>
          <h3 class='blue--text text--darken-3'>{{channelName}}</h3>
        <v-layout>
          <v-flex xs5>
            <v-text-field
              v-model='chartMin'
              label='Minimum'
              numeric>
            </v-text-field>
          </v-flex>
          <v-flex xs5 offset-xs1>
            <v-text-field
              v-model='chartMax'
              label='Maximum'
              numeric>
            </v-text-field>
          </v-flex>
        </v-layout>
        <v-layout>
          <v-flex xs5>
            <v-text-field
              v-model='maxChartPoints'
              label='Chart Width (samples)'
              @change='setConfig'
              numeric>
            </v-text-field>
          </v-flex>
        </v-layout>
          </v-flex>
        <v-flex xs8>
          <div style='display:block' v-bind:id='chartID'></div>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>

</template>

<script>
// import Component from "../component_location"

  export default {

    components: {},

    props: ['channelNumber'],

    watch: {

      chartMax () {
        this.adjustChart()
      },

      chartMin () {
        this.adjustChart()
      },

      tickInterval () {
        this.adjustChart()
      }

    },

    data () {
      return {

        sampleBuffer: [],
        chartData: [],
        lastUpdateTime: new Date().getTime(),
        maxChartPoints: 100,
        chartMax: 2.5,
        chartMin: 0,
        tickInterval: 1.0

      }

    },

    methods: {

      dataReceived (samples) {
        this.sampleBuffer = this.sampleBuffer.concat(samples)
        if (this.chartData.length == 0) {
          this.fillChart()
        }
      },

      adjustChart () {
        this.chart.options.axisY.minimum = this.chartMin
        this.chart.options.axisY.maximum = this.chartMax
        this.setConfig()
      },

      updateChart () {

        // Ensure we are updating at the appropriate rate.
        var now = new Date().getTime()
        var dt = (now - this.lastUpdateTime)
        var numberToInsert = Math.min(Math.round(dt/50), 15)
        for (var k=0; k<numberToInsert; k++) {
          var sample = this.sampleBuffer.shift()
          if (sample) {
            this.chartData.push(sample)
          }
        }
        while (this.chartData.length > this.maxChartPoints) {
          this.chartData.shift()
        }
        this.chart.render()
        this.lastUpdateTime = now
        setTimeout(this.updateChart, 50)
      },

      fillChart () {
        var numberPoints = Math.max(this.sampleBuffer.length, this.maxChartPoints)
        for (var k=0; k<numberPoints; k++) {
          var sample = this.sampleBuffer.shift()
          if (sample) {
            this.chartData.push(sample)
          }
        }
      },

      buildChart () {
        this.chart = new CanvasJS.Chart(this.chartID, {
          theme: 'theme1',
          height: 300,
          axisX: {
            gridColor: 'lightGray',
            gridThickness: 1,
            title: 'Elapsed Time (seconds)',
            titleFontFamily: 'Avenir Next',
            titleFontSize: 14,
            labelFontSize: 14,
            interval: this.tickInterval,
            intervalType: 'seconds'
          },
          axisY: {
            maximum: 2.5,
            minimum: 0,
            title: 'Amplitude (voltage)',
            titleFontFamily: 'Avenir Next',
            gridThickness: 1,
            titleFontSize: 14,
            labelFontSize: 14,
          },
          animationEnabled: true,
          data: [
            {
              type: "spline",
              lineColor: '#C62828',
              lineWidth: 2,
              color: '#C62828',
              dataPointWidth: 1,
              dataPoints: this.chartData
            }]
        })
        this.chart.render()

      },

      retrieveConfig () {
        // HACK!
        if (this.channelNumber == 0) {
          this.config = localStorage.getObj('pztConfig')
        } else {
          this.config = localStorage.getObj('ppgConfig')
        }
        if (this.config) {
          if (this.config.chartMax) {
            this.chartMax = this.config.chartMax
          }
        }
        if (this.config.chartMin) {
          this.chartMin = this.config.chartMin
        }
        if (this.config.maxChartPoints) {
          this.maxChartPoints = this.config.maxChartPoints
        }
        this.adjustChart()
      },

      setConfig () {
        if (this.channelNumber == 0) {
          var configName = 'pztConfig'
        } else {
          var configName = 'ppgConfig'
        }
        this.config = {}
        this.config.chartMax = this.chartMax
        this.config.chartMin = this.chartMin
        this.config.maxChartPoints = this.maxChartPoints
        localStorage.setObj(configName, this.config)
      },


      registerListeners () {
        if (this.channelName == 'PPG') {
          this.$store.state.socket.on('ppg', this.dataReceived)
        } else {
          this.$store.state.socket.on('pzt', this.dataReceived)
        }
        this.updateChart()
        this.retrieveConfig()
      }

    },

    computed: {

      chartID () {
        return ('channel-' + this.channelNumber)
      },

      channelName () {
        if (this.channelNumber == 0) {
          return 'PZT'
        } else {
          return 'PPG'
        }
      },

    },

    mounted () {
      setTimeout(this.buildChart, 300)
      setTimeout(this.registerListeners, 300)
      this.retrieveConfig()
    }
  }

</script>

<style>

</style>
