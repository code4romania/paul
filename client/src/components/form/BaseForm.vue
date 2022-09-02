<template>
  <ValidationObserver v-slot="{ passes }" @submit.prevent slim>
    <BaseCard :title="title">
      <template #actions>
        <a class="is-size-4 button-close" @click.prevent="$emit('close')"
          ><b-icon icon="close"
        /></a>
      </template>
      <div class="card-container card-form">
        <div class="columns is-multiline">
          <div
            v-for="(field, key) in options.actions.PUT"
            :key="key"
            class="column is-8"
          >
            <VField :label="field.label">
              <component
                :is="getComponent(field.type)"
                v-model="model[key]"
                v-bind="{ field: { ...field, field_type: 'text' } }"
              />
            </VField>
          </div>
        </div>
      </div>

      <template #footer>
        <b-button class="is-primary" @click="passes(save)">
          Save changes
        </b-button>
      </template>
    </BaseCard>
  </ValidationObserver>
</template>

<script>
// import { ToastService } from '@/services/buefy'
import FieldService from '@/services/field'
// import { mapState } from 'vuex'

export default {
  name: 'TableEntityEdit',
  components: {},
  props: { title: String, options: Object, entity: Object },
  data() {
    return {
      model: { ...this.entity }
    }
  },
  mounted() {},
  methods: {
    getComponent(type) {
      return FieldService.getComponent(type)
    },
    save() {
      this.$emit('update:entity', this.model)
      this.$emit('save')
    }
  }
}
</script>
