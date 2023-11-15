<template>
    <div id="proposecourseform">
        <div class="container-fluid mt-5">
            <h2 class="text-center">Propose Course</h2>
            <form @submit.prevent="onSubmit" @reset="onReset">
                <!--Course Name-->
                <div class="form-group mt-5 mb-4">
                    <input v-model="formData.courseName" type="text" placeholder="Course Name" required autofocus
                        :class="{ 'form-control': true, 'border-0': !v$?.formData.courseName?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.courseName?.$error }" />
                    <div v-if="v$?.formData.courseName?.$error" class="text-danger">
                        <span v-for="error in v$?.formData.courseName?.$errors" :key="error.$uid">{{ error.$message
                        }}</span>
                    </div>
                </div>
                <!--Course Category-->
                <div class="form-group mb-4">
                    <dropdown-field v-model="formData.selectedCategory" :default-placeholder="'Course Category'"
                        :errors="v$?.formData.selectedCategory?.$errors[0]?.$message">
                        <option v-for="courseCategory in formData.courseCategories" :key="courseCategory.coursecat_ID"
                            :value="courseCategory.coursecat_Name">
                            {{ courseCategory.coursecat_Name }}
                        </option>
                    </dropdown-field>
                </div>
                <!--Course Description-->
                <div class="form-group mb-4">
                    <textarea v-model="formData.courseDescription"
                        :class="{ 'form-control': true, 'border-0': !v$?.formData.courseDescription?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.courseDescription?.$error }"
                        placeholder="Course Description" style="height: 200px" required></textarea>
                    <div v-if="v$?.formData.courseDescription?.$error" class="text-danger">
                        <span v-for="error in v$?.formData.courseDescription?.$errors" :key="error.$uid">{{ error.$message
                        }}</span>
                    </div>
                </div>

                <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                    Submit
                </button>

                <!--<div v-else class="row">
                    <div class="col-md-6 form-group">
                        <button type="button" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                            Cancel
                        </button>
                    </div>

                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                            Save
                        </button>
                    </div>
                </div>-->
            </form>
        </div>
        <!-- Success modal -->
        <AlertDefaultVue :visible="showAlert" variant="success"></AlertDefaultVue>
    </div>
</template>
<script>
import DropdownField from "../DropdownField.vue";
import CourseCategoryService from "@/api/services/CourseCategoryService.js";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers } from "@vuelidate/validators";
import CourseService from "@/api/services/CourseService";
import UserService from "@/api/services/UserService";
import proposedCourseService from "@/api/services/proposedCourseService";

export default {
    name: "ProposeCourseForm",
    setup() {
        const v$ = useVuelidate(); 
        return { v$ };
    },
    data() {
        return {
            userID: 0,
            formData: {
                courseName: "",
                selectedCategory: "",
                courseCategories: [],
                courseDescription: ""
            },
            createCourseResponse: {},
            submitFormData: {}
        }
    },
    components: {
        DropdownField
    },
    validations() {
        return {
            formData: {
                courseName: { required: helpers.withMessage('Please provide a valid course Name', required) },
                selectedCategory: { required: helpers.withMessage('Please select a valid course category', required) },
                courseDescription: { required: helpers.withMessage('Please provide a valid course description', required) }
            }
        }
    }
    async mounted() {
        await this.fetchUserID();
        await this.fetchCourseCategories();
    },
    methods: {
        async fetchUserID() {
            try {
                this.userID = await UserService.getUserID();
            } catch (error) {
                console.error("Error fetching user id: ", error);
            }
        },
        async fetchCourseCategories() {
            try {
                this.formData.courseCategories = await CourseCategoryService.getAllCourseCategory();
            } catch (error) {
                console.error('Error fetching course categories:', error);
            }
        },
        async createCourse() {
            try {
                this.createCourseResponse = await CourseService.createCourse(this.submitFormData);
            } catch (error) {
                console.error('Error creating a new course', error);
            }
        },
        async createProposedCourse() {
            try {
                this.createProposedCourseResponse = await proposedCourseService.createProposedCourse(this.submitFormData);
                console.log(this.createProposedCourseResponse)
            } catch (error) {
                console.error('Error creating a new proposed course', error);
            }
        },
        async onSubmit() {
            this.v$.$touch();

            if (!this.v$.$invalid) {

                this.submitFormData["course_Name"] = this.formData.courseName;

                this.submitFormData["course_Desc"] = this.formData.courseDescription;

                this.submitFormData["coursecat_ID"] = this.formData.courseCategories.find(i => i.coursecat_Name === this.formData.selectedCategory).coursecat_ID;

                await this.createCourse();

                this.submitFormData = {};

                //Need to delete this ltr
                this.user = await this.fetchUserID();

                this.submitFormData["submitted_By"] = this.user;

                this.submitFormData["course_ID"] = this.createCourseResponse["course_ID"];

                //this.submitFormData["course_ID"] = 1;

                await this.createProposedCourse();

                console.log('Form submitted successfully');
            } else {
                console.log('Form has validation errors');
            }
        }
    }
}
</script>