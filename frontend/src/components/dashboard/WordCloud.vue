<template>
  <div class="word-cloud">
    <svg ref="wordCloudSvg" width="300" height="300"></svg>
  </div>
</template>

<script>
import * as d3 from "d3";
import cloud from "d3-cloud";

export default {
  props: {
    wordData: {
      type: Array,
      default: () => [], // set default value to an empty array
    }
  },
  created() {
    // console.log("Received wordData prop:", this.wordData);
  },
  mounted() {
    this.createWordCloud();
  },
methods: {
  createWordCloud() {
    // console.log("Word Data:", this.wordData); 

    var fill = d3.scaleOrdinal(d3.schemeCategory10);

    var svg = d3.select(this.$refs.wordCloudSvg).append("g")
      .attr("transform", "translate(150,150)");


    function draw(words) {
      // console.log(words); 
      
      var cloud = svg.selectAll("g text")
        .data(words)
        .enter()
        .append("text")
        .style("font-family", "Impact")
        .style("fill", function (d, i) {
          return fill(i);
        })
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
          return "translate(" + [d.x, d.y] + ")";
        })
        .style("fill-opacity", 1)
        .text(function (d) {
          return d.text;
        });

      cloud.exit()
        .transition()
        .duration(200)
        .style('fill-opacity', 1e-6)
        .remove();
    }

   var wordCloudLayout = cloud()
    .size([300, 300])
    .words(this.wordData.map(word => ({ text: word }))) // Convert the list of words to objects with a 'text' property
    .padding(5)
    .rotate(function () {
      return ~~(Math.random() * 2) * 90;
    })
    .font("Impact")
    .fontSize(25) // constant font size
    .on("end", draw)
    .start();
      
    return wordCloudLayout

  },
},

};
</script>

<style scoped>
/* Component-specific styles */

/* You can add more styles for your word cloud here */
</style>
