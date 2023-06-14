<template>
  <div>
    <BaseTitle :title="$t('importTableResults')" :hasBackButton="false" />

    <template v-if="importData">
      <BaseCard
        :title="
          `${$t('theTable')} ${name && JSON.stringify(name)} ${$t('was')} ${
            name ? $t('created') : $t('updated')
          }`
        "
      >
        <template #actions v-if="importData.import_count_created||importData.import_count_updated" class="da">
          <router-link
            class="button is-dark"
            :to="{ name: 'table-view', params: { idTable: importData.table } }"
            >{{ $t('viewTable') }}</router-link
          >
        </template>

        <div class="card-container">
          {{ importData.import_count_created }} {{ $t('entriesCreated') }} <br>
          {{ importData.import_count_updated }} {{ $t('entriesUpdated') }}
        </div>
      </BaseCard>

      <BaseCard v-if="importData.errors_count">
        <template #title>
          <span class="has-text-danger"
            >{{ importData.errors_count }} {{ $t('entriesWithError') }}</span
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
            >{{ $t('downloadTheseEntries') }}</a
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
