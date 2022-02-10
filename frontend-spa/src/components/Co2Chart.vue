<script>
import {defineComponent} from 'vue'
import {Line} from 'vue3-chart-v2'

export default defineComponent({
  extends: Line,
  name: "Co2Chart",
  props:{
    chartData1: {},
    chartData2: {},
    chartData3: {}, //vllt nicht ganz nötig, weil Co2 nur 2 Werte hat
    xAxis: {}
  },
  mounted() {
    // rendert den chart..
    this.renderChart({
      labels: this.xAxis,
      // datasets sind die daten die angezeigt werden
      datasets: [
        {
          label: 'CO2 Sensor 1',
          fill: false,
          borderWidth: 1,
          borderColor: '#14ccde',
          data: this.chartData1
        },
        {
          label: 'CO2 Sensor 2',
          fill: false,
          borderWidth: 1,
          borderColor: '#61d53f',
          data: this.chartData2
        },
        {
          label: 'CO2 Sensor 3',
          fill: false,
          borderWidth: 1,
          borderColor: '#ee41b5',
          data: this.chartData3
        }
      ]
    }, {
      scales: {
        yAxes: [{ // y-achsen optionen
          scaleLabel:{
            display: true,
            labelString: 'Parts per million(ppm)'
          }
        }]
      }
    })
  }

})
</script>

<style scoped>

</style>