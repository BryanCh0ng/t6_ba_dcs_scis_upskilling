<template>
    <RunCourseForm :create="create" />
</template>
  
<script>
import RunCourseForm from "@/components/forms/RunCourseForm.vue";

export default {
    name: "CreateRunCourse",
    data() {
        return {
            create: true
        };
    },
    components: {
        RunCourseForm
    },
    created() {
        document.title = "Create a Run Course";
    },
};
</script>
  