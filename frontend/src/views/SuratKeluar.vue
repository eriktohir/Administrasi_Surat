<template>
  <MainLayout>
    <ActionHeader title="Data Surat Keluar" @add="goToTambah" />

    <div v-if="isLoading" class="ion-text-center ion-padding">
      <p>Mengambil data surat keluar dari server...</p>
    </div>

    <DataTable v-else :headers="['No', 'No. Surat', 'Tujuan Surat', 'Perihal', 'Tanggal Keluar', 'Dokumen', 'Aksi']">
      <tr v-for="(surat, index) in daftarSuratKeluar" :key="surat.id">
        <td>{{ index + 1 }}</td>
        <td>{{ surat.no_surat }}</td>
        <td>{{ surat.tujuan_surat }}</td>
        <td>{{ surat.perihal }}</td>
        <td>{{ surat.tanggal_keluar }}</td>
        
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

      <tr v-if="daftarSuratKeluar.length === 0">
        <td colspan="7" style="text-align: center; color: #666; padding: 20px;">
          Tidak ada data surat keluar yang ditemukan di database.
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

import MainLayout from '../layouts/MainLayout.vue';
import ActionHeader from '../components/ActionHeader.vue';
import DataTable from '../components/DataTable.vue';

import { suratKeluarService } from '../services/suratKeluarService';
import { API_BASE_URL } from '../services/api';

const router = useRouter();
const daftarSuratKeluar = ref([]);
const isLoading = ref(true);

const loadDataSuratKeluar = async () => {
  isLoading.value = true;
  try {
    daftarSuratKeluar.value = await suratKeluarService.getAll();
  } catch (error) {
    alert("Gagal memuat data surat keluar: " + error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadDataSuratKeluar();
});

const goToTambah = () => {
  router.push('/surat-keluar/tambah');
};

const goToEdit = (id) => {
  router.push(`/surat-keluar/edit/${id}`);
};

const viewFile = (filePath) => {
  window.open(`${API_BASE_URL}/static/uploads/${filePath}`, '_blank');
};

const confirmDelete = async (id, noSurat) => {
  if (confirm(`Apakah Anda yakin ingin menghapus surat keluar Nomor: ${noSurat}?`)) {
    try {
      await suratKeluarService.delete(id);
      alert("Data surat keluar berhasil dihapus.");
      loadDataSuratKeluar();
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