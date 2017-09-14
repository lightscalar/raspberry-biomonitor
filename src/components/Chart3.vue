<template>

  <div v-bind:id='chartID'></div>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: ['channelNumber'],

    data () {
      return {

      }
    },

    methods: {

    },

    computed: {

      chartID () {
        return ('channel-' + this.channelNumber)
      },

    },

    mounted () {
      var data = [];
      var time_frame = 10000;
      var height = 250;
      var width = 800;
      var margin = 20;
      var duration = 1000;
      var time = Date.now() + duration;
      var start_time = time - (duration * 2) - time_frame;
      var self = this

      var xScale = d3.scaleTime()
        .domain([time + duration, time - (duration * 2) - time_frame])
      //    .domain([time - duration, start_time + duration])
        .range([width - (margin *2), 0]);

      var yScale = d3.scaleLinear()
        .domain([0,10])
        .range([height - (margin*2), 0]);

      var xAxis = d3.axisBottom(xScale)
        .ticks(4);

      var yAxis = d3.axisRight(yScale)
        .ticks(4);

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
        .style('stroke', 'steelblue')
        .style('stroke-width', '1.5px');


      this.update = function () {
        time = Date.now();
        data.push({'x': time, 'y': d3.randomUniform(0,9)()});
        draw();
      }

      var interval = d3.interval(this.update, 100);

      function update(){
        time = Date.now();
        data.push({'x': time, 'y': d3.randomUniform(0,9)()});
        draw();
      }

      function draw(){
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

    }
  }

</script>

<style>

</style>
