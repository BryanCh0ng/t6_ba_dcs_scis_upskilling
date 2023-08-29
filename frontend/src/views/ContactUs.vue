<template>
  <div id="contactus">
    <!-- CONTACT US FORM -->
    <div class="container mt-5">
      <h2 class="text-center mb-4">Contact Us</h2>

      <!-- Error Message -->
      <error-message :error-message="errorMessage" />

      <form @submit.prevent="submitForm">
        <div class="form-group mt-5 mb-4">
          <input-field v-model="subject" type="text" placeholder="Subject" />
        </div>
        <div class="form-group">
          <textarea
            v-model="message"
            class="form-control border-0 shadow-sm px-4 field"
            placeholder="Message"
            style="height: 200px"
          ></textarea>
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
// import { axiosClient } from "../api/axiosClient";
import ErrorMessage from "../components/ErrorMessage.vue";
import InputField from "../components/InputField.vue";
import { required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import ContactUsService from "../api/services/contactService.js"

export default {
  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      subject: "",
      errorMessage: "", // Error message for subject field
      message: "",
      showSuccessModal: false,
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
  methods: {
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
        // will need get user_ID from session
        user_ID: 1, 
        msg_Subject: this.subject,
        msg_Body: this.message,
        msg_Datetime: new Date().toISOString(), // Current datetime
      };

      try {
        const response = await ContactUsService.createNewMsg(formData);
        console.log('API Response:', response);
        this.showSuccessModal = true;
        this.resetForm();
      } catch (error) {
        console.error('Error submitting form:', error);
      }
    },
    hideSuccessModal() {
      this.showSuccessModal = false;
      this.resetForm();
    },
    resetForm() {
      this.subject = "";
      this.message = "";
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