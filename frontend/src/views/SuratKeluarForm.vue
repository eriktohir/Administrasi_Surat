<template>
  <MainLayout>
    <ion-header collapse="condense">
      <ion-toolbar>
        <ion-title size="large">Catat Surat Keluar Baru</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div class="form-container">
        <div v-if="errorMessage" class="error-banner">{{ errorMessage }}</div>

        <form @submit.prevent="handleSubmit">
          <ion-item lines="full" class="ion-margin-bottom">
            <ion-label position="stacked">Nomor Surat Keluar</ion-label>
            <ion-input v-model="form.no_surat" type="text" placeholder="Contoh: 045/TUUD-OUT/VI/2026" required></ion-input>
          </ion-item>

          <ion-item lines="full" class="ion-margin-bottom">
            <ion-label position="stacked">Tujuan Surat</ion-label>
            <ion-input v-model="form.tujuan_surat" type="text" placeholder="Contoh: Kepala Dinas Pendidikan" required></ion-input>
          </ion-item>

          <ion-item lines="full" class="ion-margin-bottom">
            <ion-label position="stacked">Perihal</ion-label>
            <ion-textarea v-model="form.perihal" placeholder="Isi ringkas perihal dokumen keluar" rows="3" required></ion-textarea>
          </ion-item>

          <ion-item lines="full" class="ion-margin-bottom">
            <ion-label position="stacked">Tanggal Keluar (Kirim)</ion-label>
            <ion-input v-model="form.tanggal_keluar" type="date" required></ion-input>
          </ion-item>

          <div class="file-upload-section ion-margin-bottom">
            <label class="file-label">Unggah Salinan Surat Keluar (PDF / Gambar)</label>
            <input type="file" accept=".pdf,.png,.jpg,.jpeg" @change="handleFileChange" class="file-input" />
            <p class="file-note">*Opsional. Unggah jika arsip fisik sudah dipindai (*scanned*).</p>
          </div>

          <div class="button-group">
            <ion-button type="button" fill="outline" color="medium" @click="goBack">Batal</ion-button>
            <ion-button type="submit" color="primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Menyimpan...' : 'Simpan Arsip' }}
            </ion-button>
          </div>
        </form>
      </div>
    </ion-content>
  </MainLayout>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonItem, IonLabel, IonInput, IonTextarea, IonButton } from '@ionic/vue';
import MainLayout from '../layouts/MainLayout.vue';
import { suratKeluarService } from '../services/suratKeluarService';

const router = useRouter();
const isSubmitting = ref(false);
const errorMessage = ref('');
const selectedFile = ref(null);

const form = reactive({
  no_surat: '',
  tujuan_surat: '',
  perihal: '',
  tanggal_keluar: new Date().toISOString().split('T')[0]
});

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
  }
};

const handleSubmit = async () => {
  isSubmitting.value = true;
  errorMessage.value = '';

  try {
    await suratKeluarService.create(form, selectedFile.value);
    alert('Data surat keluar berhasil diarsipkan!');
    router.push('/surat-keluar');
  } catch (error) {
    errorMessage.value = error;
  } finally {
    isSubmitting.value = false;
  }
};

const goBack = () => {
  router.push('/surat-keluar');
};
</script>

<style scoped>
/* Styling selaras dengan formulir surat masuk demi konsistensi UI/UX Capstone */
.form-container {
  max-width: 600px;
  margin: 20px auto;
  background: #ffffff;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.file-upload-section {
  padding: 16px;
  border: 2px dashed #ccc;
  border-radius: 6px;
  background: #f9f9f9;
}
.file-label {
  display: block;
  font-weight: bold;
  font-size: 0.9rem;
  margin-bottom: 8px;
  color: #444;
}
.file-input {
  display: block;
  width: 100%;
}
.file-note {
  font-size: 0.75rem;
  color: #888;
  margin: 6px 0 0 0;
}
.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
.error-banner {
  background: #ffebe9;
  color: #ff3b30;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 16px;
  font-size: 0.85rem;
  border: 1px solid rgba(255, 59, 48, 0.2);
}
</style>