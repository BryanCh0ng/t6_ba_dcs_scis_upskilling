<template>
    <CourseForm :view="view"></CourseForm>
</template>
  
<script>
import CourseForm from "@/components/forms/CourseForm.vue";

export default {
    name: "CreateCourse",
    data() {
        return {
            view: "createCourse"
        };
    },
    components: {
        CourseForm
    },
    created() {
        document.title = "Create Course For Registration";
    },
};
</script>
  