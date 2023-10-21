<template>
  <div class="container text-center">
    <h2 v-if="currentViewMode === 'analysis'">Feedback Analysis</h2>
    <h2 v-else>All Feedback Records</h2>
    <h4 class="mb-5 text-secondary" v-if="courseID">For {{courseName}}</h4>
    <h4 class="mb-5 text-secondary" v-else-if="runcourseID">For {{runcourseName}}</h4>
    <h4 class="mb-5 text-secondary" v-else></h4>

    <div class="container col-12 d-flex mt-3 mb-3 w-100 justify-content-between">
        <button class="btn btn-primary font-weight-bold" title="Toggle" @click="toggleViewMode">Toggle View</button>
        <button v-if="currentViewMode === 'analysis'" class="btn btn-primary font-weight-bold" title="Export" @click="exportToCSV">Export Analysis to PDF</button>
        <button v-if="currentViewMode === 'feedback'" class="btn btn-primary font-weight-bold" title="Export" @click="exportToCSV">Export Feedback to CSV</button>
    </div>
  </div>

  <div class="container text-center analysis-view" v-if="currentViewMode === 'analysis'">
    
    <!-- Ratings -->
    <div class="row">
      <!-- Display Total No. of Feedbacks -->
      <div class="col-12 col-md-4 dashboard pt-2 mb-3 custom-col">
        <h2 class="fs-1">{{totalNoOfFeedback}}</h2>
        <p><strong>Total No. of Feedbacks</strong></p>
      </div>
      <!-- Display Overall Average Course Ratings if not instructor-specific -->
      <div v-if="courseSpecific" class="col-12 col-md-4 pt-2 mb-3 dashboard custom-col">
        <h2 class="fs-1">{{courseAverageRating}} / 5</h2>
        <p><strong>Overall Average Course Ratings</strong></p>
      </div>
      <!-- Display Overall Average Instructor Ratings if not course-specific -->
      <div v-if="instructorSpecific" class="col-12 col-md-4 pt-2 mb-3 dashboard custom-col">
        <h2 class="fs-1">{{instructorAverageRating}} / 5</h2>
        <p><strong>Overall Average Instructor Ratings</strong></p>
      </div>
    </div>

    <!-- Sentiment Course -->
    <div class="row">
      <!-- Display Overall Course Sentiment -->
      <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col" v-if="courseSpecific">
        <DoughnutChart v-if="sentimentData1.labelArray.length > 0 && sentimentData1.dataArray.length > 0"
          :datasets="sentimentData1" :chartId="0" />
        <p><strong>Overall Course Sentiment</strong></p>
      </div>
      <!-- Display Overall Course Positive WordCloud -->
      <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col" v-if="courseSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordChart v-if="positiveCourseWordData.length > 0" :datasets="positiveCourseWordData" :chartId="2" :label="'Overall Course Positive WordCloud'" />
        <p><strong>Overall Course Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col" v-if="courseSpecific">
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
      <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col" v-if="instructorSpecific">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordChart v-if="positiveInstructorWordData.length > 0" :datasets="positiveInstructorWordData" :chartId="4" :label="'Overall Instructor Positive WordCloud'" />
        <p><strong>Overall Instructor Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col" v-if="instructorSpecific">
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
        class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for course done well topic -->
        <!-- <WordCloud :wordData="courseDoneWellTopics[index].wordData" /> -->
        <WordChart v-if="courseDoneWellTopics.length > 0" :datasets="courseDoneWellTopics[index].wordData" :chartId="6 + index" :label="'Overall Course Done Well'" />
        <p><strong>Overall Course Done Well - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Course Suggestions / Improve -->
      <div
        v-for="(topic, index) in courseSuggestionsTopics"
        :key="index"
        class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for course suggestions topic -->
        <!-- <WordCloud :wordData="courseSuggestionsTopics[index].wordData" /> -->
        <WordChart v-if="courseSuggestionsTopics.length > 0" :datasets="courseSuggestionsTopics[index].wordData" :chartId="15 + index" :label="'Overall Course Suggestions'" />
        <p><strong>Overall Course Suggestions - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Instructor Done Well -->
      <div
        v-for="(topic, index) in instructorDoneWellTopics"
        :key="index"
        class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for instructor done well topic -->
        <!-- <WordCloud :wordData="instructorDoneWellTopics[index].wordData" /> -->
        <WordChart v-if="instructorDoneWellTopics.length > 0" :datasets="instructorDoneWellTopics[index].wordData" :chartId="24 + index" :label="'Overall Instructor Done Well'" />
        <p><strong>Overall Instructor Done Well - Topic {{ index + 1 }}</strong></p>
      </div>

      <!-- Topic Modeling - Instructor Suggestions -->
      <div
        v-for="(topic, index) in instructorSuggestionsTopics"
        :key="index"
        class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col"
      >
        <!-- Include Word Cloud component here for instructor suggestions topic -->
        <!-- <WordCloud :wordData="instructorSuggestionsTopics[index].wordData" /> -->
        <WordChart v-if="instructorSuggestionsTopics.length > 0" :datasets="instructorSuggestionsTopics[index].wordData" :chartId="33 + index" :label="'Overall Instructor Suggestions'" />
        <p><strong>Overall Instructor Suggestions - Topic {{ index + 1 }}</strong></p>
      </div>
    </div>
  </div>

  <div class="feedback-view" v-else>
    <div class="container col-12">

      <div  v-if="feedbackData && feedbackData.length > 0" class="table-responsive rounded">
        <table class="table bg-white">
          <thead>
            <tr>
              <th scope="col" v-for="(question, index) in questions" :key="index" class="table-column text-nowrap">
                <div class="question-container">
                  {{ question.question }}
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(answers, index) in displayedCourses" :key="index">
              <td v-for="(answer, aIndex) in answers" :key="aIndex">{{ answer }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="courseID === null && runcourseID === null">
        <p class="text-center">Please filter to view the respective feedback records. </p>
      </div>

      <div v-else-if="feedbackData=[]">
        <p class="text-center">No records found</p>
      </div>
      
    </div>
    <vue-awesome-paginate v-if="feedbackData.length/itemsPerPage > 0" v-model="localCurrentPageCourses" :totalItems="feedbackData.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeCourses" class="justify-content-center pagination-container"/>
    
  </div>
</template>

<script>
import DashboardService from '@/api/services/dashboardService';
import DoughnutChart from "@/components/dashboard/DoughnutChart.vue";
import WordChart from "@/components/dashboard/WordChart.vue"
import UserService from "@/api/services/UserService.js";
import CourseService from "@/api/services/CourseService.js";
import RunCourseService from "@/api/services/runCourseService.js";
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import Papa from 'papaparse';
import FeedbackService from "@/api/services/FeedbackService.js";

export default {
  name: "ViewDashboard",
  components: {
    DoughnutChart,
    WordChart,
    VueAwesomePaginate
  },
  data() {
    return {
      courseID: null,
      courseName: "",
      runcourseID: null,
      runcourseName: "",
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
      },
      questions: [],
      feedbackData: [],
      itemsPerPage: 10,
      localCurrentPageCourses: 1,
      currentViewMode: 'analysis',
    };
  },
  async created() {
    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);
    console.log(role)
    if (role !== 'Admin' && role !== 'Trainer' && role !== 'Instructor') {
      this.$router.push({ name: 'proposeCourse' }); //need to change
    } else {
      document.title = "Feedback Analysis"; //need to change
      if (window.history.state.back === "/adminViewCourse") {
        this.courseID = this.$route.params.id;
        console.log(this.courseID);
      } else if (window.history.state.back === "/adminViewRunCourse") {
        this.runcourseID = this.$route.params.id;
        console.log(this.runcourseID);
      } else if (window.history.state.back && window.history.state.back.startsWith("/adminViewCourseRun/")) {
        this.runcourseID = this.$route.params.id;
        console.log(this.runcourseID);
      } else if (window.history.state.back === "/instructorTrainerViewProfile") {
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
          const response = await DashboardService.getCourseAverageRatings(this.courseID, this.runcourseID);
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
          const response = await DashboardService.getInstructorAverageRatings(this.courseID, this.runcourseID);
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
          const response = await DashboardService.getCourseDoneWellFeedback(this.courseID, this.runcourseID);
          
          this.courseDoneWellTopics = response.topic_words_list; 
          
        } catch (error) {
          console.error('Error fetching courseDoneWellTopics:', error);
        }
      },
      // Topic modeling for a particular course (improve)
      async fetchCourseImproveTopics() {
        try {
          const response = await DashboardService.getCourseImproveFeedback(this.courseID, this.runcourseID);
          
          this.courseSuggestionsTopics = response.topic_words_list; 
          
        } catch (error) {
          console.error('Error fetching courseSuggestionsTopics:', error);
        }
      },
      // Topic modeling for a particular instructor (done well)
      async fetchInstructorDoneWellTopics() {
        try {
          // course
          const response = await DashboardService.getInstructorDoneWellFeedback(this.courseID, this.runcourseID);
          // console.log(response)
          this.instructorDoneWellTopics = response.topic_words_list; 
          
        } catch (error) {
          console.error('Error fetching instructorDoneWellTopics:', error);
        }
      },
      // Topic modeling for a particular instructor (improve)
      async fetchInstructorImproveTopics() {
        try {
          // course
          const response = await DashboardService.getInstructorImproveFeedback(this.courseID, this.runcourseID);
          // console.log(response)
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

          console.log(this.sentimentData1.dataArray)
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

          // console.log(this.sentimentData2.dataArray)
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
          // console.log(this.positiveCourseWordData)
          this.negativeCourseWordData = negative_word_data;
          // console.log(this.positiveCourseWordData)
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
    async fetchCourseName() {
      const coursename = await CourseService.getCourseName(this.courseID)
      this.courseName = coursename.data
    },
    async fetchRunCourseName() {
      const runcoursename = await RunCourseService.getRunCourseName(this.runcourseID)
      this.runcourseName = runcoursename.data
    },
    async fetchCourseFeedbackData() {
      try {
        const feedbackForCourse = await FeedbackService.getFeedbackForRunCourse(this.courseID, this.runcourseID);
        if (feedbackForCourse.code == 200) {
          this.questions = feedbackForCourse.questions
          this.feedbackData = feedbackForCourse.data.map(item => item.answers);
        }
        
      } catch (error) {
        console.error(error);
      }
    },
    handlePageChangeCourses(newPage) {
      this.localCurrentPageCourses = newPage;
      this.$emit('page-change', newPage);
    },
    exportToCSV() {
      // Prepare the CSV data with questions as the first row
      const csvData = [this.questions.map(question => question.question)];

      // Add the data rows
      csvData.push(...this.feedbackData.map(row => row.map(cell => cell.toString())));

      // Create a CSV string using Papaparse
      const csv = Papa.unparse(csvData);

      // Create a Blob and download link
      const blob = new Blob([csv], { type: 'text/csv' });

      // Set the file name to the course name
      let courseName; 
      if (this.courseID) {
        courseName = this.courseName;
      } else {
        courseName = this.runcourseName;
      }

     
      const fileName = `${courseName}_feedback_data.csv`;

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName; // Set the file name here
      a.click();
      URL.revokeObjectURL(url);
    },
    toggleViewMode() {
      this.currentViewMode = this.currentViewMode === 'analysis' ? 'feedback' : 'analysis';
    },
    async fetchData() {
      // Create an array of promises to fetch data
      const dataPromises = [
        this.fetchCourseAverageRating(),
        this.fetchInstructorAverageRating(),
        this.fetchCourseDoneWellTopics(),
        this.fetchCourseImproveTopics(),
        this.fetchInstructorDoneWellTopics(),
        this.fetchInstructorImproveTopics(),
        this.fetchCourseSentimentData(),
        this.fetchInstructorSentimentData(),
        this.fetchCourseWordcloudData(),
        this.fetchInstructorWordcloudData(),
        this.fetchCourseName(),
        this.fetchRunCourseName(),
      ];

      // Conditionally add the promise for fetching feedback data
      if (this.courseID || this.runcourseID) {
        dataPromises.push(this.fetchCourseFeedbackData());
      }

      // Wait for all promises to resolve
      await Promise.all(dataPromises);
    }
  },
  computed: {
    displayedCourses() {
      const startIndex = (this.localCurrentPageCourses - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.feedbackData.slice(startIndex, endIndex);
    },
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

.table th .question-container {
    width: 300px;
    max-width: 300px !important;
    white-space: normal;
    overflow: hidden;
  } 

  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>
