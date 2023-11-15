<template>
    <CourseForm :view="view"></CourseForm>
</template>
  
<script>
import CourseForm from "@/components/forms/CourseForm.vue";
import UserService from "@/api/services/UserService.js";

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
    async created() {
        const user_ID = await UserService.getUserID();
        const role = await UserService.getUserRole(user_ID);
        if (role != 'Admin') {
            this.$router.push({ name: 'proposeCourse' }); 
        } else {
            document.title = "Create Course | Upskilling Engagement System";
        }
    },
};
</script>
  