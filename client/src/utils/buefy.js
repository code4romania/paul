import Vue from 'vue'

import {
  Button,
  Input,
  Checkbox,
  Datepicker,
  Datetimepicker,
  Dialog,
  Dropdown,
  Field,
  Icon,
  Loading,
  Menu,
  Message,
  Modal,
  Numberinput,
  Pagination,
  Radio,
  Select,
  Snackbar,
  Switch,
  Table,
  Tag,
  Tabs,
  Taginput,
  Timepicker,
  Toast,
  Tooltip,
  Upload,
  ConfigProgrammatic
} from 'buefy'

ConfigProgrammatic.setOptions({
  defaultTrapFocus: true,
  defaultIconComponent: 'icon-mdi',
  defaultIconPack: 'mdi',

  customIconPacks: {
    mdi: {
      iconPrefix: '',
      internalIcons: {
        // 'check': 'checkmark',
        // 'check-circle': 'checkmark-circle-outline',
        'alert-circle': 'alert-circle-outline'
        // 'chevron-right': 'arrow-forward',
        // 'chevron-left': 'arrow-back',
        // 'chevron-down': 'arrow-down',
        // 'menu-down': 'arrow-dropdown',
        // 'menu-up': 'arrow-dropup',
      }
    }
  },

  // defaultDateFormatter: date => {
  //   console.log(date)
  //   const formatter = e => e.toLocaleDateString('ro-RO', {
  //     timezone: 'UTC'
  //   })

  //   return formatter(date)
  // },

  // defaultDateParser: date => {
  //   console.log(date)
  //   const d = new Date(date)
  //   return d
  // },

  defaultNoticeQueue: false,
  defaultToastDuration: 3000,
  // defaultToastPosition: 'is-bottom',
  defaultInputHasCounter: false,
  defaultUseHtml5Validation: false,
  defaultDialogConfirmText: 'Confirm',
  defaultDialogCancelText: 'Cancel'
  // defaultModalCanCancel: false,
})

// Components
Vue.use(Button)
Vue.use(Checkbox)
Vue.use(Datepicker)
Vue.use(Datetimepicker)
Vue.use(Dialog)
Vue.use(Dropdown)
Vue.use(Field)
Vue.use(Icon)
Vue.use(Input)
Vue.use(Loading)
Vue.use(Menu)
Vue.use(Message)
Vue.use(Modal)
Vue.use(Numberinput)
Vue.use(Pagination)
Vue.use(Radio)
Vue.use(Snackbar)
Vue.use(Switch)
Vue.use(Select)
Vue.use(Table)
Vue.use(Tabs)
Vue.use(Tag)
Vue.use(Taginput)
Vue.use(Timepicker)
Vue.use(Toast)
Vue.use(Tooltip)
Vue.use(Upload)
