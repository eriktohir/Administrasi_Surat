<template>
  <ion-app>
    <ion-header>
      <ion-toolbar>
        <ion-buttons slot="start" v-if="isLoggedIn">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title class="app-title">ADMINISTRASI SURAT TUUD</ion-title>
        <ion-buttons slot="end">
          <ion-button v-if="!isLoggedIn" router-link="/login">
            <ion-icon :icon="logInOutline"></ion-icon>
            Login
          </ion-button>
          <ion-button v-else @click="logout">
            <ion-icon :icon="logOutOutline"></ion-icon>
            Logout
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-menu content-id="main-content" v-if="isLoggedIn">
      <ion-header>
        <ion-toolbar>
          <ion-title>Menu TUUD</ion-title>
        </ion-toolbar>
      </ion-header>
      <ion-content>
        <ion-list>
          <ion-menu-toggle auto-hide="false" v-for="menu in menus" :key="menu.route">
            <ion-item button :router-link="menu.route">
              <ion-icon :icon="menu.icon" slot="start"></ion-icon>
              <ion-label>{{ menu.title }}</ion-label>
            </ion-item>
          </ion-menu-toggle>
          <ion-item button @click="logout">
            <ion-icon :icon="logOutOutline" slot="start"></ion-icon>
            <ion-label>Logout</ion-label>
          </ion-item>
        </ion-list>
      </ion-content>
    </ion-menu>
    <ion-router-outlet id="main-content"></ion-router-outlet>
  </ion-app>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from './store/auth';
import { IonApp, IonHeader, IonToolbar, IonTitle, IonButtons, IonMenuButton, IonMenu, IonContent, IonList, IonItem, IonLabel, IonIcon, IonRouterOutlet, IonButton } from '@ionic/vue';
import { logOutOutline, logInOutline, gridOutline, mailOutline, paperPlaneOutline, archiveOutline, peopleOutline, documentTextOutline, statsChartOutline } from 'ionicons/icons';

const authStore = useAuthStore();
const router = useRouter();
const isLoggedIn = computed(() => !!authStore.token);

const menus = computed(() => {
  const role = authStore.roleId;
  const base = [
    { title: 'Dashboard', route: '/dashboard', icon: gridOutline },
    { title: 'Surat Masuk', route: '/surat-masuk', icon: mailOutline },
    { title: 'Surat Keluar', route: '/surat-keluar', icon: paperPlaneOutline },
    { title: 'Disposisi', route: '/disposisi', icon: documentTextOutline },
    { title: 'Arsip', route: '/arsip', icon: archiveOutline }
  ];
  if (role == 1) {
    base.push({ title: 'Kelola Pengguna', route: '/kelola-pengguna', icon: peopleOutline });
    base.push({ title: 'Statistik Staf', route: '/statistik-staf', icon: statsChartOutline });
  }
  return base;
});

const logout = () => {
  authStore.logout();
  router.push('/');
};
</script>