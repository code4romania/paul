<template>
  <div>
    <BaseTitle title="Utilizatori" />

    <ValidationObserver v-slot="{ passes }" tag="form" @submit.prevent>
      <BaseCard title="Change password" v-if="user">
        <template #actions></template>

        <template #footer>
          <b-button
            native-type="submit"
            class="is-primary"
            @click="passes(submit)"
          >
            Send request
          </b-button>
        </template>

        <template #default>
          <div class="card-container card-form">
            <b-loading :is-full-page="false" v-model="loading" />

            <div class="columns">
              <div class="column is-6">
                <VField label="Enter current password" rules="required">
                  <b-input type="password" v-model="current_password"/>
                </VField>

                <VField
                  label="Enter new password"
                  rules="required"
                  name="new_password"
                >
                  <b-input type="password" v-model="new_password"/>
                </VField>

                <VField
                  label="Repeat new password"
                  rules="required|confirmed:new_password"
                >
                  <b-input type="password" v-model="re_new_password"/>
                </VField>
              </div>
            </div>
          </div>
        </template>
      </BaseCard>
    </ValidationObserver>
  </div>
</template>

<script>
import UserService from '@/services/user'
import { ToastService } from '@/services/buefy'
import { mapState } from 'vuex'

export default {
  name: 'UserChangePass',
  data() {
    return {
      user: null,
      idUser: this.$route.params.idUser,
      loading: false,
      new_password: '',
      re_new_password: '',
      current_password: ''
    }
  },
  computed: mapState({
  }),
  mounted() {
    this.getUser()
  },
  methods: {
    getUser() {
      UserService.getUser(this.idUser).then(response => {
        this.user = response
      })
    },
    submit() {
      UserService.changePassword(
        this.new_password,
        this.re_new_password,
        this.current_password
      ).then(() => {
        this.$store.dispatch('logout')
        ToastService.open('Password has been changed, please login again')
      })
    }
  }
}
</script>
