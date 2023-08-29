<template>
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body pt-1"> 
        <div class="modal-title pt-3">
          <h5>{{ course.course_Name }}
            <course-category-badge :category="course.coursecat_Name" class="align-items-center modal-course-cat"></course-category-badge>
          </h5>
        </div>
        <div class="mt-3">
            {{ message }}
        </div>
        <div>
          <button type="button" class="mt-4 btn btn-secondary" data-bs-dismiss="modal" aria-label="Close" @click="closeModal"></button>
        </div>
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
    course: Object,
    message: String,
  },
  methods: {
    closeModal() {
      this.$emit("close-modal");
      this.$emit('model-after-action-close', true);
    }
  }
};
</script>