<template>
  <div>
    <BaseTitle :title="$t('processedData')" :hasBackButton="false" />

    <BaseCard :title="$t('processedTables')" v-if="tableViews"
      ><template #actions>
        <router-link :to="{ name: 'filter-edit' }" class="button is-primary">
          {{ $t('addTable') }}
        </router-link>
      </template>

      <BaseTableAsync
        :table="table"
        :tableEntries="tableViews"
        tableActionsComponent="ActionsTableView"
        @update="getViews"
      />
    </BaseCard>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'FilterView',
  components: {},
  data() {
    return {
      table: {
        id: 'views',
        default_fields: [
          'name',
          'creation_date',
          'tables',
          'owner.username',
          'show_dashboard'
        ],
        fields: [
          {
            name: 'name',
            component: 'FieldRouterLink',
            props: { route: 'filter-table-view', param: 'idTable' },
            display_name: this.$t('tableName')
          },
          {
            name: 'creation_date',
            field_type: 'date',
            display_name: this.$t('createdOn'),
          },
          {
            name: 'tables',
            display_name: this.$t('inputData'),
            component: 'FieldTagList'
          },
          {
            name: 'owner.username',
            display_name: this.$t('createdBy'),
          },
          {
            name: 'show_dashboard',
            display_name: this.$t('publishToDashboard'),
            component: 'FieldCheckbox',
            centered: true,
            sortable: false,
            props: {
              type: 'filters',
              action: 'add-to-dashboard'
            }
          }
        ]
      }
    }
  },
  computed: mapState({
    tableViews: state => state.data.tableViews
  }),
  mounted() {
    this.$store.commit('data/setTableView', null)
    this.getViews()
  },
  methods: {
    getViews(query) {
      this.$store.dispatch('data/getTableViews', { query })
    }
  }
}
</script>
