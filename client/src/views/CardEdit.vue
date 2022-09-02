<template>
  <div>
    <BaseTitle title="Editează card" />

    <ValidationObserver
      v-slot="{ passes }"
      @submit.prevent
      slim
      v-if="cardConfig"
    >
      <BaseCard title="Configurare">
        <div class="card-container card-form">
          <div class="columns is-multiline">
            <div class="column is-6">
              <VField label="Nume" rules="required">
                <b-input v-model="cardConfig.name" />
              </VField>

              <VField
                label="Alege o sursă de date pe care deja le-ai încărcat în platformă"
                v-if="database"
                rules="required"
              >
                <b-select expanded v-model="cardConfig.table" @input="getTable">
                  <option
                    v-for="(table, key) in database.active_tables"
                    :value="table.id"
                    :key="key"
                    v-text="table.data.name"
                  />
                </b-select>
              </VField>

              <VField
                label="Funcția de agregare"
                rules="required"
                v-if="table"
              >
                <b-select expanded v-model="cardConfig.data_column_function">
                  <option
                    v-for="(func, key) in cardFunctions"
                    :value="key"
                    :key="key"
                    v-text="func"
                  />
                </b-select>
              </VField>

              <VField
                label="Alege sursa de date pe care vrei să le calculezi"
                rules="required"
                v-if="table && cardConfig.data_column_function != 'Count'"
              >
                <b-select expanded v-model="cardConfig.data_column">
                  <option
                    v-for="(field, key) in table.sorted_fields.filter(isNumeric)"
                    :value="field.id"
                    :key="key"
                    v-text="field.display_name"
                  />
                </b-select>
              </VField>
            </div>
          </div>
        </div>

        <template #footer>
          <b-button class="is-primary" @click="passes(save)">
            Salvează modificările
          </b-button>
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
import ChartService from '@/services/chart'
import FieldService from '@/services/field'
import { TableService } from '@/services/data'
import { mapState } from 'vuex'

export default {
  name: 'CardEdit',
  components: {},
  data() {
    return {
      idCard: Number(this.$route.params.idCard),
      table: null,
      cardConfig: {
        y_axis_function: 'Count'
      },
      cardFunctions: ChartService.getFunctions(),
      isNumeric: FieldService.isNumeric
    }
  },
  computed: {
    ...mapState({
      database: state => state.data.database,
      card: state => state.data.card
    })
  },
  mounted() {
    if (!this.database) this.$store.dispatch('data/getDatabase')

    if (this.idCard) {
      this.$store.dispatch('data/getCard', this.idCard).then(() => {
        this.cardConfig = { ...this.card.config }

        this.getTable(this.cardConfig.table)
      })
    }
  },
  methods: {
    getTable(id) {
      TableService.getTable(id).then(response => {
        this.table = response
      })
    },
    save() {
      if (this.idCard)
        this.$store
          .dispatch('data/updateCard', {
            id: this.idCard,
            data: this.cardConfig
          })
          .then(this.redirect)
      else
        this.$store
          .dispatch('data/createCard', this.cardConfig)
          .then(this.redirect)
    },
    redirect(response) {
      this.$router.push({
        name: 'card-view',
        params: {
          ...(response.id && { idCard: response.id })
        }
      })
    }
  }
}
</script>
