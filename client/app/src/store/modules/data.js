// import router from '@/router'
import Vue from 'vue'
import {
  ChartService,
  DatabaseService,
  TableService,
  ImportService,
  TableViewService,
  DataService
} from '@/services/data'
import { ToastService } from '@/services/buefy'

export default {
  namespaced: true,
  state: {
    database: null,
    table: {},
    tableEntries: null,
    tableLinks: null,
    entity: null,
    import: null,
    filters: {},
    tableView: null,
    tableViews: null,
    tableViewEntries: null,
    chart: null,
    charts: null,
    card: null,
    cards: null,
    users: null,
    loading: {}
  },
  mutations: {
    setUser(state, data) {
      state.user = data
    },
    setDatabase(state, data) {
      state.database = data[0]
    },
    setTable(state, { idTable, data }) {
      Vue.set(state.table, idTable, data)
      // state.table = data
    },
    setTableEntries(state, data) {
      // Vue.set(state.tableEntries, idTable, data)
      state.tableEntries = data
    },
    setEntity(state, data) {
      state.entity = data
    },
    setTableLinks(state, data) {
      state.tableLinks = data
    },
    setFilters(state, { idTable, filter }) {
      // state.filters = data
      if (idTable) Vue.set(state.filters, idTable, filter)
      else state.filters = {}
    },
    setImport(state, data) {
      state.import = data
    },
    setTableView(state, data) {
      state.tableView = data
    },
    setTableViewEntries(state, data) {
      state.tableViewEntries = data
    },
    setTableViews(state, data) {
      state.tableViews = data
    },
    setCharts(state, data) {
      state.charts = data
    },
    setChart(state, data) {
      state.chart = data
    },
    setCards(state, data) {
      state.cards = data
    },
    setCard(state, data) {
      state.card = data
    },
    setUsers(state, data) {
      state.users = data
    },
    setLoading(state, { idTable, status }) {
      Vue.set(state.loading, idTable, status)
    }
  },
  actions: {
    // DATABASE
    //
    getDatabase({ commit }) {
      return DatabaseService.getDatabase().then(response => {
        commit('setDatabase', response)
      })
    },

    // TABLE
    //
    getTable({ commit }, idTable) {
      return TableService.getTable(idTable).then(response => {
        commit('setTable', { idTable, data: response })
      })
    },

    getTableEntries({ commit }, { idTable, query }) {
      commit('setLoading', { idTable, status: true })

      return TableService.getEntries(idTable, query)
        .then(response => {
          commit('setTableEntries', response)
          commit('setLoading', { idTable, status: false })
        })
        .catch(() => {
          commit('setLoading', { idTable, status: false })
        })
    },

    getEntity({ commit }, { idTable, idEntity }) {
      return TableService.getEntity(idTable, idEntity).then(response => {
        commit('setEntity', response)
      })
    },

    putTable({ dispatch }, { idTable, data }) {
      return TableService.putTable(idTable, data).then(() => {
        dispatch('getDatabase').then(
          ToastService.open('Tabelul a fost actualizat')
        )
      })
    },

    patchTable({ dispatch }, { idTable, data }) {
      return TableService.patchTable(idTable, data).then(() => {
        return dispatch('getDatabase').then(
          ToastService.open('Tabelul a fost actualizat')
        )
      })
    },

    postTable({ dispatch }, data) {
      return TableService.postTable(data).then(response => {
        dispatch('getDatabase').then(() => {
          ToastService.open('Tabelul a fost creat cu success.')
        })

        return response
      })
    },

    deleteTable({ dispatch }, idTable) {
      return TableService.deleteTable(idTable).then(() => {
        dispatch('getDatabase').then(
          ToastService.open('Tabelul a fost șters.')
        )
      })
    },

    deleteEntity({ dispatch }, { idTable, idEntity, query }) {
      return TableService.deleteEntity(idTable, idEntity).then(() => {
        dispatch('getTableEntries', { idTable, query }).then(() => {
          ToastService.open('Intrarea a fost ștearsă')
        })
      })
    },

    // IMPORT
    //
    getImportData({ commit }, idImport) {
      return ImportService.getData(idImport).then(response => {
        commit('setImport', response)
        return response
      })
    },

    manualImport({ commit }, { idTable, data }) {
      return ImportService.manual(idTable, data).then(response => {
        commit('setImport', response)
        return response
      })
    },

    prepareImport({ commit }, data) {
      return ImportService.prepare(data).then(response => {
        commit('setImport', response)
        return response
      })
    },

    // TABLE VIEWS
    //
    getTableViews({ commit }, { query, all }) {
      // console.log('getTableViews', query, all)
      commit('setLoading', { idTable: 'views', status: true })
      return DataService.get('filters', query, all).then(response => {
        // return TableViewService.getTableViews(query, getAll).then(response => {
        commit('setLoading', { idTable: 'views', status: false })
        commit('setTableViews', response)
      })
    },

    getTableView({ commit }, id) {
      return TableViewService.getTableView(id).then(response => {
        commit('setTableView', response)
      })
    },

    patchTableView({ dispatch }, { idTable, data }) {
      return TableViewService.patchTableView(idTable, data).then(() => {
        dispatch('getTableView', idTable)
        ToastService.open('The view has been updated')
      })
    },

    getTableViewEntries({ commit }, { idTable, query }) {
      commit('setLoading', { idTable, status: true })
      return TableViewService.getEntries(idTable, query).then(response => {
        commit('setTableViewEntries', response)
        commit('setLoading', { idTable, status: false })
      })
    },

    deleteTableView({ dispatch }, idTable) {
      return TableViewService.deleteTableView(idTable).then(() => {
        dispatch('getTableViews', { query: null }).then(() => {
          ToastService.open('The view has been deleted')
        })
      })
    },

    // CHARTS
    //

    getCharts({ commit }, query) {
      return ChartService.getCharts(query).then(response => {
        commit('setCharts', response)
      })
    },

    getChart({ commit }, id) {
      return ChartService.getChart(id).then(response => {
        commit('setChart', response)
      })
    },

    createChart({ dispatch }, id) {
      return ChartService.createChart(id).then(response => {
        return dispatch('getCharts').then(() => {
          ToastService.open('The chart has been created')
          return response
        })
      })
    },

    patchChart({ dispatch }, { id, data }) {
      return ChartService.patchChart(id, data).then(() => {
        dispatch('getCharts').then(() => {
          ToastService.open('The chart property has been changed')
        })
      })
    },

    updateChart({ dispatch }, { id, data }) {
      return ChartService.updateChart(id, data).then(response => {
        return dispatch('getCharts').then(() => {
          ToastService.open('The chart has been updated')
          return response
        })
      })
    },

    deleteChart({ dispatch }, id) {
      return ChartService.deleteChart(id).then(() => {
        dispatch('getCharts').then(
          ToastService.open('The chart has been deleted')
        )
      })
    },

    // CARDS
    //

    getCards({ commit }, query) {
      return DataService.get('cards', query).then(response => {
        commit('setCards', response)
      })
    },

    getCard({ commit }, id) {
      return DataService.getInstance('cards', id).then(response => {
        commit('setCard', response)
        return response
      })
    },

    createCard({ dispatch }, id) {
      return DataService.post('cards', id).then(response => {
        return dispatch('getCards').then(() => {
          ToastService.open('The card has been created')
          return response
        })
      })
    },

    patchCard({ dispatch }, { id, data }) {
      return DataService.patch('cards', id, data).then(() => {
        dispatch('getCards').then(() => {
          ToastService.open('The card property has been changed')
        })
      })
    },

    updateCard({ dispatch }, { id, data }) {
      return DataService.put('cards', id, data).then(response => {
        return dispatch('getCards').then(() => {
          ToastService.open('The chart has been updated')
          return response
        })
      })
    },

    deleteCard({ dispatch }, id) {
      return DataService.delete('cards', id).then(() => {
        dispatch('getCards').then(
          ToastService.open('The chart has been deleted')
        )
      })
    },

    // USERS
    // 
    
    getUsers({ commit }, query) {
      return DataService.get('users', query).then(response => {
        commit('setUsers', response)
      })
    },
    deleteUser({ dispatch }, id) {
      return DataService.delete('users', id).then(() => {
        dispatch('getUsers').then(() => {
          ToastService.open('The user has been deleted')
        })
      })
    }
  }
}
