import api from './api';

export const authService = {
  // Fungsi Login pimpinan / staf
  async login(username, password) {
    try {
      const response = await api.post('/auth/login', { username, password });
      if (response.data.access_token) {
        // Simpan token ke penyimpanan lokal browser/perangkat
        localStorage.setItem('access_token', response.data.access_token);
        
        // Dekripsi isi token secara manual untuk mengambil data role dan user_id
        const payload = JSON.parse(atob(response.data.access_token.split('.')[1]));
        localStorage.setItem('user_role', payload.role);
        localStorage.setItem('username', payload.sub);
      }
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal terhubung ke server login.';
    }
  },

  // Fungsi Registrasi Akun Baru
  async register(username, password, role) {
    try {
      const response = await api.post('/auth/register', { username, password, role });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal melakukan registrasi.';
    }
  },

  // Fungsi Logout
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('username');
  },

  // Ambil data user yang sedang login saat ini
  getCurrentUser() {
    return {
      username: localStorage.getItem('username'),
      role: localStorage.getItem('user_role'),
      token: localStorage.getItem('access_token')
    };
  }
};