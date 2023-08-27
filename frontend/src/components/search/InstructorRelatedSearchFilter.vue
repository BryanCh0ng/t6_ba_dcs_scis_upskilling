<template>
  <div id="searchfilter">
    <div class="container mt-5 mb-5">
      <form>
        <div class="row">
          <div class="col-sm">
            <input-field v-model="instructorName" type="text" placeholder="Instructor Name"/>
          </div>
          <div class="col-sm">
            <input-field v-model="organizationName" type="text" placeholder="Organization Name"/>
          </div>
          <div class="col-sm col-lg-3">
            <div class="d-flex justify-content-between">
              <button @click="resetFilter" class="btn" id="resetbtn">Clear All</button>
              <button @click.prevent="searchFilter" class="btn" id="searchbtn">Search</button>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import InputField from "../InputField.vue";

export default {
  name: "SearchFilter",
  data() {
    return {
      instructorName: "",
      organizationName: "",
      searchedInstructors: [],
    };
  },
  props: {
        searchApi: Function,
  },
  components: {
    InputField,
  },
  methods: {
    async resetFilter() {
      this.instructorName = "";
      this.organizationName = "";
      this.searchedInstructors = []; // Clear search results
    },
    async searchFilter() {
      try {
        // Assign values to variables
        const user_Name = this.instructorName;
        const organizationName = this.organizationName;
        // console.log("user_Name:", user_Name);
        // console.log("organizationName:", organizationName);

        let searchResults;

        // Call the API method from CourseService
        searchResults = await this.searchApi(user_Name, organizationName);
        console.log(searchResults)

        // Emit the search-complete event to the parent component
        this.$emit("search-complete", searchResults);

      } catch (error) {
        console.error("Error fetching instructors info:", error);
      }
    },
  },
};
</script>

<style scoped>
    .btn {
        width: 48%;
        height: 50px;
        border-radius: 10px;
    }

    #searchbtn {
        background-color: #151c55;
        color: #FFFFFF;
    }

    #resetbtn {
        background-color: transparent;
        border: 4px solid #616161;
        color:black;
    }
</style>
