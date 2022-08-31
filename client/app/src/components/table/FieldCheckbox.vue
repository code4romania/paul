<template>
  <div>
    <b-checkbox :value="props.data.show_in_dashboard" @input="onChange" />
  </div>
</template>

<script>
import ApiService from '@/services/api'
import { ToastService } from '@/services/buefy'

export default {
  props: {
    name: String,
    action: String,
    type: String,
    props: Object
  },
  methods: {
    onChange() {
      ApiService.get(`${this.type}/${this.props.id}/${this.action}/`).then(
        () => {
          ToastService.open('Property updated')
        }
      )
    }
  }
}
</script>
