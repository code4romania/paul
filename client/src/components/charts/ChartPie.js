import { Pie, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Pie,
  mixins: [reactiveProp],
  props: {
    options: Object
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
}
