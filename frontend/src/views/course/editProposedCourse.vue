<template>
  <div id="editProposedCourse">
    <div class="container mt-5">
      <h2 class="text-center mb-4">Edit Proposed Course</h2>

      <!-- Error Message -->
      <error-message :error-message="errorMessage" />

      <form @submit.prevent="submitForm">
        <div class="form-group mt-5 mb-4">
          <input v-model="course_name" type="text" placeholder="Course Name" class="form-control border-0 shadow-sm px-4 field mb-3"/>

        </div>
        <div class="form-group">
          <dropdown-field v-model="category" :default-placeholder="'Course Category'">
            <option v-for="option in categoryDropdownOptions" :key="option.coursecat_ID" :value="option.coursecat_ID">{{ option.coursecat_Name }}</option>
          </dropdown-field>
        </div>
        <div class="form-group">
          <textarea v-model="course_desc" class="form-control border-0 shadow-sm px-4 field" :placeholder="descPlaceholder" style="height: 200px"></textarea>
        </div>

        <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
          Save
        </button>
      </form>
    </div>
    <!-- Success modal -->
    <div v-if="showSuccessModal" class="modal-backdrop">
      <div class="modal-content">
        <p>
          You have updated the content of your proposed course successfully. Please refer to your profile to check its status. 
        </p>
        <button @click="hideSuccessModal" class="btn btn-secondary close-btn">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import ErrorMessage from "../../components/ErrorMessage.vue";
import DropdownField from "../../components/DropdownField.vue";
import { required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";
import CourseCategoryService from "@/api/services/CourseCategoryService.js";
import ProposedCourseService from "@/api/services/proposedCourseService.js";

export default {
  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      user_ID: null,
      category: "",
      course_name: "",
      course_desc: "",
      errorMessage: "", // Error message for validation
      showSuccessModal: false,
      descPlaceholder: "Course Description",
      categoryDropdownOptions: [],
    };
  },

  validations() {
    return {
      course_name: { required },
      course_desc: { required },
      category: { required },
    };
  },

  components: {
    ErrorMessage,
    DropdownField,
  },

  created() {
    this.getUserID();
    this.fetchCategoryDropdownOptions();
    this.fetchProposedCourseDetails();
  },

  methods: {
    async fetchCategoryDropdownOptions() {
      try {
        const categoryOptions = await CourseCategoryService.getAllCourseCategory();
        this.categoryDropdownOptions = categoryOptions;
      } catch (error) {
        console.error('Error fetching category dropdown options:', error);
      }
    },

    async getUserID() {
      try {
        const user_ID = await UserService.getUserID();
        this.user_ID = user_ID;
      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_ID = null;
      }
    },

    async fetchProposedCourseDetails() {
      try {
        const courseId = this.$route.params.courseId;
        console.log(courseId)
        const response = await ProposedCourseService.getProposedCourseByCourseId(courseId);
        console.log(response)
        const courseData = response.data // Assuming your API response structure

        if (courseData) {
          // Update the component data with the retrieved course details
          this.course_name = courseData.course_Name;
          console.log(this.course_name)
          this.course_desc = courseData.course_Desc;

          // Update the category using the ID, assuming categoryDropdownOptions contains all possible options
          const coursecat_ID = courseData.coursecat_ID;
          this.category = coursecat_ID;

          // Optional: You can set the default dropdown option if it exists
          const defaultOption = this.categoryDropdownOptions.find(option => option.coursecat_ID === coursecat_ID);
          if (defaultOption) {
            this.category = defaultOption.coursecat_ID;
          }
        } else {
          console.error('Proposed course not found.');
        }
      } catch (error) {
        console.error('Error fetching proposed course details:', error);
      }
    },

    async submitForm() {
        // Trigger Vuelidate validation
        this.v$.$touch();

        // Check for validation errors
        if (this.v$.$invalid) {
            this.errorMessage = "Please fix the validation errors.";
            return;
        }

        const courseId = this.$route.params.courseId;

        const formData = {
            course_Name: this.course_name,
            course_Desc: this.course_desc,
            coursecat_ID: this.category,
        };

        try {
            const result = await ProposedCourseService.updateProposedCourse(courseId, formData);

            if (result.success) {
                this.showSuccessModal = true;

            } else {
            this.errorMessage = result.message;
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    },

    hideSuccessModal() {
      this.showSuccessModal = false;
      this.$router.push({ name: 'studentViewProfile' });
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
