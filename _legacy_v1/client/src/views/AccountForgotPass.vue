<template>
  <div>
    <h1 class="title is-1">{{ $t('forgotPassword') }}</h1>

    <template v-if="$route.query.confirmation == null">
      <div class="subtitle">
        {{ $t('forgotPasswordInsertEmail') }}
      </div>

      <div class="form">
        <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
          <VField :label="$t('emailLabel')" rules="required|email">
            <b-input v-model="email" placeholder="test@example.com" />
          </VField>

          <b-button
            native-type="submit"
            class="button-submit is-primary"
            @click="passes(submit)"
          >
            {{ $t('forgotPasswordSendInstructions') }}
          </b-button>
        </ValidationObserver>
      </div>
    </template>
    
    <template v-else>
      <div class="subtitle">
        {{ $t('forgotPasswordInstructionsConfirmation') }}
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
