<template>
  <div>
    <router-link
      class="has-text-weight-semibold"
      :to="{
        name: route,
        params: { ...$route.params, [param]: props.id }
      }"
      v-text="value"
    />
  </div>
</template>

<script>
export default {
  components: {},
  props: {
    props: Object,
    route: String,
    param: String,
    value: null
  }
}
</script>
