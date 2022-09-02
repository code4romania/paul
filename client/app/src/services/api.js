import axios from 'axios'
import TokenService from './storage'
import { ToastService } from './buefy'

// import { QueryString } from '@/utils/helpers'

// import { ToastProgrammatic as Toast } from 'buefy'

const ApiService = {
  init(baseURL) {
    // console.log('baseURL', baseURL)
    axios.defaults.baseURL = baseURL

    axios.interceptors.response.use(
      response => response.data,
      err => {
        // this.$store.commit('loading_stop')

        let msg = ''

        try {
          switch (err.response.status) {
            case 500:
            case 404:
              msg = err.response.data.detail || 'Something went wrong'
              break
            case null:
              msg = 'Please check your internet connection'
              break
            default:
              for (let e in err.response.data) {
                const o = err.response.data[e]
                msg += (Array.isArray(o) && o[0]) || o + '<br/>'
                break
              }
              break
          }
        } catch {
          if (err.response == null) msg = 'Unable to connect to database'
        }

        msg = 'Error<br> ' + msg

        ToastService.open(`${msg}`, {
          type: 'is-danger'
        })

        return Promise.reject(err)
      }
    )
  },

  getPath(path, appendToken) {
    const newPath = axios.defaults.baseURL.slice(-1) == '/' ? path : '/' + path
    // console.log(appendToken)
    
    return (
      axios.defaults.baseURL +
      newPath +
      (appendToken && `&token=${TokenService.getToken()}`)
    )
  },

  setHeader() {
    const token = TokenService.getToken()

    if (token) axios.defaults.headers.common['Authorization'] = `Token ${token}`
  },

  removeHeader() {
    axios.defaults.headers.common = {}
  },

  get(resource) {
    return axios.get(resource)
  },

  post(resource, data) {
    return axios.post(resource, data)
  },

  put(resource, data) {
    return axios.put(resource, data)
  },

  patch(resource, data) {
    return axios.patch(resource, data)
  },

  options(resource) {
    return axios.options(resource)
  },

  delete(resource) {
    return axios.delete(resource)
  },

  customRequest(data) {
    return axios(data)
  }
}

export default ApiService
