<template>
  <router-link :to="path">
    <b-icon :icon="icon" />
  </router-link>
</template>

<script>
export default {
  props: {
    icon: String,
    path: [String, Object]
  }
}
</script>
