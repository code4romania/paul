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

    <BaseCard :title="$t('searchRecords')">
      <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
        <div class="card-container">
          <div class="columns">
            <div class="column is-6">
              <VField :label="$t('searchTermLabel')" rules="required">
                <b-input v-model.lazy="searchInput" />
              </VField>
            </div>
            <div class="column is-6">
              <br>
              <b-button class="is-primary" @click="passes(submitSearch)">
                  {{ $t('search') }}
              </b-button>
            </div>
          </div>
        </div>
      </ValidationObserver>

      <template v-if="searchTables">
        <BaseCard v-for="searchTable in searchTables" :title="searchTable.name" :key="`searchResultCard${searchTable.id}`">
          <BaseTableAsync
            :key="'searchResultTable'+searchTable.id"
            :table="searchTable"
            :tableEntries="searchTableResults[searchTable.id] || {}"
            @update="updateTableEntries(searchTable.id, $event)"
            tableActionsComponent="ActionsTableSearch"
          />
        </BaseCard>
      </template>

    </BaseCard>

</div>
</template>

<script>
import { FilterQuery } from '@/utils/helpers'
import { DataService, SearchService, TableService } from '@/services/data'
import { mapState } from 'vuex'
import BaseCardChart from '@/components/charts/BaseCardChart'

export default {
  name: 'Dashboard',
  components: { BaseCardChart },
  data() {
    return {
      searchInput: '',
      searchTerm: '',
      searchTables: [],
      searchTableIds: [],
      searchTableResults: {},
      searchFilterMode: false,
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
        ],
        results: [
          {
            name: 'context',
            display_name: 'Context'
          },
          {
            name: 'actions',
            display_name: 'Actions',
            // component: 'ActionsTableView',
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
      if (this.user.language) {
        this.$i18n.locale = this.user.language
      }
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
    updateTableEntries(tableId, queryPagination) {
      let query = {}
      if (queryPagination) {
        query = {search: this.searchTerm, page: queryPagination.page}
      } else {
        query = {search: this.searchTerm}
      }

      TableService.getEntries(tableId, query).then(response => {
        this.$set(this.searchTableResults, tableId, response)
      })
    },
    submitSearch() {
      this.searchTables = []
      this.searchTableIds = []
      this.searchTableResults = {}
      this.searchTerm = this.searchInput

      SearchService.searchEntries({
        query: this.searchTerm
      }).then(response => {
        let resultTableIds = []
        for (const item of response) {
          resultTableIds.push(item.table)
        }
        this.searchTableIds = resultTableIds

        let resultTables = []
        this.searchTableIds.forEach(tableId => {
          TableService.getTable(tableId).then(response => {
            resultTables.push(response)
          })
          this.updateTableEntries(tableId)
        })
        this.searchTables = resultTables
      })
    }
  }
}
</script>
