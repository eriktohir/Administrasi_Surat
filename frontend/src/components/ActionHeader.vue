<template>
  <div class="action-header-container">
    <h2 class="page-title">{{ title }}</h2>
    
    <ion-button v-if="showAdd" color="primary" @click="$emit('add-click')" class="add-btn">
      <ion-icon slot="start" :icon="addOutline"></ion-icon>
      Tambah
    </ion-button>
  </div>
</template>

<script setup>
import { IonButton, IonIcon } from '@ionic/vue';
import { addOutline } from 'ionicons/icons';

defineProps({
  title: {
    type: String,
    required: true
  },
  showAdd: {
    type: Boolean,
    default: true
  }
});

defineEmits(['add-click']);
</script>

<style scoped>
.action-header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e5e7eb;
}

.page-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #1e3a8a; /* Warna Biru Khas TUUD */
  margin: 0;
}

.add-btn {
  --border-radius: 6px;
  font-weight: 600;
}
</style>