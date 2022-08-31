<template>
  <a href="" @click.prevent="updateTable">
    <b-icon icon="archive-outline" />
  </a>
</template>

<script>
export default {
  props: {
    idTable: Number
  },
  methods: {
    updateTable() {
      this.$store.dispatch('data/patchTable', {
        idTable: this.idTable,
        data: { active: false }
      })
    }
  }
}
</script>
