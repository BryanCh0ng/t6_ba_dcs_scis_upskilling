<template>
    <CourseForm :view="view"></CourseForm>
</template>
  
<script>
import CourseForm from "@/components/forms/CourseForm.vue";

export default {
    name: "EditCourse",
    data() {
        return {
            view: "editCourse"
        };
    },
    components: {
        CourseForm
    },
    created() {
        document.title = "Edit Course";
    },
};
</script>
  