<template>
  <MainLayout>
    <div class="form-container">
      <div class="form-header">
        <h2>{{ isEdit ? 'Edit Lembar Disposisi' : 'Buat Instruksi Disposisi Baru' }}</h2>
        <ion-button fill="clear" color="medium" @click="goBack">
          <ion-icon slot="start" :icon="arrowBackOutline"></ion-icon>
          Kembali
        </ion-button>
      </div>

      <ion-card class="custom-card">
        <ion-card-content>
          <form @submit.prevent="handleSubmit">
            <ion-grid>
              <ion-row>
                <!-- Pilih Surat yang akan didisposisikan -->
                <ion-col size="12">
                  <ion-item lines="floating" class="custom-input">
                    <ion-label position="stacked">Hubungkan dengan Nomor Surat</ion-label>
                    <ion-select v-model="formDisposisi.no_surat" placeholder="Pilih nomor surat masuk" required>
                      <ion-select-option value="001/TUUD/V/2026">001/TUUD/V/2026 - Permohonan Alat Tulis</ion-select-option>
                      <ion-select-option value="042/B/UND/2026">042/B/UND/2026 - Undangan Rapat Evaluasi</ion-select-option>
                    </ion-select>
                  </ion-item>
                </ion-col>

                <!-- Diteruskan Kepada -->
                <ion-col size="12" size-md="6">
                  <ion-item lines="floating" class="custom-input">
                    <ion-label position="stacked">Diteruskan Kepada (Staf/Kaur)</ion-label>
                    <ion-select v-model="formDisposisi.diteruskan_kepada" placeholder="Pilih Pejabat/Staf" required>
                      <ion-select-option value="Kaur Umum">Kaur Umum</ion-select-option>
                      <ion-select-option value="Seksi Perencanaan">Seksi Perencanaan</ion-select-option>
                      <ion-select-option value="Seksi Logistik">Seksi Logistik</ion-select-option>
                    </ion-select>
                  </ion-item>
                </ion-col>

                <!-- Status Disposisi -->
                <ion-col size="12" size-md="6">
                  <ion-item lines="floating" class="custom-input">
                    <ion-label position="stacked">Status Pemrosesan</ion-label>
                    <ion-select v-model="formDisposisi.status" required>
                      <ion-select-option value="Proses">Proses (Dalam Pengerjaan)</ion-select-option>
                      <ion-select-option value="Selesai">Selesai (Arsip/Tuntas)</ion-select-option>
                    </ion-select>
                  </ion-item>
                </ion-col>

                <!-- Isi Instruksi/Catatan -->
                <ion-col size="12">
                  <ion-item lines="floating" class="custom-input">
                    <ion-label position="stacked">Instruksi / Catatan Pimpinan</ion-label>
                    <ion-textarea 
                      v-model="formDisposisi.catatan" 
                      rows="4" 
                      placeholder="Ketik instruksi penugasan di sini..." 
                      required
                    ></ion-textarea>
                  </ion-item>
                </ion-col>
              </ion-row>

              <!-- Tombol Konfirmasi -->
              <ion-row class="ion-margin-top justify-content-end">
                <ion-col size="12" class="ion-text-right">
                  <ion-button type="button" fill="outline" color="danger" @click="goBack" class="btn-action">
                    Batal
                  </ion-button>
                  <ion-button type="submit" color="success" class="btn-action">
                    <ion-icon slot="start" :icon="saveOutline"></ion-icon>
                    Simpan Disposisi
                  </ion-button>
                </ion-col>
              </ion-row>
            </ion-grid>
          </form>
        </ion-card-content>
      </ion-card>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  IonButton, IonIcon, IonCard, IonCardContent, IonGrid, 
  IonRow, IonCol, IonItem, IonLabel, IonTextarea, IonSelect, IonSelectOption 
} from '@ionic/vue';
import { arrowBackOutline, saveOutline } from 'ionicons/icons';
import MainLayout from '../layouts/MainLayout.vue';

const route = useRoute();
const router = useRouter();

const isEdit = ref(false);

const formDisposisi = ref({
  no_surat: '',
  diteruskan_kepada: '',
  status: 'Proses',
  catatan: ''
});

onMounted(() => {
  if (route.params.id) {
    isEdit.value = true;
    fetchDetailDisposisi(route.params.id);
  }
});

const fetchDetailDisposisi = (id) => {
  formDisposisi.value = {
    no_surat: '001/TUUD/V/2026',
    diteruskan_kepada: 'Kaur Umum',
    status: 'Proses',
    catatan: 'Segera koordinasikan dengan bagian logistik gudang'
  };
};

const handleSubmit = () => {
  alert(isEdit.value ? "Lembar disposisi sukses diperbarui!" : "Lembar disposisi baru berhasil diterbitkan!");
  goBack();
};

const goBack = () => {
  router.push('/disposisi');
};
</script>

<style scoped>
.form-container { max-width: 800px; margin: 0 auto; }
.form-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.form-header h2 { font-size: 1.2rem; font-weight: bold; color: #1e3a8a; margin: 0; }
.custom-card { background: white; margin: 0; border-radius: 8px; }
.custom-input { --background: transparent; --padding-start: 0; margin-bottom: 8px; }
.btn-action { margin-left: 8px; min-width: 110px; font-weight: bold; }
</style>