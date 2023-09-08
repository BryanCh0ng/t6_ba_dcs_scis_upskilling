<template>
    <RunCourseForm :create="create" />
</template>
  
<script>
import RunCourseForm from "@/components/forms/RunCourseForm.vue";

export default {
    name: "EditRunCourse",
    data() {
        return {
            create: false
        };
    },
    components: {
        RunCourseForm
    },
    created() {
        document.title = "Edit Run Course";
    },
};
</script>