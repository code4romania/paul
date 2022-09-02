<template>
  <div>
    <nav class="navbar">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          <Logo src="logo-default" width="80px" class="navbar-logo"/>
        </router-link>
      </div>

      <div class="navbar-menu">
        <div class="navbar-end">
          <router-link :to="{ name: 'forgot-password' }" class="navbar-item"
            >Ai uitat parola?</router-link
          >

          <div class="navbar-item">
            <router-link :to="{ name: 'login' }" class="button is-primary"
              >Autentifică-te</router-link
            >
          </div>
        </div>
      </div>
    </nav>

    <div class="form-view">
      <router-view />
    </div>
  </div>
</template>

<script>
import Logo from '@/components/Logo.vue'

export default {
  name: 'AccountBase',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  components: {
    Logo
  },
  mounted() {
    document.body.classList.add('account-view')
  },
  destroyed() {
    document.body.classList.remove('account-view')
  }
}
</script>

<style lang="scss">
@import '../assets/style/views/AccountBase';
</style>
