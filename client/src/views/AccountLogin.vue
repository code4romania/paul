<template>
  <div>
    <h1 class="title is-1">{{ $t('logIn') }}</h1>

    <div class="subtitle">
      {{ $t('enterCredentials') }}
    </div>

    <div class="form">
      <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
        <VField :label="$t('emailLabel')" rules="required">
          <b-input v-model="username" />
        </VField>

        <VField :label="$t('passwordLabel')" rules="required">
          <b-input v-model="password" type="password" />
        </VField>
        
        <div class="field">
          <b-button
            native-type="submit"
            class="button-submit is-primary"
            @click="passes(submit)"
          >
            {{ $t('performLogIn') }}
          </b-button>
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
