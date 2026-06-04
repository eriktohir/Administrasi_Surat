<template>
  <ion-page>
    <ion-header><ion-toolbar><ion-title>Kelola Pengguna</ion-title><ion-buttons slot="end"><ion-button @click="openModal()"><ion-icon :icon="addOutline"></ion-icon></ion-button></ion-buttons></ion-toolbar></ion-header>
    <ion-content>
      <ion-list>
        <ion-item v-for="user in users" :key="user.id">
          <ion-label>{{ user.username }} (Role: {{ user.role_id }})</ion-label>
          <ion-buttons slot="end">
            <ion-button @click="editUser(user)"><ion-icon :icon="createOutline"></ion-icon></ion-button>
            <ion-button @click="deleteUser(user.id)" color="danger"><ion-icon :icon="trashOutline"></ion-icon></ion-button>
          </ion-buttons>
        </ion-item>
      </ion-list>
    </ion-content>
    <ion-modal :is-open="modalOpen">
      <ion-header><ion-toolbar><ion-title>{{ editMode ? 'Edit User' : 'Tambah User' }}</ion-title><ion-button slot="end" @click="closeModal">Tutup</ion-button></ion-toolbar></ion-header>
      <ion-content>
        <ion-item><ion-label position="stacked">Username</ion-label><ion-input v-model="form.username"></ion-input></ion-item>
        <ion-item><ion-label position="stacked">Password</ion-label><ion-input type="password" v-model="form.password"></ion-input></ion-item>
        <ion-item><ion-label position="stacked">Role</ion-label><ion-select v-model="form.role_id"><ion-select-option :value="1">Admin</ion-select-option><ion-select-option :value="2">Staf</ion-select-option><ion-select-option :value="3">Pimpinan</ion-select-option><ion-select-option :value="4">Arsiparis</ion-select-option></ion-select></ion-item>
        <ion-button expand="block" @click="saveUser">Simpan</ion-button>
      </ion-content>
    </ion-modal>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/api';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonButtons, IonButton, IonIcon, IonContent, IonList, IonItem, IonLabel, IonModal, IonInput, IonSelect, IonSelectOption } from '@ionic/vue';
import { addOutline, createOutline, trashOutline } from 'ionicons/icons';

const users = ref([]);
const modalOpen = ref(false);
const editMode = ref(false);
const editId = ref(null);
const form = ref({ username: '', password: '', role_id: 2 });

const fetchUsers = async () => {
  const res = await api.get('/user');
  users.value = res.data;
};
const saveUser = async () => {
  if (editMode.value) {
    await api.put(`/user/${editId.value}`, form.value);
  } else {
    await api.post('/user', form.value);
  }
  closeModal();
  fetchUsers();
};
const editUser = (user) => {
  editMode.value = true;
  editId.value = user.id;
  form.value = { username: user.username, password: '', role_id: user.role_id };
  modalOpen.value = true;
};
const deleteUser = async (id) => {
  if (confirm('Hapus user?')) await api.delete(`/user/${id}`);
  fetchUsers();
};
const openModal = () => { editMode.value = false; form.value = { username: '', password: '', role_id: 2 }; modalOpen.value = true; };
const closeModal = () => { modalOpen.value = false; };
onMounted(fetchUsers);
</script>