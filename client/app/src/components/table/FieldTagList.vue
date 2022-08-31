<template>
  <div class="tags">
    <b-tag
      v-for="(item, index) in Array.isArray(value) ? value : [value]"
      :key="index"
      >{{ item }}</b-tag
    >
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    props: Object,
    value: null
  }
}
</script>

<style lang="scss" scoped>
.tags {
  margin-top: -5px;
  margin-bottom: -11px !important;
}
</style>
