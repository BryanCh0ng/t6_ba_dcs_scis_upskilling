<template>
  <div id="contactus">
    <!-- CONTACT US FORM -->
    <div class="container">
      <h2 class="text-center mb-4 pt-5">Contact Us</h2>

      <!-- Error Message -->
      <error-message :error-message="errorMessage" />

      <form @submit.prevent="submitForm">
        <div class="form-group mt-5 mb-4">
          <input-field v-model="subject" type="text" :placeholder="subjectPlaceholder" />
        </div>
        <div class="form-group">
          <textarea
            v-model="message"
            class="form-control border-0 shadow-sm px-4 field"
            :placeholder="messagePlaceholder"
            style="height: 200px"
          ></textarea>
        </div>

        <button
          type="submit"
          class="btn btn-block shadow-sm w-100 mt-5 field submitbtn"
          title="Submit"
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
        <button @click="hideSuccessModal" class="btn btn-secondary close-btn" title="Close">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
// import { axiosClient } from "../api/axiosClient";
import ErrorMessage from "../components/ErrorMessage.vue";
import InputField from "../components/InputField.vue";
import { required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import ContactUsService from "../api/services/contactService.js"
import UserService from "@/api/services/UserService.js";

export default {
  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      user_ID: null,
      subject: "",
      errorMessage: "", // Error message for subject field
      message: "",
      showSuccessModal: false,
      subjectPlaceholder: "Subject",
      messagePlaceholder: "Message"
    };
  },

  validations() {
    return {
      subject: { required},
      message: { required},
    };
  },
  components: {
    ErrorMessage,
    InputField,
  },
  created() {
    this.get_user_id();
  },
  methods: {
    async get_user_id() {
      try {
        const user_ID = await UserService.getUserID()
        this.user_ID = user_ID
        // console.log(this.user_ID)
      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_ID = null;
      }
    },
    async submitForm() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.errorMessage = ""; // Reset error message

      // Check for empty fields
      if (!this.subject || !this.message) {
        this.errorMessage = "Please ensure all fields are filled.";
        return;
      }
      
      if (this.v$.$invalid) {
        this.errorMessage = "Please fix the validation errors.";
        return;
      }

      const formData = {
        user_ID: this.user_ID, 
        msg_Subject: this.subject,
        msg_Body: this.message,
        msg_Datetime: new Date().toISOString(), 
      };

      try {
        const response = await ContactUsService.createNewMsg(formData);
        console.log('API Response:', response);
        this.showSuccessModal = true;
      } catch (error) {
        console.error('Error submitting form:', error);
      }
    },
    async hideSuccessModal() {
      this.showSuccessModal = false;
      const user_ID = await UserService.getUserID();
      const role = await UserService.getUserRole(user_ID);
      if (role == 'Student') {
        this.$router.push({name: "studentViewCourse"});
      } else if (role == 'Instructor' || role == 'Trainer') {
        this.$router.push({ name: 'instructorTrainerViewProfile' });
      }
      
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