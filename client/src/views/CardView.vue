<template>
  <div v-if="card">
    <BaseTitle title="Card view" />

    <FilterHead
      v-if="table"
      v-bind="{ table, filterData: card.filters, viewType: 'cards' }"
      @update="getCardData"
      filterMode
    />

    <BaseCard :title="`Card — ${card.name}`">
      <template #actions>
        <div class="buttons">
          <router-link
            class="button is-dark"
            :to="{
              name: 'table-view',
              params: { idTable: card.config.table }
            }"
          >
            Vezi sursa de date
          </router-link>
          <router-link
            class="button is-primary"
            :to="{
              name: 'card-edit',
              params: { idCard }
            }"
          >
            Editează card
          </router-link>
        </div>
      </template>

      <template #default>
        <div class="card-container" v-if="table">
          Ultima actualizare: {{ table.last_edit_date | parseDate }}
          <span v-if="table.last_edit_user"
            >de
            {{
              table.last_edit_user.first_name +
                ' ' +
                table.last_edit_user.last_name
            }}
          </span>
        </div>
      </template>
    </BaseCard>

    <div class="columns" v-if="cardData">
      <div class="column is-4">
        <BaseCardChart :data="cardData.value" :title="card.name" />
      </div>
    </div>
  </div>
</template>

<script>
import { DataService } from '@/services/data'
import FilterHead from '@/components/filters/FilterHead'
import BaseCardChart from '@/components/charts/BaseCardChart'

import { mapState } from 'vuex'

export default {
  name: 'CardView',
  components: { FilterHead, BaseCardChart },
  props: {},
  data() {
    return {
      idCard: Number(this.$route.params.idCard),
      cardData: null
    }
  },
  computed: {
    ...mapState('data', {
      table: function(state) {
        return state.table[this.card.config.table]
      },
      card: state => state.card
    })
  },
  mounted() {
    this.$store.commit('data/setCard', null)

    this.$store.dispatch('data/getCard', this.idCard).then(() => {
      this.$store.dispatch('data/getTable', this.card.config.table).then(() => {
        if (!this.card.filters) this.getCardData()
      })
    })
  },
  methods: {
    getCardData() {
      DataService.getInstanceData('cards', this.idCard, this.$route.query).then(
        response => {
          this.cardData = response
        }
      )
    }
  }
}
</script>
