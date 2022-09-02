<template>
  <div>
    <b-tag
      :class="{ 'is-success': props.success, 'is-danger': !props.success }"
      v-text="props.success ? 'Success' : 'Error'"
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
