<template>
  <span class="badge bg-warning" v-if="category === 'SCIS'">SCIS</span>
  <span class="badge bg-primary" v-else-if="category === 'LKCSB'">LKCSB</span>
  <span class="badge bg-success" v-else-if="category === 'SOSS'">SOSS</span>
  <span class="badge bg-light-blue" v-else-if="category === 'SOE'">SOE</span>
</template>

<script>
export default {
  props: {
    category: String,
  },
};
</script>
