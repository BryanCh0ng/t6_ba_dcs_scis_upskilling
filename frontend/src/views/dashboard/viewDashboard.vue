<template>
  <div class="container text-center">
    <h2 class="mb-5">Feedback Analysis</h2>
    
    <!-- Ratings -->
    <div class="row">
      <!-- Display Total No. of Feedbacks -->
      <div class="col-12 col-md-4 dashboard pt-3 mb-3 custom-col">
        <h2 class="fs-1">{{totalNoOfFeedback}}</h2>
        <p><strong>Total No. of Feedbacks</strong></p>
      </div>
      <!-- Display Overall Average Course Ratings if not instructor-specific -->
      <div v-if="courseSpecific" class="col-12 col-md-4 pt-3 mb-3 dashboard custom-col">
        <h2 class="fs-1">{{courseAverageRating}} / 5</h2>
        <p><strong>Overall Average Course Ratings</strong></p>
      </div>
      <!-- Display Overall Average Instructor Ratings if not course-specific -->
      <div v-if="instructorSpecific" class="col-12 col-md-4 pt-3 mb-3 dashboard custom-col">
        <h2 class="fs-1">{{instructorAverageRating}} / 5</h2>
        <p><strong>Overall Average Instructor Ratings</strong></p>
      </div>
    </div>

    <!-- Sentiment Course -->
    <div class="row">
      <!-- Display Overall Course Sentiment -->
      <div class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col" v-if="courseSpecific">
        <WordCloud :wordData="positiveCourseWordData"/> <!-- tryout, need to change -->
        <p><strong>Overall Course Sentiment</strong></p>
      </div>
      <!-- Display Overall Course Positive WordCloud -->
      <div class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col" v-if="courseSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordChart v-if="positiveCourseWordData.length > 0" :datasets="positiveCourseWordData" :chartId="2" :label="'Overall Course Positive WordCloud'" />
        <p><strong>Overall Course Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col" v-if="courseSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordChart v-if="negativeCourseWordData.length > 0" :datasets="negativeCourseWordData" :chartId="3" :label="'Overall Course Negative WordCloud'" />
        <p><strong>Overall Course Negative WordCloud</strong></p>
      </div>

      <!-- Display Overall Instructor Sentiment -->
      <div class="col-12 col-md-6 dashboard mb-3 custom-col" v-if="instructorSpecific">
        <DoughnutChart v-if="sentimentData2.labelArray.length > 0 && sentimentData2.dataArray.length > 0"
          :datasets="sentimentData2" :chartId="1" />
        <p><strong>Overall Instructor Sentiment</strong></p>
      </div>
      <!-- Display Overall Instructor Positive WordCloud -->
      <div class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col" v-if="instructorSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordChart v-if="positiveInstructorWordData.length > 0" :datasets="positiveInstructorWordData" :chartId="4" :label="'Overall Instructor Positive WordCloud'" />
        <p><strong>Overall Instructor Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col" v-if="instructorSpecific">
        <!-- Include Word Cloud component here for negative feedback -->
        <WordChart v-if="negativeInstructorWordData.length > 0" :datasets="negativeInstructorWordData" :chartId="5" :label="'Overall Instructor Negative WordCloud'" />
        <p><strong>Overall Instructor Negative WordCloud</strong></p>
      </div>
    </div>
    
    <div class="row">
      <!-- Topic Modeling - Course Done Well / Contribution -->
      <div
        v-for="(topic, index) in courseDoneWellTopics"
        :key="index"
        class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for course done well topic -->
        <WordCloud :wordData="courseDoneWellTopics[index].wordData" />
        <p><strong>Overall Course Done Well - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Course Suggestions / Improve -->
      <div
        v-for="(topic, index) in courseSuggestionsTopics"
        :key="index"
        class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for course suggestions topic -->
        <WordCloud :wordData="courseSuggestionsTopics[index].wordData" />
        <p><strong>Overall Course Suggestions - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Instructor Done Well -->
      <div
        v-for="(topic, index) in instructorDoneWellTopics"
        :key="index"
        class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for instructor done well topic -->
        <WordCloud :wordData="instructorDoneWellTopics[index].wordData" />
        <p><strong>Overall Instructor Done Well - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Instructor Suggestions -->
      <div
        v-for="(topic, index) in instructorSuggestionsTopics"
        :key="index"
        class="col-12 col-md-6 dashboard pt-3 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for instructor suggestions topic -->
        <WordCloud :wordData="instructorSuggestionsTopics[index].wordData" />
        <p><strong>Overall Instructor Suggestions - Topic {{ index + 1 }}</strong></p>
      </div>
    </div>
  </div>
</template>

<script>
import WordCloud from "@/components/dashboard/WordCloud.vue";
import DashboardService from '@/api/services/dashboardService';
import DoughnutChart from "@/components/dashboard/DoughnutChart.vue";
import WordChart from "@/components/dashboard/WordChart.vue"
import UserService from "@/api/services/UserService.js";

