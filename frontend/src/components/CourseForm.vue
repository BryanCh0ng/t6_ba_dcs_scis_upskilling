<template>
  <div id="courseform">
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
            class="form-select border-0 shadow-sm px-4 field text-muted"
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
          <!--<input
            v-model="instructorName"
            type="text"
            placeholder="Instructor Name"
            required
            autofocus=""
            class="form-control border-0 shadow-sm px-4 field"
          />-->
          <select
            v-model="selectedInstructor"
            class="form-select border-0 shadow-sm px-4 field text-muted"
          >
            <option disabled value="">Instructor</option>
            <!--<option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>-->
          </select>
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
            <VueDatePicker
              v-model="startDate"
              placeholder="Start Date"
              :enable-time-picker="false"
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              :format="datePickerFormat"
              required
            ></VueDatePicker>
          </div>
          <!--End Date-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!--<input
              v-model="endDate"
              type="text"
              placeholder="End Date"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker
              v-model="endDate"
              placeholder="End Date"
              :enable-time-picker="false"
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              :format="datePickerFormat"
              required
            ></VueDatePicker>
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
            <VueDatePicker
              v-model="startTime"
              placeholder="Start Time"
              time-picker
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              required
              ><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left:10px;"/></template
            ></VueDatePicker>
          </div>
          <!--End Time-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!--<input
              v-model="endTime"
              type="text"
              placeholder="End Time"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker
              v-model="endTime"
              placeholder="End Time"
              time-picker
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              required
              ><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left:10px;"/></template
            ></VueDatePicker>
          </div>
        </div>
        <div class="row mb-4">
          <!--Course Format-->
          <div class="col-md-6 form-group">
            <!-- Dropdown Button -->
            <select
              v-model="selectedFormat"
              class="form-select border-0 shadow-sm px-4 field text-muted"
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
          <div class="col-md-6 form-group mt-4 mt-md-0">
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
          <div class="col-md-6 form-group mt-4 mt-md-0">
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
          <!--Opening Date For Registration-->
          <div class="col-md-6 form-group">
            <!--<input
              v-model="openingDate"
              type="text"
              placeholder="Opening Date For Registration"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker
              v-model="openingDate"
              placeholder="Opening Date For Registration"
              :enable-time-picker="false"
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              :format="datePickerFormat"
              required
            ></VueDatePicker>
          </div>
          <!--Opening Time For Registration-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!--<input
              v-model="OpeningTime"
              type="text"
              placeholder="Opening Time For Registration"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker
              v-model="openingTime"
              placeholder="Opening Time For Registration"
              time-picker
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              required
              ><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left:10px;"/></template
            ></VueDatePicker>
          </div>
        </div>
        <div class="row mb-4">
          <!--Closing Date For Registration-->
          <div class="col-md-6 form-group">
            <!--<input
              v-model="closingDate"
              type="text"
              placeholder="Closing Date For Registration"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker
              v-model="closingDate"
              placeholder="Closing Date For Registration"
              :enable-time-picker="false"
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              :format="datePickerFormat"
              required
            ></VueDatePicker>
          </div>
          <!--Closing Time For Registration-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!--<input
              v-model="closingTime"
              type="text"
              placeholder="Closing Time For Registration"
              required
              autofocus=""
              class="form-control border-0 shadow-sm px-4 field"
            />-->
            <VueDatePicker
              v-model="closingTime"
              placeholder="Closing Time For Registration"
              time-picker
              class="form-control border-0 shadow-sm"
              input-class-name="dp-custom-input"
              required
            ><template #input-icon>
                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left:10px;"/></template>
            </VueDatePicker>
          </div>
        </div>
        <div class="row">
          <!--Course Fee-->
          <div class="col-md-6 form-group">
            <!-- Dropdown Button -->
            <select
              v-model="selectedFee"
              class="form-select border-0 shadow-sm px-4 field text-muted"
            >
              <option disabled value="">Course Fee</option>
              <!--<option v-for="course in courses" :key="course.id" :value="course.id">{{ course.name }}</option>-->
            </select>
          </div>
          <!--Feedback Template-->
          <div class="col-md-6 form-group mt-4 mt-md-0">
            <!-- Dropdown Button -->
            <select
              v-model="selectedTemplate"
              class="form-select border-0 shadow-sm px-4 field text-muted"
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
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

export default {
  name: "CourseForm",
  components: { VueDatePicker },
  data() {
    return {
      courseName: "",
      selectedCategory: "",
      courseDesc: "",
      selectedInstructor: "",
      startDate: null,
      datePickerFormat: "yyyy-MM-dd",
      endDate: null,
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
      openingDate: null,
      openingTime: "",
      closingDate: null,
      closingTime: "",
      selectedFee: "",
      selectedTemplate: "",
      showSuccessModal: false,
    };
  },
  methods: {
    submitForm() {
      //Conduct Form validation here

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
      (this.courseName = ""),
        (this.selectedCategory = ""),
        (this.courseDesc = ""),
        (this.selectedInstructor = ""),
        (this.startDate = ""),
        (this.endDate = ""),
        (this.startTime = ""),
        (this.endTime = ""),
        (this.selectedFormat = ""),
        (this.venue = ""),
        (this.courseSize = ""),
        (this.minSlots = ""),
        (this.openingDate = ""),
        (this.openingTime = ""),
        (this.closingDate = ""),
        (this.closingTime = ""),
        (this.selectedFee = ""),
        (this.selectedTemplate = "");
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

<style lang="scss">
.dp-custom-input {
  border-color: transparent; /* Set border color to transparent by default */
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
