import ApiService from './api'
import TokenService from './storage'

import i18n from '../plugins/i18n'
import { QueryString } from '@/utils/helpers'

const UserService = {
  login: function(username, password) {
    return ApiService.post('/api-token-auth/', {
      username,
      password
    }).then(response => {
        console.log()
      TokenService.saveToken(response.token)
      ApiService.setHeader()

      return response.access_token
    }).catch(e=>{
        console.log(e);
    })
  },

  logout() {
    TokenService.removeToken()
    ApiService.removeHeader()
  },

  register(query) {
    return ApiService.post('users/', query)
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
    return [
      {'name': i18n.t('noPermission'), 'permission':''}, 
      {'name': i18n.t('viewPermission'),'permission':'view_table'},
      {'name': i18n.t('updateDataPermission'), 'permission':'update_content'},
      {'name': i18n.t('updateTablePermission'), 'permission':'change_table'}
      ]
  }
}

export default UserService
