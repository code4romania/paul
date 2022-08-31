<template>
  <div>
    <BaseTitle title="Rezultate import tabel" :hasBackButton="false" />

    <template v-if="importData">
      <BaseCard
        :title="
          `Tabelul ${name && JSON.stringify(name)} a fost ${
            name ? 'creat' : 'actualizat'
          }`
        "
      >
        <template #actions v-if="importData.import_count_created||importData.import_count_updated" class="da">
          <router-link
            class="button is-dark"
            :to="{ name: 'table-view', params: { idTable: importData.table } }"
            >Vezi tabel</router-link
          >
        </template>

        <div class="card-container">
          {{ importData.import_count_created }} intrări au fost create <br>
          {{ importData.import_count_updated }} intrări au fost actualizate
        </div>
      </BaseCard>

      <BaseCard v-if="importData.errors_count">
        <template #title>
          <span class="has-text-danger"
            >{{ importData.errors_count }} intrări au eroare</span
          >
        </template>
        <template #default>
          <b-table :data="importData.errors" scrollable paginated :perPage="10">
            <b-table-column
              v-for="(field, index) in importData.csv_field_mapping"
              :key="`column-${index}`"
              v-bind="{
                label: field.original_name
              }"
            >
              <template v-slot="props"
                ><span
                  :class="{
                    'has-text-danger is-bold':
                      props.row.errors[field.original_name]
                  }"
                  >
                    {{ props.row.row[field.original_name] }}
                    <b-tooltip
                      v-if="props.row.errors[field.original_name]"
                      type="is-dark"
                      :label="props.row.errors[field.original_name]"
                      multilined
                    >
                      <b-icon icon="help-circle-outline" class="is-size-5"></b-icon>
                    </b-tooltip>
                  </span
                ></template
              >
            </b-table-column>
          </b-table>
        </template>

        <template #actions>
          <a class="button is-primary" target="_blank" :href="exportPath()"
            >Descarcă aceste intrări</a
          >
        </template>
      </BaseCard>
    </template>
  </div>
</template>

<script>
import ApiService from '@/services/api'
import { mapState } from 'vuex'

export default {
  name: 'TableImportResult',
  data() {
    return {
      idImport: this.$route.params.idImport,
      name: this.$route.query.name || ''
    }
  },
  computed: mapState('data', {
    importData: state => state.import
  }),
  mounted() {
    this.$store.dispatch('data/getImportData', this.idImport)
  },
  methods: {
    exportPath() {
      return ApiService.getPath(
        `csv-imports/${this.idImport}/export-errors/`,
        true, false
      )
    }
  }
}
</script>
