<template>
   <CourseForm :status="status"></CourseForm>
</template>

<script>
import CourseForm from "../components/CourseForm.vue"

export default {
    data() {
        return {
            status: true
        };
    },
    components: {
        CourseForm
    }
};

</script>