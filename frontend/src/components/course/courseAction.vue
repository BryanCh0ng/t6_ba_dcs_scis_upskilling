<template>
  <button class="btn btn-blue-green hop-on text-light font-weight-bold text-nowrap" v-if="status == 'Active'">Hop On</button>
  <button class="btn btn-warning shoutout text-light font-weight-bold text-nowrap" v-else-if="status == 'Vote'">Shout Out</button>
  <button class="btn btn-edit edit text-light font-weight-bold text-nowrap" v-else-if="status == 'Edit'">Edit</button>
  <button class="btn btn-danger delete text-light font-weight-bold text-nowrap" v-else-if="status == 'Delete'">Delete</button>
  <button class="btn btn-deactivate deactivate text-light font-weight-bold text-nowrap" v-else-if="status == 'Deactivate'">Deactivate</button>
  <button class="btn btn-activate activate text-light font-weight-bold text-nowrap" v-else-if="status == 'Activate'">Activate</button>
  <button class="btn btn-activate approve text-light font-weight-bold text-nowrap" v-else-if="status == 'Approve'">Approve</button>
  <button class="btn btn-danger reject text-light font-weight-bold text-nowrap" v-else-if="status == 'Reject'">Reject</button>
  <button class="btn btn-info open_for_voting text-light font-weight-bold text-nowrap" v-else-if="status == 'Open for Voting'">Open for Voting</button>
</template>
  
<script>
export default {
  props: {
    status: String,
    id: Number
  }
};
</script>
  