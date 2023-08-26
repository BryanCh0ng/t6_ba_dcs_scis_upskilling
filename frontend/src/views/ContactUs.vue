<template>
  <div id="contactus">
    <!-- CONTACT US FORM -->
    <div class="container mt-5">
      <h2 class="text-center">Contact Us</h2>

      <p v-if="subjectError" class="text-danger">{{ subjectError }}</p>

      <form @submit.prevent="submitForm">
        <div class="form-group mt-5 mb-4">
          <input
            v-model="subject"
            type="text"
            placeholder="Subject"
            required
            autofocus=""
            class="form-control border-0 shadow-sm px-4 field"
          />
        </div>
        <div class="form-group">
          <textarea
            v-model="message"
            class="form-control border-0 shadow-sm px-4 field"
            placeholder="Message"
            style="height: 200px"
            required
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

export default {
  data() {
    return {
      subject: "",
      subjectError: "", // Error message for subject field
      message: "",
      showSuccessModal: false,
    };
  },
  methods: {
    submitForm() {
      // Clear previous error messages
      // this.subjectError = "";

      // const formData = {
      //   subject: this.subject,
      //   message: this.message,
      // };

      // // Need to add in flask api endpoint
      // axiosClient
      //   .post("", formData)
      //   .then((response) => {
      //     console.log("Form submitted successfully:", response.data);
      //     this.showSuccessModal = true;
      //     this.resetForm();
      //   })
      //   .catch((error) => {
      //     if (error.response) {
      //       // Handle server response error
      //       if (error.response.status === 400) {
      //         this.subjectError = "Please provide a valid subject.";
      //       }
      //     }
      //   });


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