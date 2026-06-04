<template>
  <div class="table-responsive">
    <table class="tuud-table">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <slot></slot>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  headers: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.table-responsive {
  width: 100%;
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  background: white;
}

.tuud-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  background-color: #FFF2E6; /* Warna peach/oranye lembut latar tabel sesuai rencana */
}

.tuud-table th {
  background-color: #3b82f6; /* Header tabel Biru */
  color: white;
  padding: 12px 16px;
  font-size: 0.9rem;
  font-weight: 600;
  white-space: nowrap;
}

.tuud-table :deep(td) {
  padding: 12px 16px;
  border-bottom: 1px solid #FFE4CC;
  color: #333333;
  font-size: 0.9rem;
  vertical-align: middle;
}

.tuud-table :deep(tr:last-child td) {
  border-bottom: none;
}
</style>