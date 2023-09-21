<template>
  <div class="word-cloud">
    <svg ref="wordCloudSvg" :width="width" :height="height"></svg>
  </div>
</template>

<script>
import * as d3 from "d3";
import cloud from "d3-cloud";

export default {
  props: {
    wordData: {
      type: Array,
      default: () => [],
    },
    width: {
      type: Number,
      default: 350,
    },
    height: {
      type: Number,
      default: 250, 
    },
    scalingFactor: {
      type: Number,
      default: 30,
    },
    padding: {
      type: Number,
      default: 5,
    },
  },
  mounted() {
    this.createWordCloud();
  },
  methods: {
    createWordCloud() {
      const wordCloudData = this.wordData.map((item) => ({
        size: item.size,
        word: item.word,
      }));

      const fill = d3.scaleOrdinal(d3.schemeCategory10);

      const svg = d3.select(this.$refs.wordCloudSvg);

      const fontSizeScale = d3.scaleLinear()
        .domain([0, d3.max(wordCloudData, (d) => d.size)])
        .range([10, 40]); // Adjust the maximum font size as needed

      const wordCloudLayout = cloud()
        .size([this.width, this.height])
        .words(wordCloudData)
        .padding(this.padding)
        .rotate(() => (Math.random() < 0.5 ? 0 : 90)) // Rotate words either 0 or 90 degrees
        .font("Impact")
        .fontSize((d) => fontSizeScale(d.size))
        .on("end", draw);

      wordCloudLayout.start();

      function draw(words) {
        const cloud = svg
          .append("g")
          .attr("transform", `translate(${svg.attr("width") / 2},${svg.attr("height") / 2})`)
          .selectAll("text")
          .data(words)
          .enter()
          .append("text")
          .style("font-family", "Impact")
          .style("fill", (d, i) => fill(i))
          .attr("text-anchor", "middle")
          .attr("transform", (d) => `translate(${d.x},${d.y})`)
          .style("fill-opacity", 1)
          .text((d) => d.word)
          .style("font-size", (d) => d.size * 0.85);

        cloud
          .exit()
          .transition()
          .duration(1)
          .style("fill-opacity", 1e-6)
          .remove();
      }
    },

  },
};
</script>

<style scoped>
/* Component-specific styles */

/* You can add more styles for your word cloud here */
</style>
