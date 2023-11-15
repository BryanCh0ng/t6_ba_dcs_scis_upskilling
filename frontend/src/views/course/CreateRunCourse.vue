<template>
    <RunCourseForm :create="create" :courseId="courseId"/>
</template>
  
<script>
import RunCourseForm from "@/components/forms/RunCourseForm.vue";
import UserService from "@/api/services/UserService.js";

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
    async created() {
        const user_ID = await UserService.getUserID();
        const role = await UserService.getUserRole(user_ID);
        if (role != 'Admin') {
            this.$router.push({ name: 'proposeCourse' }); 
        } else {
            document.title = "Create Run Course | Upskilling Engagement System";
            this.courseId = this.$route.params.id;
        }
    },
};
</script>
  