<template>
  <canvas id='chart' height="300"></canvas>
</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {

      }
    },

    methods: {

      resize () {
        // What a hack! Need slight delay to find correct width of chart.
        var y = $('#data').width()
        $('#chart').attr('width', y)
      }

    },

    computed: {

    },

    mounted () {

      // CREATE THE SMOOTHIE-CHART!
      var options = {}
      options.grid = {
        linewidth: 1,
        verticalSections: 4,
        millisPerPixel: 1,
        fillStyle: '#fefefe',
        scaleSmoothing: 0.005
      }
      options.labels = {
        fillStyle: '#000000',
        fontSize: 18}
      var chart = new SmoothieChart(options)
      chart.streamTo(document.getElementById('chart'))

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

      var series = new TimeSeries()
      var value = 0
      setInterval( function () {
        value += 0.2 * (Math.random() - 0.5)
        series.append(new Date().getTime(), value )
      }, 10)
      chart.addTimeSeries(series, seriesOptions)
  }
}

</script>

<style>

</style>
