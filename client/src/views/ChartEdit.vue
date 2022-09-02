<template>
  <div>
    <BaseTitle title="Editează grafic" />

    <ValidationObserver
      v-slot="{ passes }"
      @submit.prevent
      slim
      v-if="chartConfig"
    >
      <BaseCard title="Configurare">
        <div class="card-container card-form">
          <div class="columns is-multiline">
            <div class="column is-6">
              <VField label="Nume" rules="required">
                <b-input v-model="chartConfig.name" />
              </VField>

              <VField label="Selectează tipul de grafic" rules="required">
                <b-select expanded v-model="chartConfig.chart_type">
                  <option
                    v-for="(type, key) in chartTypes"
                    :key="key"
                    :value="key"
                    v-text="type"
                  />
                </b-select>
              </VField>

              <VField
                label="Alege o sursă de date pe care deja le-ai încărcat în platformă"
                v-if="database"
                rules="required"
              >
                <b-select
                  expanded
                  v-model="chartConfig.table"
                  @input="getTable"
                >
                  <option
                    v-for="(table, key) in database.active_tables"
                    :value="table.id"
                    :key="key"
                    v-text="table.data.name"
                  />
                </b-select>
              </VField>

              <VField
                label="Alege ce date vrei să vezi pe axa orizontală"
                v-if="table"
              >
                <b-select expanded v-model="chartConfig.x_axis_field">
                  <option></option>
                  <option
                    v-for="(field, key) in table.sorted_fields"
                    :value="field.id"
                    :key="key"
                    v-text="field.display_name"
                  />
                </b-select>
              </VField>

              <VField
                label="Alege după ce date vrei să grupezi informația pe axa orizontală"
                v-if="table"
              >
                <b-select expanded v-model="chartConfig.x_axis_field_2">
                  <option></option>
                  <option
                    v-for="(field, key) in table.sorted_fields"
                    :value="field.id"
                    :key="key"
                    v-text="field.display_name"
                  />
                </b-select>
              </VField>

              <VField
                label="Alege ce date vrei să vezi pe axa verticală"
                v-if="table"
              >
                <b-select expanded v-model="chartConfig.y_axis_field">
                  <option></option>
                  <option
                    v-for="(field, key) in table.sorted_fields.filter(isNumeric)"
                    :value="field.id"
                    :key="key"
                    v-text="field.display_name"
                  />
                </b-select>
              </VField>

              <VField label="Care este funcția de calcul pentru axa verticală" v-if="table">
                <b-select expanded v-model="chartConfig.y_axis_function">
                  <option
                    v-for="(func, key) in chartFunctions"
                    :value="key"
                    :key="key"
                    v-text="func"
                  />
                </b-select>
              </VField>

              <VField label="Date temporale" v-if="table">
                <b-select expanded v-model="chartConfig.timeline_field">
                  <option></option>
                  <option
                    v-for="(field, key) in table.sorted_fields.filter(
                      e => e.field_type == 'date'
                    )"
                    :value="field.id"
                    :key="key"
                    v-text="field.display_name"
                  />
                </b-select>
              </VField>

              <VField
                label="Selectează tipul de interval"
                v-if="chartConfig.timeline_field"
              >
                <b-select expanded v-model="chartConfig.timeline_period">
                  <option
                    v-for="(func, key) in chartTimelineGroups"
                    :value="key"
                    :key="key"
                    v-text="func"
                  />
                </b-select>
              </VField>
              <VField v-if="chartConfig.timeline_field">
                <b-checkbox v-model="chartConfig.timeline_include_nulls">
                  Include perioade fără date
                </b-checkbox>
              </VField>
            </div>
          </div>
        </div>

        <template #footer>
          <b-button class="is-primary" @click="passes(save)">
            Salvează modificările
          </b-button>
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
import ChartConfig from '@/services/chart'
import FieldService from '@/services/field'
import { TableService } from '@/services/data'
import { mapState } from 'vuex'

export default {
  name: 'ChartEdit',
  components: {},
  data() {
    return {
      idChart: Number(this.$route.params.idChart),
      table: null,
      chartConfig: {
        y_axis_function: 'Count'
      },
      chartFunctions: ChartConfig.getFunctions(),
      chartTypes: ChartConfig.getChartTypes(),
      chartTimelineGroups: ChartConfig.getTimelineGroups(),
      isNumeric: FieldService.isNumeric
    }
  },
  computed: {
    ...mapState({
      database: state => state.data.database,
      chart: state => state.data.chart
    })
  },
  mounted() {
    if (!this.database) this.$store.dispatch('data/getDatabase')

    if (this.idChart) {
      this.$store.dispatch('data/getChart', this.idChart).then(() => {
        this.chartConfig = { ...this.chart.config }

        this.getTable(this.chartConfig.table)
      })
    }
  },
  methods: {
    getTable(id) {
      TableService.getTable(id).then(response => {
        this.table = response
      })
    },
    save() {
      if (this.idChart)
        this.$store
          .dispatch('data/updateChart', {
            id: this.idChart,
            data: this.chartConfig
          })
          .then(this.redirect)
      else
        this.$store
          .dispatch('data/createChart', this.chartConfig)
          .then(this.redirect)
    },
    redirect(response) {
      this.$router.push({
        name: 'chart-view',
        params: {
          ...(response.id && { idChart: response.id })
        }
      })
    }
  }
}
</script>
