<template>
    <div id="runcourseform">
        <div class="container mt-5">
            <h2 v-if="create" class="text-center">Create Run Course</h2>

            <h2 v-else class="text-center">Edit Run Course</h2>

            <form @submit.prevent="onSubmit" @reset="onReset">
                <!--Run Course Name-->
                <div class="form-group mt-5 mb-4">
                    <input v-model="formData.runName" type="text" placeholder="Run Course Name" required autofocus readonly
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.runName?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.runName?.$error }" />
                    <div v-if="v$?.formData.runName?.$error" class="text-danger">
                        <span v-for="error in v$?.formData.runName?.$errors" :key="error.$uid">{{ error.$message }}</span>
                    </div>
                </div>

                <div class="row mb-4">
                    <!--Opening Date For Registration-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.openingDate" placeholder="Registration Opening Date"
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
                        <VueDatePicker v-model="formData.openingTime" placeholder="Registration Start Time"
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
                        <VueDatePicker v-model="formData.closingDate" placeholder="Registration Closing Date"
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
                        <VueDatePicker v-model="formData.closingTime" placeholder="Registration Closing Time"
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
                    <!--Course Start Date-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.startDate" placeholder="Course Start Date" :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.startDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.startDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.startDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.startDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                     <!--Start Time-->
                     <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.startTime" placeholder="Course Start Time" time-picker required
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.startTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.startTime?.$error }"
                            input-class-name="dp-custom-input"><template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
                        </VueDatePicker>
                        <div v-if="v$?.formData.startTime?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.startTime?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>

                <div class="row mb-4">
                    <!--End Date-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.endDate" placeholder="Course End Date" :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.endDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.endDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.endDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.endDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--End Time-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.endTime" placeholder="Course End Time" time-picker required
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

                <!--Instructor Name-->
                <div class="row mb-4">
                    <dropdown-field v-model="formData.selectedInstructor" :default-placeholder="'Instructor'"
                        :errors="v$?.formData.selectedInstructor?.$errors[0]?.$message">
                        <option v-for="instructor in formData.instructors" :key="instructor.user_ID"
                            :value="instructor.user_Name">
                            {{ instructor.user_Name }}
                        </option>
                    </dropdown-field>
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
                        <input v-model="formData.courseSize" @input="restrictToNumbers('courseSize')" type="text" placeholder="Course Size" required autofocus
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.courseSize?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.courseSize?.$error }" />
                        <div v-if="v$?.formData.courseSize?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.courseSize?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--Minimum Slots-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <input v-model="formData.minimumSlots" @input="restrictToNumbers('minimumSlots')" type="text" placeholder="Minimum Slots" required autofocus
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.minimumSlots?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.minimumSlots?.$error }" />
                        <div v-if="v$?.formData.minimumSlots?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.minimumSlots?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>
               
                <div class="row mb-4">
                    <!--Course Fee-->
                    <div class="col-md-6 form-group">
                        <input v-model="formData.courseFee" @input="validateMoneyInput" type="text" placeholder="Course Fee" required autofocus
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

                <div class="row mb-4">
                    <!--Feedback Start Date-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.feedbackStartDate" placeholder="Feedback Start Date" :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.feedbackStartDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.feedbackStartDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.feedbackStartDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.feedbackStartDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--Feedback Start Time-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.feedbackStartTime" placeholder="Feedback Start Time" time-picker required
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.feedbackStartTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.feedbackStartTime?.$error }"
                            input-class-name="dp-custom-input"><template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
                        </VueDatePicker>
                        <div v-if="v$?.formData.feedbackStartTime?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.feedbackStartTime?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>

                <div class="row mb-4">
                    <!--Feedback End Date-->
                    <div class="col-md-6 form-group">
                        <VueDatePicker v-model="formData.feedbackEndDate" placeholder="Feedback End Date" :enable-time-picker="false"
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.feedbackEndDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.feedbackEndDate?.$error }"
                            input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
                        </VueDatePicker>
                        <div v-if="v$?.formData.feedbackEndDate?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.feedbackEndDate?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                    <!--Feedback End Time-->
                    <div class="col-md-6 form-group mt-4 mt-md-0">
                        <VueDatePicker v-model="formData.feedbackEndTime" placeholder="Feedback End Time" time-picker required
                            :class="{ 'form-control': true, 'border-0': !v$?.formData.feedbackEndTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.feedbackEndTime?.$error }"
                            input-class-name="dp-custom-input"><template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
                        </VueDatePicker>
                        <div v-if="v$?.formData.feedbackEndTime?.$error" class="text-danger">
                            <span v-for="error in v$?.formData.feedbackEndTime?.$errors" :key="error.$uid">{{ error.$message
                            }}</span>
                        </div>
                    </div>
                </div>

                <div v-if="create" class="row">
                    <div class="col-md-6 form-group">
                        <button type="reset" class="btn btn-secondary shadow-sm w-100 mt-5 field cancelbtn">
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
                        <button type="button" @click="goToAdminViewRunCourse"
                            class="btn btn-secondary shadow-sm w-100 mt-5 field cancelbtn">
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
        <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
    </div>
