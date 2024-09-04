<template>
  <div>
    {{ croninfo }}
  </div>
</template>

<script>
import * as cronstrue from 'cronstrue/i18n'

export default {
  components: {},
  props: {
    props: Object,
    value: String
  },
  computed: {
    croninfo() {
      if (this.props.schedule_enabled)
        return this.props.schedule.cron && cronstrue.toString(this.props.schedule.cron)
      else 
        return null
    }
  }
}
</script>
