<template>
  <div>
    <b-table
      v-if="data && fields"
      :data="data"
      :per-page="10"
      :paginated="data.length > 10"
      scrollable
    >
      <b-table-column>
        <template v-slot="props">
          <template v-if="column.component">
          </template>

          <template v-else>
            {{ props.row.data }}
          </template>
        </template>
      </b-table-column>

      <template slot="empty">
        <p class="has-text-centered">
          {{ $t('noDataToDisplay') }}
        </p>
      </template>
    </b-table>
  </div>
</template>

<script>
// import ActionsCharts from './ActionsCharts'
// import ActionsDatabaseArchived from './ActionsDatabaseArchived'
// import ActionsDatabaseActive from './ActionsDatabaseActive'
// import ActionsTableView from './ActionsTableView'
// import ActionsTable from './ActionsTable'

// import FieldOwnerLink from './FieldOwnerLink'
// import FieldTagList from './FieldTagList'
// import FieldCheckbox from './FieldCheckbox'
// import FieldRouterLink from './FieldRouterLink'

// import FieldService from '@/services/field'
// import getNestedObj from 'lodash.get'

export default {
  components: {
    // ActionsCharts,
    // ActionsDatabaseArchived,
    // ActionsDatabaseActive,
    // ActionsTableView,
    // ActionsTable,
    // FieldOwnerLink,
    // FieldTagList,
    // FieldCheckbox,
    // FieldRouterLink
  },
  data() {
    return {}
  },
  props: {
    fields: Array,
    data: Array
  },
  methods: {

  }
}
</script>