</template>
  
<script>
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
    'Please select a course start date after the selected registration closing date',
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
    'Please select a course end date that falls on or after the selected course start date',
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
    'Please select a registration opening date from today onwards.',
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
    'Please select a registration closing date after the selected registration opening date',
    closingDateGreaterThanOpeningDateValidator
)

//Function: Check whether Feedback Start Date is greater than the Course End Date 
const validateFeedbackStartDateGreaterThanEndDate = function (value) {

    if (value === null || this.formData.endDate === null) {
        return true;
    }

    if (value.getFullYear() > this.formData.endDate.getFullYear() || (value.getFullYear() === this.formData.endDate.getFullYear() && (value.getMonth() + 1) > (this.formData.endDate.getMonth() + 1)) || (value.getFullYear() === this.formData.endDate.getFullYear() && (value.getMonth() + 1) === (this.formData.endDate.getMonth() + 1) && value.getDate() > this.formData.endDate.getDate())) {
        return true;
    }

    return false;
};

const feedbackStartDateGreaterThanEndDateValidator = helpers.withParams(
    { type: 'feedbackStartDateGreaterThanEndDate' },
    validateFeedbackStartDateGreaterThanEndDate
);

const feedbackStartDateGreaterThanEndDateValidatorWithMessage = helpers.withMessage(
    'Please select a feedback start date after the selected course end date',
    feedbackStartDateGreaterThanEndDateValidator
)

//Function: Check whether Feedback End Date is equal to or greater than the Feedback Start Date 
const validateFeedbackEndDateFromFeedbackStartDate = function (value) {
    if (value === null || this.formData.feedbackStartDate === null) {
        return true;
    }

    if (value.getFullYear() > this.formData.feedbackStartDate.getFullYear() || (value.getFullYear() === this.formData.feedbackStartDate.getFullYear() && (value.getMonth() + 1) > (this.formData.feedbackStartDate.getMonth() + 1)) ||
        (value.getFullYear() === this.formData.feedbackStartDate.getFullYear() && value.getMonth() === this.formData.feedbackStartDate.getMonth() && value.getDate() >= this.formData.feedbackStartDate.getDate())) {
        return true;
    }

    return false;
};

const feedbackEndDateFromFeedbackStartDateValidator = helpers.withParams(
    { type: 'feedbackEndDateFromFeedbackStartDate' },
    validateFeedbackEndDateFromFeedbackStartDate
);

const feedbackEndDateFromFeedbackStartDateValidatorWithMessage = helpers.withMessage(
    'Please select a feedback end date that falls on or after the selected feedback start date',
    feedbackEndDateFromFeedbackStartDateValidator
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
    'Please select a course end time later than the selected course start time',
    endTimeGreaterThanStartTimeValidator
)

//Function: Check whether Feedback End Time is greater than Feedback Start Time when Feedback Start Date and Feedback End Date are the same 
const validateFeedbackEndTimeGreaterThanFeeedbackStartTime = function (value) {
    const allValuesFilled = (
        value !== null &&
        this.formData.feedbackStartTime !== null &&
        this.formData.feedbackStartDate !== null &&
        this.formData.feedbackEndDate !== null
    );

    if (allValuesFilled) {
        if (this.formData.feedbackStartDate.toISOString().split('T')[0] === this.formData.feedbackEndDate.toISOString().split('T')[0]) {

            // Convert time values to seconds
            const startTimeInSeconds = parseInt(this.formData.feedbackStartTime.hours) * 3600 + parseInt(this.formData.feedbackStartTime.minutes) * 60 + parseInt(this.formData.feedbackStartTime.seconds);
            const endTimeInSeconds = parseInt(value.hours) * 3600 + parseInt(value.minutes) * 60 + parseInt(value.seconds);

            // Compare time values in seconds
            return startTimeInSeconds < endTimeInSeconds;

        }
    }

    // Skip validation if any value is missing or start date doesn't equal end date
    return true;
};

