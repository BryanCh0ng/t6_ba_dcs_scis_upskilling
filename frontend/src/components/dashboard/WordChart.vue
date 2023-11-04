<template>
    <div id="chart-container">
        <canvas :id="'chart-' + uniqueChartId" width="350" height="250"></canvas>
    </div>
</template>
  
<script>
import Chart from 'chart.js/auto';
import { WordCloudController, WordElement } from 'chartjs-chart-wordcloud';
import ChartDataLabels from 'chartjs-plugin-datalabels';

export default {
    name: 'WordCloud',
    props: {
        datasets: {
            type: Array,
            required: true
        },
        label: {
            type: String,
            required: true
        },
        size1: {
            type: Number,
            default: 10
        },
        size2: {
            type: Number,
            default: 10
        },
        fit: {
            type: Boolean,
            default: true
        },

    },
    data() {
        return {
            uniqueChartId: `${Date.now()}-${Math.floor(Math.random() * 10000)}` // Generate a unique chartId
        };
    },
    methods: {
        createChart() {
            const canvas = document.getElementById('chart-' + this.uniqueChartId);
            if (canvas) {
                // Destroy the existing chart if it exists
                const existingChart = Chart.getChart(canvas);
                if (existingChart) {
                    existingChart.destroy();
                }
            }

            const ctx = canvas.getContext('2d');
            Chart.register(WordCloudController, WordElement, ChartDataLabels);

            new Chart(ctx, {
                type: 'wordCloud',
                data: {
                    labels: this.datasets.map((d) => d.word),
                    datasets: [
                        {
                            label: this.label,
                            data: this.datasets.map((d) => this.size1 + d.size* this.size2),
                            originalSizes: this.datasets.map((d) => d.size),
                            hoverOffset: 4
                        },
                    ],
                },
                options: {
                    fit: this.fit,
                    padding: 2,
                    plugins: {  
                        legend: {
                            display: false
                        },
                        datalabels: {
                            display: false,
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    
                                    //const word = context.label;

                                    const index = context.dataIndex;
                                    const size = context.dataset.originalSizes[index]; // Use original size in tooltip

                                    label += size;
                                    
                                    return label;
                                },
                            },
                        },
                    },
                    elements: {
                        word: {
                            font: 'Source Sans Pro, sans-serif',
                            color: ['#FF5733', '#C70039', '#900C3F', '#581845', '#2E86C1', '#138D75', '#16A085', '#D4AC0D'], // Word color
                            minFontSize: 10,
                            maxFontSize: 20,
                            rotate: 90, // Set rotate property to 0 to display words horizontally
                        },
                    },
                },
                            
            });
            
        }
    },
    mounted() {
        this.createChart();
    }, 
    watch: {
        datasets: {
            deep: true,
            handler(newData) {
                this.createChart();
                console.log("Received updated datasets:", newData);
                // You can also call a method to update the chart here if needed
            }
        }
    }
}
</script>

<style scoped>

/*#planet-chart {
    padding: 10px;
}*/

#chart-container {
    width: 100%;
    max-width: 350px;
    height: auto;
    position: relative;
    margin: 10px auto 0; /* Adjust top margin to reduce the gap */
    overflow: hidden; /* Hide any chart content overflowing the div */
}

#chart {
    width: 100%; /* Set the chart width to 100% of the container */
    height: auto; /* Allow the chart height to adjust proportionally */
    max-width: 100%; /* Ensure the chart doesn't exceed the container's width */
    max-height: 100%; /* Ensure the chart doesn't exceed the container's height */
}

</style>