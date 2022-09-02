<template>
  <div>
    <h1 class="title is-1">Ai uitat parola?</h1>

    <template v-if="$route.query.confirmation == null">
      <div class="subtitle">
        Introdu adresa de e-mail si vei primi un mesaj cu instrucțiuni.
      </div>

      <div class="form">
        <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
          <VField label="Email" rules="required|email">
            <b-input v-model="email" placeholder="e@mail.com" />
          </VField>

          <b-button
            native-type="submit"
            class="button-submit is-primary"
            @click="passes(submit)"
          >
            Trimite instrucțiuni
          </b-button>
        </ValidationObserver>
      </div>
    </template>
    
    <template v-else>
      <div class="subtitle">
        Vei primi un email cu un link de resetare a parolei. Dacă nu îl găsești, te rugăm sa verifici și în directorul "spam".
      </div>
    </template>
  </div>
</template>

<script>
import UserService from '@/services/user'

export default {
  name: 'AccountForgotPass',
  data() {
    return {
      email: ''
    }
  },
  methods: {
    submit() {
      UserService.resetPassword(this.email).then(() => {
        this.$router.replace({ query: { confirmation: this.email } })
      })
    }
  }
}
</script>
