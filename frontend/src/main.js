import { createApp } from 'vue';
import { IonicVue } from '@ionic/vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

import '@ionic/vue/css/core.css';
import './theme/variables.css';

const app = createApp(App).use(IonicVue).use(router).use(createPinia());
router.isReady().then(() => app.mount('#app'));