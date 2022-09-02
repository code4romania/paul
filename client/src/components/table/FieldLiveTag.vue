<template>
  <div>
    <div
      class="tag"
      :class="{ 'is-success': props.schedule_enabled, 'is-danger': !props.schedule_enabled }"
      v-text="props.schedule_enabled ? 'Live' : 'Manual'"
    ></div>
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    props: Object
  }
}
</script>
