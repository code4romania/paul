import Vue from 'vue'
import Vuex from 'vuex'
import router from '@/router'

import UserService from '@/services/user'
import TokenService from '@/services/storage'

import data from './modules/data'
import plugin from './modules/plugin'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: TokenService.getToken(),
    user: null,
    users: null
  },
  mutations: {
    login(state, token) {
      state.token = token
    },
    logout(state) {
      state.token = null
    },
    setUsers(state, data) {
      state.users = data
    },
    setUser(state, data) {
      state.user = data
    }
  },
  actions: {
    login({ commit }, { username, password }) {
      return UserService.login(username, password)
        .then(response => {
          commit('login', response)

          router.replace(
            router.history.current.query.redirect || '/app/dashboard'
          )
        })
        .catch(() => {})
    },

    logout({ commit }) {
      UserService.logout()
      commit('logout')

      router.push('/')
    },

    getActiveUser({ commit }) {
      return UserService.getActiveUser().then(response => {
        commit('setUser', response)
      })
    },

    getUsers({ commit }, query) {
      return UserService.getUsers(query).then(response => {
        commit('setUsers', response)
      })
    },

    registerUser({commit}, query) {
      return UserService.register(query).then(response => {
        commit('setUser', response)
      })
    }
  },
  modules: {
    data,
    plugin
  }
})
