<template>
  <div>
    <b-table
      ref="table"
      v-if="tableEntries && columns"
      :data="tableEntries.results"
      :loading="loading"
      :per-page.sync="perPage"
      :current-page.sync="page"
      :total="tableEntries.count"
      @page-change="onPageChange"
      paginated
      backend-pagination
      backend-sorting
      scrollable
      :sticky-header="fixedHeader"
      @sort="onSort"
    >
      <b-table-column
        v-for="(column, index) in columns"
        :key="`${index}-${column.name}-${columns.length}`"
        v-bind="{
          label: column.display_name || column.name,
          field: column.name,
          cellClass: column.custom_class,
          headerClass: column.custom_class,
          sticky: column.sticky,
          sortable: column.sortable !== false,
          centered: column.centered,
          numeric: ['int', 'float'].indexOf(column.field_type) != -1
        }"
      >
        <template v-slot="props">
          <template v-if="column.component">
            <component
              :is="column.component"
              v-bind="{
                props: props.row,
                ...column.props,
                value: getValue(props.row, column.name, column.field_type)
              }"
              @update="$emit('update', query)"
            />
          </template>

          <template v-else>
            {{ getValue(props.row, column.name, column.field_type) }}
          </template>
        </template>
      </b-table-column>

      <template slot="bottom-left" v-if="customPerPage">
        <div class="pagination-per-page">
          Listează
          <div class="control">
            <input
              class="input"
              type="number"
              :value="perPage"
              @keyup.enter="$event.target.blur()"
              @blur="onPerPageChange"
            />
          </div>
          intrări pe pagină.

          <span>
            Listare {{ (page - 1) * perPage + 1 }} din
            {{ Math.min(page * perPage, tableEntries.count) }}
          </span>
        </div>

        <div class="pagination-jump" v-if="tableEntries.count / perPage > 4">
          <div class="control">
            <input
              placeholder="Mergi la pagina"
              class="input"
              type="number"
              @keyup.enter="$event.target.blur()"
              @blur="onPageJump"
            />
          </div>
        </div>
      </template>

      <template slot="empty">
        <p>
          No data to display.
        </p>
      </template>
    </b-table>
  </div>
</template>

<script>
import ActionsCards from './ActionsCards'
import ActionsCharts from './ActionsCharts'
import ActionsPlugin from './ActionsPlugin'
import ActionsTable from './ActionsTable'
import ActionsTableEntity from './ActionsTableEntity'
import ActionsTableView from './ActionsTableView'
import ActionsUser from './ActionsUser'

import FieldCheckbox from './FieldCheckbox'
import FieldCronInfo from './FieldCronInfo'
import FieldLiveTag from './FieldLiveTag'
import FieldPluginTaskDetail from './FieldPluginTaskDetail'
import FieldOwnerLink from './FieldOwnerLink'
import FieldRouterLink from './FieldRouterLink'
import FieldStatusTag from './FieldStatusTag'
import FieldTagList from './FieldTagList'

import FieldService from '@/services/field'
import getNestedObj from 'lodash.get'

import { mapState } from 'vuex'

const maximumPerPage = 100

export default {
  components: {
    ActionsCards,
    ActionsCharts,
    ActionsPlugin,
    ActionsTable,
    ActionsTableEntity,
    ActionsTableView,
    ActionsUser,

    FieldCronInfo,
    FieldCheckbox,
    FieldLiveTag,
    FieldPluginTaskDetail,
    FieldOwnerLink,
    FieldRouterLink,
    FieldStatusTag,
    FieldTagList
  },
  data() {
    return {
      idTable: this.table.id,
      perPage: this.$route.query.perPage || 10,
      page: this.$route.query.page ? Number(this.$route.query.page) : 1,
      orderBy: this.$route.query.orderBy || null
    }
  },
  props: {
    table: Object,
    tableEntries: Object,
    filterMode: Boolean,
    customPerPage: Boolean,
    updateQueryNav: { type: Boolean, default: false },
    tableActionsComponent: { type: String, default: 'ActionsTable' },
    fixedHeader: { type: Boolean, default: false },
    fullHeight: { type: Boolean, default: false }
  },
  computed: {
    ...mapState('data', {
      loading: function(state) {
        return state.loading[this.idTable]
      }
    }),
    columns() {
      if (this.table == null) return

      let selectedFields = this.$route.query.__fields
        ? this.$route.query.__fields.split(',')
        : this.table.default_fields

      const fields = []

      selectedFields.forEach(e => {
        const field = this.table.fields.find(f => f.name == e)
        field && fields.push({ ...field })
      })

      if (!this.filterMode)
        fields.push({
          name: 'actions',
          custom_class: 'actions',
          component: this.tableActionsComponent,
          display_name: ' ',
          sticky: true,
          sortable: false,
          props: {
            idTable: this.idTable
          }
        })

      return fields
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize)
      this.onResize()
    })
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize)
  },
  methods: {
    getValue(row, field, type) {
      const obj = row.data ? row.data : row
      const value = getNestedObj(obj, field)

      return value != null ? FieldService.getParsedValue(value, type) : null
    },
    updateQueryRequest(query) {
      const newQuery = Object.assign({}, this.$route.query, query)

      if (this.updateQueryNav) {
        this.$router
          .push({
            query: newQuery
          })
          .catch(() => {})
      }

      this.$emit('update', newQuery)
    },
    updateTableHeight() {
      // TODO: Find a way to not require using setTimeout
      this.fullHeight &&
        setTimeout(() => {
          const $tableWrapper = this.$refs.table.$el.querySelector(
            '.table-wrapper'
          )
          const top =
            window.pageYOffset + $tableWrapper.getBoundingClientRect().top
          // TODO: Find where 120px is coming from
          const height = window.innerHeight - top - 120
          $tableWrapper.setAttribute('style', `height: ${height}px`)
        }, 500)
    },
    onPageJump(event) {
      let page = parseInt(event.target.value)
      const total = Math.ceil(this.tableEntries.count / this.perPage)

      if (page == this.page) return

      if (page) {
        if (page < 0) page = 1
        if (page > total) page = total

        this.page = page
        this.onPageChange(this.page)
        event.target.value = null
      }
    },
    onPageChange(page) {
      // console.log('onPageChange', page)
      this.updateQueryRequest({ page })
    },
    onPerPageChange(event) {
      let perPage = Math.abs(parseInt(event.target.value))

      if (perPage == this.perPage) return

      this.perPage = Math.min(perPage, maximumPerPage)
      if (perPage > this.tableEntries.count)
        this.perPage = this.tableEntries.count
      this.updateQueryRequest({ perPage: this.perPage })
    },
    onSort(field, order) {
      this.updateQueryRequest({ __order: (order == 'desc' ? '-' : '') + field })
    },
    onResize() {
      this.updateTableHeight()
    }
  },
  watch: {
    page() {
      this.updateTableHeight()
    },
    perPage() {
      this.updateTableHeight()
    }
  }
}
</script>
