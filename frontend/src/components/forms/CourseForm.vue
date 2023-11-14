<template>
    <div id="courseform">
        <div class="container pt-5">
            <h2 v-if="view === 'createCourse'" class="text-center">Create Course</h2>
            <h2 v-else-if="view === 'proposeCourse'" class="text-center">Propose Course</h2>
            <h2 v-else class="text-center">Edit Course</h2>

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
                        placeholder="Course Description" style="height: 200px" @input="limitCourseDescription"
                        required></textarea>
                    <div class="text-muted mt-2">
                        Character Count: {{ courseDescLength }}/800
                    </div>
                    <div v-if="v$?.formData.courseDescription?.$error" class="text-danger">
                        <span v-for="error in v$?.formData.courseDescription?.$errors" :key="error.$uid">{{ error.$message
                        }}</span>
                    </div>
                </div>

                <div v-if="view === 'createCourse' || view === 'proposeCourse'" class="row mt-5">
                    <div class="col-md-6 form-group">
                        <button type="reset" class="btn btn-secondary shadow-sm w-100 field cancelbtn">
                            Reset
                        </button>
                    </div>

                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <button type="submit" class="btn btn-block shadow-sm w-100 field submitbtn">
                            Submit
                        </button>
                    </div>
                </div>

                <div v-else class="row mt-5">
                    <div class="col-md-6 form-group">
                        <button type="button" @click="goToAdminViewCourse"
                            class="btn btn-secondary shadow-sm w-100 field cancelbtn">
                            Cancel
                        </button>
                    </div>

                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <button type="submit" class="btn btn-block shadow-sm w-100 field submitbtn">
                            Save
                        </button>
                    </div>
                </div>
            </form>
        </div>
        <!-- Success modal -->
        <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType"
            @modal-closed="handleModalClosed" />
    </div>
</template>
<script>
import DropdownField from "./DropdownField.vue";
import CourseCategoryService from "@/api/services/CourseCategoryService.js";
import DefaultModal from "../DefaultModal.vue";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers, maxLength } from "@vuelidate/validators";
import CourseService from "@/api/services/CourseService";
import UserService from "@/api/services/UserService";
import proposedCourseService from "@/api/services/proposedCourseService";

