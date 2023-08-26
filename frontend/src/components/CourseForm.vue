<template>
  <div id="courseform">
    <div class="container-fluid mt-5">
      <h2 v-if="status" class="text-center">Create Course For Registration</h2>

      <h2 v-else class="text-center">Edit Course</h2>

      <form ref="courseForm" @submit.prevent="submitForm">
        <!--Course Name-->
        <div class="form-group mt-5 mb-4">
          <!--<input v-model="courseName" type="text" placeholder="Course Name" required autofocus=""
            class="form-control border-0 shadow-sm px-4 field" />-->
          <input-field v-model="course.courseName" type="text" placeholder="Course Name"></input-field>
        </div>
        <!--Course Category-->
        <div class="form-group mb-4">
          <!-- Dropdown Button -->
          <!--<select v-model="selectedCategory" class="form-select border-0 shadow-sm px-4 field text-muted">
            <option disabled hidden value="">Course Category</option>
            <option v-for="courseCat in courseCats" :key="courseCat.coursecat_ID" :value="courseCat.coursecat_Name">
              {{ courseCat.coursecat_Name }}
            </option>
          </select>-->
          <dropdown-field v-model="course.selectedCategory" :default-placeholder="'Course Category'">
            <option v-for="courseCategory in course.courseCategories" :key="courseCategory.coursecat_ID" :value="courseCategory.coursecat_Name">
              {{ courseCategory.coursecat_Name }}
            </option>
          </dropdown-field>
        </div>
        <!--Course Description-->
        <div class="form-group mb-4">
          <textarea v-model="course.courseDescription" class="form-control border-0 shadow-sm px-4 field"
            placeholder="Course Description" style="height: 200px" required></textarea>
        </div>
        <!--Instructor Name-->
        <div class="form-group mb-4">
          <!--<select v-model="selectedInstructor" class="form-select border-0 shadow-sm px-4 field text-muted">
            <option disabled hidden value="">Instructor</option>
            <option v-for="instructor in instructors" :key="instructor.id" :value="instructor.name">{{ instructor.name }}</option>
          </select>-->
          <dropdown-field v-model="course.selectedInstructor" :default-placeholder="'Instructor'">
            <option v-for="instructor in course.instructors" :key="instructor.id" :value="instructor.name">
              {{ instructor.name }}
            </option>
          </dropdown-field>
        </div>
        <div class="row mb-4">
          <!--Start Date-->
          <div class="col-md-6 form-group">
            <VueDatePicker v-model="course.startDate" placeholder="Start Date" :enable-time-picker="false"
              class="form-control border-0 shadow-sm" input-class-name="dp-custom-input" :format="datePickerFormat"
              required></VueDatePicker>
          </div>
          <!--End Date-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="course.endDate" placeholder="End Date" :enable-time-picker="false"
              class="form-control border-0 shadow-sm" input-class-name="dp-custom-input" :format="datePickerFormat"
              required></VueDatePicker>
          </div>
        </div>
        <div class="row mb-4">
          <!--Start Time-->
          <div class="col-md-6 form-group">
            <VueDatePicker v-model="course.startTime" placeholder="Start Time" time-picker
              class="form-control border-0 shadow-sm" input-class-name="dp-custom-input" required><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template></VueDatePicker>
          </div>
          <!--End Time-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="course.endTime" placeholder="End Time" time-picker class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input" required><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template></VueDatePicker>
          </div>
        </div>
        <div class="row mb-4">
          <!--Course Format-->
          <div class="col-md-6 form-group">
            <!-- Dropdown Button -->
            <!--<select v-model="selectedFormat" class="form-select border-0 shadow-sm px-4 field text-muted">
              <option disabled hidden value="">Course Format</option>
              <option v-for="format in formats" :key="format.id" :value="format.name">
                {{ format.name }}
              </option>
            </select>-->
            <dropdown-field v-model="course.selectedFormat" :default-placeholder="'Course Format'">
              <option v-for="courseFormat in course.courseFormats" :key="courseFormat.id" :value="courseFormat.name">
                {{ courseFormat.name }}
              </option>
            </dropdown-field>
          </div>
          <!--Venue-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!--<input v-model="venue" type="text" placeholder="Venue" required autofocus=""
              class="form-control border-0 shadow-sm px-4 field" />-->
            <input-field v-model="course.venue" type="text" placeholder="Venue"></input-field>
          </div>
        </div>
        <div class="row mb-4">
          <!--Course Size-->
          <div class="col-md-6 form-group">
            <!--<input v-model="courseSize" type="text" placeholder="Course Size" required autofocus=""
              class="form-control border-0 shadow-sm px-4 field" />-->
            <input-field v-model="course.courseSize" type="text" placeholder="Course Size"></input-field>
          </div>
          <!--Minimum Slots-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!--<input v-model="minSlots" type="text" placeholder="Min Slots" required autofocus=""
              class="form-control border-0 shadow-sm px-4 field" />-->
            <input-field v-model="course.minimumSlots" type="text" placeholder="Minimum Slots"></input-field>
          </div>
        </div>
        <div class="row mb-4">
          <!--Opening Date For Registration-->
          <div class="col-md-6 form-group">
            <VueDatePicker v-model="course.openingDate" placeholder="Opening Date For Registration" :enable-time-picker="false"
              class="form-control border-0 shadow-sm" input-class-name="dp-custom-input" :format="datePickerFormat"
              required></VueDatePicker>
          </div>
          <!--Opening Time For Registration-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="course.openingTime" placeholder="Opening Time For Registration" time-picker
              class="form-control border-0 shadow-sm" input-class-name="dp-custom-input" required><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template></VueDatePicker>
          </div>
        </div>
        <div class="row mb-4">
          <!--Closing Date For Registration-->
          <div class="col-md-6 form-group">
            <VueDatePicker v-model="course.closingDate" placeholder="Closing Date For Registration" :enable-time-picker="false"
              class="form-control border-0 shadow-sm" input-class-name="dp-custom-input" :format="datePickerFormat"
              required></VueDatePicker>
          </div>
          <!--Closing Time For Registration-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <VueDatePicker v-model="course.closingTime" placeholder="Closing Time For Registration" time-picker
              class="form-control border-0 shadow-sm" input-class-name="dp-custom-input" required><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" /></template>
            </VueDatePicker>
          </div>
        </div>
        <div class="row">
          <!--Course Fee-->
          <div class="col-md-6 form-group">
            <!--<input v-model="courseFee" type="text" placeholder="Course Fee" required autofocus=""
            class="form-control border-0 shadow-sm px-4 field" />-->
            <input-field v-model="course.courseFee" type="text" placeholder="Course Fee"></input-field>
          </div>
          <!--Feedback Template-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!-- Dropdown Button -->
            <!--<select v-model="selectedTemplate" class="form-select border-0 shadow-sm px-4 field text-muted">
              <option disabled hidden value="">Feedback Template</option>
              <option v-for="template in templates" :key="template.id" :value="template.name">{{ template.name }}</option>
            </select>-->
            <dropdown-field v-model="course.selectedTemplate" :default-placeholder="'Feedback Template'">
              <option v-for="feedbackTemplate in course.feedbackTemplates" :key="feedbackTemplate.id" :value="feedbackTemplate.name">
                {{ feedbackTemplate.name }}
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
    <success-modal :show="showSuccessModal" :message="successMessage" @close="hideSuccessModal"/>
  </div>
