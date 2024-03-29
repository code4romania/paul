import Vue from 'vue'

import App from './App.vue'
import router from './router'
import store from './store'
import Meta from 'vue-meta'

import ApiService from './services/api'

import './utils/buefy'
import './components/'
import './utils/form-validation'
import './utils/filters'

import i18n from './plugins/i18n'

// Styles
import './assets/style/base.scss'

// Services
ApiService.init(process.env.VUE_APP_ROOT_API)
ApiService.setHeader()

Vue.use(Meta)

Vue.config.productionTip = false

new Vue({
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
