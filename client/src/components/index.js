import Vue from 'vue'
import IconMdi from './IconMdi'
import BaseTable from './table/BaseTable'
import BaseTableAsync from './table/BaseTableAsync'
import SearchResultsTable from './table/SearchResultsTable'

import BaseCard from './BaseCard'
import BaseTitle from './BaseTitle'
import Banner from './Banner'
import './form'

Vue.component('icon-mdi', IconMdi)
Vue.component('Banner', Banner)
Vue.component('BaseTable', BaseTable)
Vue.component('BaseTableAsync', BaseTableAsync)
Vue.component('SearchResultsTable', SearchResultsTable)
Vue.component('BaseCard', BaseCard)
Vue.component('BaseTitle', BaseTitle)
