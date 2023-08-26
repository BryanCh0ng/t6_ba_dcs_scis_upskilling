<template>
 <div>
  <form action="">
    <div class="container">
      <div class="row d-flex align-items-center justify-content-center">
        <div class="form-group col-md-3 search-filter-div">
          <input type="text" placeholder="Course Name" autofocus class="form-control border-0 shadow-sm px-4 field"/>
        </div>
        <div class="form-group col-md-3 search-filter-div">
          <select placeholder="Course Category" class="form-control border-0 shadow-sm px-4 field" id="course_category">
            <option value=""></option>
          </select>
        </div>
        <div class="form-group col-md-3 search-filter-div"  v-if="role == 'student'">
          <select placeholder="All Courses" class="form-control border-0 shadow-sm px-4 field" id="course_type">
            <option value=""></option>
          </select>
        </div>
        <div class="form-group col-md-3 search-filter-div"  v-else-if="role == 'admin' && page != 'register'">
          <select placeholder="Status" class="form-control border-0 shadow-sm px-4 field" id="status">
            <option value=""></option>
          </select>
        </div>
        <div class="col-md-3 d-flex justify-content-center text-nowrap search-filter-btn-div">
          <div class="col" style="display:contents;">
            <button class="btn btn-secondary me-2 font-weight-bold">Clear All</button>
            <button class="btn btn-primary font-weight-bold">Search</button>
          </div>
        </div>
      </div>
    </div>
  </form>
 </div>
</template>

<style>
@media (max-width: 767.98px) {
  .search-filter-div {
    margin-bottom: 1rem;
  }
  .search-filter-btn-div {
    justify-content: flex-start !important;
  }
}

button {
  font-weight: bold;
}
</style>

<script>
  export default {
    props: {
      role: String,
      page: String
    },
  };
</script>