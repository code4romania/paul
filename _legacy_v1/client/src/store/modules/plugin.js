import Vue from 'vue'
import PluginService from '@/services/plugins'
// import { ToastService } from '@/services/buefy'

export default {
  namespaced: true,
  state: {
    service: null,
    task: null,
    tasks: null,
    taskOptions: null,
    loading: {}
  },
  mutations: {
    setPlugin(state, plugin) {
      state.service = new PluginService(plugin)
    },
    setTask(state, data) {
      state.task = data
    },
    setTasks(state, data) {
      state.tasks = data
    },
    setTaskOptions(state, data) {
      state.taskOptions = data
    },
    setLoading(state, action, status) {
      Vue.set(state.loading, action, status)
    }
  },
  actions: {
    getTasks({ commit, state }, query) {
      return state.service.getTasks(query).then(response => {
        commit('setTasks', response)
      })
    },

    getTask({ commit, state }, idTask) {
      return state.service.getTask(idTask).then(response => {
        commit('setTask', response)
      })
    },

    getTaskOptions({ commit, state }, idTask) {
      return state.service.getTaskOptions(idTask).then(response => {
        commit('setTaskOptions', response.actions.POST)
      })
    },

    deleteTask({ commit, state }, { idTask }) {
      return state.service.deleteTask(idTask).then(() => {
        commit('setTask', null)
      })
    }
  }
}
