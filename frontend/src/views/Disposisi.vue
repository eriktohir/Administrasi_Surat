<template>
  <MainLayout>
    <ActionHeader title="Pelacakan Lembar Disposisi Pimpinan" :showAdd="false" />

    <div v-if="isLoading" class="ion-text-center ion-padding">
      <p>Mengambil data disposisi dari server...</p>
    </div>

    <DataTable v-else :headers="['No', 'ID Surat Masuk', 'Diteruskan Kepada', 'Instruksi / Catatan', 'Tanggal Disposisi', 'Status', 'Aksi']">
      <tr v-for="(disposisi, index) in daftarDisposisi" :key="disposisi.id">
        <td>{{ index + 1 }}</td>
        <td>ID-{{ disposisi.surat_masuk_id }}</td>
        <td>{{ disposisi.diteruskan_kepada }}</td>
        <td>{{ disposisi.catatan }}</td>
        <td>{{ disposisi.tanggal_disposisi }}</td>
        
        <td>
          <span :class="['status-badge', disposisi.status.toLowerCase()]">
            {{ disposisi.status }}
          </span>
        </td>
        
        <td>
          <div class="action-buttons">
            <ion-button size="small" fill="solid" color="warning" @click="goToEdit(disposisi.id)">
              <ion-icon slot="icon-only" :icon="createOutline"></ion-icon>
            </ion-button>
            <ion-button size="small" fill="solid" color="danger" @click="confirmDelete(disposisi.id)">
              <ion-icon slot="icon-only" :icon="trashOutline"></ion-icon>
            </ion-button>
          </div>
        </td>
      </tr>

      <tr v-if="daftarDisposisi.length === 0">
        <td colspan="7" style="text-align: center; color: #666; padding: 20px;">
          Belum ada riwayat lembar disposisi pimpinan.
        </td>
      </tr>
    </DataTable>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { IonButton, IonIcon } from '@ionic/vue';
import { createOutline, trashOutline } from 'ionicons/icons';

import MainLayout from '../layouts/MainLayout.vue';
import ActionHeader from '../components/ActionHeader.vue';
import DataTable from '../components/DataTable.vue';

import { disposisiService } from '../services/disposisiService';

const router = useRouter();
const daftarDisposisi = ref([]);
const isLoading = ref(true);

const loadDataDisposisi = async () => {
  isLoading.value = true;
  try {
    daftarDisposisi.value = await disposisiService.getAll();
  } catch (error) {
    alert("Gagal memuat data disposisi: " + error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadDataDisposisi();
});

const goToEdit = (id) => {
  router.push(`/disposisi/edit/${id}`);
};

const confirmDelete = async (id) => {
  if (confirm(`Apakah Anda yakin ingin menghapus Lembar Disposisi ID #${id}?`)) {
    try {
      await disposisiService.delete(id);
      alert("Lembar disposisi berhasil dihapus.");
      loadDataDisposisi();
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

/* Styling Badge Status */
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  text-align: center;
}
.status-badge.proses {
  background-color: #fef3c7;
  color: #92400e;
}
.status-badge.selesai {
  background-color: #d1fae5;
  color: #065f46;
}
</style>