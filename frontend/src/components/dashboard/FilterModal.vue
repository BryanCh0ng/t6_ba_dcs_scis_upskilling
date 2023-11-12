<template>
    <div v-if="OpenClose" class="modal fade show custom-modal-backdrop" tabindex="1" aria-labelledby="exampleModalLabel"
        aria-modal="true" role="dialog" style="display:block;">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="btn-close" @click="OpenCloseFun()" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <h3 style="text-align: center;">Dashboard Filters</h3>
                    <form @submit.prevent="onSubmit" @reset="onReset">
                        <!--Course-->
                        <div v-if="currentPage!=='course'" class="form-group mt-5 mb-4">
                            <label for="course" class="mb-2">Course</label>
                            <select class="form-select" size="3" multiple aria-label="multiple select example" id="course" v-model="formData.selectedCourses">
                                <option v-for="course in formData.courses" :key="course.course_ID"
                                    :value="course.course_ID">
                                    {{ course.course_Name }}
                                </option>
                            </select>
                        </div>
                        <!--Course Category-->
                        <div v-if="currentPage!=='course'" class="form-group mb-4">
                            <label for="coursecat" class="mb-2">Course Category</label>
                            <select class="form-select" size="3" multiple aria-label="multiple select example"
                                id="coursecat" v-model="formData.selectedCourseCats">
                                <option v-for="coursecat in formData.courseCats" :key="coursecat.coursecat_ID"
                                    :value="coursecat.coursecat_ID">
                                    {{ coursecat.coursecat_Name }}
                                </option>
                            </select>
                        </div>
                        <!--Run Course-->
                        <div class="form-group mb-4">
                            <label for="runcourse" class="mb-2">Run Course</label>
                            <select class="form-select" size="3" multiple aria-label="multiple select example"
                                id="runcourse" v-model="formData.selectedRunCourses">
                                <option v-for="runcourse in formData.runCourses" :key="runcourse.rcourse_ID"
                                    :value="runcourse.rcourse_ID">
                                    {{ runcourse.run_Name }}
                                </option>
                            </select>
                        </div>
                        <!--Instructor / Trainer-->
                        <div v-if="currentPage!=='coach'" class="form-group mb-4">
                            <label for="coach" class="mb-2">Instructor / Trainer</label>
                            <select class="form-select" size="3" multiple aria-label="multiple select example" id="coach"  v-model="formData.selectedCoaches">
                                <option v-for="coach in formData.coaches" :key="coach.user_ID" :value="coach.user_ID">
                                    {{ coach.user_Name }}
                                </option>
                            </select>
                        </div>
                        <div class="row mb-4">
                            <!--Start Date-->
                            <div class="col-md-6 form-group">
                                <label for="startdate" class="mb-2">Start Date</label>
                                <VueDatePicker v-model="formData.startDate" placeholder="Start Date"
                                    :enable-time-picker="false"
                                    :class="{'border-0': !v$?.formData.startDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.startDate?.$error }"
                                    input-class-name="dp-custom-input" :format="this.formData.datePickerFormat">
                                </VueDatePicker>
                                <div v-if="v$?.formData.startDate?.$error" class="text-danger">
                                    <span v-for="error in v$?.formData.startDate?.$errors" :key="error.$uid">{{
                                        error.$message
                                    }}</span>
                                </div>
                            </div>
                            <!--End Date-->
                            <div class="col-md-6 form-group mt-4 mt-md-0">
                                <label for="enddate" class="mb-2">End Date</label>
                                <VueDatePicker v-model="formData.endDate" placeholder="End Date" :enable-time-picker="false"
                                    :class="{'border-0': !v$?.formData.endDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.endDate?.$error }"
                                    input-class-name="dp-custom-input" :format="this.formData.datePickerFormat">
                                </VueDatePicker>
                                <div v-if="v$?.formData.endDate?.$error" class="text-danger">
                                    <span v-for="error in v$?.formData.endDate?.$errors" :key="error.$uid">{{ error.$message
                                    }}</span>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 form-group d-flex justify-content-center">
                                <button type="reset" class="btn btn-secondary shadow-sm w-50 mt-5 field cancelbtn">
                                    Clear All
                                </button>
                            </div>

                            <div class="col-md-6 form-group mt-4 mt-md-0 d-flex justify-content-center">
                                <button type="submit" class="btn btn-block shadow-sm w-50 mt-5 field submitbtn">
                                    Apply
                                </button>
                            </div>
                        </div>
                        <!--<button type="button" @click="OpenCloseFun()" class="btn btn-primary">Close</button>-->
                    </form>
                </div>
            </div>
        </div>

        <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
    </div>
