<template>
  <div style="background: white; font-size: 12px; padding: 6px 0; color: black">
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
