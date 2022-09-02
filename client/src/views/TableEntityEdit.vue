<template>
  <div>
    <BaseTitle :title="pageTitle" />

    <ValidationObserver
      v-slot="{ passes }"
      @submit.prevent
      slim
      v-if="table && entity"
    >
      <BaseCard :title="`Tabel – ${table.name}: ${pageTitle}`">
        <div class="card-container card-form">
          <div class="columns is-multiline">
            <div
              v-for="field in table.fields"
              :key="`field-${field.id}`"
              class="column is-6"
            >
              <VField :label="field.display_name" required="true">
                <component
                  :is="getComponent(field.field_type)"
                  v-model="entity[field.name]"
                  v-bind="{ field }"
                />
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
import { TableService } from '@/services/data'
import { ToastService } from '@/services/buefy'
import FieldService from '@/services/field'
import { mapState } from 'vuex'

export default {
  name: 'TableEntityEdit',
  components: {},
  data() {
    return {
      idTable: Number(this.$route.params.idTable),
      entity: null
    }
  },
  computed: {
    ...mapState({
      table: function(state) {
        return state.data.table[this.idTable]
      }
    }),
    pageTitle() {
      return this.$route.params.idEntity ? 'Editează intrarea' : 'Adaugă intrare nouă'
    }
  },
  mounted() {
    if (!this.table) this.$store.dispatch('data/getTable', this.idTable)

    if (this.$route.params.idEntity)
      TableService.getEntity(this.idTable, this.$route.params.idEntity).then(
        response => {
          this.entity = response.data
        }
      )
    else this.entity = {}
  },
  methods: {
    findField(name) {
      return this.table.find(e => e.name == name)
    },
    getComponent(type) {
      return FieldService.getComponent(type)
    },
    save() {
      // @TODO: update entries for TableEntityView after edit/delete
      // 1 - have a one-time consumable edit_id in vuex
      // 2 - query param
      // 3 - global EventBus?

      if (this.$route.params.idEntity)
        TableService.putEntity(
          this.idTable,
          this.$route.params.idEntity,
          this.entity
        ).then(() => {
          ToastService.open('Update successful')
          this.$router.go(-1)
        })
      else
        TableService.postEntity(this.idTable, this.entity).then(() => {
          ToastService.open('Add successful')
          this.$router.go(-1)
        })
    }
  }
}
</script>
