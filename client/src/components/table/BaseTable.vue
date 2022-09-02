<template>
  <div>
    <b-table
      v-if="data && fields"
      :data="data"
      :per-page="10"
      :paginated="data.length > 10"
      scrollable
    >
      <b-table-column
        v-for="(column, index) in fields"
        :key="`${column.name}-${index}`"
        v-bind="{
          label: column.display_name || column.name,
          field: column.name,
          cellClass: column.custom_class,
          headerClass: column.custom_class,
          sticky: column.sticky,
          centered: column.centered,
          sortable: column.sortable !== false
        }"
        :custom-sort="customSort(column.name)"
      >
        <template v-slot="props">
          <template v-if="column.component">
            <component
              :is="column.component"
              v-bind="{
                props: props.row,
                ...column.props,
                value: getValue(props.row.data, column.name, column.field_type)
              }"
            ></component>
          </template>

          <template v-else>
            {{ getValue(props.row.data, column.name, column.field_type) }}
          </template>
        </template>
      </b-table-column>

      <template slot="empty">
        <p class="has-text-centered">
          No data to display.
        </p>
      </template>
    </b-table>
  </div>
</template>

<script>
import ActionsCharts from './ActionsCharts'
import ActionsDatabaseArchived from './ActionsDatabaseArchived'
import ActionsDatabaseActive from './ActionsDatabaseActive'
import ActionsTableView from './ActionsTableView'
import ActionsTable from './ActionsTable'

import FieldOwnerLink from './FieldOwnerLink'
import FieldTagList from './FieldTagList'
import FieldCheckbox from './FieldCheckbox'
import FieldRouterLink from './FieldRouterLink'

import FieldService from '@/services/field'
import getNestedObj from 'lodash.get'

export default {
  components: {
    ActionsCharts,
    ActionsDatabaseArchived,
    ActionsDatabaseActive,
    ActionsTableView,
    ActionsTable,
    FieldOwnerLink,
    FieldTagList,
    FieldCheckbox,
    FieldRouterLink
  },
  data() {
    return {}
  },
  props: {
    fields: Array,
    data: Array
  },
  methods: {
    getValue(row, field, type) {
      // console.log(row, field, type)
      const value = getNestedObj(row, field)
      return value != null ? FieldService.getParsedValue(value, type) : null
    },
    customSort(field) {
      return FieldService.getSortFunction(field)
    }
  }
}
</script>
