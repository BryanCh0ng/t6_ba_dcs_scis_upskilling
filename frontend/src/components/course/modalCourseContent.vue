<template>
  <div class="modal-content">
    <div class="modal-header">
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body pt-1"> 
      <div class="modal-title pt-3">
        <h5>{{ course.name }}
          <course-category-badge :category="course.category" class="align-items-center modal-course-cat"></course-category-badge>
        </h5>
      </div>
      <div>{{ course.description }}</div>
      <div v-if="course.status == 'Active'">
        <div class="pt-4 row">
          <div class="col-6">
            Course Start Date: <br> <strong>{{ course.start_date }}</strong>
          </div>
          <div class="col-6">
            Course Start Time: <br> <strong>{{ course.start_time }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Course End Date: <br> <strong>{{ course.end_date }}</strong>
          </div>
          <div class="col-6">
            Course End Time: <br> <strong>{{ course.end_time }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Course Venue: <br> <strong>{{ course.venue }}</strong>
          </div>
          <div class="col-6">
            Course Format: <br> <strong>{{ course.format }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Fee: <br> <strong>${{ course.fee }}</strong>
          </div>
          <div class="col-6">
            Available Slots: <br> <strong>{{ course.available_slots }}</strong>
          </div>
        </div>
        <div class="pt-3 row" v-if="regCountExists">
          <div class="col-6">
            Registration Count: <br> <strong>{{ course.reg_count }}</strong>
          </div>
        </div>
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
    course: Object
  },
  computed: {
    regCountExists() {
      return this.course.reg_count !== null && this.course.reg_count !== undefined;
    }
  }
};
</script>