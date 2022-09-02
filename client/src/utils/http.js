import axios from 'axios'
const token = localStorage.getItem('token')

export default axios.create({
  baseURL: process.env.VUE_APP_ROOT_API,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`
  }
})
