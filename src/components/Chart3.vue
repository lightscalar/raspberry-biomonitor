<template>
  <v-layout>
    <v-flex xs6 class='ma-3'>
      <v-card>
        <v-card-title>
          <h4 class='blue--text text--darken-3'>{{channelName}}</h4>
        </v-card-title>
        <v-card-text style='margin-top:-80px' v-if='dataAvailable'>
          <div v-bind:id='chartID'></div>
        </v-card-text>
        <v-card-text v-else>
          <v-layout>
            <v-flex xs2>
              <v-progress-circular
                indeterminate
                v-bind:size="50"
                class="primary--text">
              </v-progress-circular>
            </v-flex>
            <v-flex xs6>
              <h5 class='mt-2'>
                Buffering Data. One Moment.
              </h5>
            </v-flex>
          </v-layout>

        </v-card-text>
      </v-card>
    </v-flex>
    <v-flex xs6 class='ma-3'>
      <v-card>
        <v-card-text>

          <v-layout>
            <v-flex xs3>
              <v-text-field
                @change='scaleVerticalAxis'
                label='Maximum (V)' v-model='chartMax'>
              </v-text-field>
            </v-flex>
            <v-flex xs1 class='ml-5'>
              <v-btn icon outline class='mt-3' @click.native='maxUp'>
                <v-icon light>keyboard_arrow_up</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs2>
              <v-btn icon outline class='mt-3' @click.native='maxDown'>
                <v-icon light>keyboard_arrow_down</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs2>
              <v-select
                hint='Sensitivity'
                persistent-hint
                v-bind:items='sensitivities'
                item-text= 'value'
                v-model='maxSensitivity'>
              </v-select>
            </v-flex xs>
          </v-layout>
          <br/>
          <v-layout>
            <v-flex xs3>
              <v-text-field
                @change='scaleVerticalAxis'
                label='Minimum (V)' v-model='chartMin'>
              </v-text-field>
            </v-flex>
            <v-flex xs1 class='ml-5'>
              <v-btn icon outline class='mt-3' @click.native='minUp'>
                <v-icon light>keyboard_arrow_up</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs2>
              <v-btn icon outline class='mt-3' @click.native='minDown'>
                <v-icon light>keyboard_arrow_down</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs2>
              <v-select
                hint='Sensitivity'
                persistent-hint
                v-bind:items='sensitivities'
                item-text= 'value'
                v-model='maxSensitivity'>
              </v-select>
            </v-flex xs>
          </v-layout>

          <br/>
          <v-layout>
            <v-flex xs3>
              <v-text-field
                @change='scaleHorizontalAxis'
                label='Width (seconds)' v-model='chartWidth'>
              </v-text-field>
            </v-flex>
            <v-flex xs1 class='ml-5'>
              <v-btn icon outline class='mt-3' @click.native='widthUp'>
                <v-icon light>keyboard_arrow_up</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs2>
              <v-btn icon outline class='mt-3' @click.native='widthDown'>
                <v-icon light>keyboard_arrow_down</v-icon>
              </v-btn>
            </v-flex>
            <v-flex xs2>
              <v-select
                hint='Sensitivity'
                persistent-hint
                v-bind:items='sensitivities'
                item-text= 'value'
                v-model='widthSensitivity'>
              </v-select>
            </v-flex xs>
          </v-layout>

        </v-card-text>
      </v-card>
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

        dataBuffer: [],
        maxSensitivity: 0.1,
        widthSensitivity: 1,
        chartMax: 10,
        chartMin: 0,
        chartWidth: 10,
        timeFrame: 10000,
        sensitivities: [
          {value: 0.01}, {value: 0.1}, {value: 0.5}, {value: 1}, {value:10}],
      }
    },

    methods: {

      maxUp () {
        // Increase chart maximum.
        this.chartMax = parseFloat(this.chartMax)
        this.chartMax += this.maxSensitivity
        this.chartMax = Math.round(this.chartMax*100)/100
        this.scaleVerticalAxis()
      },

      maxDown () {
        // Increase chart maximum.
        this.chartMax = parseFloat(this.chartMax)
        this.chartMax -= this.maxSensitivity
        this.chartMax = Math.round(this.chartMax*100)/100
        this.scaleVerticalAxis()
      },

      minUp () {
        // Increase chart minimum.
        this.chartMin = parseFloat(this.chartMin)
        this.chartMin += this.maxSensitivity
        this.chartMin = Math.round(this.chartMin*100)/100
        this.scaleVerticalAxis()
      },

      minDown () {
        // Decrease chart minimum.
        this.chartMin = parseFloat(this.chartMin)
        this.chartMin -= this.maxSensitivity
        this.chartMin = Math.round(this.chartMin*100)/100
        this.scaleVerticalAxis()
      },

      widthUp () {
        // Increase chart width.
        this.chartWidth = parseFloat(this.chartWidth)
        this.chartWidth += this.widthSensitivity
        this.chartWidth = Math.round(this.chartWidth*100)/100
        this.scaleHorizontalAxis()
      },

      widthDown () {
        // Decrease chart width.
        this.chartWidth = parseFloat(this.chartWidth)
        this.chartWidth -= this.widthSensitivity
        this.chartWidth = Math.round(this.chartWidth*100)/100
        this.scaleHorizontalAxis()
      },

      scaleVerticalAxis () {
        this.yScale.domain([this.chartMin, this.chartMax])
        var svg = d3.select('#'+this.chartID)
        svg.selectAll('g')
          .select('.y.axis')
          .transition().duration(200)
          .call(this.yAxis)
        this.setConfig()
      },

      scaleHorizontalAxis () {
        this.timeFrame = 1000 * this.chartWidth
        this.setConfig()
        return
      },

      buildChart () {
        var e = d3.select('#'+this.chartID)
        var width = e.node().getBoundingClientRect().width

        var data = this.dataBuffer;
        var time_frame = this.timeFrame;
        var height = 250;
        var margin = 20;
        var duration = 1000;
        var time = Date.now() + duration;
        var start_time = time - (duration * 2) - time_frame;
        var self = this;

        var xScale = d3.scaleTime()
          .domain([time + duration, time - (duration * 2) - time_frame])
        //    .domain([time - duration, start_time + duration])
          .range([width - (margin *2), 0]);
        this.xScale = xScale
        this.duration = duration

        var yScale = d3.scaleLinear()
          .domain([0,10])
          .range([height - (margin*2), 0]);

        this.yScale = yScale

        var xAxis = d3.axisBottom(xScale)
          .ticks(4);
        this.xAxis = xAxis

        var yAxis = d3.axisRight(yScale)
          .ticks(4);

        this.yAxis = yAxis

        var svg = d3.select('#'+this.chartID)
          .append('svg')
          .attr('width', width)
          .attr('height', height)
          .append('g');

        this.svg = svg

        svg.append('g')
          .attr('transform', 'translate(' + (width - margin * 2) + ',' + margin + ')')
          .classed('y axis', true)
          .call(yAxis);

        svg.append('g')
          .attr('transform', 'translate(0,' + (height - margin) + ')')
          .classed('x axis', true);

        svg.append('defs')
          .append('clipPath')
          .attr('id', 'clip')
          .append('rect')
          .attr('width', (width - (margin * 2)))
          .attr('height', (height - (margin * 2)))
          .attr('transform', 'translate(-1.5, 20)');

        svg.append('g')
          .attr('clip-path', 'url(#clip)')
          .classed('line_', true)
          .append('path')
          .datum(data)
          .classed('line', true)
          .style('fill', 'none')
          .style('stroke', '#c62828')
          .style('stroke-width', '3px');


        this.update = function () {
          time = Date.now();
          var sample = self.dataBuffer.shift()
          if (sample) {
            data.push({'x': time, 'y': sample.y});
            // data.push({'x': time, 'y': d3.randomUniform(0,9)()});
            draw();
          }
        }

        var interval = d3.interval(this.update, 40);

        function update(){
          time = Date.now();
          data.push({'x': time, 'y': d3.randomUniform(0,9)()});
          draw();
        }

        function draw(){
          time_frame = self.timeFrame
          var line = d3.line()
            .x(function(d) { return xScale(d.x); })
            .y(function(d) { return yScale(d.y); })
            .curve(d3.curveBasis)

          var lineselection = svg.selectAll('.line_')
            .select('path');

          lineselection.interrupt()
            .transition()
            .duration(duration)
            .ease(d3.easeLinear)
            .attr('transform', 'translate(' + -(xScale.range()[0]/((duration / 100)-2)) + ',0)');

          if (data[0].x < time - time_frame - duration ){
            data.shift();
          }

          lineselection.attr('d',line)
            .attr('transform', null);

          start_time = time - (duration * 2) - time_frame;

          xScale.domain([time, time + (duration * 2) - time_frame])
            .range([width - (margin *2),0]);

          d3.select('#'+self.chartID)
            .select('g')
            .select('.x.axis')
            .transition()
            .duration(duration)
            .ease(d3.easeLinear)
            .call(xAxis);
        }
        this.retrieveConfig()

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
        this.config.chartWidth = this.chartWidth
        this.config.maxSensitivity = this.maxSensitivity
        this.config.maxWidth = this.maxWidth
        localStorage.setObj(configName, this.config)
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
        if (this.config.chartWidth) {
          this.chartWidth = this.config.chartWidth
        }
        if (this.config.maxSensitivity) {
          this.maxSensitivity = this.config.maxSensitivity
        }
        if (this.config.widthSensitivity) {
          this.widthSensitivity = this.config.widthSensitivity
        }
        this.scaleHorizontalAxis()
        this.scaleVerticalAxis()
      },

      registerListeners () {
        if (this.channelName == 'PPG') {
          this.$store.state.socket.on('ppg', this.dataReceived)
        } else {
          this.$store.state.socket.on('pzt', this.dataReceived)
        }
      },

      dataReceived (samples) {
        this.dataBuffer = this.dataBuffer.concat(samples)
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

      console.log('Mounted')
      setTimeout(this.buildChart, 500)
      setTimeout(this.registerListeners, 1000)

    }
  }

</script>

<style scoped>

.label {
  margin-top: 10px;
}

</style>
