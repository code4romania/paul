<template>
  <header class="main-header">
    <div class="back-button" v-if="hasBackButton">
      <b-button @click="goBack" iconLeft="arrow-left">
        Înapoi
      </b-button>
    </div>
    <p class="title">{{ title }}</p>
  </header>
</template>

<script>
export default {
  name: 'BaseTitle',
  components: {},
  props: {
    title: String,
    hasBackButton: {
      type: Boolean,
      default: true
    },
    backTo: String
  },
  methods: {
    goBack() {
      if (!this.backTo) this.$router.go(-1)
      else this.$router.push({ name: this.backTo })
    }
  }
}
</script>
