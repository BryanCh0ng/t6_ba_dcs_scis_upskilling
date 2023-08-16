<template>
  <div id="test">
    <div class="container">
      <form @submit.prevent="submitForm">
        <!--Course Name-->
        <div class="form-group mt-5 mb-4">
          <input
            v-model="courseName"
            type="text"
            placeholder="Course Name"
            required
            autofocus=""
            class="form-control border-0 shadow-sm px-4 field"
          />
        </div>
        <!--Course Category-->
        <div class="form-group mb-4">
          <!-- Dropdown Button -->
          <select
            v-model="selectedCategory"
            class="form-select border-0 shadow-sm px-4 field"
          >
            <option disabled value="">Course Category</option>
            <!--<option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>-->
          </select>
        </div>
        <!--Course Description-->
        <div class="form-group mb-4">
          <textarea
            v-model="courseDesc"
            class="form-control border-0 shadow-sm px-4 field"
            placeholder="Course Description"
            style="height: 200px"
            required
          ></textarea>
        </div>
        <!--Instructor Name-->
        <div class="form-group mb-4">
          <input
            v-model="instructorName"
            type="text"
            placeholder="Instructor Name"
            required
            autofocus=""
            class="form-control border-0 shadow-sm px-4 field"
          />
        </div>
        <div class="row mb-4">
          <!--Start Date-->
          <div class="col-md-6 form-group">
            <!--<input
              v-model="startDate"
              type="text"
              placeholder="Start Date"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker v-model="startDate" placeholder="Start Date" :enable-time-picker="false" class="form-control border-0 shadow-sm px-4 field"></VueDatePicker>
          </div>
          <!--End Date-->
          <div class="col-md-6 form-group mt-3 mt-md-0">
            <!--<input
              v-model="endDate"
              type="text"
              placeholder="End Date"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker v-model="endDate" placeholder="End Date" :enable-time-picker="false" class="form-control border-0 shadow-sm px-4 field"></VueDatePicker>
          </div>
        </div>
        <div class="row mb-4">
          <!--Start Time-->
          <div class="col-md-6 form-group">
            <!--<input
              v-model="startTime"
              type="text"
              placeholder="Start Time"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker v-model="startTime" placeholder="Start Time" class="form-control shadow-sm px-4 field" time-picker style="border: 0px;"/>
          </div>
          <!--End Time-->
          <div class="col-md-6 form-group mt-3 mt-md-0">
            <!--<input
              v-model="endTime"
              type="text"
              placeholder="End Time"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker v-model="endTime" placeholder="End Time" class="form-control border-0 shadow-sm px-4 field" time-picker />
          </div>
        </div>
        <div class="row mb-4">
          <!--Course Format-->
          <div class="col-md-6 form-group">
            <!-- Dropdown Button -->
            <select
              v-model="selectedFormat"
              class="form-select border-0 shadow-sm px-4 field"
            >
              <option disabled hidden value="">Course Format</option>
              <option
                v-for="format in formats"
                :key="format.id"
                :value="format.id"
              >
                {{ format.name }}
              </option>
            </select>
          </div>
          <!--Venue-->
          <div class="col-md-6 form-group mt-3 mt-md-0">
            <input
              v-model="venue"
              type="text"
              placeholder="Venue"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />
          </div>
        </div>
        <div class="row mb-4">
          <!--Course Size-->
          <div class="col-md-6 form-group">
            <input
              v-model="courseSize"
              type="text"
              placeholder="Course Size"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />
          </div>
          <!--Minimum Slots-->
          <div class="col-md-6 form-group mt-3 mt-md-0">
            <input
              v-model="minSlots"
              type="text"
              placeholder="Min Slots"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />
          </div>
        </div>
        <div class="row mb-4">
          <!--Closing Date For Registration-->
          <div class="col-md-6 form-group">
            <input
              v-model="closingDate"
              type="text"
              placeholder="Closing Date For Registration"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />
          </div>
          <!--Closing Time For Registration-->
          <div class="col-md-6 form-group mt-3 mt-md-0">
            <input
              v-model="closingTime"
              type="text"
              placeholder="Closing Time For Registration"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />
          </div>
        </div>
        <div class="row">
          <!--Course Fee-->
          <div class="col-md-6 form-group">
            <!-- Dropdown Button -->
            <select
              v-model="selectedFee"
              class="form-select border-0 shadow-sm px-4 field"
            >
              <option disabled value="">Course Fee</option>
              <!--<option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>-->
            </select>
          </div>
          <!--Feedback Template-->
          <div class="col-md-6 form-group mt-3 mt-md-0">
            <!-- Dropdown Button -->
            <select
              v-model="selectedTemplate"
              class="form-select border-0 shadow-sm px-4 field"
            >
              <option disabled value="">Feedback Template</option>
              <!--<option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>-->
            </select>
          </div>
        </div>
        <button
          type="submit"
          class="btn btn-block shadow-sm w-100 mt-5 field submitbtn"
        >
          Submit
        </button>
      </form>
    </div>
    <!-- Success modal -->
    <div v-if="showSuccessModal" class="modal-backdrop">
      <div class="modal-content">
        <p>
          Your message has been successfully sent. We appreciate your feedback!
        </p>
        <button @click="hideSuccessModal" class="btn btn-secondary close-btn">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

export default {
  name: "CourseForm",
  components: { VueDatePicker },
  data() {
    return {
      courseName: "",
      selectedCategory: "",
      courseDesc: "",
      instructorName: "",
      startDate: "",
      endDate: "",
      startTime: "",
      endTime: "",
      selectedFormat: "", // Holds the selected course format ID
      formats: [
        { id: 1, name: "Online" },
        { id: 2, name: "Face-to-Face" },
        // Add more course format here
      ],
      venue: "",
      courseSize: "",
      minSlots: "",
      closingDate: "",
      closingTime: "",
      selectedFee: "",
      selectedTemplate: "",
      showSuccessModal: false,
    };
  },
  methods: {
    submitForm() {
      // Test Simulate a successful submission
      setTimeout(() => {
        this.showSuccessModal = true;
      }, 1000); // Show modal after 1 second (simulating response)
    },
    hideSuccessModal() {
      this.showSuccessModal = false;
      this.resetForm();
    },
    resetForm() {
        this.courseName = "",
        this.selectedCategory = "",
        this.courseDesc = "",
        this.instructorName = "",
        this.startDate = "",
        this.endDate = "",
        this.startTime = "",
        this.endTime = "",
        this.selectedFormat = "", // Holds the selected course format ID
        this.venue = "",
        this.courseSize = "",
        this.minSlots = "",
        this.closingDate = "",
        this.closingTime = "",
        this.selectedFee = "",
        this.selectedTemplate = "";
    },
  },
};
</script>

<style scoped>
.modal-content {
  width: 50%;
  height: 15%;
}

.close-btn {
  position: absolute;
  bottom: 25px;
  right: 20px;
  width: 150px;
}
</style>
