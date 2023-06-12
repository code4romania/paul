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
            <!-- <div class="column is-narrow">
              <VField label="Alege tipul de fișier" rules="required">
                <VSelect :choices="['csv']" v-model="filetype" />
              </VField>
            </div> -->
            <div class="column is-2">
              <VField
                :label="$t('delimiterLabel')"
                :labelInfo="$t('leaveEmptyForAutocomplete')"
              >
                <b-input v-model="delimiter" />
              </VField>
            </div>
            <div class="column is-7">
              <VField label="Alege fisier" rules="required">
                <div class="file is-right is-dark is-fullwidth">
                  <b-upload v-model="file" expanded>
                    <span class="file-cta">
                      <span class="file-label">{{ $t('') }}Caută</span>
                    </span>
                    <span class="file-name">
                      <span v-if="file">{{ file.name }}</span>
                    </span>
                  </b-upload>
                </div>
              </VField>
            </div>
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

      if (this.isManualImport) {
        if (!this.database) {
          this.loading = true
          this.$store.dispatch('data/getDatabase').then(() => {
            this.loading = false
          })
        }
        this.title = this.$t('loadDataToExistingTable')
      } else {
        this.title = `${this.$t('importAndCreateTable')} ${JSON.stringify(
          this.$route.query.name
        )}`
      }
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
