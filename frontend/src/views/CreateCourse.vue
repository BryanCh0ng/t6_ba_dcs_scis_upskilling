<template>
  <CourseForm :status="status"></CourseForm>
</template>

<script>
import CourseForm from "../components/CourseForm.vue";

export default {
  name: "CreateCourse",
  data() {
    return {
      status: true,
    };
  },
  components: {
    CourseForm
  },
  created() {
    document.title = "Create Course";
  },
};
</script>