export default {
    name: "CourseForm",
    props: {
        view: {
            type: String,
            required: true
        },
        courseId: {
            type: Number
        }
    },
    setup() {
        const v$ = useVuelidate();
        return { v$ };
    },
    data() {
        return {
            formData: {
                courseName: "",
                selectedCategory: "",
                courseCategories: [],
                courseDescription: ""
            },
            title: "",
            message: "",
            buttonType: "",
            showAlert: false,
            courseID: 0,
            coursecatID: 0,
            createCourseResponse: {},
            userID: 0,
            createProposedCourseResponse: {},
            updateCourseResponse: {},
            submitFormData: {}
        }
    },
    components: {
        DropdownField,
        DefaultModal
    },
    validations() {
        return {
            formData: {
                courseName: { required: helpers.withMessage('Please provide a valid course name', required) },
                selectedCategory: { required: helpers.withMessage('Please select a valid course category', required) },
                courseDescription: { required: helpers.withMessage('Please provide a valid course description', required), maxLength: maxLength(800) }
            }
        }
    },
    async mounted() {
        try {
            await this.fetchCourseCategories();

            if (this.view === "editCourse") {
                await this.fetchEditCourseData();
            }

        } catch (error) {
            const errorMsgParts = error.toString().split(":");
            this.message = errorMsgParts[1];
            this.buttonType = "danger";
            this.showAlert = !this.showAlert;
        }

    },
    methods: {
        limitCourseDescription() {
            if (this.formData.courseDescription.length > 800) {
                this.formData.courseDescription = this.formData.courseDescription.substring(0, 800); // Limit the description to 800 characters
            }
        },
        async handleModalClosed(value) {
            this.showAlert = value;

            if (!this.showAlert && this.buttonType === "success") {
                if (this.view === "proposeCourse") {
                    this.userRole = await UserService.getUserRole();
                    if (this.userRole === 'Student') {
                        this.$router.push({ name: 'studentViewProfile' });
                    } else if (this.userRole === 'Instructor' || this.userRole === 'Trainer') {
                        this.$router.push({ name: 'instructorTrainerViewProfile' });
                    }
                } else {
                    this.$router.push('/adminViewCourse');
                }

            }
        },
        async fetchCourseCategories() {
            try {
                this.formData.courseCategories = await CourseCategoryService.getAllCourseCategory();

            } catch (error) {
                console.error('Error fetching course categories:', error);

                this.title = "Form Data Retrieval Error";

                throw new Error("There is a problem retrieving the data for the form fields");
            }
        },
        async fetchCourseByID() {
            try {
                const courseData = await CourseService.getCourseById(this.courseId);

                this.formData.courseName = courseData.data.course[0].course_Name;
                this.coursecatID = courseData.data.course[0].coursecat_ID;
                this.formData.courseDescription = courseData.data.course[0].course_Desc;

            } catch (error) {
                console.error('Error fetching course by ID:', error);

                throw new Error("An error occurred in fetching course by ID");
            }
        },
        async fetchCourseCategoryByID() {
            try {
                const coursecatData = await CourseCategoryService.getCategoryById(this.coursecatID);

                this.formData.selectedCategory = coursecatData.coursecat_Name;

            } catch (error) {
                console.error('Error fetching course category by ID:', error);

                throw new Error("An error occurred in fetching course category by ID");
            }
        },
        async fetchEditCourseData() {
            try {
                await this.fetchCourseByID();
                await this.fetchCourseCategoryByID();

            } catch (error) {
                this.title = "Course Data Retrieval Error";
                throw new Error("There is a problem retrieving the data for this course");
            }
        },
        async createCourse() {
            try {
                this.createCourseResponse = await CourseService.createCourse(this.submitFormData);
            } catch (error) {
                console.error('Error creating a new course', error);
                this.title = "Course Creation Failed";

                if (error.response.status === 500) {
                    throw new Error("Course Creation was unsuccessful");
                } else {
                    throw new Error(error.response.data.message);
                }
            }
        },
        async fetchUserID() {
            try {
                this.userID = await UserService.getUserID();

            } catch (error) {
                console.error("Error fetching user id: ", error);
                this.title = "Propose Course Creation Failed";
                throw new Error("Proposed Course Creation was unsuccessful");
            }
        },
        async createProposedCourse() {
            try {

                this.createProposedCourseResponse = await proposedCourseService.createProposedCourse(this.submitFormData);

            } catch (error) {
                console.error('Error creating a new proposed course', error);
                this.title = "Propose Course Creation Failed";
                throw new Error("Proposed Course Creation was unsuccessful");
            }
        },
        async updateCourse() {
            try {
                this.updateCourseResponse = await CourseService.editCourse(this.courseId, this.submitFormData);

            } catch (error) {
                console.error('Error updating the course:', error);
                this.title = "Course Update Failed";
                //throw new Error("Course Update was unsuccessful");

                if (error.response.status === 500) {
                    throw new Error("Course Update was unsuccessful");
                } else {
                    throw new Error(error.response.data.message);
                }
            }
        },
        goToAdminViewCourse() {
            this.$router.push("/adminViewCourse");
        },
        async onReset() {
            this.v$.$reset();

            this.formData = {
                courseName: "",
                selectedCategory: "",
                courseCategories: [],
                courseDescription: ""
            },
                this.submitFormData = {}

            try {
                await this.fetchCourseCategories();

            } catch (error) {
                const errorMsgParts = error.toString().split(":");
                this.message = errorMsgParts[1];
                this.buttonType = "danger";
                this.showAlert = !this.showAlert;
            }
        },
        formatDateToYYYYMMDD(dateObj) {
            const parsedYear = dateObj.getUTCFullYear();
            const parsedMonth = String(dateObj.getUTCMonth() + 1).padStart(2, "0");
            const parsedDay = String(dateObj.getUTCDate()).padStart(2, "0");
            return `${parsedYear}-${parsedMonth}-${parsedDay}`;
        },
        setSuccessAlert(action) {
            this.title = `${action} Success`;
            this.message = `${action} was successful`;
            this.buttonType = "success";
            this.showAlert = !this.showAlert;
        },
        async onSubmit() {
            this.v$.$touch();

            if (!this.v$.$invalid) {

                console.log('Form has no validation errors');

                try {

                    this.submitFormData["course_Name"] = this.formData.courseName;

                    this.submitFormData["course_Desc"] = this.formData.courseDescription;

                    this.submitFormData["coursecat_ID"] = this.formData.courseCategories.find(i => i.coursecat_Name === this.formData.selectedCategory).coursecat_ID;

                    this.submitFormData["course_Status"] = "Active";

                    if (this.view === "createCourse") {

                        await this.createCourse();

                        this.setSuccessAlert("Course Creation");

                    } else if (this.view === "proposeCourse") {

                        this.submitFormData["course_Status"] = "Inactive";

                        await this.createCourse();

                        this.submitFormData = {};

                        await this.fetchUserID();

                        this.submitFormData["submitted_By"] = this.userID;

                        //this.submitFormData["course_ID"] = this.createCourseResponse["course_ID"];
                        this.submitFormData["course_ID"] = this.createCourseResponse.data.course_ID;

                        const today = new Date();

                        this.submitFormData["proposed_Date"] = this.formatDateToYYYYMMDD(today);

                        await this.createProposedCourse();

                        this.setSuccessAlert("Propose Course Creation");

                    } else {
                        await this.updateCourse();

                        this.setSuccessAlert("Course Update");
                    }

                } catch (error) {
                    const errorMsgParts = error.toString().split(":")
                    this.message = errorMsgParts[1];
                    this.buttonType = "danger"
                    this.showAlert = !this.showAlert;
                }
            } else {
                console.log('Form has validation errors');
            }
        }
    },
    computed: {
        courseDescLength() {
            return this.formData.courseDescription.length;
        }
    }
}
</script>