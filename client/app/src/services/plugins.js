import ApiService from './api'
import { QueryString } from '@/utils/helpers'

class PluginService {
  constructor(plugin) {
    this.plugin = plugin ? plugin + '/' : ''
  }

  getTasks(query) {
    const queryString = query != null ? '?' + QueryString(query) : ''
    return ApiService.get(`${this.plugin}tasks/${queryString}`)
  }

  createTask(data) {
    return ApiService.post(`${this.plugin}tasks/`, data)
  }

  getTask(id) {
    return ApiService.get(`${this.plugin}tasks/${id}/`)
  }

  deleteTask(id) {
    return ApiService.delete(`${this.plugin}tasks/${id}/`)
  }

  getTaskDetail(idTask, idLog) {
    return ApiService.get(
      `${this.plugin}tasks/${idTask}/task-results/${idLog}/`
    )
  }

  getTaskOptions() {
    return ApiService.options(`${this.plugin}tasks/`)
  }

  putTask(id, data) {
    return ApiService.put(`${this.plugin}tasks/${id}/`, data)
  }

  postTask(data) {
    return ApiService.post(`${this.plugin}tasks/`, data)
  }

  getTaskResults(id, query) {
    const queryString = query != null ? '?' + QueryString(query) : ''
    return ApiService.get(
      `${this.plugin}tasks/${id}/task-results/${queryString}`
    )
  }

  runTask(id) {
    return ApiService.get(`${this.plugin}tasks/${id}/run/`)
  }

  getSettingsOptions() {
    return ApiService.options(`${this.plugin}settings/1/`)
  }

  getSettings() {
    return ApiService.get(`${this.plugin}settings/1/`)
  }

  saveSettings(data) {
    return ApiService.put(`${this.plugin}settings/1/`, data)
  }
}

export default PluginService
