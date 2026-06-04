import { defineStore } from 'pinia';
import api from '../services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    roleId: localStorage.getItem('roleId') || null,
    userId: localStorage.getItem('userId') || null
  }),
  actions: {
    async login(username, password) {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      const res = await api.post('/auth/login', formData);
      this.token = res.data.access_token;
      this.roleId = res.data.role_id;
      localStorage.setItem('token', this.token);
      localStorage.setItem('roleId', this.roleId);
      // decode user_id dari token? Bisa simpan dari response tambahan, tapi kita sederhana
      return true;
    },
    logout() {
      this.token = null;
      this.roleId = null;
      localStorage.clear();
    }
  }
});