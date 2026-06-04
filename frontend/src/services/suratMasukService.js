import api from './api';

export const suratMasukService = {
  // Fetch semua daftar surat masuk
  async getAll() {
    try {
      const response = await api.get('/surat-masuk/');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal mengambil data surat masuk.';
    }
  },

  // Ambil detail surat berdasarkan ID
  async getById(id) {
    try {
      const response = await api.get(`/surat-masuk/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Data surat tidak ditemukan.';
    }
  },

  // Tambah Surat Masuk Baru beserta Upload File PDF berkas fisik
  async create(formDataFields, fileObject) {
    try {
      const formData = new FormData();
      formData.append('no_surat', formDataFields.no_surat);
      formData.append('asal_surat', formDataFields.asal_surat);
      formData.append('perihal', formDataFields.perihal);
      formData.append('tanggal_masuk', formDataFields.tanggal_masuk);
      
      if (fileObject) {
        formData.append('file', fileObject);
      }

      const response = await api.post('/surat-masuk/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal menyimpan data surat masuk.';
    }
  },

  // Hapus data surat masuk beserta file fisiknya
  async delete(id) {
    try {
      const response = await api.delete(`/surat-masuk/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal menghapus surat.';
    }
  },

  // ==========================================
  // LOGIKA DISPOSISI TERIKAT SURAT MASUK
  // ==========================================
  async createDisposisi(suratMasukId, diteruskanKepada, catatan, status = "Proses") {
    try {
      const response = await api.post('/disposisi/', {
        surat_masuk_id: suratMasukId,
        diteruskan_kepada: diteruskanKepada,
        catatan: catatan,
        status: status
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Gagal menerbitkan lembar disposisi.';
    }
  }
};