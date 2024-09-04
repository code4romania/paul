<template>
  <div>
    <h1 class="title is-1">{{ $t('createAccount') }}</h1>

    <template v-if="$route.query.confirmation == null">
      <div class="subtitle">
        {{ $t('enterEmailAndSetPassword') }}
      </div>

      <div class="form">
        <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
          <VField :label="$t('emailLabel')" rules="required">
            <b-input v-model="username" />
          </VField>

          <VField :label="$t('passwordLabel')" rules="required" name="password">
            <b-input v-model="password" type="password" />
          </VField>

          <VField :label="$t('confirmPasswordLabel')" rules="required|confirmed:password">
            <b-input v-model="re_password" type="password" />
          </VField>

          <b-button
            native-type="submit"
            class="button-submit is-primary"
            @click="passes(submit)"
          >
            {{ $t('createAccount') }}
          </b-button>
        </ValidationObserver>
      </div>
    </template>

    <div class="has-text-centered" v-else>
      <div class="subtitle">
        {{ $t('registerActivationConfirmation') }}
      </div>
      <br />
      <br />
      <b-button class="is-primary" @click="resend"
        >{{ $t('resendActivationLink') }}</b-button
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
        ToastService.open(this.$t('emailSent'))
      })
    }
  }
}
</script>
