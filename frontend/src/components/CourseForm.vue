<template>
  <div id="courseform">
    <div class="container-fluid mt-5">
      <h2 v-if="status" class="text-center">Create Course For Registration</h2>

      <h2 v-else class="text-center">Edit Course</h2>

      <form @submit.prevent="onSubmit" @reset="onReset">
        <!--Course Name-->
        <div class="form-group mt-5 mb-4">
          <input v-model="formData.courseName" type="text" placeholder="Course Name" required autofocus
            :class="{ 'form-control': true, 'border-0': !v$?.formData.courseName?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.courseName?.$error }" />
          <div v-if="v$?.formData.courseName?.$error" class="text-danger">
            <span v-for="error in v$?.formData.courseName?.$errors" :key="error.$uid">{{ error.$message }}</span>
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
            <span v-for="error in v$?.formData.courseDescription?.$errors" :key="error.$uid">{{ error.$message }}</span>
          </div>
          <div class="text-muted mt-2">Character Count: {{ courseDescLength }}/800</div>
        </div>
        <!--Instructor Name-->
        <div class="form-group mb-4">
          <dropdown-field v-model="formData.selectedInstructor" :default-placeholder="'Instructor'"
            :errors="v$?.formData.selectedInstructor?.$errors[0]?.$message">
            <option v-for="instructor in formData.instructors" :key="instructor.user_ID" :value="instructor.user_Name">
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
              <span v-for="error in v$?.formData.startDate?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
          <!--End Date-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="formData.endDate" placeholder="End Date" :enable-time-picker="false"
              :class="{ 'form-control': true, 'border-0': !v$?.formData.endDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.endDate?.$error }"
              input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required>
            </VueDatePicker>
            <div v-if="v$?.formData.endDate?.$error" class="text-danger">
              <span v-for="error in v$?.formData.endDate?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
        </div>
        <div class="row mb-4">
          <!--Start Time-->
          <div class="col-md-6 form-group">
            <VueDatePicker v-model="formData.startTime" placeholder="Start Time" time-picker required
              :class="{ 'form-control': true, 'border-0': !v$?.formData.startTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.startTime?.$error }"
              input-class-name="dp-custom-input"><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template></VueDatePicker>
            <div v-if="v$?.formData.startTime?.$error" class="text-danger">
              <span v-for="error in v$?.formData.startTime?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
          <!--End Time-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="formData.endTime" placeholder="End Time" time-picker required
              :class="{ 'form-control': true, 'border-0': !v$?.formData.endTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.endTime?.$error }"
              input-class-name="dp-custom-input"><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template></VueDatePicker>
            <div v-if="v$?.formData.endTime?.$error" class="text-danger">
              <span v-for="error in v$?.formData.endTime?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
        </div>
        <div class="row mb-4">
          <!--Course Format-->
          <div class="col-md-6 form-group">
            <dropdown-field v-model="formData.selectedFormat" :default-placeholder="'Course Format'"
              :errors="v$?.formData.selectedFormat?.$errors[0]?.$message">
              <option v-for="courseFormat in formData.courseFormats" :key="courseFormat.id" :value="courseFormat.name">
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
              <span v-for="error in v$?.formData.courseSize?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
          <!--Minimum Slots-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <input v-model="formData.minimumSlots" type="text" placeholder="Minimum Slots" required autofocus
              :class="{ 'form-control': true, 'border-0': !v$?.formData.minimumSlots?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.minimumSlots?.$error }" />
            <div v-if="v$?.formData.minimumSlots?.$error" class="text-danger">
              <span v-for="error in v$?.formData.minimumSlots?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
        </div>
        <div class="row mb-4">
          <!--Opening Date For Registration-->
          <div class="col-md-6 form-group">
            <VueDatePicker v-model="formData.openingDate" placeholder="Opening Date For Registration"
              :enable-time-picker="false"
              :class="{ 'form-control': true, 'border-0': !v$?.formData.openingDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.openingDate?.$error }"
              input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required></VueDatePicker>
            <div v-if="v$?.formData.openingDate?.$error" class="text-danger">
              <span v-for="error in v$?.formData.openingDate?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
          <!--Opening Time For Registration-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="formData.openingTime" placeholder="Opening Time For Registration" time-picker required
              :class="{ 'form-control': true, 'border-0': !v$?.formData.openingTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.openingTime?.$error }"
              input-class-name="dp-custom-input"><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template></VueDatePicker>
            <div v-if="v$?.formData.openingTime?.$error" class="text-danger">
              <span v-for="error in v$?.formData.openingTime?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
        </div>
        <div class="row mb-4">
          <!--Closing Date For Registration-->
          <div class="col-md-6 form-group">
            <VueDatePicker v-model="formData.closingDate" placeholder="Closing Date For Registration"
              :enable-time-picker="false"
              :class="{ 'form-control': true, 'border-0': !v$?.formData.closingDate?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.closingDate?.$error }"
              input-class-name="dp-custom-input" :format="this.formData.datePickerFormat" required></VueDatePicker>
            <div v-if="v$?.formData.closingDate?.$error" class="text-danger">
              <span v-for="error in v$?.formData.closingDate?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
          <!--Closing Time For Registration-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="formData.closingTime" placeholder="Closing Time For Registration" time-picker required
              :class="{ 'form-control': true, 'border-0': !v$?.formData.closingTime?.$error, 'shadow-sm': true, 'is-invalid': v$?.formData.closingTime?.$error }"
              input-class-name="dp-custom-input"><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
            </VueDatePicker>
            <div v-if="v$?.formData.closingTime?.$error" class="text-danger">
              <span v-for="error in v$?.formData.closingTime?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
        </div>
        <div class="row">
          <!--Course Fee-->
          <div class="col-md-6 form-group">
            <input v-model="formData.courseFee" type="text" placeholder="Course Fee" required autofocus
              :class="{ 'form-control': true, 'border-0': !v$?.formData.courseFee?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.courseFee?.$error }" />
            <div v-if="v$?.formData.courseFee?.$error" class="text-danger">
              <span v-for="error in v$?.formData.courseFee?.$errors" :key="error.$uid">{{ error.$message }}</span>
            </div>
          </div>
          <!--Feedback Template-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <dropdown-field v-model="formData.selectedTemplate" :default-placeholder="'Feedback Template'"
              :errors="v$?.formData.selectedTemplate?.$errors[0]?.$message">
              <option v-for="feedbackTemplate in formData.feedbackTemplates" :key="feedbackTemplate.template_ID"
                :value="feedbackTemplate.template_Name">
                {{ feedbackTemplate.template_Name }}
              </option>
            </dropdown-field>
          </div>
        </div>

        <button v-if="status" type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
          Submit
        </button>

        <div v-else class="row">
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
        </div>
      </form>
    </div>
    <!-- Success modal -->
    <success-modal :show="showSuccessModal" :message="successMessage" @close="hideSuccessModal" />
  </div>
