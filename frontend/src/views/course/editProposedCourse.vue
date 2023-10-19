<template>
  <div id="editProposedCourse">
    <div class="container mt-5">
      <h2 v-if="action == 'approve'" class="text-center mb-4">
        Edit Course (Proposed Course Approved)
      </h2>
      <h2 v-else class="text-center mb-4">Edit Proposed Course</h2>

      <form @submit.prevent="submitForm">
        <div class="form-group mt-5 mb-4">
          <input v-model="course_name"
            type="text"
            placeholder="Course Name"
            class="form-control border-0 shadow-sm px-4 field mb-3"
          />
        </div>
        <div class="form-group">
          <dropdown-field
            v-model="category"
            :default-placeholder="'Course Category'"
          >
            <option
              v-for="option in categoryDropdownOptions"
              :key="option.coursecat_ID"
              :value="option.coursecat_ID"
            >
              {{ option.coursecat_Name }}
            </option>
          </dropdown-field>
        </div>
        <div class="form-group">
          <textarea
            v-model="course_desc"
            class="form-control border-0 shadow-sm px-4 field"
            :placeholder="descPlaceholder"
            style="height: 200px"
            @input="limitCourseDescription"
          ></textarea>
          <div class="text-muted mt-2">
            Character Count: {{ courseDescLength }}/800
          </div>
        </div>
        <div class="row mt-5">
          <div class="col-md-6 mb-2">
            <button
              type="button"
              class="btn btn-secondary shadow-sm w-100 mt-2 field cancelbtn"
              @click="cancelForm"
            >
              Cancel
            </button>
          </div>
          <div class="col-md-6 mb-2">
            <button
              v-if="action == 'approve'"
              type="submit"
              class="btn btn-block shadow-sm w-100 mt-2 field submitbtn"
            >
              Approve Proposed Course
            </button>
            <button
              v-else
              type="submit"
              class="btn btn-block shadow-sm w-100 mt-2 field submitbtn"
            >
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
import DropdownField from "@/components/DropdownField.vue";
import { required, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";
import CourseCategoryService from "@/api/services/CourseCategoryService.js";
import ProposedCourseService from "@/api/services/proposedCourseService.js";
import DefaultModal from "@/components/DefaultModal.vue";

// Utility function to show a success message
function showSuccessMessage(vm) {
  vm.title = "Proposed Course Updated Successfully";
  vm.message = "You have successfully updated the proposed course details.";
  vm.showAlert = true;
  vm.buttonType = "success";
}

// Utility function to show an unsuccessful message
function showUnsuccessMessage(vm) {
  vm.title = "Proposed Course Unsuccessful";
  vm.message = "There is already a course with the same course name. Please change it to a different one.";
  vm.showAlert = true;
  vm.buttonType = "danger";
}

export default {
  setup() {
    const v$ = useVuelidate();
    return { v$ };
  },

  data() {
    return {
      user_ID: null,
      category: "",
      course_name: "",
      course_desc: "",
      errorMessage: "",
      showAlert: false,
      title: "",
      message: "",
      buttonType: "",
      descPlaceholder: "Course Description",
      categoryDropdownOptions: []
    };
  },

  validations() {
    return {
      course_name: { required },
      course_desc: { required, maxLength: maxLength(800) },
      category: { required },
      action: ""
    };
  },

  components: {
    DropdownField,
    DefaultModal
  },

  async created() {
    this.getUserID();
    const action = this.$route.params.action;
    this.action = action;
    if (this.action == 'approve') {
      const user_ID = await UserService.getUserID();
      const role = await UserService.getUserRole(user_ID);
      if (role == 'Student') {
        this.$router.push({ name: 'studentViewProfile' });
      } else if (role == 'Instructor' || role == 'Trainer') {
        this.$router.push({ name: 'instructorTrainerViewProfile' });
      }
    }
    this.get_user_role();
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

    async get_user_role() {
      try {
        const user_role = await UserService.getUserRole()
        this.user_role = user_role
      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_role = null;
      }
    },

    async fetchProposedCourseDetails() {
      try {
        const courseId = this.$route.params.courseId;
        const response = await ProposedCourseService.getProposedCourseByCourseId(courseId);
        const courseData = response.data;

        if (courseData) {
          this.course_name = courseData.course_Name;
          this.course_desc = courseData.course_Desc;
          const coursecat_ID = courseData.coursecat_ID;
          this.category = coursecat_ID;
          this.pcourse_ID = courseData.pcourse_ID;
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
      if (!this.course_name || !this.course_desc || !this.category) {
        this.errorMessage = "Please ensure all fields are filled.";
        return;
      }

      if (this.course_desc.length > 800) {
        this.errorMessage = "Course description must be 800 characters or less.";
        return;
      }

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
        if (this.action == 'approve') {
          const result = await ProposedCourseService.updateProposedCourse(courseId, formData);
          console.log(result);
          if (result.message == "Proposed course updated successfully") {
            let approve_result;
            if (result.success) {
              const course = await ProposedCourseService.getProposedCourseByCourseId(courseId);
              const acceptPromise = ProposedCourseService.approveProposedCourse({ "pcourseID": course['data'].pcourse_ID });
              approve_result = await acceptPromise;
            } else {
              approve_result = { code: 200 };
            }

            if (approve_result.code == 200) {
              showSuccessMessage(this);
            } else {
              this.errorMessage = approve_result.message;
            }
          } else if (result.message == "Course Update Unsuccessful. A course with the same name already exists.") {
            showUnsuccessMessage(this);
          }
        } else {
          const result = await ProposedCourseService.updateProposedCourse(courseId, formData);
          console.log(result);
          if (result.message == "Proposed course updated successfully") {
            showSuccessMessage(this);
          } else if (result.message == "Course Update Unsuccessful. A course with the same name already exists.") {
            showUnsuccessMessage(this);
          }
        }
      } catch (error) {
        console.error('Error submitting form:', error);
      }
    },

    async handleModalClosed(value) {
      this.showAlert = value;

      if (this.action == 'approve' && this.buttonType === "success") {
        this.$router.push({ name: 'adminViewProposedCourse' });
      } else {
        if (this.user_role === 'Student' && this.buttonType === "success") {
          this.$router.push({ name: 'studentViewProfile' });
        } else if (this.user_role === 'Instructor' || this.user_role === 'Trainer') {
          this.$router.push({ name: 'instructorTrainerViewProfile' });
        }
      }
    },

    cancelForm() {
      this.$router.go(-1);
    },

    limitCourseDescription() {
      if (this.course_desc.length > 800) {
        this.course_desc = this.course_desc.substring(0, 800); // Limit the description to 800 characters
      }
    },
  },
  computed: {
    courseDescLength() {
      return this.course_desc.length;
    },
  },
};
</script>