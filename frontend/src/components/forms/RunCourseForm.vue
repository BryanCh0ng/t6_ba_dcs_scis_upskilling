<template>
    <div id="runcourseform">
        <div class="container-fluid mt-5">
            <h2 v-if="create" class="text-center">Create Run Course</h2>

            <h2 v-else class="text-center">Edit Run Course</h2>

            <form @submit.prevent="onSubmit" @reset="onReset">
                <!--Instructor Name-->
                <div class="form-group mt-5 mb-4">
                    <dropdown-field v-model="formData.selectedInstructor" :default-placeholder="'Instructor'"
                        :errors="v$?.formData.selectedInstructor?.$errors[0]?.$message">
                        <option v-for="instructor in formData.instructors" :key="instructor.user_ID"
                            :value="instructor.user_Name">
                            {{ instructor.user_Name }}
                        </option>
                    </dropdown-field>
                </div>
                <div class="row mb-4">
                    <!--Start Date-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.startDate" placeholder="Start Date" :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.startDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.startDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.startDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.startDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--End Date-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.endDate" placeholder="End Date" :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.endDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.endDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.endDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.endDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>
                <div class="row mb-4">
                    <!--Start Time-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.startTime" placeholder="Start Time" time-picker required
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.startTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.startTime?.$error }"
                            input-class-name="dp-custom-input"><template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
                        </VueDatePicker>
                        <div v-if="v$?.formData.startTime?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.startTime?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--End Time-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.endTime" placeholder="End Time" time-picker required
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.endTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.endTime?.$error }"
                            input-class-name="dp-custom-input"><template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
                        </VueDatePicker>
                        <div v-if="v$?.formData.endTime?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.endTime?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>
                <div class="row mb-4">
                    <!--Course Format-->
                    <div class="col-md-6 form-group">
                        <dropdown-field v-model="formData.selectedFormat" :default-placeholder="'Course Format'"
                            :errors="v$?.formData.selectedFormat?.$errors[0]?.$message">
                            <option v-for="courseFormat in formData.courseFormats" :key="courseFormat.id"
                                :value="courseFormat.name">
                                {{ courseFormat.name }}
                            </option>
                        </dropdown-field>
                    </div>
                    <!--Venue-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <input v-model="formData.venue" type="text" placeholder="Venue" required autofocus
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.venue?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.venue?.$error }" />
                        <div v-if="v$?.formData.venue?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.venue?.$errors" :key="error.$uid">{{ error.$message }}</span>
                        </div>
                    </div>
                </div>
                <div class="row mb-4">
                    <!--Course Size-->
                    <div class="col-md-6 form-group">
                        <input v-model="formData.courseSize" type="text" placeholder="Course Size" required autofocus
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.courseSize?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.courseSize?.$error }" />
                        <div v-if="v$?.formData.courseSize?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.courseSize?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--Minimum Slots-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <input v-model="formData.minimumSlots" type="text" placeholder="Minimum Slots" required autofocus
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.minimumSlots?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.minimumSlots?.$error }" />
                        <div v-if="v$?.formData.minimumSlots?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.minimumSlots?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>
                <div class="row mb-4">
                    <!--Opening Date For Registration-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.openingDate" placeholder="Opening Date For Registration"
                            :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.openingDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.openingDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.openingDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.openingDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--Opening Time For Registration-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.openingTime" placeholder="Opening Time For Registration"
                            time-picker required
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.openingTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.openingTime?.$error }"
                            input-class-name="dp-custom-input"><template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
                        </VueDatePicker>
                        <div v-if="v$?.formData.openingTime?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.openingTime?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>
                <div class="row mb-4">
                    <!--Closing Date For Registration-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.closingDate" placeholder="Closing Date For Registration"
                            :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.closingDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.closingDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.closingDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.closingDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--Closing Time For Registration-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.closingTime" placeholder="Closing Time For Registration"
                            time-picker required
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.closingTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.closingTime?.$error }"
                            input-class-name="dp-custom-input"><template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
                        </VueDatePicker>
                        <div v-if="v$?.formData.closingTime?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.closingTime?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>
                <div class="row mb-4">
                    <!--Course Fee-->
                    <div class="col-md-6 form-group">
                        <input v-model="formData.courseFee" type="text" placeholder="Course Fee" required autofocus
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.courseFee?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.courseFee?.$error }" />
                        <div v-if="v$?.formData.courseFee?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.courseFee?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--Feedback Template-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <dropdown-field v-model="formData.selectedTemplate" :default-placeholder="'Feedback Template'"
                            :errors="v$?.formData.selectedTemplate?.$errors[0]?.$message">
                            <option v-for="feedbackTemplate in formData.feedbackTemplates"
                                :key="feedbackTemplate.template_ID" :value="feedbackTemplate.template_Name">
                                {{ feedbackTemplate.template_Name }}
                            </option>
                        </dropdown-field>
                    </div>
                </div>

                <!--<button v-if="status" type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
            Submit
          </button>-->

                <div v-if="create" class="row">
                    <div class="col-md-6 form-group">
                        <button type="reset" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                            Reset
                        </button>
                    </div>

                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                            Submit
                        </button>
                    </div>
                </div>

                <div v-else class="row">
                    <div class="col-md-6 form-group">
                        <button type="button" @click="goToAdminViewRunCourse" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                            Cancel
                        </button>
                    </div>

                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
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
//import InputField from "../components/InputField.vue";
import DropdownField from "./DropdownField.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import RunCourseService from "@/api/services/runCourseService.js";
import UserService from "@/api/services/UserService.js";
import FeedbackTemplateService from "@/api/services/FeedbackTemplateService.js"; //need to import
import { useVuelidate } from "@vuelidate/core";
import { required, numeric, helpers } from "@vuelidate/validators";
import DefaultModal from '../DefaultModal.vue';

