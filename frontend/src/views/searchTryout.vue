<template>
  <div>
    <search-filter
      :search-api="searchAllSubmittedProposedCoursesAdmin" 
      @search-complete="handleSearchComplete"
    />
    <div v-if="hasSearchResults">
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
  computed: {
    hasSearchResults() {
      return this.searchResults && this.searchResults.length > 0;
    },
  },
  methods: {
    async handleSearchComplete(searchResults) {
      this.searchResults = searchResults;
    },
    async searchAllSubmittedProposedCoursesAdmin(course_Name, coursecat_ID) {
      try {
        // Assuming that course_Name and coursecat_ID are optional parameters
        let response = await CourseService.searchAllSubmittedProposedCoursesAdmin(
          course_Name,
          coursecat_ID
        );
        this.searchResults = response.data;
        return this.searchResults;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
  },
  async created() {
    try {
      // Perform the initial search when the component is created
      await this.searchAllSubmittedProposedCoursesAdmin();
    } catch (error) {
      console.error("Error initializing search results:", error);
    }
  },
};
</script>
