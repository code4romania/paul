<template>
  <div>
    <h1 class="title is-1">Activate account</h1>

    <div class="subtitle" v-if="status != null">
      <template v-if="status">
        Account was activated successfully and is awaiting moderation from an
        administrator. <br> You will receive an e-mail shortly.
      </template>
      <template v-else>
        There was a problem activating your account. Please try again or contact your administrator.
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
