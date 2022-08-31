<template>
  <b-select
    v-model="innerValue"
    v-bind="{ customClass, disabled, placeholder, readonly }"
    expanded
  >
    <option
      v-for="(choice, index) in field.choices"
      :key="`option-${index}`"
      :value="choice"
      >{{ choice }}</option
    >
  </b-select>
</template>

<script>
export default {
  props: {
    field: Object,
    customClass: String,
    disabled: String,
    placeholder: { type: String, default: 'Select' },
    readonly: Boolean,
    value: null
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
