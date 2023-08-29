<template>
  <div id="searchfilter">
    <div class="container mb-5">
      <form>
        <div class="row">
          <div class="col-md">
            <input-field v-model="instructorName" type="text" placeholder="Instructor Name"/>
          </div>
          <div class="col-md">
            <dropdown-field v-model="role" :default-placeholder="'Role'">
              <option v-for="option in statusDropdownOptions" :key="option" :value="option">{{ option }}</option>
              </dropdown-field>
            </div>
          <div class="col-md">
            <input-field v-model="organizationName" type="text" placeholder="Organization Name"/>
          </div>
          <div class="col-md col-lg-3">
            <div class="d-flex justify-content-between">
              <button @click="resetFilter" class="btn" id="resetbtn">Clear</button>
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
import DropdownField from "../DropdownField.vue";

export default {
  name: "SearchFilter",
  data() {
    return {
      instructorName: "",
      organizationName: "",
      role: "",
      searchedInstructors: [],
      statusDropdownOptions: [],
    };
  },
  props: {
        searchApi: Function,
        statusOptions: Array, 
  },
  components: {
    InputField,
    DropdownField,
  },
  async mounted() {
    this.statusDropdownOptions = this.statusOptions;
  },
  methods: {
    async resetFilter() {
      this.instructorName = "";
      this.organizationName = "";
      this.role = "";
      this.searchedInstructors = []; // Clear search results
    },
    async searchFilter() {
      try {
        // Assign values to variables
        const user_Name = this.instructorName;
        const organizationName = this.organizationName;
        const role = this.role;
        // console.log("user_Name:", user_Name);
        // console.log("organizationName:", organizationName);

        let searchResults;

        // Call the API method from CourseService
        searchResults = await this.searchApi(user_Name, role, organizationName);
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
        border: 3px solid #616161;
        color:black;
    }
</style>