</template>

<script>
//import InputField from "../components/InputField.vue";
import DropdownField from "../components/DropdownField.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import SuccessModal from "../components/SuccessModal.vue";
import "@vuepic/vue-datepicker/dist/main.css";
import CourseCategoryService from "@/api/services/CourseCategoryService.js";
import UserService from "@/api/services/UserService.js";
import FeedbackTemplateService from "@/api/services/FeedbackTemplateService.js";
import { useVuelidate } from "@vuelidate/core";
import { required, numeric, helpers } from "@vuelidate/validators";
import { axiosClient } from "@/api/axiosClient";
//import ErrorMessage from "../components/ErrorMessage.vue";

//Validating the date fields


//Function: Check whether the entered numeric value is smaller than the courseSize
const validateMinSlotsSmallerThanCourseSize = function (value) {
  const numericRegex = /^[0-9]*$/;

  if (value === null || this.formData.courseSize === null) {
    return true;
  }

  if (!value.match(numericRegex) || !this.formData.courseSize.match(numericRegex)) {
    return true; // Skip validation if either field is not numeric
  }

  return value < this.formData.courseSize;
}

const minSlotsSmallerThanCourseSizeValidator = helpers.withParams(
  { type: 'minSlotsSmallerThanCourseSize' },
  validateMinSlotsSmallerThanCourseSize
);

