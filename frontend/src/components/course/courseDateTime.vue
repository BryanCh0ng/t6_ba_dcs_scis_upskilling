<template>
  <div>
    <div class="col-12">
      {{ date }}
    </div>
    <div class="col-12 text-grey">
      {{ time }}
    </div>
  </div>
</template>
    
<script>
export default {
props: {
    date: String,
    time: String,
}
};
</script>