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
      default: 380,
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
      default: 10,
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
        .range([15, 35]); // Adjust the maximum font size as needed

      const wordCloudLayout = cloud()
        .size([this.width, this.height])
        .words(wordCloudData)
        .padding(this.padding)
        .rotate(() => (Math.random() < 0.5 ? 0 : 35))
        .font("Impact")
        .text(function(d) { return d.word; })
        .fontSize((d) => fontSizeScale(d.size))
        .on("end", draw)
        .random(() => 0.5)

      wordCloudLayout.start();

      function draw(words) {
        const cloud = svg
          .append("g")
          .attr("transform", `translate(${svg.attr("width") / 2},${svg.attr("height") / 2})`)
          .selectAll("text")
          .data(words)
          .enter()
          .append("text")
          .attr('font-family', 'Impact')
          .style("fill", (d, i) => fill(i))
          .attr("text-anchor", "middle")
          .style("fill-opacity", 1)
          .text((d) => d.word)
          .style("font-size", (d) => d.size * 0.85)
          .call(handleCollision);

        cloud
          .exit()
          .transition()
          .duration(1)
          .style("fill-opacity", 1e-6)
          .remove();
      }

      function handleCollision(selection) {
        selection.each(function() {
          d3.select(this).attr("transform", (d) => `translate(${d.x},${d.y})`);
        });
      }

    },

  },
};
</script>
