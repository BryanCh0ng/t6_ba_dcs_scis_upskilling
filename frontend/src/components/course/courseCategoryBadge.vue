<template>
  <span class="badge bg-warning" v-if="category === 'SCIS'">SCIS</span>
  <span class="badge bg-primary" v-else-if="category === 'SOB'">SOB</span>
  <span class="badge bg-success" v-else-if="category === 'SOSS'">SOSS</span>
  <span class="badge bg-light-blue" v-else-if="category === 'SOE'">SOE</span>
  <span class="badge bg-light-blue" v-else-if="category === 'SOL'">SOL</span>
  <span class="badge bg-light-blue" v-else-if="category === 'SOA'">SOA</span>
</template>

<script>
export default {
  props: {
    category: String,
  },
};
</script>