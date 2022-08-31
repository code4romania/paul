<template>
  <div v-if="chart">
    <BaseTitle title="Chart view" backTo="charts-view" />

    <FilterHead
      v-if="table"
      v-bind="{ table, filterData: chart.filters, viewType: 'charts' }"
      @update="getChartData"
      filterMode
    />

    <BaseCard :title="`Chart — ${chart.name}`">
      <template #actions>
        <div class="buttons">
          <router-link
            class="button is-dark"
            :to="{
              name: 'table-view',
              params: { idTable: chart.config.table }
            }"
          >
            Vezi sursa de date
          </router-link>
          <router-link
            class="button is-primary"
            :to="{
              name: 'chart-edit',
              params: { idChart }
            }"
          >
            Editează grafic
          </router-link>
        </div>
      </template>

      <template #default>
        <div class="card-container" v-if="table">
          Ultima actualizare: {{ table.last_edit_date | parseDate }}
          <span v-if="table.last_edit_user"
            >de
            {{
              table.last_edit_user.first_name +
                ' ' +
                table.last_edit_user.last_name
            }}
          </span>
        </div>

        <BaseChart
          v-bind="{ idChart, chartData, chartConfig: chart.config }"
          v-if="chartData"
        />
      </template>
    </BaseCard>
  </div>
</template>

<script>
import { ChartService } from '@/services/data'
import BaseChart from '@/components/charts/BaseChart'
import FilterHead from '@/components/filters/FilterHead'

import { mapState } from 'vuex'

export default {
  name: 'ChartView',
  components: { FilterHead, BaseChart },
  props: {},
  data() {
    return {
      idChart: Number(this.$route.params.idChart),
      chartData: null
    }
  },
  computed: {
    ...mapState('data', {
      table: function(state) {
        return state.table[this.chart.config.table]
      },
      chart: state => state.chart
    })
  },
  mounted() {
    this.$store.commit('data/setChart', null)

    this.$store.dispatch('data/getChart', this.idChart).then(() => {
      this.$store
        .dispatch('data/getTable', this.chart.config.table)
        .then(() => {
          if (!this.chart.filters) this.getChartData()
        })
    })
  },
  methods: {
    getChartData() {
      ChartService.getChartData(this.idChart, this.$route.query).then(
        response => {
          this.chartData = response
        }
      )
    }
  }
}
</script>
