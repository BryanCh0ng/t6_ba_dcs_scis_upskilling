<template>
    <ProposeCourseForm />
</template>
  
  <script>
  import ProposeCourseForm from "@/components/course/proposeCourseForm.vue"
  
  export default {
      name: "StudentProposeCourse",
      data() {
         return {
              status: false
          };
      },
      components: {
          ProposeCourseForm
      },
      created() {
          document.title = "Propose a Course";
      },
  };
  </script>
  