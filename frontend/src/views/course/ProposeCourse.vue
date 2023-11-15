<template>
    <CourseForm :view="view"></CourseForm>
</template>
  
<script>
import CourseForm from "@/components/forms/CourseForm.vue";

export default {
    name: "ProposeCourse",
    data() {
        return {
            view: "proposeCourse"
        };
    },
    components: {
        CourseForm
    },
    created() {
        document.title = "Propose Course | Upskilling Engagement System";
    },
};
</script>
  