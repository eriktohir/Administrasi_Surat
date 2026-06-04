import { createRouter, createWebHistory } from '@ionic/vue-router';
import Dashboard from '../views/Dashboard.vue';
import Login from '../views/Login.vue';

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    // Tandai meta guest agar pengguna yang sudah login tidak perlu ke halaman login lagi
    meta: { guestOnly: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    // Halaman ini diatur secara eksplisit sebagai PUBLIK
    meta: { isPublic: true }
  },
  {
    path: '/surat-masuk',
    name: 'Surat Masuk',
    component: () => import('../views/SuratMasuk.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/surat-masuk/tambah',
    name: 'Tambah Surat Masuk',
    component: () => import('../views/SuratMasukForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/surat-masuk/edit/:id',
    name: 'Edit Surat Masuk',
    component: () => import('../views/SuratMasukForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/surat-keluar',
    name: 'Surat Keluar',
    component: () => import('../views/SuratKeluar.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/surat-keluar/tambah',
    name: 'Tambah Surat Keluar',
    component: () => import('../views/SuratKeluarForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/surat-keluar/edit/:id',
    name: 'Edit Surat Keluar',
    component: () => import('../views/SuratKeluarForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/disposisi',
    name: 'Disposisi',
    component: () => import('../views/Disposisi.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/disposisi/tambah',
    name: 'Tambah Disposisi',
    component: () => import('../views/DisposisiForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/disposisi/edit/:id',
    name: 'Edit Disposisi',
    component: () => import('../views/DisposisiForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/arsip',
    name: 'Arsip',
    component: () => import('../views/Arsip.vue'),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// --- SISTEM GUARDS AUTENTIKASI ---
router.beforeEach((to, from, next) => {
  // Mengecek status login pengguna dari localStorage (Token JWT/Session)
  const isAuthenticated = !!localStorage.getItem('token'); 

  // 1. Jika halaman bersifat PUBLIK (seperti Dashboard), izinkan akses langsung[cite: 1]
  if (to.meta.isPublic) {
    next();
  } 
  // 2. Jika halaman membutuhkan autentikasi dan pengguna belum login, tendang ke Login
  else if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' });
  } 
  // 3. Jika pengguna sudah login tapi mencoba mengakses halaman Login kembali
  else if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'Dashboard' });
  } 
  // 4. Kondisi lainnya, izinkan lewat
  else {
    next();
  }
});

export default router;