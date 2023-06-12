<template>
  <div>
    <BaseTitle :title="$t('users')" :hasBackButton="false" />

    <BaseCard :title="$t('platformUsers')" v-if="users">
      <template #default>
        <BaseTableAsync
          :table="userTable"
          :tableEntries="users"
          tableActionsComponent="ActionsUser"
          @update="getUsers"
        />
      </template>
        <template #actions>
            <router-link :to="{ name: 'user-add' }" class="button is-primary">
                {{ $t('addUser') }}
            </router-link>
        </template>
    </BaseCard>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Users',
  data() {
    return {
      userTable: {
        id: 'users',
        default_fields: ['username', 'first_name', 'last_name', 'email'],
        fields: [
          {
            name: 'username',
            component: 'FieldRouterLink',
            props: { route: 'user-profile', param: 'idUser' },
            display_name: this.$t('userName')
          },
          {
            name: 'first_name',
            display_name: this.$t('firstName')
          },
          {
            name: 'last_name',
            display_name: this.$t('lastName')
          },
          {
            name: 'email',
            display_name: this.$t('email')
          }
        ]
      }
    }
  },
  computed: mapState({
    users: state => state.data.users
  }),
  mounted() {
    this.getUsers()
  },
  methods: {
    getUsers(query) {
      this.$store.dispatch('data/getUsers', query)
    }
  }
}
</script>
