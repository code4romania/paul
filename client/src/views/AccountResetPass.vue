<template>
  <div>
    <h1 class="title is-1">{{ $t('passwordReset') }}</h1>

    <div class="subtitle">
      {{ $t('enterNewPassword') }}
    </div>

    <div class="form">
      <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
        <VField :label="$t('passwordLabel')" rules="required" name="new_password">
          <b-input type="password" v-model="new_password" />
        </VField>

        <VField
          rules="required|confirmed:new_password"
          label="$t('confirmPasswordLabel')"
        >
          <b-input type="password" v-model="re_new_password"
        /></VField>

        <b-button
          native-type="submit"
          class="button-submit is-primary"
          @click="passes(submit)"
        >
          {{ $t('save') }}
        </b-button>
      </ValidationObserver>
    </div>
  </div>
</template>

<script>
import UserService from '@/services/user'
import { ToastService } from '@/services/buefy'

export default {
  name: 'AccountResetPass',
  data() {
    return {
      new_password: '',
      re_new_password: ''
    }
  },
  mounted() {},
  methods: {
    submit() {
      UserService.resetPasswordConfirm(
        this.$route.params.uid,
        this.$route.params.token,
        this.new_password,
        this.re_new_password
      ).then(() => {
        ToastService.open(this.$t('passwordChanged'))
        this.$router.push({ name: 'login' })
      })
    }
  }
}
</script>
