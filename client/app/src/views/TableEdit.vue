<template>
  <div v-if="table && fields">
    <BaseTitle :title="title" />

    <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
      <BaseCard v-bind="{ title, loading }">
        <template #title>
          <div class="info" v-if="idImport">
            <div>
              The table you want to import contains multiple columns. Please
              name the columns and select the column type for each. The column
              type refers to the type of data present in a specific column (eg:
              Column name: Age will have a Column type: Integer (whole number))
              . The system provides you with five default column types. If you
              are not sure of the data type in a column, we recommend you to
              select the Text type.
            </div>
            <div><br>File: {{ importData.filename }}</div>
          </div>
        </template>
        <div class="card-container">
          <div class="columns">
            <div class="column is-4">
              <VField label="Nume tabel">
                <b-input v-model="name" />
              </VField>
            </div>
            <div class="column is-8">
              <div
                class="columns field-list"
                v-for="(field, index) in fields"
                :key="`cname-${index}`"
              >
                <div class="column is-7">
                  <VField :label="`Nume coloană #${index + 1}`" rules="required">
                    <div class="field-container">
                      <b-input v-model="field.display_name" placeholder="" />
                    </div>
                  </VField>
                </div>
                <div class="column is-5">
                  <VField
                    :label="`Tip coloană #${index + 1}`"
                    rules="required"
                    grouped
                  >
                    <b-select
                      v-model="field.field_type"
                      placeholder=""
                      :disabled="field.disabled"
                      expanded
                    >
                      <option
                        v-for="(type, key) in fieldTypes"
                        :key="key"
                        :value="key"
                        >{{ type }}</option
                      >
                    </b-select>

                    <b-button class="is-white" :disabled="fields.length == 1">
                      <ActionButtonDelete
                        :dialogTitle="
                          `Șterge coloană ${
                            field.display_name != null
                              ? JSON.stringify(field.display_name)
                              : ''
                          }`
                        "
                        dialogMessage="Ești sigur?"
                        :bypassDialog="!idTable"
                        @on-confirm="deleteColumn(index)"
                    /></b-button>
                  </VField>
                  <div class="enum-values" v-if="field.field_type=='enum'">
                    Adaugă valorile separate de virgulă
                    <b-taginput
                        v-model="field.choices"
                        ellipsis
                        icon="label"
                        placeholder="valoare nouă"
                        aria-close-label="Șterge">
                    </b-taginput>
                    
                  </div>
                  <div class="checkbox-list">
                  <b-checkbox v-model="field.unique">
                    Valoare unică
                  </b-checkbox>
                  <b-checkbox v-model="field.required">
                    Valoare obligatorie
                  </b-checkbox>
                </div>
                  <VField
                    v-if="idImport && field.field_type == 'date'"
                    :label="`Column format #${index + 1}`"
                    rules="required"
                  >
                    <VDateformat v-model="field.field_format" />
                  </VField>
                </div>
              </div>

              <div class="columns">
                <div class="column is-7">
                  <br />
                  <b-button class="is-dark" @click="addColumn" expanded
                    >Adaugă o coloană nouă</b-button
                  >
                </div>
              </div>
            </div>
          </div>
        </div>

        <template #footer>
          <b-button class="is-primary" @click="passes(submit)">
            {{ idTable ? 'Salvează modificările' : 'Continuă' }}
          </b-button>
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
import ActionButtonDelete from '@/components/table/ActionButtonDelete'
import FieldService from '@/services/field'
import { mapState } from 'vuex'

export default {
  name: 'TableEdit',
  components: { ActionButtonDelete },
  data() {
    return {
      idTable: Number(this.$route.params.idTable),
      idImport: this.$route.query.idImport,
      name: this.$route.query.name,
      fields: [{ display_name: null, field_type: 'text', field_format: null }],
      fieldTypes: FieldService.getFieldTypes(),
      loading: false
    }
  },
  computed: {
    ...mapState('data', {
      database: state => state.database,
      table: function(state) {
        return this.idTable ? state.table[this.idTable] : {}
      },
      importData: state => state.import
    }),
    title() {
      return this.idTable && !this.idImport
        ? `Editează tabel — ${this.table.name}`
        : `Construiește un tabel`
    }
  },
  mounted() {
    if (!this.database) this.$store.dispatch('data/getDatabase')

    if (this.idTable) {
      this.$store.dispatch('data/getTable', this.idTable).then(() => {
        this.name = this.table.name
        this.fields = this.table.fields.map(e => ({
          ...e,
          disabled: true
        }))
      })
    } else if (this.idImport) {
      this.$store
        .dispatch('data/getImportData', this.idImport)
        .then(response => {
          this.fields = response.csv_field_mapping.map(e => {
            return {
              original_name: e.original_name,
              display_name: e.display_name,
              field_type: e.field_type,
              field_format: null
            }
          })
        })
    }
  },
  methods: {
    addColumn() {
      this.fields.push({
        display_name: null,
        field_type: null,
        field_format: null
      })
    },
    deleteColumn(index) {
      this.fields.length > 1 && this.fields.splice(index, 1)
    },
    submit() {
      const resource = {
        database: this.database.id,
        name: this.name,
        fields: this.fields,
        active: true
      }

      if (this.idImport) {
        // create new table & import
        //
        this.loading = true
        this.$store
          .dispatch('data/postTable', {
            import_id: this.importData.id,
            ...resource
          })
          .then(() => {
            this.loading = false

            this.$router.push({
              name: 'table-import-result',
              params: { idImport: this.importData.id },
              query: { name: this.$route.query.name }
            })
          })
          .catch(() => {
            this.loading = false
          })
      } else if (!this.idTable) {
        // create new table
        //
        this.$store.dispatch('data/postTable', resource).then(response => {
          this.$router.push({
            name: 'table-view',
            params: { idTable: response.id }
          })
        })
      } else {
        // update table
        //
        this.$store
          .dispatch('data/putTable', { idTable: this.idTable, data: resource })
          .then(() => {
            this.$router.push({
              name: 'table-view',
              params: { idTable: this.idTable }
            })
          })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.field-list {
  .column {
    margin-bottom: -15px;
  }
}
</style>