const minSlotsSmallerThanCourseSizeValidatorWithMessage = helpers.withMessage(
  'Please select a minimum slot smaller than the selected course size',
  minSlotsSmallerThanCourseSizeValidator
)


//Function: Check whether the selected date is greater than the closingDate 
const validateStartDateGreaterThanClosingDate = function (value) {
  if (value === null || this.formData.closingDate === null) {
    return true;
  }

  return value > this.formData.closingDate;
};

const startDateGreaterThanClosingDateValidator = helpers.withParams(
  { type: 'startDateGreaterThanClosingDate' },
  validateStartDateGreaterThanClosingDate
);

const startDateGreaterThanClosingDateValidatorWithMessage = helpers.withMessage(
  'Please select a start date after the selected closing date for registration',
  startDateGreaterThanClosingDateValidator
)

//Function: Check whether the selected date is equal to or greater than the startDate
const validateEndDateFromStartDate = function (value) {
  if (value === null || this.formData.startDate === null) {
    return true;
  }

  return value >= this.formData.startDate;
};

const endDateFromStartDateValidator = helpers.withParams(
  { type: 'endDateFromStartDate' },
  validateEndDateFromStartDate
);

const endDateFromStartDateValidatorWithMessage = helpers.withMessage(
  'Please select an end date that falls on or after the selected start date',
  endDateFromStartDateValidator
)