</template>
  
<script>
import CourseService from "@/api/services/CourseService";
import CourseCategoryService from "@/api/services/CourseCategoryService";
import RunCourseService from "@/api/services/runCourseService";
import UserService from "@/api/services/UserService";
import DefaultModal from "../DefaultModal.vue";
import { useVuelidate } from "@vuelidate/core";
import { helpers } from "@vuelidate/validators";

//Function: Check whether End Date is equal to or greater than the Start Date 
const validateEndDateFromStartDate = function (value) {
    if (value === null || this.formData.startDate === null) {
        return true;
    }

    if (value.getFullYear() > this.formData.startDate.getFullYear() || (value.getFullYear() === this.formData.startDate.getFullYear() && (value.getMonth() + 1) > (this.formData.startDate.getMonth() + 1)) ||
        (value.getFullYear() === this.formData.startDate.getFullYear() && value.getMonth() === this.formData.startDate.getMonth() && value.getDate() >= this.formData.startDate.getDate())) {
        return true;
    }

    return false;
};

const endDateFromStartDateValidator = helpers.withParams(
    { type: 'endDateFromStartDate' },
    validateEndDateFromStartDate
);

const endDateFromStartDateValidatorWithMessage = helpers.withMessage(
    'Please select an end date that falls on or after the selected start date',
    endDateFromStartDateValidator
)

// Function: Check whether End Date is null when Start Date is selected
const validateEndDate = function (value) {
    if (value === null && this.formData.startDate !== null) {
        return false;
    }

    return true;
}

const endDateValidator = helpers.withParams(
    { type: 'endDate' },
    validateEndDate
)

const endDateValidatorWithMessage = helpers.withMessage(
    'Please select an end date that falls on or after the selected start date',
    endDateValidator
)

// Function: Check whether Start Date is null when End Date is selected
const validateStartDate = function (value) {
    if (value === null && this.formData.endDate !== null) {
        return false;
    }

    return true;
}

const startDateValidator = helpers.withParams(
    { type: 'startDate' },
    validateStartDate
)

const startDateValidatorWithMessage = helpers.withMessage(
    'Please select a start date',
    startDateValidator
)

