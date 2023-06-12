<template>
  <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
    <BaseCard :title="$t('addATableView')">
      <div class="card-container" v-if="database">
        <div class="columns">
          <div class="column">
            <VField :label="$t('sourceFieldLabel')" rules="required">
              <b-select
                v-if="table"
                :placeholder="$t('selectAField')"
                v-model="sourceField"
                @input="linkField = null"
                expanded
              >
                <option
                  v-for="field in table.sorted_fields"
                  :value="field.name"
                  :key="field.id"
                >
                  {{ field.display_name }}
                </option>
              </b-select>
            </VField>
          </div>
          <div class="column">
            <VField :label="$t('tableLabel')" rules="required">
              <b-select
                :placeholder="$t('selectATable')"
                v-model="idTable"
                @input="getTableFields"
                expanded
              >
                <option
                  v-for="table in database.active_tables"
                  :value="table.id"
                  :key="table.id"
                >
                  {{ $t('table') }} – {{ table.data.name }}
                </option>
              </b-select>
            </VField>
          </div>

          <div class="column">
            <VField
              :label="$t('linkedFieldLabel')"
              :labelInfo="$t('linkedFieldInfo')"
              rules="required"
            >
              <b-select
                :placeholder="$t('selectAField')"
                v-model="linkField"
                :loading="loading"
                expanded
              >
                <option
                  v-for="field in linkTable.sorted_fields"
                  :value="field.name"
                  :key="field.id"
                  :disabled="checkLinkFieldtype(field.field_type)"
                >
                  {{ field.display_name }}
                </option>
              </b-select>
            </VField>
          </div>
        </div>
      </div>

      <template #footer>
        <b-button class="is-dark" @click="passes(addTableView)">
          {{ $t('addView') }}
        </b-button>
      </template>
    </BaseCard>
  </ValidationObserver>
</template>

<script>
import { TableService } from '@/services/data'
import { mapState } from 'vuex'

export default {
  name: 'TableEntityLinkCard',
  components: {},
  data() {
    return {
      linkField: null,
      sourceField: null,
      idTable: null,
      loading: false,
      fields: [],
      linkTable: { sorted_fields: [] }
    }
  },
  props: {
    table: Object
  },
  computed: mapState({
    database: state => state.data.database
  }),
  methods: {
    getTableFields() {
      this.loading = true
      this.linkField = null

      TableService.getTable(this.idTable).then(response => {
        this.linkTable = response
        this.loading = false
      })
    },
    addTableView() {
      this.$emit('input', {
        sourceField: this.sourceField,
        table: this.linkTable,
        linkField: this.linkField
      })
    },
    checkLinkFieldtype(type) {
      if (this.sourceField == null) return false

      return (
        this.table.fields.find(e => e.name == this.sourceField).field_type !=
        type
      )
    }
  },
  mounted() {
    if (!this.database) this.$store.dispatch('data/getDatabase')
  }
}
</script>
