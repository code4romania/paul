import ApiService from './api'
import TokenService from './storage'

import { QueryString } from '@/utils/helpers'

const UserService = {
  login: function(username, password) {
    return ApiService.post('/api-token-auth/', {
      username,
      password
    }).then(response => {
      TokenService.saveToken(response.token)
      ApiService.setHeader()

      return response.access_token
    })
  },

  logout() {
    TokenService.removeToken()
    ApiService.removeHeader()
  },

  register(query) {
    return ApiService.post('auth/users/', query)
  },

  resend(email) {
    return ApiService.post('auth/users/resend_activation/', { email })
  },

  activate(uid, token) {
    return ApiService.post('auth/users/activation/', { uid, token })
  },

  toggleActivate(id) {
    return ApiService.get(`users/${id}/toggle-activation/`)
  },

  resetPassword(email) {
    return ApiService.post('auth/users/reset_password/', { email })
  },

  resetPasswordConfirm(uid, token, new_password, re_new_password) {
    return ApiService.post('auth/users/reset_password_confirm/', {
      uid,
      token,
      new_password,
      re_new_password
    })
  },

  changePassword(new_password, re_new_password, current_password) {
    return ApiService.post('auth/users/set_password/', {
      new_password,
      re_new_password,
      current_password
    })
  },

  getUsers(query) {
    const queryString = query != null ? '?' + QueryString(query) : ''
    return ApiService.get(`users/${queryString}`)
  },

  getUser(id) {
    return ApiService.get(`users/${id}/`)
  },

  putUser(id, data) {
    return ApiService.put(`users/${id}/`, data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  patchUser(id, data) {
    return ApiService.patch(`users/${id}/`, data)
  },

  getActiveUser() {
    return ApiService.get('user/')
  },

  getRights() {
    return ['Fără drepturi', 'Vizualizare', 'Editare']
  }
}

export default UserService