export default {
    name: 'FilterModal',
    props: {
        visible: Boolean,
        currentPage: {
            type: String,
            required: true
        }
    },
    setup() {
        // Initialize Vuelidate
        const v$ = useVuelidate();
        return { v$ };
    },
    data() {
        return {
            OpenClose: this.visible,
            formData: {
                selectedCourses: [],
                courses: [],
                selectedRunCourses: [],
                runCourses: [],
                selectedCoaches: [],
                coaches: [],
                selectedCourseCats: [],
                courseCats: [],
                datePickerFormat: "dd/MM/yyyy",
                startDate: null, 
                endDate: null
            },
            errorMsg: [],
            //Modal 
            title: "",
            message: "",
            buttonType: "",
            showAlert: false
        }
    },
    components: {
        DefaultModal
    },
    validations() {
        return {
            formData: {
                startDate: { startDate: startDateValidatorWithMessage },
                endDate: { endDateFromStartDate: endDateFromStartDateValidatorWithMessage, endDate: endDateValidatorWithMessage }
            }
        }
    },
    async mounted() {
        try {
            await this.fetchFilterData();
        } catch (error) {
            const errorMsgParts = error.toString().split(":")
            this.message = errorMsgParts[1];
            this.buttonType = "danger"
            this.showAlert = !this.showAlert;
        }
    },
    methods: {
        OpenCloseFun() {
            this.OpenClose = false;
            document.body.style.overflowY = 'auto';
            this.$emit('modal-closed', this.OpenClose);
        },
        async fetchAllCourses() {
            try {
                let response = await CourseService.getAllCoursesAdmin();
                this.formData.courses = response.data.course;
            } catch (error) {
                // console.error('Error fetching all courses: ', error);
                this.errorMsg.push('Error fetching all courses:', error);
            }
        },
        async fetchAllCourseCats() {
            try {
                let response = await CourseCategoryService.getAllCourseCategory();
                this.formData.courseCats = response;
            } catch (error) {
                this.errorMsg.push('Error fetching all course categories', error)
            }
        },
        async fetchAllRunCourses() {
            try {
                let response = await RunCourseService.getAllRunCourses();
                this.formData.runCourses = response.data.course;
            } catch (error) {
                this.errorMsg.push('Error fetching all run courses', error);
            }
        },
        async fetchAllCoaches() {
            try {
                let response = await UserService.getAllCoaches();
                this.formData.coaches = response;
            } catch (error) {
                // console.error('Error fetching all instructors and trainers: ', error)
                this.errorMsg.push('Error fetching all instructors and trainers', error)
            }
        },
        async fetchFilterData() {
            await this.fetchAllCourses()
            await this.fetchAllCoaches()
            await this.fetchAllRunCourses()
            await this.fetchAllCourseCats()

            if (this.errorMsg.length > 0) {
                this.title = "Dashboard Filter Data Retrieval Error";
                throw new Error("There is a problem retrieving the data for the dashboard filter")
            }
        },
        async onReset() {
            this.v$.$reset();
            
            this.formData =  {
                selectedCourses: [],
                courses: [],
                selectedRunCourses: [],
                runCourses: [],
                selectedCoaches: [],
                coaches: [],
                selectedCourseCats: [],
                courseCats: [],
                datePickerFormat: "dd/MM/yyyy",
                startDate: null, 
                endDate: null
            },
            this.errorMsg = [],
            //Modal 
            this.title = "",
            this.message =  "",
            this.buttonType =  "",
            this.showAlert = false

            try {
                await this.fetchFilterData();
            } catch (error) {
                const errorMsgParts = error.toString().split(":")
                this.message = errorMsgParts[1];
                this.buttonType = "danger"
                this.showAlert = !this.showAlert;
            }
            
        },
        async onSubmit() {
            this.v$.$touch();

            if (!this.v$.$invalid) {
                // Form is valid, submit or perform further actions
                this.$emit('apply-filters', {
                    courses: this.formData.selectedCourses,
                    coursecats: this.formData.selectedCourseCats,
                    runcourses: this.formData.selectedRunCourses,
                    coaches: this.formData.selectedCoaches,
                    startDate: this.formData.startDate,
                    endDate: this.formData.endDate,
                })

                this.OpenCloseFun()

            } else {
                // Form has validation errors
                console.log('Filter has validation errors');
            }

        }
    },
    watch: {
        visible: function (newVal) {
            this.OpenClose = newVal;
            if (this.OpenClose) {
                document.body.style.overflowY = 'hidden';
            }
        }
    }
}
</script>
  
<style scoped>
.custom-modal-backdrop {
    background-color: rgba(0, 0, 0, 0.5);
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1050;
}

.modal-dialog {
    max-width: 40%;
}
</style>

<style lang="scss">
//For the datepicker and timepicker fields 
.dp-custom-input {
    font-size: 18px;

    &::placeholder {
        /* Change the placeholder color here */
        color: black;
    }
}
</style>