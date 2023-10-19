<template>
  <div class="container text-center">
    <!-- Ratings -->
    <div class="row">
      <!-- Display Total No. of Feedbacks -->
      <div class="col-12 col-md-4 dashboard mb-3">
        <h2 class="fs-1">{{totalNoOfFeedback}}</h2>
        <p><strong>Total No. of Feedbacks</strong></p>
      </div>
      <!-- Display Overall Average Course Ratings if not instructor-specific -->
      <div v-if="courseSpecific" class="col-12 col-md-4 mb-3 dashboard">
        <h2 class="fs-1">{{courseAverageRating}} / 5</h2>
        <p><strong>Overall Average Course Ratings</strong></p>
      </div>
      <!-- Display Overall Average Instructor Ratings if not course-specific -->
      <div v-if="instructorSpecific" class="col-12 col-md-4 mb-3 dashboard">
        <h2 class="fs-1">{{instructorAverageRating}} / 5</h2>
        <p><strong>Overall Average Instructor Ratings</strong></p>
      </div>
    </div>

    <!-- Sentiment Course -->
    <div class="row">
      <!-- Display Overall Course Sentiment -->
      <div class="col-12 col-md-6 dashboard mb-3" v-if="courseSpecific">
        <WordCloud :wordData="positiveCourseWordData"/> <!-- tryout, need to change -->
        <p><strong>Overall Course Sentiment</strong></p>
      </div>
      <!-- Display Overall Course Positive WordCloud -->
      <div class="col-12 col-md-6 dashboard mb-3" v-if="courseSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordCloud :wordData="positiveCourseWordData"/>
        <p><strong>Overall Course Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-12 col-md-6 dashboard mb-3" v-if="courseSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordCloud :wordData="negativeCourseWordData"/>
        <p><strong>Overall Course Negative WordCloud</strong></p>
      </div>

      <!-- Display Overall Instructor Sentiment -->
      <div class="col-12 col-md-6 dashboard mb-3" v-if="instructorSpecific">
        <WordCloud :wordData="overallInstructorWordData"/>
        <p><strong>Overall Instructor Sentiment</strong></p>
      </div>
      <!-- Display Overall Instructor Positive WordCloud -->
      <div class="col-12 col-md-6 dashboard mb-3" v-if="instructorSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordCloud :wordData="positiveInstructorWordData"/>
        <p><strong>Overall Instructor Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-12 col-md-6 dashboard mb-3" v-if="instructorSpecific">
        <!-- Include Word Cloud component here for negative feedback -->
        <WordCloud :wordData="negativeInstructorWordData"/>
        <p><strong>Overall Instructor Negative WordCloud</strong></p>
      </div>
    </div>

    <div class="row">
      <!-- Topic Modeling - Course Done Well / Contribution -->
      <div
        v-for="(topic, index) in courseDoneWellTopics"
        :key="index"
        class="col-12 col-md-6 dashboard mb-3"
      >
        <!-- Include Word Cloud component here for course done well topic -->
        <WordCloud :wordData="courseDoneWellTopics[index].wordData" />
        <p><strong>Overall Course Done Well - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Course Suggestions / Improve -->
      <div
        v-for="(topic, index) in courseSuggestionsTopics"
        :key="index"
        class="col-12 col-md-6 dashboard mb-3"
      >
        <!-- Include Word Cloud component here for course suggestions topic -->
        <WordCloud :wordData="courseSuggestionsTopics[index].wordData" />
        <p><strong>Overall Course Suggestions - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Instructor Done Well -->
      <div
        v-for="(topic, index) in instructorDoneWellTopics"
        :key="index"
        class="col-12 col-md-6 dashboard mb-3"
      >
        <!-- Include Word Cloud component here for instructor done well topic -->
        <WordCloud :wordData="instructorDoneWellTopics[index].wordData" />
        <p><strong>Overall Instructor Done Well - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Instructor Suggestions -->
      <div
        v-for="(topic, index) in instructorSuggestionsTopics"
        :key="index"
        class="col-12 col-md-6 dashboard mb-3"
      >
        <!-- Include Word Cloud component here for instructor suggestions topic -->
        <WordCloud :wordData="instructorSuggestionsTopics[index].wordData" />
        <p><strong>Overall Instructor Suggestions - Topic {{ index + 1 }}</strong></p>
      </div>
    </div>
  </div>
</template>


<script>
import WordCloud from "@/components/dashboard/WordCloud.vue"; // Adjust the import path based on your project structure
import DashboardService from '@/api/services/dashboardService';

export default {
    components: {
        WordCloud, 
    },
    data() {
        return {
            instructorSpecific: true, 
            courseSpecific: true,
            totalNoOfFeedback: null,
            courseAverageRating: null,
            instructorAverageRating: null,
            overallCourseWordData: [],
            positiveCourseWordData: [],
            negativeCourseWordData: [],
            overallInstructorWordData: [],
            positiveInstructorWordData: [],
            negativeInstructorWordData: [],
            courseDoneWellTopics: [],
            courseSuggestionsTopics: [],
            instructorDoneWellTopics: [],
            instructorSuggestionsTopics: [],
        };
    },
    methods: {
      // Course Average Rating
      async fetchCourseAverageRating() {
        try {
          const response = await DashboardService.getCourseAverageRatings(null);
          console.log(response)
          this.courseAverageRating = response.data.overall_average_rating; 
          this.totalNoOfFeedback = response.data.total_feedback;
          console.log(this.courseAverageRating)
        } catch (error) {
          console.error('Error fetching courseDoneWellTopics:', error);
        }
      },
      // Instructor Average Rating
      async fetchInstructorAverageRating() {
        try {
          const response = await DashboardService.getInstructorAverageRatings(null);
          console.log(response)
          this.instructorAverageRating = response.data.instructor_average_rating; 
          console.log(this.instructorAverageRating)
        } catch (error) {
          console.error('Error fetching courseDoneWellTopics:', error);
        }
      },
      // Topic modeling for a particular course
      async fetchCourseDoneWellTopics() {
        try {
          const response = await DashboardService.getCourseDoneWellFeedback(null);
          // console.log(response)
          this.courseDoneWellTopics = response.topic_words_list; 
          // console.log(this.courseDoneWellTopics)
        } catch (error) {
          console.error('Error fetching courseDoneWellTopics:', error);
        }
      },
    },
    mounted() {
      this.fetchCourseAverageRating();
      this.fetchInstructorAverageRating();
      this.fetchCourseDoneWellTopics();
    }
};
</script>

<style scoped>
.container {
  color: #404040;
}

.dashboard {
  border: 2px solid #616161;
  margin-right: 20px;
  padding: 5px;
  flex: 0 0 calc(33.33% - 20px); 
}

@media (max-width: 1399px) {
  .dashboard {
    flex: 0 0 calc(50% - 20px); 
  }
}

@media (max-width: 991px) {
  .dashboard {
    flex: 0 0 100%; 
  }
}
</style>
