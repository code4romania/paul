<template>
  <div
    class="container is-fluid"
    :class="{ 'menu-closed': !menuActive }"
    id="app-container"
  >
    <nav class="navbar">
      <BaseMenu
        :isAdmin="user && user.is_admin"
        v-bind="{ menuActive }"
        @toggleMenu="menuActive = !menuActive"
      />
      <div class="navbar-menu">
        <div class="navbar-end">
          <router-link
            v-if="user"
            :to="{ name: 'user-profile', params: { idUser: user.id } }"
            class="navbar-item"
          >
            <figure class="avatar-image image is-pulled-left">
              <img v-if="user.avatar" :src="user.avatar" class="is-rounded" />

              <div v-else class="placeholder">
                <b-icon icon="account" class="is-size-4"></b-icon>
              </div>
            </figure>

            <p class="has-text-weight-semibold">{{ user.username }}</p>
          </router-link>

          <a href="#" @click="logout()" class="navbar-item"
            ><b-icon icon="power" class="is-size-3" /> <span>Log out</span></a
          >
        </div>
      </div>
    </nav>

    <div class="main-view">
      <router-view />
    </div>
  </div>
</template>

<script>
import BaseMenu from '@/components/BaseMenu.vue'
import { mapState } from 'vuex'

export default {
  name: 'Base',
  components: {
    BaseMenu
  },
  data() {
    return {
      menuActive: true
    }
  },
  computed: mapState({
    user: state => state.user
  }),
  mounted() {
    this.$store.dispatch('getActiveUser')
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar-item .image {
  margin-right: 8px;
  width: 40px;
  height: 40px;
}
</style>
