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
      </div>
    </div>
    <div class="modal-footer"> 
      <button class="btn btn-danger" @click="reject">Reject</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedRadio: 'no-reason', 
      rejectionReason: '',
    };
  },
  methods: {
    reject() {
      console.log( this.selectedRadio);
      console.log(this.rejectionReason);
    }
  }
}
</script>

 