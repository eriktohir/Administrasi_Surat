<template>
  <ion-header>
    <ion-toolbar class="custom-header">
      <ion-buttons slot="start">
        <ion-menu-button></ion-menu-button>
      </ion-buttons>
      
      <ion-title>{{ title }}</ion-title>

      <ion-buttons slot="end" v-if="!authStore.isAuthenticated">
        <ion-button fill="solid" color="light" router-link="/login" class="login-btn">
          <ion-icon slot="start" :icon="logInOutline"></ion-icon>
          Login
        </ion-button>
      </ion-buttons>
      
      <ion-buttons slot="end" v-else>
        <ion-button color="light" @click="handleLogout">
          <ion-icon slot="icon-only" :icon="logOutOutline"></ion-icon>
        </ion-button>
      </ion-buttons>
    </ion-toolbar>
  </ion-header>
</template>

<script setup>
import { IonHeader, IonToolbar, IonButtons, IonMenuButton, IonTitle, IonButton, IonIcon } from '@ionic/vue';
import { logInOutline, logOutOutline } from 'ionicons/icons';
import { useAuthStore } from '../store/auth';
import { useRouter } from 'vue-router';

defineProps({
  title: {
    type: String,
    default: 'Administrasi Surat'
  }
});

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = async () => {
  await authStore.logout();
  router.push('/dashboard');
};
</script>

<style scoped>
/* Tempat Kustomisasi Warna Identitas TUUD pada Header */
.custom-header {
  --background: #1e3a8a; /* Contoh: Biru Gelap khas TUUD, silakan disesuaikan */
  --color: #ffffff;
}
.login-btn {
  --border-radius: 20px;
  font-weight: bold;
}
</style>