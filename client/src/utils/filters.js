import Vue from 'vue'
import { Parser } from './helpers'

Vue.filter('parseDate', Parser.date)
Vue.filter('parseDatetime', Parser.datetime)
Vue.filter('parseNumber', Parser.float)
