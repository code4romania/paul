<template>
  <div>
    <b-tag v-if="props.status=='Finished'"
      :class="{ 'is-success': props.success, 'is-danger': !props.success }"
      v-text="props.success ? $t('success') : $t('error')"
    />
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
