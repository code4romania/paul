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
        return this.props.crontab && cronstrue.toString(this.props.crontab)
      else 
        return null
    }
  }
}
</script>