//Validating numeric fields 

//Function: Check whether Minimum Slots is smaller than Course Size 
const validateMinSlotsSmallerThanCourseSize = function (value) {

    const numericRegex = /^[0-9]*$/;

    if (value === "" || this.formData.courseSize === "") {
        return true;
    }

    if (!value.match(numericRegex) || !this.formData.courseSize.match(numericRegex)) {
        return true; // Skip validation if either field is not numeric
    }

    return parseInt(value) < parseInt(this.formData.courseSize);
}

const minSlotsSmallerThanCourseSizeValidator = helpers.withParams(
    { type: 'minSlotsSmallerThanCourseSize' },
    validateMinSlotsSmallerThanCourseSize
);

const minSlotsSmallerThanCourseSizeValidatorWithMessage = helpers.withMessage(
    'Please select a minimum slot smaller than the selected course size',
    minSlotsSmallerThanCourseSizeValidator
)

//Validating the date fields

//Function: Check whether Start Date is greater than the Closing Date 
const validateStartDateGreaterThanClosingDate = function (value) {

    if (value === null || this.formData.closingDate === null) {
        return true;
    }

    if (value.getFullYear() > this.formData.closingDate.getFullYear() || (value.getFullYear() === this.formData.closingDate.getFullYear() && (value.getMonth() + 1) > (this.formData.closingDate.getMonth() + 1)) || (value.getFullYear() === this.formData.closingDate.getFullYear() && (value.getMonth() + 1) === (this.formData.closingDate.getMonth() + 1) && value.getDate() > this.formData.closingDate.getDate())) {
        return true;
    }

    return false;
};

const startDateGreaterThanClosingDateValidator = helpers.withParams(
    { type: 'startDateGreaterThanClosingDate' },
    validateStartDateGreaterThanClosingDate
);

const startDateGreaterThanClosingDateValidatorWithMessage = helpers.withMessage(
    'Please select a start date after the selected closing date for registration',
    startDateGreaterThanClosingDateValidator
)

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

//Function: Check whether Opening Date for Registration is equal to or greater than today's date 
// Define the custom validation function
const validateDateFromToday = (value) => {
    if (value === null) {
        return true; // Field is empty, so no validation needed
    }
    const selectedDate = new Date(value);
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Set today's time to midnight

    return selectedDate >= today;
};

// Create a custom validator using withParams and withMessage
const dateFromTodayValidator = helpers.withParams(
    { type: 'dateFromToday' },
    validateDateFromToday
);

const dateFromTodayValidatorWithMessage = helpers.withMessage(
    'Please select an opening date for registration from today onwards.',
    dateFromTodayValidator
);

//Function: Check whether Closing Date for Registration is greater than Opening Date for Registration
const validateClosingDateGreaterThanOpeningDate = function (value) {
    if (value === null || this.formData.openingDate === null) {
        return true;
    }

    if (value.getFullYear() > this.formData.openingDate.getFullYear() || (value.getFullYear() === this.formData.openingDate.getFullYear() && (value.getMonth() + 1) > (this.formData.openingDate.getMonth() + 1)) || (value.getFullYear() === this.formData.openingDate.getFullYear() && (value.getMonth() + 1) === (this.formData.openingDate.getMonth() + 1) && value.getDate() > this.formData.openingDate.getDate())) {
        return true;
    }

    return false;
};

