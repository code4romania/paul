<template>
  <div>
    <BaseTitle :title="$t('chartManagement')" :hasBackButton="false" />

    <BaseCard :title="$t('charts')" v-if="charts"
      ><template #actions>
        <router-link :to="{ name: 'chart-edit' }" class="button is-primary">
          $t('addNewChart')
        </router-link>
      </template>

      <BaseTableAsync
        :table="table"
        :tableEntries="charts"
        tableActionsComponent="ActionsCharts"
        @update="getCharts"
      />
    </BaseCard>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'ChartsView',
  components: {},
  data() {
    return {
      table: {
        id: 'charts',
        default_fields: [
          'name',
          'creation_date',
          'table',
          'owner.username',
          'show_dashboard'
        ],
        fields: [
          {
            name: 'name',
            component: 'FieldRouterLink',
            props: { route: 'chart-view', param: 'idChart' },
            display_name: this.$t('chartName')
          },
          {
            name: 'creation_date',
            field_type: 'date',
            display_name: this.$t('createdOn'),
          },
          {
            name: 'table',
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
              type: 'charts',
              action: 'add-to-dashboard'
            }
          }
        ]
      }
    }
  },
  computed: mapState({
    charts: state => state.data.charts
  }),
  mounted() {
    this.getCharts()
  },
  methods: {
    getCharts(query) {
      this.$store.dispatch('data/getCharts', query)
    }
  }
}
</script>
