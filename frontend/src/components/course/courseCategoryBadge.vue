<template>
  <span class="badge" style="background-color: #C69214;" v-if="category === 'SCIS'">SCIS</span>
  <span class="badge" style="background-color: #00558C;" v-else-if="category === 'SOB'">SOB</span>
  <span class="badge" style="background-color: #006341;" v-else-if="category === 'SOSS'">SOSS</span>
  <span class="badge" style="background-color: #00677F;" v-else-if="category === 'SOE'">SOE</span>
  <span class="badge" style="background-color: #3C1053;" v-else-if="category === 'SOL'">SOL</span>
  <span class="badge" style="background-color: #8A1538;" v-else-if="category === 'SOA'">SOA</span>
</template>

<script>
export default {
  props: {
    category: String,
  },
};
</script>