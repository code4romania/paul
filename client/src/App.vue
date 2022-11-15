<template>
  <div class="pt-6">
    <banner />
    <router-view />
  </div>
</template>

<script>
export default {
  metaInfo: {
    titleTemplate: (title) => (title !== '' ? `${title} - ` : '') + 'Paul',
  },
}
</script>
