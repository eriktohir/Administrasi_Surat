<template>
  <ion-menu content-id="main-content" type="overlay">
    <ion-header>
      <ion-toolbar color="primary">
        <ion-title>TUUD Kearsipan</ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content class="sidebar-content">
      <ion-list lines="none">
        <ion-item button @click="handleAuthAction" detail="false" class="menu-item auth-btn">
          <ion-icon slot="start" :icon="isLoggedIn ? logOutOutline : logInOutline"></ion-icon>
          <ion-label>{{ isLoggedIn ? 'Keluar Sistem' : 'Masuk (Login)' }}</ion-label>
        </ion-item>

        <ion-item button router-link="/surat-masuk" router-direction="root">
          <ion-icon slot="start" :icon="mailUnreadOutline"></ion-icon>
          <ion-label>Surat Masuk</ion-label>
        </ion-item>

        <ion-item button router-link="/surat-keluar" router-direction="root">
          <ion-icon slot="start" :icon="mailOpenOutline"></ion-icon>
          <ion-label>Surat Keluar</ion-label>
        </ion-item>

        <ion-item button router-link="/disposisi" router-direction="root">
          <ion-icon slot="start" :icon="shareSocialOutline"></ion-icon>
          <ion-label>Disposisi</ion-label>
        </ion-item>

        <ion-item button router-link="/arsip" router-direction="root">
          <ion-icon slot="start" :icon="archiveOutline"></ion-icon>
          <ion-label>Arsip Surat</ion-label>
        </ion-item>

        <ion-item button router-link="/kelola-pengguna" router-direction="root">
          <ion-icon slot="start" :icon="peopleOutline"></ion-icon>
          <ion-label>Kelola Pengguna</ion-label>
        </ion-item>

        <ion-item button router-link="/audit-log" router-direction="root">
          <ion-icon slot="start" :icon="analyticsOutline"></ion-icon>
          <ion-label>Audit Log</ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-menu>
</template>

<script setup>
import { 
  IonMenu, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonIcon, IonLabel 
} from '@ionic/vue';
import { 
  homeOutline, mailUnreadOutline, mailOpenOutline, shareSocialOutline, 
  archiveOutline, peopleOutline, analyticsOutline 
} from 'ionicons/icons';
</script>

<style scoped>
/* Tempat Kustomisasi Background Sidebar */
.sidebar-content {
  --background: #f4f5f8; /* Ganti dengan warna background sidebar pilihan Anda */
}
ion-item {
  --background: transparent;
  margin: 4px 8px;
  --border-radius: 8px;
}
ion-item:hover {
  --background: rgba(var(--ion-color-primary-rgb), 0.08);
}
</style>