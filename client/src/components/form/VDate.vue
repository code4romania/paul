<template>
  <b-datepicker
    icon="calendar-blank-outline"
    iconPrev="arrow-left"
    iconNext="arrow-right"
    v-model="innerValue"
    v-bind="{ customClass, disabled, placeholder, readonly, inline }"
  />
</template>

<script>
export default {
  props: {
    customClass: String,
    disabled: String,
    placeholder: String,
    inline: Boolean,
    readonly: Boolean,
    value: null
  },
  data() {
    return {
      innerValue: this.value ? new Date(this.value) : null,
      locale: 'en-US'
    }
  },
  watch: {
    innerValue(input) {
      if (input) {
        const date = new Date(input.getTime())
        date.setHours(date.getHours() - input.getTimezoneOffset() / 60)
        // console.log('innerValue', date)
        // console.log(date.toISOString())

        this.$emit('input', date.toISOString().substr(0, 10))
      }
    },
    value(input) {
      const date = new Date(input)

      date.setHours(date.getHours() + date.getTimezoneOffset() / 60)
      // console.log('value', date)
      // console.log(date.toISOString())

      this.innerValue = input ? date : null
    }
  }
}
</script>
