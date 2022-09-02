<template>
  <div>
    <h1 class="title is-1">Creează cont</h1>

    <template v-if="$route.query.confirmation == null">
      <div class="subtitle">
        Introdu un email și setează o parolă
      </div>

      <div class="form">
        <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
          <VField label="Email" rules="required">
            <b-input v-model="username" />
          </VField>

          <VField label="Parola" rules="required" name="password">
            <b-input v-model="password" type="password" />
          </VField>

          <VField label="Confirmă parola" rules="required|confirmed:password">
            <b-input v-model="re_password" type="password" />
          </VField>

          <b-button
            native-type="submit"
            class="button-submit is-primary"
            @click="passes(submit)"
          >
            Creează cont
          </b-button>
        </ValidationObserver>
      </div>
    </template>

    <div class="has-text-centered" v-else>
      <div class="subtitle">
        Vei primi un email cu un link de activare. <br>
        Dacă nu îl găsești, te rugăm sa verifici și în directorul "spam".

      </div>
      <br />
      <br />
      <b-button class="is-primary" @click="resend"
        >Resend activation link</b-button
      >
    </div>
  </div>
</template>

<script>
import UserService from '@/services/user'
import { ToastService } from '@/services/buefy'

export default {
  name: 'AccountRegister',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      re_password: ''
    }
  },
  methods: {
    submit() {
      this.$store
        .dispatch('registerUser', {
          username: this.username,
          email: this.username,
          password: this.password,
          re_password: this.re_password
        })
        .then(() => {
          // console.log(response)
          this.$router.replace({ query: { confirmation: this.username } })
        })
    },
    resend() {
      UserService.resend(this.$route.query.confirmation).then(() => {
        ToastService.open('E-mail has been sent')
      })
    }
  }
}
</script>
