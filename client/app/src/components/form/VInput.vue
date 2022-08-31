<template>
  <b-input v-if="field.field_type == 'text'" v-model="innerValue" />
  <b-input v-else type="number" v-model.number="innerValue" />
</template>

<script>

export default {
  props: {
    value: null,
    field: Object,
    rules: {
      type: [Object, String],
      default: ''
    },
    name: String,
    label: String,
    column: String,
    description: String,
    labelInfo: String,
    mode: String,
    grouped: Boolean,
    expanded: Boolean
  },
  data() {
    return {
      innerValue: this.value
    }
  },
  watch: {
    innerValue(input) {
      this.$emit('input', input)
    },
    value(input) {
      this.innerValue = input
    }
  }
}
</script>
