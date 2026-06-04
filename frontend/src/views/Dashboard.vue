<template>
  <!-- Bungkus seluruh halaman operasional dengan MainLayout -->
  <MainLayout>
    <div class="dashboard-container">
      
      <!-- Bagian Atas: Kartu Statistik Ringkas -->
      <ion-grid>
        <ion-row>
          <ion-col size="12" size-md="4">
            <ion-card class="stat-card masuk">
              <ion-card-header>
                <ion-card-title>Surat Masuk</ion-card-title>
              </ion-card-header>
              <ion-card-content>
                <h2>{{ statistik.masuk }}</h2>
              </ion-card-content>
            </ion-card>
          </ion-col>

          <ion-col size="12" size-md="4">
            <ion-card class="stat-card keluar">
              <ion-card-header>
                <ion-card-title>Surat Keluar</ion-card-title>
              </ion-card-header>
              <ion-card-content>
                <h2>{{ statistik.keluar }}</h2>
              </ion-card-content>
            </ion-card>
          </ion-col>

          <ion-col size="12" size-md="4">
            <ion-card class="stat-card disposisi">
              <ion-card-header>
                <ion-card-title>Disposisi</ion-card-title>
              </ion-card-header>
              <ion-card-content>
                <h2>{{ statistik.disposisi }}</h2>
              </ion-card-content>
            </ion-card>
          </ion-col>
        </ion-row>

        <!-- Bagian Bawah: Tabel Informasi Ringkas (Sesuai Rencana Gambar 1 & 2) -->
        <ion-row class="ion-margin-top">
          <ion-col size="12">
            <h3 class="section-title">Surat Masuk Terbaru</h3>
            <table class="custom-table">
              <thead>
                <tr>
                  <th>No</th>
                  <th>Perihal</th>
                  <th>Asal Surat</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(surat, index) in suratMasukTerbaru" :key="surat.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ surat.perihal }}</td>
                  <td>{{ surat.asal_tujuan }}</td>
                </tr>
                <tr v-if="suratMasukTerbaru.length === 0">
                  <td colspan="3" class="text-center">Belum ada data surat masuk terbaru</td>
                </tr>
              </tbody>
            </table>
          </ion-col>
        </ion-row>

        <ion-row class="ion-margin-top">
          <ion-col size="12">
            <h3 class="section-title">Surat Keluar Terbaru</h3>
            <table class="custom-table">
              <thead>
                <tr>
                  <th>No</th>
                  <th>Perihal</th>
                  <th>Tujuan Surat</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(surat, index) in suratKeluarTerbaru" :key="surat.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ surat.perihal }}</td>
                  <td>{{ surat.asal_tujuan }}</td>
                </tr>
                <tr v-if="suratKeluarTerbaru.length === 0">
                  <td colspan="3" class="text-center">Belum ada data surat keluar terbaru</td>
                </tr>
              </tbody>
            </table>
          </ion-col>
        </ion-row>
      </ion-grid>

    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api'; // Mengambil interceptor axios Anda
import MainLayout from '../layouts/MainLayout.vue'; // Import layout utama
import { 
  IonGrid, IonRow, IonCol, IonCard, IonCardHeader, IonCardTitle, IonCardContent 
} from '@ionic/vue';

// State Data Dummy/API awal sesuai Gambar 1 & 2 dokumen TUUD[cite: 1]
const statistik = ref({ masuk: 1, keluar: 2, disposisi: 1 });
const suratMasukTerbaru = ref([
  { id: 1, perihal: 'Form Kerjasama 1', asal_tujuan: 'Surat' }
]);
const suratKeluarTerbaru = ref([
  { id: 1, perihal: 'Form Kerjasama', asal_tujuan: 'Kementerian A' }
]);

const fetchDashboardData = async () => {
  try {
    // Jalur integrasi API backend dikemudian hari
    // const resMasuk = await api.get('/dokumen?arah=masuk&limit=5');
    // suratMasukTerbaru.value = resMasuk.data;
  } catch (error) {
    console.error("Gagal memuat data dashboard", error);
  }
};

onMounted(fetchDashboardData);
</script>

<style scoped>
/* Kustomisasi tabel dan warna sesuai Gambar 2 dokumen TUUD */
.section-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #1e3a8a;
  margin-bottom: 8px;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #FFF2E6; /* Warna peach/oranye lembut sesuai mockup Gambar 2 */
  border-radius: 4px;
  overflow: hidden;
}

.custom-table th {
  background-color: #3b82f6; /* Header tabel biru */
  color: white;
  text-align: left;
  padding: 10px;
  font-size: 0.9rem;
}

.custom-table td {
  padding: 10px;
  border-bottom: 1px solid #FFE4CC;
  color: #333;
  font-size: 0.9rem;
}

.stat-card {
  margin: 0;
  --background: white;
  border-left: 5px solid #3b82f6; /* Aksen warna vertikal kartu */
}

.stat-card h2 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
}
</style>