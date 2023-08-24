<template>
  <div class="col-md-6 d-none d-md-flex bg-image">
    <div class="overlay"></div>
    <div class="image-text">
      <p>Upskilling Engagement System</p>
    </div>
  </div>
</template>

<script>
    export default {
        name: "ImageHalf",
    };
</script>

<style scoped>

.bg-image {
  background-image: url("../assets/smu_building.jpg");
  background-size: cover;
  background-position: center center;
  position: relative; /* Add this to make the overlay relative to the .bg-image div */
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.4); /* Adjust the color and opacity as needed */
}

.image-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  font-size: 60px;
}


</style>>