</template>

<script>
import InputField from "../components/InputField.vue";
import DropdownField from "../components/DropdownField.vue";
import VueDatePicker from "@vuepic/vue-datepicker";
import SuccessModal from "../components/SuccessModal.vue";
import "@vuepic/vue-datepicker/dist/main.css";
import CourseCategoryService from "@/api/services/CourseCategoryService.js"

export default {
  name: "CourseForm",
  components: {
    VueDatePicker,
    InputField,
    DropdownField,
    SuccessModal
  },
  data() {
    return {
      course: {
        courseName: "",
        selectedCategory: "",
        courseCategories: [],
        courseDescription: "",
        selectedInstructor: "",
        //To be removed 
        instructors: [
          { id: 1, name: "Miss Tan"},
          { id: 2, name: "Miss Lee"}
        ],
        datePickerFormat: "yyyy-MM-dd",
        startDate: null,
        endDate: null,
        startTime: "",
        endTime: "",
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
        openingTime: "",
        closingDate: null,
        closingTime: "",
        courseFee: "",
        selectedTemplate: "",
        //To be removed
        feedbackTemplates: [
          { id: 1, name: "Template 1"},
          { id: 2, name: "Template 2"}
        ]
      },
      showSuccessModal: false,
      successMessage: "The course has been successfully created and is now available for registration.",
      formIsValid: false
    };
  },
  async mounted() {
    await this.fetchCourseCategories();
    //await this.fetchInstructors();
    //await this.fetchFeedbackTemplates();
  },
  methods: {
    async fetchCourseCategories() {
      try {
        this.course.courseCategories = await CourseCategoryService.getAllCourseCategory(); // Use the CourseCategoryService
      } catch (error) {
        console.error('Error fetching course categories:', error);
      }
    },
    validateForm() {
      this.formIsValid = 
        this.courseName.trim() !== "" &&
        this.selectedCategory !== "" &&
        this.courseDesc.trim() !== "" &&
        this.selectedInstructor !== "" &&
        this.startDate !== null &&
        this.endDate !== null &&
        this.startTime.trim() !== "" &&
        this.endTime.trim() !== "" &&
        this.selectedFormat !== "" &&
        this.venue.trim() !== "" &&
        this.courseSize.trim() !== "" &&
        this.minSlots.trim() !== "" &&
        this.openingDate !== null &&
        this.openingTime.trim() !== "" &&
        this.closingDate !== null &&
        this.closingTime.trim() !== "" &&
        this.courseFee.trim() !== "" &&
        this.selectedTemplate !== "";
    },
    submitForm() {
      //Conduct Form validation here
      this.$refs.courseForm.reset();

      // Test Simulate a successful submission
      setTimeout(() => {
        this.showSuccessModal = true;
      }, 1000); // Show modal after 1 second (simulating response)
    },
    hideSuccessModal() {
      this.showSuccessModal = false;
      //this.resetForm();
    }
  },
  props: {
    status: {
      type: Boolean,
      required: true,
    },
  },
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
}
</style>
