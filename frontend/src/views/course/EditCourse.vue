<template>
    <CourseForm :view="view" :courseId="courseId"></CourseForm>
</template>
  
<script>
import CourseForm from "@/components/forms/CourseForm.vue";

export default {
    name: "EditCourse",
    data() {
        return {
            view: "editCourse",
            courseId: null
        };
    },
    components: {
        CourseForm
    },
    created() {
        document.title = "Edit Course";
        this.courseId = this.$route.params.id;
        console.log(this.courseId)
    },
};
</script>
  