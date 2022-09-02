import Vue from 'vue'

const ToastService = {
  open: function(message, config) {
    const options = {
      message,
      type: 'is-success'
    }

    Object.assign(options, config)
    Vue.prototype.$buefy.toast.open(options)
  }
}

export { ToastService }
