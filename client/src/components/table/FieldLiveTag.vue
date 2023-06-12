<template>
  <div>
    <div
      class="tag"
      :class="{ 'is-success': props.schedule_enabled, 'is-danger': !props.schedule_enabled }"
      v-text="props.schedule_enabled ? $t('liveTask') : $t('manualTask')"
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
