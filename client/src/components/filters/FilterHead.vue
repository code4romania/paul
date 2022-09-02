<template>
  <div v-if="table">
    <BaseCard title="Filtrare">
      <template #actions>
        <div class="buttons">
          <b-button class="is-light" @click="resetFilters">
            Resetează filtre
          </b-button>
          <b-button class="is-dark" @click="openModalFilters">
            {{ filtersNotEmpty ? 'Editează filtre' : 'Adaugă filtre' }}
          </b-button>

          <template v-if="filterMode">
            <b-button class="is-primary" @click="saveFilters">Salvează</b-button>
          </template>
        </div>
      </template>

      <template #default v-if="filtersNotEmpty">
        <div class="card-container">
          <FilterDisplay
            :fields="table.fields"
            :filterData="filters"
            :filterMode="filterMode"
            class="is-horizontal"
          />
        </div>
      </template>
    </BaseCard>
  </div>
</template>

<script>
import ModalFilters from '@/components/modals/ModalFilters'
import FilterDisplay from '@/components/filters/FilterDisplay'
import ApiService from '@/services/api'
import { ToastService } from '@/services/buefy'
import { FilterQuery } from '@/utils/helpers'

import { mapState } from 'vuex'

export default {
  name: 'FilterHead',
  components: { FilterDisplay },
  props: {
    table: Object,
    filterMode: Boolean,
    filterData: Object,
    viewType: String
  },
  data() {
    return {}
  },
  computed: {
    ...mapState('data', {
      filters: function(state) {
        return state.filters[this.table.id]
      }
    }),
    filtersNotEmpty() {
      return this.filters && Object.keys(this.filters).length
    }
  },
  mounted() {
    if (this.filterMode) {
      this.$store.commit('data/setFilters', {
        idTable: this.table.id,
        filter: this.filterData
      })
    }
    
    if (this.filters) this.updateFilterQuery()
  },
  methods: {
    openModalFilters() {
      this.$buefy.modal.open({
        parent: this,
        component: ModalFilters,
        hasModalCard: true,
        trapFocus: true,
        width: '100%',
        props: {
          table: this.table
        },
        events: {
          submit: () => {
            this.updateFilterQuery()
          }
        }
      })
    },

    saveFilters() {
      const id =
        this.$route.params.idChart || this.$route.params.idCard || this.table.id

      ApiService.patch(`${this.viewType}/${id}/`, {
        filters: this.filters
      }).then(() => {
        ToastService.open('Filters have been saved')
      })
    },

    resetFilters() {
      this.$store.commit('data/setFilters', {
        idTable: this.table.id,
        filter: null
      })

      const __fields = this.$route.query.__fields
      const query = { ...(__fields && { __fields }) }

      this.$router.replace({ query }).catch(() => {})
      this.$emit('update', query)
    },

    updateFilterQuery() {
      // processing filterData object from Modal and updating page query

      // const filterData = this.filters
      let query = FilterQuery(this.filters)

      const __fields = this.$route.query.__fields
      const newQuery = Object.assign({ ...(__fields && { __fields }) }, query)

      this.$router
        .replace({
          query: newQuery
        })
        .catch(() => {})
        .then(() => {})

      this.$emit('update', newQuery)
    }
  }
}
</script>
