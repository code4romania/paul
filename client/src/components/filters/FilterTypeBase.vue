<template>
  <ValidationObserver v-slot="{ passes, reset }" v-if="field" slim>
    <div class="filter-component">
      <fieldset class="filter-body" :disabled="innerValue.blank">
        <component
          v-model="innerValue"
          v-bind="{ field, rules: innerValue.blank ? '' : 'required' }"
          :is="getComponent(field.field_type)"
        />
      </fieldset>

      <div class="filter-buttons">
        <b-field>
          <b-checkbox :value="innerValue.blank" @input="toggleBlank">
            Show only empty or "blank" values.
          </b-checkbox>
        </b-field>

        <div class="buttons">
          <b-button
            type="is-dark is-outlined"
            :disabled="checkDisabled(field)"
            @click="$emit('remove', field.name, null, reset)"
          >
            Clear filter
          </b-button>

          <b-button type="is-dark" @click="passes(update)">
            Set filter
          </b-button>
        </div>
      </div>
    </div>
  </ValidationObserver>
</template>

<script>
import FieldService from '@/services/field'

import FilterTypeText from '@/components/filters/FilterTypeText'
import FilterTypeEnum from '@/components/filters/FilterTypeEnum'
import FilterTypeNumeric from '@/components/filters/FilterTypeNumeric'
import FilterTypeDate from '@/components/filters/FilterTypeDate'

export default {
  components: {
    FilterTypeText,
    FilterTypeEnum,
    FilterTypeNumeric,
    FilterTypeDate
  },
  props: {
    filterData: Object,
    field: Object,
    value: Object
  },
  data() {
    return {
      innerValue: this.computeValue()
    }
  },
  methods: {
    computeValue() {
      return this.value
        ? JSON.parse(JSON.stringify(this.value))
        : {
            type: null,
            values: [],
            blank: false
          }
    },
    getComponent(type) {
      return FieldService.getFilterComponent(type)
    },
    update() {
      this.$emit('input', this.innerValue)
    },
    toggleBlank(value) {
      this.innerValue = { ...this.innerValue, blank: value }
    },
    checkDisabled(field) {
      if (this.filterData[field.name] != null) return false
      return true
    }
  },
  watch: {
    value() {
      this.innerValue = this.computeValue()
    }
  }
}
</script>
