<template>
    <div>
       <template v-if="role === 'Admin'">
         <CourseForm :view="view"></CourseForm>
       </template>
     </div> 
   </template>
     
   <script>
   import CourseForm from "@/components/forms/CourseForm.vue";
   import UserService from "@/api/services/UserService.js";
   
   export default {
       name: "EditCourse",
       data() {
           return {
               view: "editCourse",
               courseId: null,
               role: null,
           };
       },
       components: {
           CourseForm
       },
       async created() {
           const user_ID = await UserService.getUserID();
           this.role = await UserService.getUserRole(user_ID);
           if (this.role != 'Admin') {
               this.$router.push({ name: 'proposeCourse' }); 
           } else {
               document.title = "Edit Course";
           }
       },
   };
   </script>
     
  