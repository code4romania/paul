<template>
  <div>
    <BaseTitle title="Date procesate" :hasBackButton="false" />

    <BaseCard title="Tabele procesate" v-if="tableViews"
      ><template #actions>
        <router-link :to="{ name: 'filter-edit' }" class="button is-primary">
          Adaugă tabel
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
            display_name: 'Nume tabel'
          },
          {
            name: 'creation_date',
            field_type: 'date',
            display_name: 'Creat la'
          },
          {
            name: 'tables',
            display_name: 'Date de intrare',
            component: 'FieldTagList'
          },
          {
            name: 'owner.username',
            display_name: 'Creat de'
          },
          {
            name: 'show_dashboard',
            display_name: 'Publică în dashboard',
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