export default {
  name: "ViewDashboard",
  components: {
    WordCloud,
    DoughnutChart,
    WordChart
  },
  data() {
    return {
      courseID: null,
      runcourseID: null,
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
      sentimentData1: {
        labelArray: [],
        dataArray: [],
        label: ""
      },
      sentimentData2: {
        labelArray: [],
        dataArray: [],
        label: ""
      }
    };
  },
  async created() {
    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);
    if (role != 'Admin') {
      this.$router.push({ name: 'proposeCourse' }); //need to change
    } else {
      document.title = "Feedback Analysis"; //need to change
      if (window.history.state.back === "/adminViewCourse") {
        this.courseID = this.$route.params.id;
        console.log(this.courseID);
      } else if (window.history.state.back === "/adminViewRunCourse") {
        this.runcourseID = this.$route.params.id;
        console.log(this.runcourseID);
      } 
      await this.fetchData();
    }
  },
  methods: {
    // Course Average Rating
      async fetchCourseAverageRating() {
        try {
          const response = await DashboardService.getCourseAverageRatings(null);
          // console.log(response)
          this.courseAverageRating = response.data.overall_average_rating; 
          this.totalNoOfFeedback = response.data.total_feedback;
          // console.log(this.courseAverageRating)
        } catch (error) {
          console.error('Error fetching courseDoneWellTopics:', error);
        }
      },
      // Instructor Average Rating
      async fetchInstructorAverageRating() {
        try {
          const response = await DashboardService.getInstructorAverageRatings(null);
          // console.log(response)
          this.instructorAverageRating = response.data.instructor_average_rating; 
          // console.log(this.instructorAverageRating)
        } catch (error) {
          console.error('Error fetching courseDoneWellTopics:', error);
        }
      },
      // Topic modeling for a particular course (done well)
      async fetchCourseDoneWellTopics() {
        try {
          const response = await DashboardService.getCourseDoneWellFeedback(null);
          
          this.courseDoneWellTopics = response.topic_words_list; 
          
        } catch (error) {
          console.error('Error fetching courseDoneWellTopics:', error);
        }
      },
      // Topic modeling for a particular course (improve)
      async fetchCourseImproveTopics() {
        try {
          const response = await DashboardService.getCourseImproveFeedback(null);
          
          this.courseSuggestionsTopics = response.topic_words_list; 
          
        } catch (error) {
          console.error('Error fetching courseSuggestionsTopics:', error);
        }
      },
      // Topic modeling for a particular course (done well)
      async fetchInstructorDoneWellTopics() {
        try {
          const response = await DashboardService.getInstructorDoneWellFeedback(null);
          console.log(response)
          this.instructorDoneWellTopics = response.topic_words_list; 
          
        } catch (error) {
          console.error('Error fetching instructorDoneWellTopics:', error);
        }
      },
      // Topic modeling for a particular course (improve)
      async fetchInstructorImproveTopics() {
        try {
          const response = await DashboardService.getInstructorImproveFeedback(null);
          console.log(response)
          this.instructorSuggestionsTopics = response.topic_words_list; 
          
        } catch (error) {
          console.error('Error fetching instructorSuggestionsTopics:', error);
        }
      },
    async fetchCourseSentimentData() {
      try {
        const response = await DashboardService.getCourseSentimentData(this.courseID, this.runcourseID);
        if(response.data.code === 200) {
          const { sentiment_labels, sentiment_percentages } = response.data;

          this.sentimentData1.labelArray = sentiment_labels;
          this.sentimentData1.dataArray = sentiment_percentages;
          this.sentimentData1.label = "Overall Course Sentiment";
        }

      } catch (error) {
        console.error("Error fetching course sentiment data: ", error);
      }
    },
    async fetchInstructorSentimentData() {
      try {
        const response = await DashboardService.getInstructorSentimentData(this.courseID, this.runcourseID);
        if (response.data.code === 200) {
          const { sentiment_labels, sentiment_percentages } = response.data;

          this.sentimentData2.labelArray = sentiment_labels;
          this.sentimentData2.dataArray = sentiment_percentages;
          this.sentimentData2.label = "Overall Instructor Sentiment";

          console.log(this.sentimentData2.dataArray)
        }

      } catch (error) {
        console.error("Error fetching instructor sentiment data: ", error);
      }
    },
    async fetchCourseWordcloudData() {
      try {
        const response = await DashboardService.getCourseWordcloudData(this.courseID, this.runcourseID);
        if (response.data.code === 200) {
          const { positive_word_data, negative_word_data } = response.data;

          this.positiveCourseWordData = positive_word_data;
          console.log(this.positiveCourseWordData)
          this.negativeCourseWordData = negative_word_data;
          console.log(this.positiveCourseWordData)
        }
      } catch (error) {
        console.error("Error fetching instructor feedbacks: ", error);
      }
    },
    async fetchInstructorWordcloudData() {
      try {
        const response = await DashboardService.getInstructorWordcloudData(this.courseID, this.runcourseID);
        console.log(response.data.code)
        if (response.data.code === 200) {
          const { positive_word_data, negative_word_data } = response.data;

          this.positiveInstructorWordData = positive_word_data;
          this.negativeInstructorWordData = negative_word_data;
        }
      } catch (error) {
        console.error("Error fetching instructor feedbacks: ", error);
      }
    },
    async fetchData() {
      await Promise.all([
        this.fetchCourseAverageRating(),
        this.fetchInstructorAverageRating(),
        this.fetchCourseDoneWellTopics(),
        this.fetchCourseSentimentData(),
        this.fetchInstructorSentimentData(),
        this.fetchCourseWordcloudData(),
        this.fetchInstructorWordcloudData(),
      ]);
    }
  },
  /*mounted() {
    this.fetchCourseAverageRating();
    this.fetchInstructorAverageRating();
    this.fetchCourseDoneWellTopics();
    this.fetchCourseSentimentData();
    this.fetchInstructorSentimentData();
    this.fetchCourseWordcloudData();
    this.fetchInstructorWordcloudData();
  }*/
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

.custom-col {
  background-color: white;
  border: none;
  border-radius: 10px;
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
