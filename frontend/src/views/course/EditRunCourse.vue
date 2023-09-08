<template>
    <RunCourseForm :create="create" :runcourseId="runcourseId" />
</template>
  
<script>
import RunCourseForm from "@/components/forms/RunCourseForm.vue";

export default {
    name: "EditRunCourse",
    data() {
        return {
            create: false, 
            runcourseId: null
        };
    },
    components: {
        RunCourseForm
    },
    created() {
        document.title = "Edit Run Course";
        this.runcourseId = this.$route.params.id;
    },
};
</script>