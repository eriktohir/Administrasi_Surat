<template>
  <MainLayout>
    <ActionHeader title="Data Surat Masuk" @add="goToTambah" />

    <div v-if="isLoading" class="ion-text-center ion-padding">
      <p>Mengambil data dari server...</p>
    </div>

    <DataTable v-else :headers="['No', 'No. Surat', 'Asal Surat', 'Perihal', 'Tanggal Masuk', 'Dokumen', 'Aksi']">
      <tr v-for="(surat, index) in daftarSurat" :key="surat.id">
        <td>{{ index + 1 }}</td>
        <td>{{ surat.no_surat }}</td>
        <td>{{ surat.asal_surat }}</td>
        <td>{{ surat.perihal }}</td>
        <td>{{ surat.tanggal_masuk }}</td>
        
        <td>
          <ion-button v-if="surat.file_path" size="small" fill="clear" color="primary" @click="viewFile(surat.file_path)">
            <ion-icon slot="start" :icon="documentTextOutline"></ion-icon>
            Lihat
          </ion-button>
          <span v-else style="color: #999; font-size: 0.85rem;">Tidak ada file</span>
        </td>
        
        <td>
          <div class="action-buttons">
            <ion-button size="small" fill="solid" color="warning" @click="goToEdit(surat.id)">
              <ion-icon slot="icon-only" :icon="createOutline"></ion-icon>
            </ion-button>
            <ion-button size="small" fill="solid" color="danger" @click="confirmDelete(surat.id, surat.no_surat)">
              <ion-icon slot="icon-only" :icon="trashOutline"></ion-icon>
            </ion-button>
          </div>
        </td>
      </tr>

      <tr v-if="daftarSurat.length === 0">
        <td colspan="7" style="text-align: center; color: #666; padding: 20px;">
          Tidak ada data surat masuk yang ditemukan di database.
        </td>
      </tr>
    </DataTable>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { IonButton, IonIcon } from '@ionic/vue';
import { documentTextOutline, createOutline, trashOutline } from 'ionicons/icons';

// Import Layout & Reusable Components
import MainLayout from '../layouts/MainLayout.vue';
import ActionHeader from '../components/ActionHeader.vue';
import DataTable from '../components/DataTable.vue';

// Import Service dan API Base URL untuk pemanggilan file statis
import { suratMasukService } from '../services/suratMasukService';
import { API_BASE_URL } from '../services/api';

const router = useRouter();
const daftarSurat = ref([]);
const isLoading = ref(true);

// Ambil data dari database phpMyAdmin saat halaman dimuat
const loadDataSurat = async () => {
  isLoading.value = true;
  try {
    daftarSurat.value = await suratMasukService.getAll();
  } catch (error) {
    alert("Gagal memuat data: " + error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadDataSurat();
});

// Navigasi ke Form Tambah Data
const goToTambah = () => {
  router.push('/surat-masuk/tambah');
};

// Navigasi ke Form Edit Data
const goToEdit = (id) => {
  router.push(`/surat-masuk/edit/${id}`);
};

// Membuka File PDF / Dokumen Fisik di Tab Baru
const viewFile = (filePath) => {
  const fullUrl = `${API_BASE_URL}/static/uploads/${filePath}`;
  window.open(fullUrl, '_blank');
};

// Aksi Hapus Data Surat
const confirmDelete = async (id, noSurat) => {
  if (confirm(`Apakah Anda yakin ingin menghapus surat dengan Nomor: ${noSurat}?`)) {
    try {
      await suratMasukService.delete(id);
      alert("Data berhasil dihapus.");
      // Refresh tabel data setelah berhasil dihapus
      loadDataSurat();
    } catch (error) {
      alert("Gagal menghapus data: " + error);
    }
  }
};
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: 6px;
}

ion-button {
  margin: 0;
  --padding-start: 6px;
  --padding-end: 6px;
}
</style>