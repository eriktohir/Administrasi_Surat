import api from './api';

export const disposisiService = {
  // Ambil semua riwayat instruksi disposisi
  async getAll() {
    try {
      const response = await api.get('/disposisi/');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal mengambil data disposisi.';
    }
  },

  // Ambil detail lembar disposisi berdasarkan ID
  async getById(id) {
    try {
      const response = await api.get(`/disposisi/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Data disposisi tidak ditemukan.';
    }
  },

  // Perbarui catatan atau status pemrosesan disposisi (Proses -> Selesai)
  async update(id, dataUpdate) {
    try {
      const response = await api.put(`/disposisi/${id}`, {
        diteruskan_kepada: dataUpdate.diteruskan_kepada,
        catatan: dataUpdate.catatan,
        status: dataUpdate.status
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal memperbarui data disposisi.';
    }
  },

  // Hapus lembar disposisi
  async delete(id) {
    try {
      const response = await api.delete(`/disposisi/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal menghapus lembar disposisi.';
    }
  }
};