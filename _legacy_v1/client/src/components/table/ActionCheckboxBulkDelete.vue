<template>
  <b-checkbox :value="idEntity" @input="onCheckDelete" />
</template>

<script>
export default {
  props: {
    idEntity: Number
  },
  methods: {
    onCheckDelete: function(checked) {
      this.$store.dispatch('data/updateBulkDeleteEntry', {
        entryId: this.idEntity,
        checked: checked,
      })
    }
  },
}
</script>
