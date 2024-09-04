<template>
  <div>
    <h1 class="title is-1">{{ $t('activateAccount') }}</h1>

    <div class="subtitle" v-if="status != null">
      <template v-if="status">
        {{ $t('activateAccountSuccess') }}
        
      </template>
      <template v-else>
        {{ $t('activateAccountFailed') }}
      </template>
    </div>
  </div>
</template>

<script>
import UserService from '@/services/user'

export default {
  name: 'AccountActivate',
  data() {
    return {
      status: null
    }
  },
  mounted() {
    UserService.activate(this.$route.params.uid, this.$route.params.token)
      .then(() => {
        this.status = true
      })
      .catch(() => {
        this.status = false
      })
  },
  methods: {}
}
</script>
