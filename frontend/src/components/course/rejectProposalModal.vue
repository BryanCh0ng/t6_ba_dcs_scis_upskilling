<template>
  <div class="modal-content">
    <div class="modal-header">
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body pt-1"> 
      <div class="modal-title pt-3">
        <h5>Reject Proposal</h5>
      </div>
      <div>
        <div>
          <input type="radio" id="radio-no-reason" name="rejectRadio" v-model="selectedRadio" value="no-reason">
          <label class="reject-reason-label" for="radio-no-reason">Reject Proposal without specifying reason</label>
        </div>
        <div>
          <input type="radio" id="radio-with-reason" name="rejectRadio" v-model="selectedRadio" value="with-reason">
          <label class="reject-reason-label" for="radio-with-reason">Reject Proposal including reason</label>
        </div>
        <div class="mt-2">
          <textarea placeholder="Rejection Reason" class="form-control" id="reject-reason" rows="4" v-model="rejectionReason"></textarea>
        </div>
        <div :class="{ 'd-none': !showResponse, 'd-block': showResponse }">
           <p :class="{ 'text-danger mt-2': isError, 'text-success mt-2': !isError }">{{ responseText }}</p> 
        </div>
      </div>
    </div>
    <div class="modal-footer"> 
      <button class="btn btn-danger" :disabled="disabled" id="reject-proposed-course-btn" @click="reject">Reject</button>
    </div>
  </div>
</template>

<script>
import ProposedCourseService from "@/api/services/proposedCourseService"

export default {
  props: {
    course: Object
  },
  data() {
    return {
      selectedRadio: 'no-reason', 
      rejectionReason: '',
      showResponse: false,
      responseText: "",
      isError: false,
      disabled: false
    };
  },
  methods: {
    reject() {
      this.showResponse = false
      if (this.selectedRadio == 'with-reason' && /^[^a-zA-Z]*$/.test(this.rejectionReason)){
        this.showResponse = true
        this.responseText = "Please Specify reason for rejecting"
        this.isError = true
      }
      if (!this.showResponse) {
       this.reject_proposed_course()
      }
    },
    resetData(){
      this.rejectionReason = ''
      this.showResponse = false;
      this.selectedRadio = 'no-reason'
      this.responseText = "";
      this.isError = false;
      this.disabled = false;
    },
    async reject_proposed_course() {
      try {
        let response = await ProposedCourseService.rejectProposedCourse({"pcourseID": this.course.pcourse_ID, "reason": this.rejectionReason})
        if (response.code == 200) {
          this.responseText = response.message
          this.isError = false
          this.disabled = true;
        }
        else {
          this.responseText = response.message
          this.isError = true
        }
        this.showResponse = true
      } catch (error) {
        this.isError = true
        this.responseText = error
        this.showResponse = true
      }
    }
  },
}
</script>

 