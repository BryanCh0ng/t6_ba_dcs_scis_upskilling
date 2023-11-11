<template>
  <div>
    <div class="col-12 d-flex">
        <div class="text-nowrap">{{ name }}</div>
        <div class="ms-2">
          <course-category-badge :category="category"></course-category-badge>
        </div>
      </div>
      <div class="col-12 text-grey two-lines text-start">
        {{ description }}
      </div>
  </div>
</template>
    
<script>
import courseCategoryBadge from './courseCategoryBadge.vue';

export default {
  components: {
    courseCategoryBadge
  },
  props: {
    name: String,
    category: String,
    description: String
  }
};
</script>
    