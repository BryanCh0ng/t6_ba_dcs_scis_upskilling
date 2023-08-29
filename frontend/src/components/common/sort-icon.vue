<template>
  <span>
      <span v-if="sortColumn">
        <span v-if="sortDirection === 'asc'">🔼</span>
        <span v-else-if="sortDirection === 'desc'">🔽</span>
      </span>
    </span>
</template>
  
<script>
export default {
  props: {
    sortColumn: Boolean,
    sortDirection: String
  },
};
</script>
  