<template>
  <div>
    <component
      v-if="data"
      class="chart-container"
      :is="chartComponent"
      v-bind="{ chartData: data, options }"
    />
  </div>
</template>

<script>
import 'chartjs-plugin-zoom'
import * as Charts from '.'
import ChartService from '@/services/chart'
import { mapState } from 'vuex'

export default {
  components: { ...Charts },
  props: {
    idChart: Number,
    chartData: Object,
    chartConfig: Object
  },
  data() {
    return {
      data: null,
      options: {}
    }
  },
  computed: {
    ...mapState('data', {
      loading: function(state) {
        return state.loading[this.idChart]
      }
    }),
    chartComponent() {
      return ChartService.getComponent(this.chartConfig.chart_type)
    },
    hasAxes() {
      return ['Pie', 'Doughnut'].indexOf(this.chartConfig.chart_type) == -1
    }
  },
  mounted() {
    if (this.hasAxes) {
      this.options = {
        scales: {
          xAxes: [
            {
              ticks: {
                callback: function(value) {
                  const maxlen = 20

                  if (typeof value == 'string')
                    return (
                      value.substr(0, maxlen) +
                      (value.length > maxlen ? '...' : '')
                    )
                  else return value
                }
              }
            }
          ]
        },
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              mode: 'x',
              speed: 10,
              threshold: 10
            },
            zoom: {
              enabled: true,
              mode: 'x'
            }
          }
        }
      }
    }

    this.prepareData()
  },
  methods: {
    prepareData() {
      this.data = {
        datasets: this.chartData.datasets,
        labels: this.chartData.labels
      }

      this.options = Object.assign({}, this.chartData.options, this.options)
    }
  },
  watch: {
    chartData() {
      this.prepareData()
    }
  }
}
</script>