const closingDateGreaterThanOpeningDateValidator = helpers.withParams(
    { type: 'closingDateFromOpeningDate' },
    validateClosingDateGreaterThanOpeningDate
);

const closingDateGreaterThanOpeningDateValidatorWithMessage = helpers.withMessage(
    'Please select a closing date for registration after the selected opening date for registration',
    closingDateGreaterThanOpeningDateValidator
)

//Validating the time fields 

//Function: Check whether End Time is greater than Start Time when Start Date and End Date are the same 
const validateEndTimeGreaterThanStartTime = function (value) {
    const allValuesFilled = (
        value !== null &&
        this.formData.startTime !== null &&
        this.formData.startDate !== null &&
        this.formData.endDate !== null
    );

    if (allValuesFilled) {
        if (this.formData.startDate.toISOString().split('T')[0] === this.formData.endDate.toISOString().split('T')[0]) {

            // Convert time values to seconds
            const startTimeInSeconds = parseInt(this.formData.startTime.hours) * 3600 + parseInt(this.formData.startTime.minutes) * 60 + parseInt(this.formData.startTime.seconds);
            const endTimeInSeconds = parseInt(value.hours) * 3600 + parseInt(value.minutes) * 60 + parseInt(value.seconds);

            // Compare time values in seconds
            return startTimeInSeconds < endTimeInSeconds;

        }
    }

    // Skip validation if any value is missing or start date doesn't equal end date
    return true;
};

const endTimeGreaterThanStartTimeValidator = helpers.withParams(
    { type: 'endTimeGreaterThanStartTime' },
    validateEndTimeGreaterThanStartTime
);

const endTimeGreaterThanStartTimeValidatorWithMessage = helpers.withMessage(
    'Please select an end time later than the selected start time',
    endTimeGreaterThanStartTimeValidator
)


//Validating the currency field

//Function: Check whether Course Fee matches the currency regex pattern
const validateCurrency = (value) => {
    if (value === "") {
        return true;
    }

    const currencyRegex = /^\d+(\.\d{1,2})?$/;
    return currencyRegex.test(value);
};

const currencyValidator = helpers.withParams(
    { type: 'currency' },
    validateCurrency
);
const currencyValidatorWithMessage = helpers.withMessage(
    'Please enter a valid currency amount.',
    currencyValidator
);

