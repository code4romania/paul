<template>
  <div>
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
