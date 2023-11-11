<template>
    <RunCourseForm :create="create" :runcourseId="runcourseId" />
</template>
  
<script>
import RunCourseForm from "@/components/forms/RunCourseForm.vue";
import UserService from "@/api/services/UserService.js";

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
    async created() {
        const user_ID = await UserService.getUserID();
        const role = await UserService.getUserRole(user_ID);
        if (role != 'Admin') {
            this.$router.push({ name: 'proposeCourse' }); 
        } else {
            document.title = "Edit Run Course | Upskilling Engagement System";
            this.runcourseId = this.$route.params.id;
        }
    },
};
</script>