//Function: Check whether the selected date is equal to or greater than today's date 
// Define the custom validation function
const validateDateFromToday = (value) => {
  if (!value) {
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

//Function: Check whether the selected date is equal to or greater than the openingDate 
const validateClosingDateFromOpeningDate = function (value) {
  if (value === null || this.formData.openingDate === null) {
    return true;
  }

  return value > this.formData.openingDate;
};

const closingDateFromOpeningDateValidator = helpers.withParams(
  { type: 'closingDateFromOpeningDate' },
  validateClosingDateFromOpeningDate
);

const closingDateFromOpeningDateValidatorWithMessage = helpers.withMessage(
  'Please select a closing date for registration that falls on or after the selected opening date for registration',
  closingDateFromOpeningDateValidator
)


//Validating the time fields 

//Function: Check whether the selected time is greater than the startTime
const validateEndTimeGreaterThanStartTime = function (value) {
  const allValuesFilled = (
    value !== null &&
    this.formData.startTime !== null &&
    this.formData.startDate !== null &&
    this.formData.endDate !== null
  );

  if (allValuesFilled) {
    if (new Date(this.formData.startDate).toISOString().split('T')[0] === new Date(this.formData.endDate).toISOString().split('T')[0]) {
      // Convert time values to seconds
      const startTimeInSeconds = this.formData.startTime.hours * 3600 + this.formData.startTime.minutes * 60 + this.formData.startTime.seconds;
      const endTimeInSeconds = value.hours * 3600 + value.minutes * 60 + value.seconds;

      // Compare time values in seconds
      return startTimeInSeconds < endTimeInSeconds;

    }
  }

  return true; // Skip validation if any value is missing or start date doesn't equal end date
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

//Function: Check whether the entered value matches the currency regex pattern
const validateCurrency = (value) => {
  if (!value) {
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
  name: "CourseForm",
  props: {
    status: {
      type: Boolean,
      required: true,
    },
  },
  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },
  data() {
    return {
      formData: {
        courseName: "",
        selectedCategory: "",
        courseCategories: [],
        courseDescription: "",
        selectedInstructor: "",
        instructors: [],
        datePickerFormat: "dd/MM/yyyy",
        startDate: null,
        endDate: null,
        startTime: null,
        endTime: null,
        selectedFormat: "", // Holds the selected course format ID
        courseFormats: [
          { id: 1, name: "Online" },
          { id: 2, name: "Face-to-Face" },
          // Add more course format here
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
        feedbackTemplates: []
      },
      showSuccessModal: false,
      successMessage: "The course has been successfully created and is now available for registration.",
      errorMessage: ""
    };
  },
  components: {
    VueDatePicker,
    //InputField,
    DropdownField,
    SuccessModal
  },
  validations() {
    return {
      formData: {
        courseName: { required: helpers.withMessage('Please provide a valid course Name', required) },
        selectedCategory: { required: helpers.withMessage('Please select a valid course category', required) },
        courseDescription: { required: helpers.withMessage('Please provide a valid course description', required) },
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
        closingDate: { required: helpers.withMessage('Please select a valid closing date for registration', required), closingDateFromOpeningDate: closingDateFromOpeningDateValidatorWithMessage },
        closingTime: { required: helpers.withMessage('Please select a valid closing time for registration', required) },
        courseFee: { required: helpers.withMessage('Please provide a valid course fee', required), currency: currencyValidatorWithMessage },
        selectedTemplate: { requiredL: helpers.withMessage('Please select a valid feedback template', required) }
      }
    }
  },
  async mounted() {
    await this.fetchCourseCategories();
    await this.fetchInstructors();
    await this.fetchFeedbackTemplates();
  },
  methods: {
    async fetchCourseCategories() {
      try {
        this.formData.courseCategories = await CourseCategoryService.getAllCourseCategory(); // Use the CourseCategoryService
      } catch (error) {
        console.error('Error fetching course categories:', error);
      }
    },
    async fetchInstructors() {
      try {
        this.formData.instructors = await UserService.getInstructors(); // Use the UserService
      } catch (error) {
        console.error('Error fetching instructors:', error);
      }
    },
    async fetchFeedbackTemplates() {
      try {
        this.formData.feedbackTemplates = await FeedbackTemplateService.getTemplates(); // Use the UserService
      } catch (error) {
        console.error('Error fetching feedback templates:', error);
      }
    },
    async onReset() {
      this.v$.$reset();
      this.formData = {
        courseName: "",
        selectedCategory: "",
        courseCategories: [],
        courseDescription: "",
        selectedInstructor: "",
        instructors: [],
        datePickerFormat: "dd/MM/yyyy",
        startDate: null,
        endDate: null,
        startTime: null,
        endTime: null,
        selectedFormat: "", // Holds the selected course format ID
        courseFormats: [
          { id: 1, name: "Online" },
          { id: 2, name: "Face-to-Face" },
          // Add more course format here
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
        feedbackTemplates: []
      }

      await this.fetchCourseCategories();
      await this.fetchInstructors();
      await this.fetchFeedbackTemplates();

    },
    async onSubmit() {
      this.v$.$touch();

      if (!this.v$.$invalid) {
        // Form is valid, submit or perform further actions
        console.log('Form submitted successfully');

        //Create the course service
        await axiosClient.post("/course/create_course", {
          courseName : this.formData.courseName,
          selectedCategory : this.formData.selectedCategory,
          courseDescription : this.formData.courseDescription,
          selectedInstructor : this.formData.selectedInstructor,
          startDate : this.formData.startDate,
          endDate : this.formData.endDate,
          startTime : this.formData.startTime,
          endTime : this.formData.endTime,
          selectedFormat : this.formData.selectedFormat, // Holds the selected course format ID
          venue : this.formData.venue,
          courseSize : this.formData.courseSize,
          minimumSlots : this.formData.minimumSlots,
          openingDate : this.formData.openingDate,
          openingTime : this.formData.openingTime,
          closingDate : this.formData.closingDate,
          closingTime : this.formData.closingTime,
          courseFee : this.formData.courseFee,
          selectedTemplate : this.formData.selectedTemplate
        }).then(response => {
            console.log(response.data);
          })
          .catch(error => {
            console.error(error);
          });

        this.showSuccessModal = true;
      } else {
        // Form has validation errors
        console.log('Form has validation errors');        
      }
    },
    hideSuccessModal() {
      this.showSuccessModal = false;
      this.onReset();
    },
  }
};
</script>

<style lang="scss">
.dp-custom-input {
  border-color: transparent;
  /* Set border color to transparent by default */
  font-size: 18px;

  &:hover {
    border-color: transparent;
  }

  &::placeholder {
    /* Change the placeholder color here */
    color: black;
  }
}</style>
