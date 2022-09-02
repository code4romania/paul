<template>
  <div>
    <VField label="Choose filter mode" v-bind="{ rules }">
      <b-select v-model="innerValue.type" @input="reset">
        <option
          v-for="(choice, index) in choices"
          :key="`choice-${choice}`"
          :value="index"
        >
          {{ choice }}
        </option>
      </b-select>
    </VField>

    <template v-if="!isRelative">
      <VField
        :disabled="innerValue.blank"
        label="Enter date"
        v-bind="{ rules }"
      >
        <VDate v-model="innerValue.values[0]" @input="update" />
      </VField>

      <VField
        :disabled="innerValue.blank"
        label="Enter end date"
        v-if="innerValue.type == 'interval'"
        @input="update"
        v-bind="{ rules }"
      >
        <VDate v-model="innerValue.values[1]" @input="update" />
      </VField>
    </template>

    <VField label="Time frame" v-if="isRelative">
      <b-select v-model="innerValue.values[0]" @input="update">
        <option
          v-for="(type, key) in relativeDate"
          :value="key"
          :key="key"
          v-text="type"
        />
      </b-select>
    </VField>
  </div>
</template>

<script>
import { FilterOptions, FilterRelativeDate } from '@/services/field'

export default {
  props: {
    field: Object,
    value: Object,
    rules: String
  },
  data() {
    return {
      innerValue: this.computeValue(),
      choices: FilterOptions.date,
      relativeDate: FilterRelativeDate
    }
  },
  computed: {
    isRelative() {
      return this.innerValue.type == 'relative'
    }
  },
  methods: {
    computeValue() {
      return JSON.parse(JSON.stringify({ ...this.value }))
    },
    update() {
      if (this.innerValue.type != 'interval') this.innerValue.values.length = 1

      this.$emit('input', this.innerValue)
    },
    reset() {
      if (
        !this.isRelative &&
        new Date(this.innerValue.values[0]) == 'Invalid Date'
      ) {
        this.innerValue.values = []
      }

      this.update()
    }
  },
  watch: {
    value() {
      this.innerValue = this.computeValue()
    }
  }
}
</script>
