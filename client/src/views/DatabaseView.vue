<template>
  <div v-if="database">
    <BaseTitle title="Manage database" :hasBackButton="false" />

    <BaseCard title="Tabele active"
      ><template #actions>
        <router-link :to="{ name: 'table-add' }" class="button is-primary">
          Adaugă tabel
        </router-link>
      </template>

      <BaseTable
        :data="database.active_tables"
        :fields="fields.active_tables"
      />
    </BaseCard>

    <BaseCard title="Tabele arhivate">
      <BaseTable
        :data="database.archived_tables"
        :fields="fields.archived_tables"
      />
    </BaseCard>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'DatabaseView',
  components: {},
  data() {
    return {
      fields: {
        active_tables: [
          {
            name: 'name',
            component: 'FieldRouterLink',
            props: { route: 'table-view', param: 'idTable' },
            display_name: 'Nume tabel'
          },
          {
            name: 'last_edit_date',
            field_type: 'datetime',
            display_name: 'Actualizat la'
          },
          {
            name: 'entries',
            display_name: 'Intrări',
            field_type: 'int'
          },
          {
            name: 'last_edit_user.username',
            display_name: 'Actualizat de'
          },
          {
            name: 'actions',
            display_name: ' ',
            component: 'ActionsDatabaseActive',
            custom_class: 'actions',
            sortable: false,
            sticky: true
          }
        ],
        archived_tables: [
          {
            name: 'name',
            component: 'FieldRouterLink',
            props: { route: 'table-view', param: 'idTable' },
            display_name: 'Nume tabel'
          },
          {
            name: 'last_edit_date',
            field_type: 'datetime',
            display_name: 'Data arhivării'
          },
          {
            name: 'entries',
            display_name: 'Intrări'
          },
          {
            name: 'owner.username',
            display_name: 'Arhivat de',
            component: 'FieldOwnerLink'
          },
          {
            name: 'actions',
            display_name: ' ',
            component: 'ActionsDatabaseArchived',
            custom_class: 'actions',
            sortable: false,
            sticky: true
          }
        ]
      }
    }
  },
  computed: mapState({
    database: state => state.data.database
  }),
  mounted() {
    this.$store.dispatch('data/getDatabase')
    this.$store.commit('data/setFilters', {})
  }
}
</script>
