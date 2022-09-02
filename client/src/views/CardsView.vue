<template>
  <div>
    <BaseTitle title="Management carduri" :hasBackButton="false" />

    <BaseCard title="Carduri" v-if="cards"
      ><template #actions>
        <router-link :to="{ name: 'card-edit' }" class="button is-primary">
          Adaugă un card
        </router-link>
      </template>

      <BaseTableAsync
        :table="table"
        :tableEntries="cards"
        tableActionsComponent="ActionsCards"
        @update="getCards"
      />
    </BaseCard>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'CardsView',
  components: {},
  data() {
    return {
      table: {
        id: 'tasks',
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
            props: { route: 'card-view', param: 'idCard' },
            display_name: 'Nume card'
          },
          {
            name: 'creation_date',
            field_type: 'date',
            display_name: 'Creat la'
          },
          {
            name: 'table',
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
              type: 'cards',
              action: 'add-to-dashboard'
            }
          },
          {
            name: 'actions',
            display_name: ' ',
            component: 'ActionsCards',
            custom_class: 'actions',
            sortable: false,
            sticky: true
          }
        ]
      }
    }
  },
  computed: mapState({
    cards: state => state.data.cards
  }),
  mounted() {
    this.getCards()
  },
  methods: {
    getCards(query) {
      this.$store.dispatch('data/getCards', query)
    }
  }
}
</script>