const feedbackEndTimeGreaterThanFeedbackStartTimeValidator = helpers.withParams(
    { type: 'feedbackEndTimeGreaterThanFeedbackStartTime' },
    validateFeedbackEndTimeGreaterThanFeeedbackStartTime
);

const feedbackEndTimeGreaterThanFeedbackStartTimeValidatorWithMessage = helpers.withMessage(
    'Please select a feedback end time later than the selected feedback start time',
    feedbackEndTimeGreaterThanFeedbackStartTimeValidator
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
        },
        courseId: {
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
                runName: "",
                datePickerFormat: "dd/MM/yyyy",
                openingDate: null,
                openingTime: null,
                closingDate: null,
                closingTime: null,
                startDate: null,
                endDate: null,
                startTime: null,
                endTime: null,
                instructors: [],
                selectedInstructor: "",
                courseFormats: [],
                selectedFormat: "",
                venue: "",
                courseSize: "",
                minimumSlots: "",
                courseFee: "",
                feedbackTemplates: [],
                selectedTemplate: "",
                feedbackStartDate: null,
                feedbackStartTime: null, 
                feedbackEndDate: null, 
                feedbackEndTime: null
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
            courseID: 0,
            createRunCourseResponse: {},
            editRunCourseResponse: {},
            submitFormData: {}
        };
    },
    components: {
        VueDatePicker,
        DropdownField,
        DefaultModal
    },
    validations() {
        return {
            formData: {
                openingDate: { required: helpers.withMessage('Please select a valid registration opening date', required), dateFromToday: dateFromTodayValidatorWithMessage },
                openingTime: { required: helpers.withMessage('Please select a valid registration opening time', required) },
                closingDate: { required: helpers.withMessage('Please select a valid registration closing date', required), closingDateGreaterThanOpeningDate: closingDateGreaterThanOpeningDateValidatorWithMessage },
                closingTime: { required: helpers.withMessage('Please select a valid registration closing time', required) },
                startDate: { required: helpers.withMessage('Please select a valid course start date', required), startDateGreaterThanClosingDate: startDateGreaterThanClosingDateValidatorWithMessage },
                startTime: { required: helpers.withMessage('Please select a valid course start time', required) },
                endDate: { required: helpers.withMessage('Please select a valid course end date', required), endDateFromStartDate: endDateFromStartDateValidatorWithMessage },
                endTime: { required: helpers.withMessage('Please select a valid course end time', required), endTimeGreaterThanStartTime: endTimeGreaterThanStartTimeValidatorWithMessage },
                selectedInstructor: { required: helpers.withMessage('Please select a valid instructor', required) },
                selectedFormat: { required: helpers.withMessage('Please select a valid course format', required) },
                venue: { required: helpers.withMessage('Please provide a valid venue', required) },
                courseSize: { required: helpers.withMessage('Please provide a valid course size', required), numeric: helpers.withMessage('Please provide a valid numeric value', numeric) },
                minimumSlots: { required: helpers.withMessage('Please provide a valid minimum slots', required), numeric: helpers.withMessage('Please provide a valid numeric value', numeric), minSlotsSmallerThanCourseSize: minSlotsSmallerThanCourseSizeValidatorWithMessage },
                courseFee: { required: helpers.withMessage('Please provide a valid course fee', required), currency: currencyValidatorWithMessage },
                selectedTemplate: { required: helpers.withMessage('Please select a valid feedback template', required) },
                feedbackStartDate: { required: helpers.withMessage('Please select a valid feedback start date', required), feedbackStartDateGreaterThanEndDate: feedbackStartDateGreaterThanEndDateValidatorWithMessage },
                feedbackStartTime: { required: helpers.withMessage('Please select a valid feedback start time', required) },
                feedbackEndDate: { required: helpers.withMessage('Please select a valid feedback end date', required), feedbackEndDateFromFeedbackStartDate: feedbackEndDateFromFeedbackStartDateValidatorWithMessage },
                feedbackEndTime: { required: helpers.withMessage('Please select a valid feedback end time', required), feedbackEndTimeGreaterThanFeedbackStartTime: feedbackEndTimeGreaterThanFeedbackStartTimeValidatorWithMessage }
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
        restrictToNumbers(fieldName) {
            // Allow only numeric input
            this.formData[fieldName] = this.formData[fieldName].replace(/[^0-9]/g, '');
        },
        validateMoneyInput() {
            // Regular expression to allow numeric values with optional decimal points
            const regex = /^\d+(\.\d{1,2})?$/;
            if (!regex.test(this.formData.courseFee)) {
                // If input does not match the pattern, set the value to a valid money format
                this.formData.courseFee = this.formData.courseFee.replace(/[^\d.]/g, '');
            }
        },
        handleModalClosed(value) {
            this.showAlert = value;

            if (!this.showAlert && this.buttonType === "success") {
                this.$router.push('/adminViewRunCourse');
            }
        },
        async fetchCoaches() {
            try {
                this.formData.instructors = await UserService.getAllCoaches();

            } catch (error) {
                console.error('Error fetching instructors:', error);
                this.errorMsg.push('Error fetching instructors or trainers');
            }
        },
        async fetchCourseFormats() {
            try {
                let apiResponse = await RunCourseService.getCourseFormats();
                
                // Process the strings and extract the values between single quotes

                // Variable to keep track of the ID
                let idCounter = 0; 

                apiResponse.forEach(str => {
                    // Extract the value between the single quotes
                    let extractedValue = str.match(/'(.*?)'/)[1];
                    // Convert the value to the desired format (capitalize first letter)
                    let formattedValue = extractedValue.charAt(0).toUpperCase() + extractedValue.slice(1).toLowerCase();
                    // Create an object with id and name properties
                    let formatObject = {
                        // Assign the current idCounter value
                        id: idCounter, 
                        name: formattedValue
                    };
                    // Increment the idCounter for the next element
                    idCounter++;
                    // Store the formatted object in the courseFormats array
                    this.formData.courseFormats.push(formatObject);
                });
            } catch (error) {
                console.error('Error fetching course formats:', error);
                this.errorMsg.push('Error fetching course formats');
            }
        },
        async fetchFeedbackTemplates() {
            try {
                const feedback_template_response = await FeedbackTemplateService.getAllTemplates();
        
                if (feedback_template_response.code == 200) {
                    this.formData.feedbackTemplates =  feedback_template_response.templates
                } else {
                    this.errorMsg.push('Error fetching feedback templ ates');
                }
            } catch (error) {
                console.error('Error fetching feedback templates:', error);
                this.errorMsg.push('Error fetching feedback templates');
            }
        },
        async fetchRunCourseByCourseID() {
            try {
                const response = await RunCourseService.getRunCourseCountByCourseId(this.courseId);

                console.log(response.data.run_course_count)
                
                this.formData.runName = response.data.course_name + " - Run " + (parseInt(response.data.run_course_count) + 1);

                //console.log(response.data);
            } catch (error) {
                console.error('Error fetching run course name:', error);
                this.errorMsg.push('Error fetching run course name');
            }
        },
        async fetchFormFieldsData() {
            await this.fetchCoaches();
            await this.fetchCourseFormats();
            await this.fetchFeedbackTemplates();
            
            if(this.create) {
                await this.fetchRunCourseByCourseID();
            }

            if (this.errorMsg.length > 0) {
                this.title = "Form Data Retrieval Error";
                throw new Error("There is a problem retrieving the data for the form fields")
            }
        },
        async fetchRunCourseByRunCourseID() {
            try {
                const runcourseData = await RunCourseService.getRunCourseById(this.runcourseId);

                //NEED TO CHANGE
                this.formData.runName = runcourseData.run_Name;

                this.formData.openingDate = new Date(runcourseData.reg_Startdate);

                const openingTimeParts = runcourseData.reg_Starttime.split(":");
                this.formData.openingTime = { hours: parseInt(openingTimeParts[0]), minutes: parseInt(openingTimeParts[1]), seconds: 0 }

                this.formData.closingDate = new Date(runcourseData.reg_Enddate);

                const closingTimeParts = runcourseData.reg_Endtime.split(":");
                this.formData.closingTime = { hours: parseInt(closingTimeParts[0]), minutes: parseInt(closingTimeParts[1]), seconds: 0 }

                this.formData.startDate = new Date(runcourseData.run_Startdate);

                const startTimeParts = runcourseData.run_Starttime.split(":");
                this.formData.startTime = { hours: parseInt(startTimeParts[0]), minutes: parseInt(startTimeParts[1]), seconds: 0 }

                this.formData.endDate = new Date(runcourseData.run_Enddate);

                const endTimeParts = runcourseData.run_Endtime.split(":");
                this.formData.endTime = { hours: parseInt(endTimeParts[0]), minutes: parseInt(endTimeParts[1]), seconds: 0 }

                this.instructorID = runcourseData.instructor_ID;

                if (runcourseData.course_Format === "face-to-face") {
                    this.formData.selectedFormat = this.formData.courseFormats[0].name;
                } else {
                    this.formData.selectedFormat = this.formData.courseFormats[1].name;
                }

                this.formData.venue = runcourseData.course_Venue;

                this.formData.courseSize = (runcourseData.course_Size).toString();

                this.formData.minimumSlots = (runcourseData.course_Minsize).toString();

                this.formData.courseFee = (runcourseData.course_Fee).toString();

                this.templateID = runcourseData.template_ID;

                this.formData.feedbackStartDate = new Date(runcourseData.feedback_Startdate);

                const feedbackStartTimeParts = runcourseData.feedback_Starttime.split(":");
                this.formData.feedbackStartTime = { hours: parseInt(feedbackStartTimeParts[0]), minutes: parseInt(feedbackStartTimeParts[1]), seconds: 0 }

                this.formData.feedbackEndDate = new Date(runcourseData.feedback_Enddate);

                const feedbackEndTimeParts = runcourseData.feedback_Endtime.split(":");
                this.formData.feedbackEndTime = { hours: parseInt(feedbackEndTimeParts[0]), minutes: parseInt(feedbackEndTimeParts[1]), seconds: 0 }
              
                this.courseID = runcourseData.course_ID;

            } catch (error) {
                console.error('Error fetching run course by ID:', error);
                throw new Error("An error occurred in fetching run course by ID");
            }
        },
        async fetchCoachByID() {
            try {
                const coachData = await UserService.getCoachById(this.instructorID);
                this.formData.selectedInstructor = coachData.user_Name; 

            } catch (error) {
                console.error('Error fetching coach by ID:', error);
                this.errorMsg.push('Error fetching instructor or trainer by ID');
            }
        },
        async fetchTemplateByID() {
            try {
                let response = await FeedbackTemplateService.getTemplateById(this.templateID);
            
                if(response.code == 200) {
                    const templateData = response.data.template;
                    this.formData.selectedTemplate = templateData.feedback_template_name;
                }
            } catch (error) {
                console.error('Error fetching template by ID:', error);
                this.errorMsg.push('Error fetching template by ID');
            }
        },
        async fetchEditRunCourseData() {
            try {
                await this.fetchRunCourseByRunCourseID();

                //need instructor id from runcourse
                await this.fetchCoachByID();

                //need template id from runcourse 
                await this.fetchTemplateByID();

                if (this.errorMsg.length > 0) {
                    throw new Error("There is a problem retrieving the data for this run course");
                }

            } catch (error) {
                this.title = "Run Course Data Retrieval Error";
                throw new Error("There is a problem retrieving the data for this run course");
            }
        },
        async createRunCourse() {
            try {
                console.log(this.courseId)
                this.createRunCourseResponse = await RunCourseService.createRunCourse(this.courseId, this.submitFormData);
               
            } catch (error) {
                console.error('Error creating a new run course:', error);
                this.title = "Run Course Creation Failed";

                if(error.response.status === 500) {
                    throw new Error("Run Course Creation was unsuccessful")
                } else {
                    throw new Error(error.response.data.message);
                }
            }
        },
        async updateRunCourse() {
            try {
                this.updateRunCourseResponse = await RunCourseService.editRunCourse(this.runcourseId, this.submitFormData);

            } catch (error) {
                console.error('Error updating the run course:', error);

                this.title = "Run Course Update Failed";

                //throw new Error("Run Course Update was unsuccessful");
                throw new Error(error.response.data.message)

            }
        },
        goToAdminViewRunCourse() {
            this.$router.push("/adminViewRunCourse");
        },
        async onReset() {
            this.v$.$reset();

            this.formData = {
                runName: "",
                datePickerFormat: "dd/MM/yyyy",
                openingDate: null,
                openingTime: null,
                closingDate: null,
                closingTime: null,
                startDate: null,
                startTime: null,
                endDate: null,
                endTime: null,
                instructors: [],
                selectedInstructor: "",
                courseFormats: [],
                selectedFormat: "",
                venue: "",
                courseSize: "",
                minimumSlots: "",
                courseFee: "",
                feedbackTemplates: [],
                selectedTemplate: "",
                feedbackStartDate: null,
                feedbackStartTime: null, 
                feedbackEndDate: null, 
                feedbackEndTime: null
            }

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
            const parsedYear = dateObj.getFullYear();
            const parsedMonth = dateObj.getMonth() + 1;
            const parsedDay = dateObj.getDate();
            return `${parsedYear}-${parsedMonth}-${parsedDay}`;
        },
        //Converting Object to String (For Time variable)
        formatTimeObjectToString(timeObject) {
            const hours = String(timeObject.hours).padStart(2, '0');
            const minutes = String(timeObject.minutes).padStart(2, '0');
            const seconds = String(timeObject.seconds).padStart(2, '0');
            return `${hours}:${minutes}:${seconds}`;
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
                // Form is valid, submit or perform further actions
                console.log('Form has no validation errors');

                try {

                    //NEED TO CHANGE
                    this.submitFormData["run_Name"] = "test";

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

                    const todayDay = today.getDate();
                    const todayMonth = today.getMonth() + 1;
                    const todayYear = today.getFullYear();

                    const currentHours = today.getHours();
                    const currentMinutes = today.getMinutes();

                    const openingDay = this.formData.openingDate.getDate();
                    const openingMonth = this.formData.openingDate.getMonth() + 1;
                    const openingYear = this.formData.openingDate.getFullYear();

                    const selectedHours = this.formData.openingTime.hours;
                    const selectedMinutes = this.formData.openingTime.minutes;

                    if (todayYear === openingYear && todayMonth === openingMonth && todayDay === openingDay) {
                        if (
                            currentHours > selectedHours ||
                            (currentHours === selectedHours && currentMinutes > selectedMinutes) ||
                            (currentHours === selectedHours && currentMinutes === selectedMinutes)
                        )   {
                                // Today's date is within the range, and the selected time is before the current time.
                                this.submitFormData["runcourse_Status"] = "Ongoing";
                            } else {
                            // Today's date is within the range, but the selected time is after the current time.
                            this.submitFormData["runcourse_Status"] = "Closed";
                        }
                    } else {
                        // Today's date is outside the range.
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

                    this.submitFormData["feedback_Startdate"] = this.formatDateToYYYYMMDD(this.formData.feedbackStartDate);

                    this.submitFormData["feedback_Enddate"] = this.formatDateToYYYYMMDD(this.formData.feedbackEndDate);

                    this.submitFormData["feedback_Starttime"] = this.formatTimeObjectToString(this.formData.feedbackStartTime);

                    this.submitFormData["feedback_Endtime"] = this.formatTimeObjectToString(this.formData.feedbackEndTime);

                    this.submitFormData["template_ID"] = this.formData.feedbackTemplates.find(i => i.template_Name === this.formData.selectedTemplate).template_ID;

                    //For Edit Course (Updating the run course and course)  
                    if (!this.create) {

                        this.submitFormData["course_ID"] = this.courseID;

                        //Update the run course 
                        await this.updateRunCourse();

                        this.setSuccessAlert("Run Course Update")

                    } else {

                        this.submitFormData["course_ID"] = this.courseId;

                        await this.createRunCourse();

                        this.setSuccessAlert("Run Course Creation")
                    }

                } catch (error) {
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