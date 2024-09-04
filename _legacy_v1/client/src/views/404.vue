<template>
  <div>
    <h1 class="title">
      <br />
      
      <p style="font-size: 96px">404</p>
      <h2>{{ $t('pageNotFound') }}</h2>
      
      <br /><br />
      <a href="/" class="button is-primary">{{ $t('startOver') }}</a>
    </h1>
  </div>
</template>

<script>
export default {
  name: 'Page404'
}
</script>

<style scoped lang="scss">
h1 {
  margin-top: 3rem;
  text-align: center;
}
</style>
