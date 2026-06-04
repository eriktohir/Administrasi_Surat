<template>
  <MainLayout>
    <!-- 1. Header Halaman (Tombol Tambah Dinonaktifkan via showAdd="false") -->
    <ActionHeader title="Arsip Data Surat Keluar & Masuk" :showAdd="false" />

    <!-- 2. Tabel Arsip Menggunakan Komponen Dinamis -->
    <DataTable :headers="['No', 'No. Surat', 'Jenis', 'Asal / Tujuan', 'Perihal', 'Tanggal Arsip', 'Aksi']">
      <tr v-for="(arsip, index) in daftarArsip" :key="arsip.id">
        <td>{{ index + 1 }}</td>
        <td>{{ arsip.no_surat }}</td>
        
        <!-- Badge Pembeda Jenis Surat -->
        <td>
          <span :class="['type-badge', arsip.jenis.toLowerCase()]">
            {{ arsip.jenis }}
          </span>
        </td>
        
        <td>{{ arsip.asal_tujuan }}</td>
        <td>{{ arsip.perihal }}</td>
        <td>{{ arsip.tanggal_arsip }}</td>
        
        <!-- Kolom Aksi Khusus: Baca (View) & Cetak (Print) -->
        <td>
          <div class="action-buttons">
            <!-- Fitur Baca / Lihat Dokumen -->
            <ion-button size="small" fill="solid" color="secondary" @click="readDocument(arsip.file_path)" title="Baca Dokumen">
              <ion-icon slot="icon-only" :icon="eyeOutline"></ion-icon>
            </ion-button>
            
            <!-- Fitur Cetak Arsip -->
            <ion-button size="small" fill="solid" color="dark" @click="printArchive(arsip.id)" title="Cetak Arsip">
              <ion-icon slot="icon-only" :icon="printOutline"></ion-icon>
            </ion-button>
          </div>
        </td>
      </tr>

      <!-- Kondisi jika tabel arsip kosong -->
      <tr v-if="daftarArsip.length === 0">
        <td colspan="7" style="text-align: center; color: #666;">Belum ada dokumen yang diarsipkan.</td>
      </tr>
    </DataTable>
  </MainLayout>
</template>

<script setup>
import { ref } from 'vue';
import { IonButton, IonIcon } from '@ionic/vue';
import { eyeOutline, printOutline } from 'ionicons/icons';

// Import Layout & Reusable Components
import MainLayout from '../layouts/MainLayout.vue';
import ActionHeader from '../components/ActionHeader.vue';
import DataTable from '../components/DataTable.vue';

// Mock Data Arsip (Representasi Hasil Gabungan Dokumen Selesai)
const daftarArsip = ref([
  { 
    id: 501, 
    no_surat: '001/TUUD/V/2026', 
    jenis: 'Masuk', 
    asal_tujuan: 'Seksi Logistik', 
    perihal: 'Permohonan Pengadaan Alat Tulis', 
    tanggal_arsip: '2026-05-30',
    file_path: 'nota_dinas_log.pdf'
  },
  { 
    id: 502, 
    no_surat: '002/TUUD/V/2026', 
    jenis: 'Keluar', 
    asal_tujuan: 'Kementerian Pusat', 
    perihal: 'Laporan Berkala Kearsipan', 
    tanggal_arsip: '2026-05-31',
    file_path: 'lap_berkala.pdf'
  }
]);

// Fungsi Aksi Baca Dokumen
const readDocument = (filePath) => {
  console.log("Membuka file arsip:", filePath);
  alert(`Membuka berkas fisik: ${filePath} (Fitur Read)`);
  // Di masa mendatang, logika ini akan mengarah ke window.open(URL_API + filePath, '_blank')
};

// Fungsi Aksi Cetak Dokumen
const printArchive = (id) => {
  console.log("Memicu cetak dokumen ID:", id);
  alert(`Mempersiapkan dokumen ID #${id} untuk dicetak... (Fitur Print)`);
  // Integrasi pencetakan client-side atau trigger cetak PDF dari server
};
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: 8px;
}

ion-button {
  margin: 0;
  --padding-start: 8px;
  --padding-end: 8px;
}

/* Badge pembeda Surat Masuk dan Surat Keluar di tabel arsip */
.type-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  text-align: center;
  min-width: 60px;
}

.type-badge.masuk {
  background-color: #d1fae5;
  color: #065f46;
}

.type-badge.keluar {
  background-color: #e0f2fe;
  color: #075985;
}
</style>