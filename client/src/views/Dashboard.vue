<template>
  <div v-if="user">
    <BaseTitle :title="$t('dashboard')" :hasBackButton="false" />

    <div class="columns is-multiline">
      <template v-for="(card, index) in user.dashboard.cards">
        <div class="column is-4-desktop is-3-widescreen" :key="index">
          <router-link :to="{ name: 'card-view', params: { idCard: card.id } }">
            <BaseCardChart
              class="card-button"
              :data="cards[index]"
              :title="card.data.name"
            />
          </router-link>
        </div>
      </template>
    </div>

    <BaseCard :title="$t('selectedCharts')"
      ><template #actions>
        <router-link :to="{ name: 'charts-view' }" class="button is-primary">
          {{ $t('viewAll') }}
        </router-link>
      </template>

      <BaseTable :data="user.dashboard.charts" :fields="fields.charts" />
    </BaseCard>

    <BaseCard :title="$t('selectedProcessedData')"
      ><template #actions>
        <router-link :to="{ name: 'filter-view' }" class="button is-primary">
          {{ $t('viewAll') }}
        </router-link>
      </template>

      <BaseTable :data="user.dashboard.filters" :fields="fields.tableViews" />
    </BaseCard>

    <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
      <BaseCard :title="$t('searchRecords')">
        <div class="card-container">
          <div class="columns">
            <div class="column is-6">
              <VField :label="$t('searchTermLabel')" rules="required">
                <b-input v-model="searchTerm" />
              </VField>
            </div>
            <div class="column is-6">
            </div>
          </div>
        </div>
        <template #footer>
          <b-button class="is-primary" @click="passes(submitSearch)">
              {{ $t('search') }}
          </b-button>
        </template>
      </BaseCard>
    </ValidationObserver>

</div>
</template>

<script>
import { FilterQuery } from '@/utils/helpers'
import { DataService, SearchService } from '@/services/data'
import { mapState } from 'vuex'
import BaseCardChart from '@/components/charts/BaseCardChart'

export default {
  name: 'Dashboard',
  components: { BaseCardChart },
  data() {
    return {
      searchTerm: '',
      cards: [],
      fields: {
        charts: [
          {
            name: 'name',
            component: 'FieldRouterLink',
            props: { route: 'chart-view', param: 'idChart' },
            display_name: this.$t('chartName'),
          },
          {
            name: 'creation_date',
            field_type: 'date',
            display_name: this.$t('createdOn')
          },
          {
            name: 'table',
            display_name: this.$t('inputData'),
            component: 'FieldTagList'
          },
          {
            name: 'owner.username',
            display_name: this.$t('createdBy')
          },
          {
            name: 'actions',
            display_name: ' ',
            component: 'ActionsCharts',
            custom_class: 'actions',
            sortable: false,
            sticky: true
          }
        ],
        tableViews: [
          {
            name: 'name',
            component: 'FieldRouterLink',
            props: { route: 'filter-table-view', param: 'idTable' },
            display_name: this.$t('tableName'),
          },
          {
            name: 'creation_date',
            field_type: 'date',
            display_name: this.$t('createdOn')
          },
          {
            name: 'tables',
            display_name: this.$t('inputData'),
            component: 'FieldTagList'
          },
          {
            name: 'owner.username',
            display_name: this.$t('createdBy')
          },
          {
            name: 'actions',
            display_name: ' ',
            component: 'ActionsTableView',
            custom_class: 'actions',
            sortable: false,
            sticky: true
          }
        ]
      }
    }
  },
  computed: mapState({
    user: state => state.user
  }),
  mounted() {
    this.$store.dispatch('getActiveUser').then(() => {
      this.getCards()
    })
  },
  methods: {
    getCards() {
      this.user.dashboard.cards.forEach((e, index) => {
        DataService.getInstanceData(
          'cards',
          e.id,
          e.data.filters && FilterQuery(e.data.filters)
        ).then(response => {
          this.$set(this.cards, index, response.value)
        })
      })
    },
    submitSearch() {
      SearchService.searchEntries({
        query: this.searchTerm
      }).then(response => {
        console.log(response)
      })
    }
  }
}
</script>
