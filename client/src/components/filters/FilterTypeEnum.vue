<template>
  <div>
    <div class="is-size-6">
      <b-input
        v-model="search"
        placeholder="Search"
        icon-right="close"
        icon-right-clickable
        @icon-right-click="search = null"
      />
      <a @click.prevent="selectAll">Select all</a> |
      <a @click.prevent="selectNone">Select none</a>
    </div>

    <div class="checkbox-list is-4">
      <VField v-bind="{ rules }">
        <b-checkbox
          v-for="(choice, index) in filterChoices"
          :key="index"
          :native-value="choice"
          v-model="innerValue.values"
          @input="update"
        >
          {{ choice }}
        </b-checkbox>
      </VField>
    </div>
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
      search: null,
      filterChoices: [...this.field.choices],
      innerValue: this.computeValue()
    }
  },
  mounted() {},
  methods: {
    computeValue() {
      return JSON.parse(JSON.stringify({ ...this.value, type: 'enum' }))
    },
    selectAll() {
      const f = this.filterChoices.filter(
        e => this.innerValue.values.indexOf(e) == -1
      )
      this.innerValue.values = this.innerValue.values.concat(f)

      this.update()
    },
    selectNone() {
      if (this.search == null) this.innerValue.values = []
      else {
        this.innerValue.values = this.innerValue.values.filter(
          e => this.filterChoices.indexOf(e) == -1
        )
      }

      this.update()
    },
    update() {
      this.$emit('input', this.innerValue)
    }
  },
  watch: {
    value() {
      this.innerValue = this.computeValue()
    },

    search(value) {
      if (value != null)
        this.filterChoices = this.field.choices.filter(
          e => e.toLowerCase().indexOf(value.toLowerCase()) != -1
        )
      else this.filterChoices = this.field.choices.slice()
    }
  }
}
</script>

<style lang="scss" scoped>
/deep/ .b-checkbox.checkbox {
  align-items: flex-start;

  .check {
    margin-top: 3px;
  }
}
</style>
