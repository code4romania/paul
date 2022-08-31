<template>
  <div>
    <VField label="Choose filter mode" v-bind="{ rules }">
      <b-select v-model="innerValue.type" @input="update">
        <option
          v-for="(choice, index) in choices"
          :key="`choice-${choice}`"
          :value="index"
        >
          {{ choice }}
        </option>
      </b-select>
    </VField>

    <VField label="Enter value" v-bind="{ rules }">
      <b-input
        type="number"
        v-model.number="innerValue.values[0]"
        @input="update"
      />
    </VField>

    <VField
      label="Enter end value"
      v-bind="{ rules }"
      v-if="innerValue.type == 'interval'"
    >
      <b-input
        type="number"
        v-model.number="innerValue.values[1]"
        @input="update"
      />
    </VField>
  </div>
</template>

<script>
import { FilterOptions } from '@/services/field'

export default {
  props: {
    field: Object,
    value: Object,
    rules: String
  },
  data() {
    return {
      type: null,
      choices: FilterOptions[this.field.field_type],
      innerValue: this.computeValue()
    }
  },
  methods: {
    computeValue() {
      return JSON.parse(JSON.stringify(this.value))
    },
    update() {
      if (this.innerValue.type != 'interval') this.innerValue.values.length = 1

      this.$emit('input', this.innerValue)
    }
  },
  watch: {
    value() {
      this.innerValue = this.computeValue()
    }
  }
}
</script>
