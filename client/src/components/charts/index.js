import { Bar, Line, Pie, Doughnut, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

const ChartBar = {
  extends: Bar,
  mixins: [reactiveProp],
  props: {
    options: Object
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
}

const ChartLine = {
  extends: Line,
  mixins: [reactiveProp],
  props: {
    options: Object
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
}

const ChartPie = {
  extends: Pie,
  mixins: [reactiveProp],
  props: {
    options: Object
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
}

const ChartDoughnut = {
  extends: Doughnut,
  mixins: [reactiveProp],
  props: {
    options: Object
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
}

export { ChartBar, ChartLine, ChartPie, ChartDoughnut }
