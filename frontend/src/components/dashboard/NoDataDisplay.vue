<template>
    <div id="chart-container">
      <div class="content">
        <h4>No Data to Display</h4>
        <p v-if="displayMessage">Please make a different filter selection</p>
      </div>
    </div>
</template>
  

<script>

export default {
    name: 'NoDataDisplay',
    props: {
        displayMessage: {
            type: Boolean,
            required: true,
            default: false
        }
    }
}

</script>

<style scoped>
#chart-container {
    width: 100%;
    max-width: 350px;
    height: auto;
    position: relative;
    margin: 10px auto 0;
    /* Adjust top margin to reduce the gap */
    overflow: hidden;
    /* Hide any chart content overflowing the div */
}


.content {
    width: 350px;
    height: 250px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

</style>