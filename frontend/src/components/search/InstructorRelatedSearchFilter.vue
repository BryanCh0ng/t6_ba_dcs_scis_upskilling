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
    <!-- Display search results here -->
    <div v-if="searchedInstructors.length !== 0" class="mt-4">
      <h3>Search Results</h3>
      <ul>
        <li v-for="(instructor, index) in searchedInstructors" :key="index">
          <!-- Display instructor info here -->
          {{ instructor.user_Name }} - {{ instructor.organisation_Name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import InputField from "../InputField.vue";
import CourseService from "@/api/services/CourseService.js"

export default {
  name: "SearchFilter",
  data() {
    return {
      instructorName: "",
      organizationName: "",
      searchedInstructors: [],
    };
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
        console.log("user_Name:", user_Name);
        console.log("organizationName:", organizationName);

        // Call the API method from CourseService
        const instructorsInfo = await CourseService.getAllInstructorsAndTrainers(user_Name, organizationName);

        // Update the data with the retrieved results
        this.searchedInstructors = instructorsInfo.data;

      } catch (error) {
        console.error("Error fetching instructors info:", error);
      }
    },
  },
};
</script>

<style scoped>
    button {
        width: 48%;
        height: 45px;
        border-radius: 10px;
    }

    #searchbtn {
        background-color: #151c55;
        color: #FFFFFF;
    }

    #resetbtn {
        background-color: transparent;
        border: 4px solid #616161;
    }
</style>
