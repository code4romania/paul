<template>
  <div>
    <VField label="Enter value" v-bind="{ rules }">
      <b-input
        v-model="innerValue.values[0]"
        @input="$emit('input', innerValue)"
      />
    </VField>
  </div>
</template>

<script>
export default {
  props: {
    field: Object,
    value: Object,
    rules: String
  },
  data() {
    return {
      innerValue: this.computeValue()
    }
  },
  methods: {
    computeValue() {
      return JSON.parse(JSON.stringify({ ...this.value, type: 'icontains' }))
    }
  },
  watch: {
    value() {
      this.innerValue = this.computeValue()
    }
  }
}
</script>
