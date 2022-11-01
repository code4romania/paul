<template>
  <div class="banner">
    <div class="container is-fluid">
      <div>
        <Logo
          src="code4romania"
          width="102"
          style="vertical-align: middle; margin-right: 20px"
        />
        <span
          >O soluție
          <a
            href="https://code4.ro/ro"
            style="text-decoration: underline; color: black"
          >
            Code for Romania</a
          >
          și
          <a
            href="https://dor.ro"
            style="text-decoration: underline; color: black"
            >Media DOR</a
          >.
          <a
            href="https://code4.ro/ro/putem"
            style="text-decoration: underline;color: blue"
            >Află mai multe.</a
          ></span
        >
      </div>
    </div>
  </div>
</template>

<script>
import Logo from '@/components/Logo'

export default {
  name: 'Banner',
  components: {
    Logo
  }
}
</script>

<style scoped>
  .banner {
    box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.1);
    background-color: #FFF; 
    font-size: 12px; 
    padding: 6px 0; 
    color: #000;
    z-index: 40;
    position: fixed;
    right: 0;
    left: 0;
    top: 0;
  }
</style>
