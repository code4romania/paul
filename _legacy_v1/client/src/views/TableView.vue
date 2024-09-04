<template>
  <div v-if="table">
    <BaseTitle
      :title="title"
      :backTo="filterMode ? 'filter-view' : 'database-view'"
    />

    <FilterHead
      v-bind="{
        table,
        filterMode,
        filterData: table.filters,
        viewType: filterMode ? 'filters' : null
      }"
      @update="getTableEntries"
    />

    <BaseCard :title="title">
      <template #title v-if="tableEntries">
        <span class="entries">{{ tableEntries.count }} {{ $t('entries') }}</span>
      </template>
      <template #actions>
        <div class="buttons">
          <b-button class="is-dark" @click="openModalColumns">
            {{ $t('changeTable') }}
          </b-button>

          <router-link
            class="button is-primary"
            :to="{
              name: filterMode ? 'filter-edit' : 'table-edit',
              params: { idTable }
            }"
            v-text="$t('edit')"
          />

          <router-link
            v-if="!filterMode"
            class="button is-primary"
            :to="{ name: 'entity-edit', params: { idTable } }"
          >
            {{ $t('addNewEntry') }}
          </router-link>

          <a :href="exportCsvPath" class="button is-primary" target="_blank">
            {{ $t('csvExport') }}
          </a>

          <a :href="exportXlsxPath" class="button is-primary" target="_blank">
            {{ $t('xlsxExport') }}
          </a>
        </div>
      </template>

      <template #default>
        <div class="card-container">
          {{ $t('lastUpdate') }}: {{ table.last_edit_date | parseDate }}
          <span
            v-if="table.last_edit_user"
            v-text="
              `${$t('by')} ${table.last_edit_user.first_name} ${table.last_edit_user.last_name}`
            "
          />
        </div>

        <BaseTableAsync
          v-bind="{ table, filterMode }"
          :tableEntries="tableEntries || {}"
          @update="getTableEntries"
          updateQueryNav
          customPerPage
        />
      </template>
    </BaseCard>
  </div>
</template>

<script>
import ModalColumns from '@/components/modals/ModalColumns'
import FilterHead from '@/components/filters/FilterHead'

import ApiService from '@/services/api'
import { QueryString } from '@/utils/helpers'
import { mapState } from 'vuex'

export default {
  name: 'TableView',
  components: { FilterHead },
  props: {
    filterMode: Boolean
  },
  data() {
    return {
      idTable: Number(this.$route.params.idTable)
    }
  },
  computed: {
    // @TODO: parameter for filter/table/chart api + simplify `tableViewEntries`, `tableView``

    ...mapState('data', {
      table: function(state) {
        return this.filterMode ? state.tableView : state.table[this.idTable]
      },
      tableEntries: function(state) {
        return this.filterMode ? state.tableViewEntries : state.tableEntries
      },
      filters: function(state) {
        return state.filters[this.idTable]
      }
    }),
    title() {
      return (
        (this.filterMode ? this.$t('processedData') : this.$t('table')) + ' – ' + this.table.name
      )
    },
    exportCsvPath() {
      return ApiService.getPath(
        (this.filterMode ? 'filters' : 'tables') +
          '/' +
          this.idTable +
          '/csv-export/?' +
          QueryString(this.$route.query),
        true
      )
    },
    exportXlsxPath() {
      return ApiService.getPath(
        (this.filterMode ? 'filters' : 'tables') +
          '/' +
          this.idTable +
          '/xlsx-export/?' +
          QueryString(this.$route.query),
        true
      )
    }
  },
  mounted() {
    this.$store.commit('data/setTableLinks', null)

    this.$store
      .dispatch(
        this.filterMode ? 'data/getTableView' : 'data/getTable',
        this.idTable
      )
      .then(() => {
        // if we have filters from the store/api then FilterHead handles entries update
        if (!this.table.filters || (!this.filterMode && !this.filters))
          this.getTableEntries()
      })
  },
  methods: {
    getTableEntries() {
      this.$store.commit('data/clearBulkDeleteItems')
      this.$store.dispatch(
        this.filterMode ? 'data/getTableViewEntries' : 'data/getTableEntries',
        {
          idTable: this.idTable,
          query: this.$route.query
        }
      )
    },

    openModalColumns() {
      this.$buefy.modal.open({
        parent: this,
        component: ModalColumns,
        hasModalCard: true,
        trapFocus: true,
        props: {
          table: this.table,
          filterMode: this.filterMode
        },
        events: {
          update: this.getTableEntries
        }
      })
    },

  }
}
</script>
