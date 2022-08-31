<template>
  <div>
    <h1 class="title is-1">Autentifică-te</h1>

    <div class="subtitle">
      Introdu credențialele mai jos
    </div>

    <div class="form">
      <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
        <VField label="Email" rules="required">
          <b-input v-model="username" />
        </VField>

        <VField label="Parola" rules="required">
          <b-input v-model="password" type="password" />
        </VField>
        
        <div class="field">
          <b-button
            native-type="submit"
            class="button-submit is-primary"
            @click="passes(submit)"
          >
            Autentificare
          </b-button>
        </div>

        <div class="field">
          Nu ai cont?
          <router-link :to="{ name: 'register' }"
            >Creează un cont</router-link
          >
        </div>
      </ValidationObserver>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AccountLogin',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    submit() {
      this.$store.dispatch('login', {
        username: this.username,
        password: this.password
      })
    }
  }
}
</script>
