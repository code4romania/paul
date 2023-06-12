<template>
  <div>
    <BaseTitle :title="$t('dataUpdate')" :hasBackButton="!isManualImport" />

    <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
      <BaseCard v-bind="{ title, loading }">
        <div class="card-container">
          <div class="columns">
            <div class="column is-5" v-if="isManualImport && database">
              <VField :label="$t('destinationTable')" rules="required">
                <b-select
                  :placeholder="$t('chooseATable')"
                  v-model="idTable"
                  expanded
                >
                  <option
                    v-for="table in database.active_tables"
                    :value="table.id"
                    :key="table.id"
                    v-text="`${$t('table')} – ${table.data.name}`"
                  />
                </b-select>
              </VField>
            </div>
          </div>
          <div class="columns">
          </div>
        </div>

        <template #footer>
          <b-button type="is-primary" @click="passes(submit)"
            >{{ $t('continue') }}</b-button
          >
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'TableImportForm',
  data() {
    return {
      title: null,
      idTable: null,
      isManualImport: null,
      loading: false,
      filetype: 'csv',
      delimiter: null,
      file: null
    }
  },
  computed: mapState({
    database: state => state.data.database
  }),
  mounted() {
    this.checkIfManual()
  },
  methods: {
    checkIfManual() {
      this.isManualImport = this.$route.query.manual

      this.title = `${this.$t('importAndCreateTable')} ${JSON.stringify(
        this.$route.query.name
      )}`

    },
    submit() {
      const formData = new FormData()
      formData.append('file', this.file)
      formData.append('delimiter', this.delimiter)
      this.idTable && formData.append('table_id', this.idTable)

      this.loading = true
      this.$store
        .dispatch('data/prepareImport', formData)
        .then(response => {
          this.loading = false
          
          this.$router.push({
            name: this.isManualImport ? 'table-import-edit' : 'table-edit',
            params: { ...(this.isManualImport && { idTable: this.idTable }) },
            query: {
              idImport: response.import_id,
              ...(this.$route.query.name && { name: this.$route.query.name })
            }
          })
        })
        .catch(() => {
          this.loading = false
        })
    }
  },
  watch: {
    '$route.query'() {
      this.checkIfManual()
    }
  }
}
</script>
