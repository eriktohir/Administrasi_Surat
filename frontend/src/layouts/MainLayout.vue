<template>
  <ion-page>
    <SidebarMenu />

    <div class="ion-page" id="main-content">
      <HeaderTitle :title="pageTitle" />

      <ion-content class="main-workspace">
        <div class="workspace-wrapper">
          <slot></slot> <ion-router-outlet></ion-router-outlet>
        </div>
      </ion-content>
    </div>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent, IonRouterOutlet } from '@ionic/vue';
import SidebarMenu from '../components/SidebarMenu.vue';
import HeaderTitle from '../components/HeaderTitle.vue';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { logInOutline, logOutOutline } from 'ionicons/icons';

const router = useRouter();

// Reactive check status login
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token');
});

const handleAuthAction = () => {
  if (isLoggedIn.value) {
    // Jalankan fungsi logout
    localStorage.removeItem('token');
    localStorage.removeItem('user_role'); // Jika ada penugasan role khusus
    alert("Anda telah keluar dari sistem.");
    router.push('/dashboard'); // Tetap di dashboard karena bersifat publik[cite: 1]
    window.location.reload();  // Refresh state aplikasi
  } else {
    // Arahkan ke halaman login
    router.push('/login');
  }
};
</script>

<style scoped>
/* Tempat Kustomisasi Kunci untuk Background Area Kerja Utama */
.main-workspace {
  --background: #f3f4f6; /* Warna abu-abu terang netral agar tabel/kartu terlihat kontras */
}

/* Wrapper agar konten tidak terlalu menempel ke pinggir screen */
.workspace-wrapper {
  padding: 16px;
  max-width: 1400px;
  margin: 0 auto;
}
</style>