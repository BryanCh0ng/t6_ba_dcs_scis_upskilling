<template>
    <CourseForm :view="view"></CourseForm>
</template>
  
<script>
import CourseForm from "@/components/forms/CourseForm.vue";

export default {
    name: "EditCourse",
    data() {
        return {
            view: "editCourse"
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
        }
    },
};
</script>
  