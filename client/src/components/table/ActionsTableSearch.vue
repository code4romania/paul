<template>
  <div>
    <ActionButtonGoto
      icon="eye-outline"
      :path="{ name: 'entity-view', params: { idTable, idEntity: props.id } }"
    />

  </div>
</template>

<script>
import ActionButtonGoto from './ActionButtonGoto'

export default {
  components: {
    ActionButtonGoto
  },
  props: {
    idTable: Number,
    props: Object
  },
  methods: {}
}
</script>
