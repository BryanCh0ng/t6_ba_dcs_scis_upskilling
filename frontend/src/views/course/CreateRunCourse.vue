<template>
    <RunCourseForm :create="create" :courseId="courseId"/>
</template>
  
<script>
import RunCourseForm from "@/components/forms/RunCourseForm.vue";

export default {
    name: "CreateRunCourse",
    data() {
        return {
            create: true,
            courseId: null
        };
    },
    components: {
        RunCourseForm
    },
    created() {
        document.title = "Create a Run Course";
        this.courseId = this.$route.params.id;
    },
};
</script>
  