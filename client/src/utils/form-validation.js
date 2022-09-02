import { extend, setInteractionMode, localize } from 'vee-validate'

import {
  required,
  email,
  length,
  confirmed
} from 'vee-validate/dist/rules'

import ro from './locale/ro.json'

const rules = { required, email, length, confirmed }

Object.keys(rules).forEach(rule => {
  extend(rule, rules[rule])
})

extend('under', {
  validate(value, args) {
    return value.length <= args.length
  },
  params: ['length']
})

extend('over', {
  validate(value, args) {
    // console.log(value, args)
    return value.length >= args.length
  },
  params: ['length']
})

localize('ro', ro)
// setInteractionMode('lazy')
setInteractionMode('eager')
