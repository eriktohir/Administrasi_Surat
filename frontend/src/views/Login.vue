<template>
  <ion-page>
    <ion-content class="ion-padding login-container">
      <div class="login-box">
        <div class="logo-area">
          <ion-icon :icon="mailOpenOutline" class="main-logo"></ion-icon>
          <h2>Surat Administration</h2>
          <p>Sistem Informasi Tata Usaha & Urusan Dalam (TUUD)</p>
        </div>

        <div v-if="errorMessage" class="error-banner">
          {{ errorMessage }}
        </div>

        <form @submit.prevent="handleLogin">
          <ion-item lines="full" class="ion-margin-bottom">
            <ion-label position="stacked">Username</ion-label>
            <ion-input 
              v-model="username" 
              type="text" 
              placeholder="Masukkan username Anda" 
              required
            ></ion-input>
          </ion-item>

          <ion-item lines="full" class="ion-margin-bottom">
            <ion-label position="stacked">Password</ion-label>
            <ion-input 
              v-model="password" 
              type="password" 
              placeholder="Masukkan password Anda" 
              required
            ></ion-input>
          </ion-item>

          <div class="ion-margin-top">
            <ion-button type="submit" expand="block" color="primary" :disabled="isLoading">
              {{ isLoading ? 'Memverifikasi...' : 'Masuk Sistem' }}
            </ion-button>
          </div>
        </form>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { IonPage, IonContent, IonItem, IonLabel, IonInput, IonButton, IonIcon } from '@ionic/vue';
import { mailOpenOutline } from 'ionicons/icons';
import { authService } from '../services/authService';

const router = useRouter();
const username = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  
  try {
    await authService.login(username.value, password.value);
    
    // Sukses login, arahkan ke Dashboard
    router.push('/dashboard').then(() => {
      // Force reload ringan agar state layout/sidebar terbarui dengan token baru
      window.location.reload();
    });
  } catch (error) {
    // Menangkap pesan error dari FastAPI (pydantic/database validation)
    errorMessage.value = error;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  --background: #f4f5f8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  background: #ffffff;
  padding: 30px 24px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  max-width: 400px;
  width: 100%;
  margin: 10% auto;
}

.logo-area {
  text-align: center;
  margin-bottom: 30px;
}

.main-logo {
  font-size: 4rem;
  color: var(--ion-color-primary);
}

.logo-area h2 {
  font-weight: 700;
  margin: 10px 0 4px;
  color: #222428;
}

.logo-area p {
  font-size: 0.85rem;
  color: #666;
  margin: 0;
}

.error-banner {
  background-color: #ffebe9;
  color: #ff3b30;
  padding: 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-bottom: 20px;
  border: 1px solid rgba(255, 59, 48, 0.2);
}
</style>