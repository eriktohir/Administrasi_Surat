<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Statistik Surat per Staf</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-grid fixed>
        <ion-row class="table-header">
          <ion-col>Nama Staf</ion-col>
          <ion-col v-for="bulan in months" :key="bulan.index" :size="1">{{ bulan.singkat }}</ion-col>
        </ion-row>
        <ion-row v-for="staf in statistik" :key="staf.user_id">
          <ion-col>{{ staf.username }}</ion-col>
          <ion-col v-for="m in months" :key="m.index" :size="1">
            <span>M:{{ staf.data[m.index].masuk }}</span> / K:{{ staf.data[m.index].keluar }}
          </ion-col>
        </ion-row>
      </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonGrid, IonRow, IonCol } from '@ionic/vue';

const months = [
  { index: 1, nama: 'Januari', singkat: 'Jan' },
  { index: 2, nama: 'Februari', singkat: 'Feb' },
  { index: 3, nama: 'Maret', singkat: 'Mar' },
  { index: 4, nama: 'April', singkat: 'Apr' },
  { index: 5, nama: 'Mei', singkat: 'Mei' },
  { index: 6, nama: 'Juni', singkat: 'Jun' },
  { index: 7, nama: 'Juli', singkat: 'Jul' },
  { index: 8, nama: 'Agustus', singkat: 'Ags' },
  { index: 9, nama: 'September', singkat: 'Sep' },
  { index: 10, nama: 'Oktober', singkat: 'Okt' },
  { index: 11, nama: 'November', singkat: 'Nov' },
  { index: 12, nama: 'Desember', singkat: 'Des' }
];
const statistik = ref([]);

onMounted(async () => {
  const res = await api.get('/statistik/staf?tahun=2026');
  statistik.value = res.data;
});
</script>