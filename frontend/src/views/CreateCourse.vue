<template>
    <div id="createcourse">
        <div class="container-fluid mt-5">
           <h2 class="text-center">Create Course For Registration</h2> 
           <CourseForm></CourseForm>
        </div>
    </div>
</template>

<script>
import CourseForm from "../components/CourseForm.vue"

export default {
    components: {
        CourseForm
    }
};

</script>