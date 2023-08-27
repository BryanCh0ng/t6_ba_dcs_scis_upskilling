<template>
  <div>
    <!-- Use the component with the desired API endpoint -->
    <search-filter
      :search-api="searchAllSubmittedProposedCoursesAdmin" 
      @search-complete="handleSearchComplete"
    />
    <div v-if="searchResults">
      <h2>Search Results:</h2>
      <ul>
        <li v-for="result in searchResults" :key="result.course.course_ID">
          {{ result.course.course_Name }} - {{ result.coursecat_Name }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No results found.</p>
    </div>
  </div>
</template>

<script>
import SearchFilter from "@/components/search/ProposalCourseRelatedSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";

export default {
  components: {
    SearchFilter,
  },
  data() {
    return {
      searchResults: [],
    };
  },
  methods: {
    async handleSearchComplete(searchResults) {
      this.searchResults = searchResults;
    },
    async searchAllSubmittedProposedCoursesAdmin(course_Name, coursecat_ID) {
      try {
        console.log(course_Name);
        // Use the axiosClient or another HTTP client to make the API request
        
        let response = await CourseService.searchAllSubmittedProposedCoursesAdmin(
            course_Name,
            coursecat_ID,
        );
          
        this.searchResults = response.data;
        return this.searchResults;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
  },
};
</script>
