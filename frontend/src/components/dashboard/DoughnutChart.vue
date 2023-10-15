<template>
    <div id="chart-container">
        <canvas id="chart" width="350" height="250"></canvas>
    </div>
</template>
  
<script>
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';

export default {
    name: 'DoughnutChart',
    props: {
        labelArray: {
            type: Array
        },
        dataArray: {
            type: Array
        },
        label: String
    },
    mounted() {
        this.$nextTick(() => {
            const ctx = document.getElementById('chart');
            Chart.register(ChartDataLabels);

            // Change default options for ALL charts
            /*Chart.defaults.set('plugins.datalabels', {
                color: '#FE777B'
            });*/

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: this.labelArray,
                    datasets: [{
                        label: this.label,
                        data: this.dataArray,
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 205, 86)'
                        ],
                        hoverOffset: 4
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'bottom'
                        },
                        datalabels: {
                            display: true,
                            color: 'white',
                            formatter: function(value) {
                                return value + '%';
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    
                                    const value = context.parsed;
                                    label += value + '%';
                                    return label;
                                }
                            }
                        }
                    }
                }
            });
        });
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