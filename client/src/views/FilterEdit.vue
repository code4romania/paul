<template>
  <div v-if="database">
    <BaseTitle :title="title" />

    <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
      <BaseCard :title="$t('configureTable')">
        <div class="card-container">
          <div class="columns">
            <div class="column is-6">
              <VField
                :label="
                   $t('selectSourceCountLabel')"
                rules="required"
              >
                <b-select v-model.number="type" expanded>
                  <option value="0">{{ $t('') }}O singură sursă</option>
                  <option value="1">{{ $t('') }}Mai multe surse</option>
                </b-select>
              </VField>
            </div>
          </div>
          <div class="columns">
            <div class="column is-6">
              <VField :label="$t('newTableName')" rules="required">
                <b-input v-model="name" />
              </VField>
            </div>
          </div>
        </div>
        <div
          class="card-container"
          v-for="(link, link_index) in links"
          :key="`link-${link_index}`"
        >
          <div class="columns is-multiline">
            <div class="column is-6">
              <VField
                :label="$t('selectSourceLabel')"
                rules="required"
                :name="`Table #${link_index + 1} name`"
                :key="`field-table-${link_index}`"
              >
                <b-select
                  v-model="link.table"
                  @input="getTableFields($event, link_index)"
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
            <div class="column is-4" v-if="type">
              <VField
                :label="$t('linkField')"
                rules="required"
                :key="`field-link-${link_index}`"
                :name="`Table #${link_index + 1} link `"
                :labelInfo="$t('linkFieldLabelInfo')"
              >
                <b-select
                  v-model="link.join_field"
                  @input="resetLinkField(link_index)"
                  expanded
                >
                  <option
                    v-for="field in table[link.table]
                      ? table[link.table].sorted_fields
                      : []"
                    :value="field.id"
                    :key="link_index + '-' + field.id"
                    :disabled="checkLinkFieldtype(field.field_type, link_index)"
                  >
                    {{ field.display_name }}
                  </option>
                </b-select>
              </VField>
            </div>

            <div class="column is-12" v-if="table[link.table]">
              <VField
                :name="`Table #${link_index + 1} columns `"
                :label="$t('chooseColumnsToKeep')"
                rules="required"
              >
                <div class="checkbox-list is-1">
                  <b-checkbox
                    v-for="(field, index) in table[link.table].sorted_fields"
                    :key="'check' + index"
                    v-model="link.fields"
                    :native-value="field.id"
                  >
                    {{ field.display_name }}
                  </b-checkbox>
                </div>
              </VField>
            </div>
          </div>
        </div>

        <template #footer>
          <b-button class="is-primary" @click="passes(submit)"
            >{{ $t('continue') }}</b-button
          >
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { TableViewService } from '@/services/data'
import { ToastService } from '@/services/buefy'

export default {
  name: 'FilterEdit',
  data() {
    return {
      idTable: this.$route.params.idTable,
      name: null,
      type: 0,
      links: [{ table: null, join_field: null, fields: [] }],
      title: null
    }
  },
  computed: mapState('data', {
    database: state => state.database,
    table: state => state.table,
    tableView: state => state.tableView
  }),
  watch: {
    type() {
      // console.log(JSON.stringify(this.type))

      if (this.type)
        this.links.push({ table: null, join_field: null, fields: [] })
      else this.links.pop()
    }
  },
  mounted() {
    this.title = this.idTable ? this.$t('editProcessedData') : this.$t('addProcessedData')

    this.$store.dispatch('data/getDatabase')

    if (this.idTable)
      this.$store.dispatch('data/getTableView', this.idTable).then(() => {
        this.name = this.tableView.name
        this.type = Number(
          this.tableView.config.join_tables &&
            this.tableView.config.join_tables.length
        )

        this.$store
          .dispatch('data/getTable', this.tableView.config.primary_table.table)
          .then(() => {
            this.$set(this.links, 0, {
              ...this.tableView.config.primary_table
            })

            if (this.tableView.config.join_tables.length)
              this.$store
                .dispatch(
                  'data/getTable',
                  this.tableView.config.join_tables[0].table
                )
                .then(() => {
                  this.$set(this.links, 1, {
                    ...this.tableView.config.join_tables[0]
                  })
                })
          })
      })
  },
  methods: {
    getTableFields(value, index) {
      this.$store.dispatch('data/getTable', value).then(() => {
        Object.assign(this.links[index], { join_field: null, fields: [] })
      })
    },
    checkLinkFieldtype(type, index) {
      // console.log('checkLinkFieldtype', type, index)
      if (index == 0 || this.links[0].join_field == null) return false

      return (
        this.table[this.links[0].table].fields.find(
          e => e.id == this.links[0].join_field
        ).field_type != type
      )
    },
    resetLinkField(index) {
      if (index == 0) {
        this.links.forEach((e, i) => {
          i && (e.join_field = null)
        })
      }
    },
    submit() {
      const resource = {
        name: this.name,
        primary_table: this.links[0],
        join_tables: this.links.length > 1 ? [this.links[1]] : []
      }

      if (!this.idTable) {
        TableViewService.postTableView(resource).then(response => {
          ToastService.open(this.$t('viewCreated'))
          this.$router.push({
            name: 'filter-table-view',
            params: {
              idTable: response.id
            }
          })
        })
      } else {
        TableViewService.putTableView(this.idTable, resource).then(() => {
          ToastService.open(this.$t('viewUpdated'))
          this.$router.push({
            name: 'filter-table-view',
            params: {
              idTable: this.idTable
            }
          })
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.card-container {
  &:not(:last-child) {
    border-bottom: 1px solid $grey;
  }
}
</style>