export default {
    name: "RunCourseForm",
    props: {
        create: {
            type: Boolean,
            required: true
        },
        runcourseId: {
            type: Number
        }
    },
    setup() {
        // Initialize Vuelidate
        const v$ = useVuelidate();
        return { v$ };
    },
    data() {
        return {
            //Initializing values for the form fields 
            formData: {
                selectedInstructor: "",
                instructors: [],
                datePickerFormat: "dd/MM/yyyy",
                startDate: null,
                endDate: null,
                startTime: null,
                endTime: null,
                selectedFormat: "",
                courseFormats: [
                    { id: 1, name: "Online" },
                    { id: 2, name: "Face-to-Face" },
                ],
                venue: "",
                courseSize: "",
                minimumSlots: "",
                openingDate: null,
                openingTime: null,
                closingDate: null,
                closingTime: null,
                courseFee: "",
                selectedTemplate: "",
                feedbackTemplates: [],
            },
            errorMsg: [],
            //Modal 
            title: "",
            message: "",
            buttonType: "",
            showAlert: false,
            //Edit Run Course
            instructorID: 0,
            templateID: 0,
            createRunCourseResponse: {},
            //Should be pass from the other page 
            courseID: 1,
            editRunCourseResponse: {},
            submitFormData: {}
        };
    },
    components: {
        VueDatePicker,
        //InputField,
        DropdownField,
        DefaultModal
    },
    validations() {
        return {
            formData: {
                selectedInstructor: { required: helpers.withMessage('Please select a valid instructor', required) },
                startDate: { required: helpers.withMessage('Please select a valid start date', required), startDateGreaterThanClosingDate: startDateGreaterThanClosingDateValidatorWithMessage },
                endDate: { required: helpers.withMessage('Please select a valid end date', required), endDateFromStartDate: endDateFromStartDateValidatorWithMessage },
                startTime: { required: helpers.withMessage('Please select a valid start time', required) },
                endTime: { required: helpers.withMessage('Please select a valid end time', required), endTimeGreaterThanStartTime: endTimeGreaterThanStartTimeValidatorWithMessage },
                selectedFormat: { required: helpers.withMessage('Please select a valid course format', required) },
                venue: { required: helpers.withMessage('Please provide a valid venue', required) },
                courseSize: { required: helpers.withMessage('Please provide a valid course size', required), numeric: helpers.withMessage('Please provide a valid numeric value', numeric) },
                minimumSlots: { required: helpers.withMessage('Please provide a valid minimum slots', required), numeric: helpers.withMessage('Please provide a valid numeric value', numeric), minSlotsSmallerThanCourseSize: minSlotsSmallerThanCourseSizeValidatorWithMessage },
                openingDate: { required: helpers.withMessage('Please select a valid opening date for registration', required), dateFromToday: dateFromTodayValidatorWithMessage },
                openingTime: { required: helpers.withMessage('Please select a valid opening time for registration', required) },
                closingDate: { required: helpers.withMessage('Please select a valid closing date for registration', required), closingDateGreaterThanOpeningDate: closingDateGreaterThanOpeningDateValidatorWithMessage },
                closingTime: { required: helpers.withMessage('Please select a valid closing time for registration', required) },
                courseFee: { required: helpers.withMessage('Please provide a valid course fee', required), currency: currencyValidatorWithMessage },
                selectedTemplate: { requiredL: helpers.withMessage('Please select a valid feedback template', required) }
            }
        }
    },
    async mounted() {
        try {
            await this.fetchFormFieldsData();

            if (!this.create) {
                await this.fetchEditRunCourseData();
            }
        } catch (error) {
            const errorMsgParts = error.toString().split(":")
            this.message = errorMsgParts[1];
            this.buttonType = "danger"
            this.showAlert = !this.showAlert;
        }
    },
    methods: {
        handleModalClosed(value) {
            this.showAlert = value;
        },
        async fetchInstructors() {
            try {
                this.formData.instructors = await UserService.getAllInstructors();
            } catch (error) {
                console.error('Error fetching instructors:', error);

                this.errorMsg.push('Error fetching instructors:', error);
            }
        },
        async fetchFeedbackTemplates() {
            try {
                this.formData.feedbackTemplates = await FeedbackTemplateService.getAllTemplates();
            } catch (error) {
                console.error('Error fetching feedback templates:', error);

                this.errorMsg.push('Error fetching feedback templates:', error);
            }
        },
        async fetchFormFieldsData() {
            await this.fetchInstructors();
            await this.fetchFeedbackTemplates();

            if (this.errorMsg.length > 0) {
                this.title = "Form Data Retrieval Error";
                throw new Error("There is a problem retrieving the data for the form fields")
            }
        },
        async fetchRunCourseByID() {
            try {
                const runcourseData = await RunCourseService.getRunCourseById(this.runcourseId);

                this.instructorID = runcourseData.instructor_ID;

                this.formData.startDate = new Date(runcourseData.run_Startdate);

                this.formData.endDate = new Date(runcourseData.run_Enddate);

                const startTimeParts = runcourseData.run_Starttime.split(":");
                this.formData.startTime = { hours: parseInt(startTimeParts[0]), minutes: parseInt(startTimeParts[1]), seconds: 0 }

                const endTimeParts = runcourseData.run_Endtime.split(":");
                this.formData.endTime = { hours: parseInt(endTimeParts[0]), minutes: parseInt(endTimeParts[1]), seconds: 0 }

                if (runcourseData.course_Format === "face-to-face") {
                    this.formData.selectedFormat = this.formData.courseFormats[0].name;
                } else {
                    this.formData.selectedFormat = this.formData.courseFormats[1].name;
                }

                this.formData.venue = runcourseData.course_Venue;

                this.formData.courseSize = (runcourseData.course_Size).toString();

                this.formData.minimumSlots = (runcourseData.course_Minsize).toString();

                this.formData.openingDate = new Date(runcourseData.reg_Startdate);

                const openingTimeParts = runcourseData.reg_Starttime.split(":");
                this.formData.openingTime = { hours: parseInt(openingTimeParts[0]), minutes: parseInt(openingTimeParts[1]), seconds: 0 }

                this.formData.closingDate = new Date(runcourseData.reg_Enddate);

                const closingTimeParts = runcourseData.reg_Endtime.split(":");
                this.formData.closingTime = { hours: parseInt(closingTimeParts[0]), minutes: parseInt(closingTimeParts[1]), seconds: 0 }

                this.formData.courseFee = (runcourseData.course_Fee).toString();

                this.templateID = runcourseData.template_ID;

            } catch (error) {
                console.error('Error fetching run course by ID:', error);

                throw new Error("An error occurred in fetching run course by ID");
            }
        },
        async fetchInstructorByID() {
            try {
                const instructorData = await UserService.getInstructorById(this.instructorID);

                this.formData.selectedInstructor = instructorData.user_Name;

            } catch (error) {
                console.error('Error fetching instructor by ID:', error);
                this.errorMsg.push('Error fetching instructor by ID:', error);
            }
        },
        async fetchTemplateByID() {
            try {
                const templateData = await FeedbackTemplateService.getTemplateById(this.templateID);

                this.formData.selectedTemplate = templateData.template_Name;

            } catch (error) {
                console.error('Error fetching template by ID:', error);
                this.errorMsg.push('Error fetching template by ID:', error);
            }
        },
        async fetchEditRunCourseData() {
            try {
                await this.fetchRunCourseByID();

                //need instructor id from runcourse
                await this.fetchInstructorByID();

                //need template id from runcourse 
                await this.fetchTemplateByID();

                if (this.errorMsg.length > 0) {

                    this.title = "Course Data Retrieval Error";

                    throw new Error("There is a problem retrieving the data for this run course");
                }

            } catch (error) {

                this.title = "Course Data Retrieval Error";

                throw new Error("There is a problem retrieving the data for this run course");

            }
        },
        async createRunCourse() {
            try {
                this.createRunCourseResponse = await RunCourseService.createRunCourse(this.submitFormData);

            } catch (error) {
                console.error('Error creating a new run course:', error);

                this.title = "Run Course Creation Failed";

                throw new Error("Run Course Creation was unsuccessful");

            }
        },
        async updateRunCourse() {
            try {
                this.updateRunCourseResponse = await RunCourseService.editRunCourse(this.runcourseId, this.submitFormData);

            } catch (error) {
                console.error('Error updating the run course:', error);

                this.title = "Run Course Update Failed";

                throw new Error("Run Course Update was unsuccessful");

            }
        },
        goToAdminViewRunCourse() {
            this.$router.push("/adminViewRunCourse");
        },
        async onReset() {
            this.v$.$reset();

            this.formData = {
                selectedInstructor: "",
                instructors: [],
                datePickerFormat: "dd/MM/yyyy",
                startDate: null,
                endDate: null,
                startTime: null,
                endTime: null,
                selectedFormat: "",
                courseFormats: [
                    { id: 1, name: "Online" },
                    { id: 2, name: "Face-to-Face" },
                ],
                venue: "",
                courseSize: "",
                minimumSlots: "",
                openingDate: null,
                openingTime: null,
                closingDate: null,
                closingTime: null,
                courseFee: "",
                selectedTemplate: "",
                feedbackTemplates: [],
            },
                //Initializing values for success message
                this.showAlert = false,
                this.message = "",
                this.errorMsg = []

            try {
                await this.fetchFormFieldsData();

            } catch (error) {
                const errorMsgParts = error.toString().split(":")
                this.message = errorMsgParts[1];
                this.showAlert = !this.showAlert;
            }

        },
        //Converting Object to String (For Date variable)
        formatDateToYYYYMMDD(dateObj) {
            const parsedYear = dateObj.getUTCFullYear();
            const parsedMonth = String(dateObj.getUTCMonth() + 1).padStart(2, "0");
            const parsedDay = String(dateObj.getUTCDate()).padStart(2, "0");
            return `${parsedYear}-${parsedMonth}-${parsedDay}`;
        },
        //Converting Object to String (For Time variable)
        formatTimeObjectToString(timeObject) {
            const hours = String(timeObject.hours).padStart(2, '0');
            const minutes = String(timeObject.minutes).padStart(2, '0');
            const seconds = String(timeObject.seconds).padStart(2, '0');
            return `${hours}:${minutes}:${seconds}`;
        },
        async onSubmit() {
            this.v$.$touch();

            if (!this.v$.$invalid) {
                // Form is valid, submit or perform further actions
                console.log('Form has no validation errors');

                try {

                    this.submitFormData["run_Startdate"] = this.formatDateToYYYYMMDD(this.formData.startDate);

                    this.submitFormData["run_Enddate"] = this.formatDateToYYYYMMDD(this.formData.endDate);

                    this.submitFormData["run_Starttime"] = this.formatTimeObjectToString(this.formData.startTime);

                    this.submitFormData["run_Endtime"] = this.formatTimeObjectToString(this.formData.endTime);

                    this.submitFormData["instructor_ID"] = this.formData.instructors.find(i => i.user_Name === this.formData.selectedInstructor).user_ID;

                    if (this.formData.selectedFormat === "Online") {
                        this.submitFormData["course_Format"] = "online"
                    } else {
                        this.submitFormData["course_Format"] = "face-to-face"
                    }

                    this.submitFormData["course_Venue"] = this.formData.venue;

                    const today = new Date();

                    today.setHours(0, 0, 0, 0); // Set today's time to midnight

                    const todayDay = today.getDate();
                    const todayMonth = today.getMonth() + 1;
                    const todayYear = today.getFullYear();

                    const openingDay = this.formData.openingDate.getDate();
                    const openingMonth = this.formData.openingDate.getMonth() + 1;
                    const openingYear = this.formData.openingDate.getFullYear();

                    const closingDay = this.formData.closingDate.getDate();
                    const closingMonth = this.formData.closingDate.getMonth() + 1;
                    const closingYear = this.formData.closingDate.getFullYear();

                    if (todayYear >= openingYear && todayYear <= closingYear &&
                        todayMonth >= openingMonth && todayMonth <= closingMonth &&
                        todayDay >= openingDay && todayDay <= closingDay) {

                        //console.log("Today's date is in between the range");

                        this.submitFormData["runcourse_Status"] = "Ongoing";
                    } else {
                        this.submitFormData["runcourse_Status"] = "Closed";
                    }

                    this.submitFormData["course_Size"] = parseInt(this.formData.courseSize);

                    this.submitFormData["course_Minsize"] = parseInt(this.formData.minimumSlots);

                    this.submitFormData["course_Fee"] = this.formData.courseFee;

                    this.submitFormData["class_Duration"] = (parseInt(this.formData.endTime.hours) + parseInt(this.formData.endTime.minutes) / 60 + parseInt(this.formData.endTime.seconds) / 3600) - (parseInt(this.formData.startTime.hours) + parseInt(this.formData.startTime.minutes) / 60 + parseInt(this.formData.startTime.seconds) / 3600);

                    this.submitFormData["reg_Startdate"] = this.formatDateToYYYYMMDD(this.formData.openingDate);

                    this.submitFormData["reg_Enddate"] = this.formatDateToYYYYMMDD(this.formData.closingDate);

                    this.submitFormData["reg_Starttime"] = this.formatTimeObjectToString(this.formData.openingTime);

                    this.submitFormData["reg_Endtime"] = this.formatTimeObjectToString(this.formData.closingTime);

                    this.submitFormData["template_ID"] = this.formData.feedbackTemplates.find(i => i.template_Name === this.formData.selectedTemplate).template_ID;

                    this.submitFormData["course_ID"] = this.courseID;

                    this.submitFormData["course_Status"] = "Active";


                    //For Edit Course (Updating the run course and course)
                    if (!this.create) {

                        //Update the run course 
                        await this.updateRunCourse();

                        this.title = "Run Course Update Success"
                        this.message = "Run Course Update was successful"
                        this.buttonType = "success"
                        this.showAlert = !this.showAlert;

                        //console.log('Form has submitted successfully')

                    } else {

                        await this.createRunCourse();

                        this.title = "Run Course Creation Success"
                        this.message = "Run Course Creation was successful"
                        this.buttonType = "success"
                        this.showAlert = !this.showAlert;

                        //create the run course

                    }

                } catch (error) {
                    //console.error(error)
                    this.title = "Run Course Update Failed"
                    const errorMsgParts = error.toString().split(":")
                    this.message = errorMsgParts[1];
                    this.buttonType = "danger"
                    this.showAlert = !this.showAlert;
                }

            } else {
                // Form has validation errors
                console.log('Form has validation errors');
            }
        }
    }
};
</script>
  
<style lang="scss">
//For the datepicker and timepicker fields 
.dp-custom-input {
    /* Set border color to transparent by default */
    border-color: transparent;
    font-size: 18px;

    &:hover {
        border-color: transparent;
    }

    &::placeholder {
        /* Change the placeholder color here */
        color: black;
    }
}
</style>
  