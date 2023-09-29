<template>
    <CourseForm :view="view" :courseId="courseId"></CourseForm>
</template>
  
<script>
import CourseForm from "@/components/forms/CourseForm.vue";
import UserService from "@/api/services/UserService.js";

export default {
    name: "EditCourse",
    data() {
        return {
            view: "editCourse",
            courseId: null
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
            document.title = "Edit Course";
            this.courseId = this.$route.params.id;
            console.log(this.courseId)
        }
    },
};
</script>
  