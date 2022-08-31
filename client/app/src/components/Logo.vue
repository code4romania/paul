<template>
  <img :src="logoSrc" alt="" />
</template>

<script>
export default {
  name: 'Logo',
  props: {
    src: {
      type: String
    }
  },
  computed: {
    logoSrc: function() {
      var images = require.context('../assets/img/', false, /\.svg$/)
      return images('./' + this.src + '.svg')
    }
  }
}
</script>
