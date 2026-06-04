import api from './api';

export const suratKeluarService = {
  // Ambil seluruh daftar surat keluar
  async getAll() {
    try {
      const response = await api.get('/surat-keluar/');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal mengambil data surat keluar.';
    }
  },

  // Ambil detail surat keluar berdasarkan ID
  async getById(id) {
    try {
      const response = await api.get(`/surat-keluar/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Data surat keluar tidak ditemukan.';
    }
  },

  // Tambah Surat Keluar Baru beserta Upload File
  async create(formDataFields, fileObject) {
    try {
      const formData = new FormData();
      formData.append('no_surat', formDataFields.no_surat);
      formData.append('tujuan_surat', formDataFields.tujuan_surat);
      formData.append('perihal', formDataFields.perihal);
      formData.append('tanggal_keluar', formDataFields.tanggal_keluar);
      
      if (fileObject) {
        formData.append('file', fileObject);
      }

      const response = await api.post('/surat-keluar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal menyimpan data surat keluar.';
    }
  },

  // Hapus data surat keluar beserta file fisiknya
  async delete(id) {
    try {
      const response = await api.delete(`/surat-keluar/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal menghapus surat keluar.';
    }
  }
};