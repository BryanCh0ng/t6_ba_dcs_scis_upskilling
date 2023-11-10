<template>
  <div>
    <div class="container text-center pt-5">
      <h2 v-if="currentViewMode === 'analysis'">Feedback Analysis</h2>
      <h2 v-else>All Feedback Records</h2>
      <div class="mb-5">
        <h4 class="text-secondary" v-if="currentPage === 'course' || courseName !== ''">For {{ courseName }}</h4>
        <h4 class="text-secondary" v-if="currentPage === 'runcourse' || runcourseName !== ''">For {{ runcourseName }}</h4>
        <h4 class="text-secondary" v-if="currentPage === 'coach' || instructorName !== ''">For {{ instructorName }}</h4>
      </div>

      <div class="container col-12 d-flex mt-3 mb-3 w-100 justify-content-between">
        <div class="d-flex">
          <button class="btn btn-primary font-weight-bold" title="Toggle" @click="toggleViewMode">Toggle View</button>
        </div>
        <div class="d-flex">
          <button v-if="currentPage !== 'runcourse'" class="btn btn-primary font-weight-bold me-2" title="Filter"
            @click="openModal">Filter</button>
          <button v-if="currentViewMode === 'analysis'" class="btn btn-primary font-weight-bold" title="Export to PDF"
            @click="exportToPDF">Export Analysis to PDF</button>
          <button v-if="currentViewMode === 'feedback'" class="btn btn-primary font-weight-bold" title="Export to CSV"
            @click="exportToCSV">Export Feedback to CSV</button>
        </div>
      </div>
    </div>

    <div class="container text-center analysis-view" v-if="currentViewMode === 'analysis'" ref="analysisView">

      <!-- Ratings -->
      <div class="row page-break">
        <!-- Display Total No. of Feedbacks -->
        <div class="col-12 col-md-4 dashboard pt-2 mb-3 custom-col">
          <h2 class="fs-1">{{ totalNoOfFeedback }}</h2>
          <p><strong>Total No. of Feedbacks</strong></p>
        </div>
        <!-- Display Overall Average Course Ratings if not instructor-specific -->
        <div v-if="courseSpecific" class="col-12 col-md-4 pt-2 mb-3 dashboard custom-col">
          <h2 class="fs-1">{{ courseAverageRating }} / 5</h2>
          <p><strong>Overall Average Course Ratings</strong></p>
        </div>
        <!-- Display Overall Average Instructor Ratings if not course-specific -->
        <div v-if="instructorSpecific" class="col-12 col-md-4 pt-2 mb-3 dashboard custom-col">
          <h2 class="fs-1">{{ instructorAverageRating }} / 5</h2>
          <p><strong>Overall Average Instructor Ratings</strong></p>
        </div>
      </div>

      <!-- Sentiment Course -->
      <div class="row">
        <!-- Display Overall Course Sentiment -->
        <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break" v-if="courseSpecific">
          <template v-if="sentimentData1.labelArray.length > 0 && sentimentData1.dataArray.length > 0">
            <DoughnutChart :datasets="sentimentData1" />
          </template>
          <template v-else>
            <NoDataDisplay :displayMessage="filterSelected" />
          </template>
          <p><strong>Overall Course Sentiment</strong></p>
        </div>
        <!-- Display Overall Course Positive WordCloud -->
        <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break" v-if="courseSpecific">
          <template v-if="positiveCourseWordData.length > 0">
            <WordChart :datasets="positiveCourseWordData" :label="'Overall Course Positive WordCloud'"
              :fit="coursePositive" />
          </template>
          <template v-else>
            <NoDataDisplay :displayMessage="filterSelected" />
          </template>
          <p><strong>Overall Course Positive WordCloud</strong></p>
        </div>
        <!-- Display Overall Course Negative WordCloud -->
        <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break" v-if="courseSpecific">
          <template v-if="negativeCourseWordData.length > 0">
            <WordChart :datasets="negativeCourseWordData" :label="'Overall Course Negative WordCloud'"
              :fit="courseNegative" />
          </template>
          <template v-else>
            <NoDataDisplay :displayMessage="filterSelected" />
          </template>
          <p><strong>Overall Course Negative WordCloud</strong></p>
        </div>

        <!-- Display Overall Instructor Sentiment -->
        <div class="col-12 col-md-6 dashboard mb-3 custom-col page-break" v-if="instructorSpecific">
          <template v-if="sentimentData2.labelArray.length > 0 && sentimentData2.dataArray.length > 0">
            <DoughnutChart :datasets="sentimentData2" />
          </template>
          <template v-else>
            <NoDataDisplay :displayMessage="filterSelected" />
          </template>
          <p><strong>Overall Instructor Sentiment</strong></p>
        </div>
        <!-- Display Overall Instructor Positive WordCloud -->
        <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break" v-if="instructorSpecific">
          <template v-if="positiveInstructorWordData.length > 0">
            <WordChart :datasets="positiveInstructorWordData" :label="'Overall Instructor Positive WordCloud'"
              :fit="instructorPositive" />
          </template>
          <template v-else>
            <NoDataDisplay :displayMessage="filterSelected" />
          </template>
          <p><strong>Overall Instructor Positive WordCloud</strong></p>
        </div>
        <!-- Display Overall Course Negative WordCloud -->
        <div class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break" v-if="instructorSpecific">
          <template v-if="negativeInstructorWordData.length > 0">
            <WordChart :datasets="negativeInstructorWordData" :label="'Overall Instructor Negative WordCloud'"
              :fit="instructorNegative" />
          </template>
          <template v-else>
            <NoDataDisplay :displayMessage="filterSelected" />
          </template>
          <p><strong>Overall Instructor Negative WordCloud</strong></p>
        </div>
      </div>

      <div class="row">
        <!-- Topic Modeling - Course Done Well / Contribution -->
        <div v-for="(topic, index) in courseDoneWellTopics" :key="index"
          class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break">
          <!-- Include Word Cloud component here for course done well topic -->
          <!-- <WordCloud :wordData="courseDoneWellTopics[index].wordData" /> -->
          <WordChart v-if="courseDoneWellTopics.length > 0" :datasets="courseDoneWellTopics[index].wordData"
            :label="'Overall Course Done Well'" :size1="13" :size2="15" :fit="false" />
          <p><strong>Overall Course Done Well - {{ getFirstWord(topic) }}</strong></p>
        </div>

        <!-- Topic Modeling - Course Suggestions / Improve -->
        <div v-for="(topic, index) in courseSuggestionsTopics" :key="index"
          class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break">
          <!-- Include Word Cloud component here for course suggestions topic -->
          <!-- <WordCloud :wordData="courseSuggestionsTopics[index].wordData" /> -->
          <WordChart v-if="courseSuggestionsTopics.length > 0" :datasets="courseSuggestionsTopics[index].wordData"
            :label="'Overall Course Suggestions'" :size1="13" :size2="15" :fit="false" />
          <p><strong>Overall Course Suggestions - {{ getFirstWord(topic) }}</strong></p>
        </div>

        <!-- Topic Modeling - Instructor Done Well -->
        <div v-for="(topic, index) in instructorDoneWellTopics" :key="index"
          class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break">
          <!-- Include Word Cloud component here for instructor done well topic -->
          <!-- <WordCloud :wordData="instructorDoneWellTopics[index].wordData" /> -->
          <WordChart v-if="instructorDoneWellTopics.length > 0" :datasets="instructorDoneWellTopics[index].wordData"
            :label="'Overall Instructor Done Well'" :size1="13" :size2="15" :fit="false" />
          <p><strong>Overall Instructor Done Well - {{ getFirstWord(topic) }}</strong></p>
        </div>

        <!-- Topic Modeling - Instructor Suggestions -->
        <div v-for="(topic, index) in instructorSuggestionsTopics" :key="index"
          class="col-12 col-md-6 dashboard pt-2 mb-3 custom-col page-break">
          <!-- Include Word Cloud component here for instructor suggestions topic -->
          <!-- <WordCloud :wordData="instructorSuggestionsTopics[index].wordData" /> -->
          <WordChart v-if="instructorSuggestionsTopics.length > 0" :datasets="instructorSuggestionsTopics[index].wordData"
            :label="'Overall Instructor Suggestions'" :size1="13" :size2="15" :fit="false" />
          <p><strong>Overall Instructor Suggestions - {{ getFirstWord(topic) }}</strong></p>
        </div>
      </div>
    </div>

    <div class="feedback-view" v-else>
      <div class="container col-12">

        <div v-if="feedbackData && feedbackData.length > 0" class="table-responsive rounded">
          <table class="table bg-white">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col" v-for="(question, index) in header" :key="index" class="table-column text-nowrap">
                  <div class="question-container">
                    {{ question }}
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(answerSet, index) in displayedCourses" :key="index">
                <th scope="row">{{ (localCurrentPageCourses - 1) * itemsPerPage + index + 1 }}</th>
                <td v-for="(answer, rowIndex) in answerSet" :key="rowIndex">
                  {{ answer }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!--<div v-else-if="courseID === null && runcourseID === null">
          <p class="text-center">Please filter to view the respective feedback records. </p>
        </div>-->

        <div v-else-if="feedbackData = []">
          <p class="text-center">No records found</p>
          <p v-if="filterSelected" class="text-center">Please make a different filter selection</p>
        </div>

      </div>

      <vue-awesome-paginate v-if="feedbackData.length / itemsPerPage > 0" v-model="localCurrentPageCourses"
        :totalItems="feedbackData.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeCourses"
        class="justify-content-center pagination-container" />

    </div>

    <FilterModal :visible="showAlert" :currentPage="currentPage" @modal-closed="handleModalClosed" @apply-filters="updateVisualizations" />
  </div>
</template>

<script>
import UserService from "@/api/services/UserService.js";
import DashboardService from '@/api/services/dashboardService';
import DoughnutChart from "@/components/dashboard/DoughnutChart.vue";
import WordChart from "@/components/dashboard/WordChart.vue"
import Papa from 'papaparse';
import FeedbackService from "@/api/services/FeedbackService.js";
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import html2pdf from 'html2pdf.js';
import FilterModal from "@/components/dashboard/FilterModal.vue";
import NoDataDisplay from '@/components/dashboard/NoDataDisplay.vue';

export default {
  name: "ViewDashboard",
  components: {
    DoughnutChart,
    WordChart,
    VueAwesomePaginate,
    FilterModal,
    NoDataDisplay
  },
  data() {
    return {
      instructorSpecific: true,
      courseSpecific: true,
      currentPage: "",
      courseID: null,
      courseIDs: [],
      runcourseID: null,
      runcourseIDs: [],
      coachesID: null,
      coachesIDs: [],
      courseName: "",
      runcourseName: "",
      instructorName: "",
      coursecatIDs: [],
      startDate: null,
      endDate: null,
      totalNoOfFeedback: null,
      courseAverageRating: null,
      instructorAverageRating: null,
      courseDoneWellTopics: [],
      courseSuggestionsTopics: [],
      instructorDoneWellTopics: [],
      instructorSuggestionsTopics: [],
      sentimentData1: {
        labelArray: [],
        dataArray: [],
        label: ""
      },
      filterSelected: false,
      sentimentData2: {
        labelArray: [],
        dataArray: [],
        label: ""
      },
      coursePositive: true,
      courseNegative: true,
      positiveCourseWordData: [],
      negativeCourseWordData: [],
      instructorPositive: true,
      instructorNegative: true,
      positiveInstructorWordData: [],
      negativeInstructorWordData: [],
      currentViewMode: 'analysis',
      header: [],
      feedbackData: [],
      localCurrentPageCourses: 1,
      showAlert: false,
      itemsPerPage: 10
    };
  },
  async created() {
    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);

    if (role !== 'Admin' && role !== 'Trainer' && role !== 'Instructor') {
      this.$router.push({ name: 'studentViewCourse' }); //need to change
    } else {
      const url = window.location.pathname;
      const parts = url.split("/"); // Split the URL by "/"
      const lastPart = parts[parts.length - 1]; // Get the last element of the array

      document.title = "Feedback Analysis"; //need to change

      if (window.history.state.back === "/adminViewCourse") {
        this.currentPage = "course";
        this.courseID = this.$route.params.id;
        this.courseIDs.push(parseInt(this.$route.params.id));
        this.courseIDs = JSON.stringify(this.courseIDs);
      } else if (window.history.state.back === "/adminViewRunCourse") {
        this.currentPage = "runcourse";
        this.runcourseID = this.$route.params.id;
        this.runcourseIDs.push(parseInt(this.$route.params.id));
        this.runcourseIDs = JSON.stringify(this.runcourseIDs);
      } else if (window.history.state.back && window.history.state.back.startsWith("/adminViewCourseRun/")) {
        this.currentPage = "runcourse";
        this.runcourseID = this.$route.params.id;
        this.runcourseIDs.push(parseInt(this.$route.params.id));
        this.runcourseIDs = JSON.stringify(this.runcourseIDs);
      } else if (window.history.state.back === "/adminViewManagement") {
        this.currentPage = "coach";
        this.coachesID = this.$route.params.id;
        this.coachesIDs.push(parseInt(this.$route.params.id));
        this.coachesIDs = JSON.stringify(this.coachesIDs);
      } else if ((lastPart === "viewDashboard" && (role === "Trainer" || role === "Instructor"))) {
        this.currentPage = "coach";
        this.coachesID = user_ID;
        this.coachesIDs.push(parseInt(user_ID));
        this.coachesIDs = JSON.stringify(this.coachesIDs);
      }
      await this.fetchData();
    }
  },
  methods: {
    async fetchCourseName() {
      if (this.courseID !== []) {
        const coursenames = await DashboardService.getFilteredCoursesName(this.courseIDs)
        if (coursenames.data.length > 5) {
          this.courseName = ""
        } else {
          this.courseName = coursenames.data.join(", ");
        }
      } 
    },
    async fetchRunCourseName() {
      if (this.runcourseIDs !== []) {
        const runcoursenames = await DashboardService.getFilteredRunCoursesName(this.runcourseIDs)
        if (runcoursenames.data.length > 5) {
          this.runcourseName = ""
        } else {
          this.runcourseName = runcoursenames.data.join(", ");
        }
      } 
    },
    async fetchInstructorName() {
      if (this.coachesIDs.length !== []) {
        const instructorNames = await DashboardService.getFilteredCoachesName(this.coachesIDs)
        if (instructorNames.data.length > 5) {
          this.instructorName = ""
        } else {
          this.instructorName = instructorNames.data.join(", ");
        }
      }
    },
    //Total Feedbacks 
    async fetchTotalFeedbacks() {
      try {
        const response = await DashboardService.getTotalFeedbacks(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        this.totalNoOfFeedback = response.data.total_feedbacks;
      } catch (error) {
        console.error('Error fetching total number of feedbacks: ', error);
      }
    },
    // Course Average Rating
    async fetchCourseAverageRating() {
      try {
        const response = await DashboardService.getCourseAverageRatings(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        this.courseAverageRating = response.data.overall_average_rating;
        //this.totalNoOfFeedback = response.data.total_feedbacks;
      } catch (error) {
        console.error('Error fetching overall average course ratings: ', error);
      }
    },
    // Instructor Average Rating
    async fetchInstructorAverageRating() {
      try {
        const response = await DashboardService.getInstructorAverageRatings(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        this.instructorAverageRating = response.data.overall_average_rating;
      } catch (error) {
        console.error('Error fetching overall average instructor ratings: ', error);
      }
    },
    // Topic modeling for a particular course (done well)
    async fetchCourseDoneWellTopics() {
      try {
        const response = await DashboardService.getCourseDoneWellFeedback(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);

        this.courseDoneWellTopics = response.topic_words_list;

      } catch (error) {
        console.error('Error fetching courseDoneWellTopics:', error);
      }
    },
    // Topic modeling for a particular course (improve)
    async fetchCourseImproveTopics() {
      try {
        const response = await DashboardService.getCourseImproveFeedback(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);

        this.courseSuggestionsTopics = response.topic_words_list;

      } catch (error) {
        console.error('Error fetching courseSuggestionsTopics:', error);
      }
    },
    // Topic modeling for a particular instructor (done well)
    async fetchInstructorDoneWellTopics() {
      try {
        // course
        const response = await DashboardService.getInstructorDoneWellFeedback(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
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
        const response = await DashboardService.getInstructorImproveFeedback(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        // console.log(response)
        this.instructorSuggestionsTopics = response.topic_words_list;

      } catch (error) {
        console.error('Error fetching instructorSuggestionsTopics:', error);
      }
    },
    //Overall Course Sentiment
    async fetchCourseSentimentData() {
      try {
        const response = await DashboardService.getCourseSentimentData(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);

        if (response.data.code === 200) {
          const { sentiment_labels, sentiment_percentages } = response.data;

          this.sentimentData1.labelArray = sentiment_labels;
          this.sentimentData1.dataArray = sentiment_percentages;
          this.sentimentData1.label = "Overall Course Sentiment";

          this.filterSelected = false;
        }

        if (response.data.code === 400) {
          this.sentimentData1.labelArray = [];
          this.sentimentData1.dataArray = [];
        }
      } catch (error) {
        console.error("Error fetching course sentiment data: ", error);
      }
    },
    //Overall Instructor Sentiment
    async fetchInstructorSentimentData() {
      try {
        const response = await DashboardService.getInstructorSentimentData(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        if (response.data.code === 200) {
          const { sentiment_labels, sentiment_percentages } = response.data;

          this.sentimentData2.labelArray = sentiment_labels;
          this.sentimentData2.dataArray = sentiment_percentages;
          this.sentimentData2.label = "Overall Instructor Sentiment";

          this.filterSelected = false;

          // console.log(this.sentimentData2.dataArray)
        }

        if (response.data.code === 400) {
          this.sentimentData2.labelArray = [];
          this.sentimentData2.dataArray = [];
        }

      } catch (error) {
        console.error("Error fetching instructor sentiment data: ", error);
      }
    },
    //Overall Course Positive and Negative WordCloud
    async fetchCourseWordcloudData() {
      try {
        const response = await DashboardService.getCourseWordcloudData(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        if (response.data.code === 200) {
          const { positive_word_data, negative_word_data } = response.data;

          if (response.data.positive_word_data.length <= 35) {
            this.coursePositive = false;
          } else {
            this.coursePositive = true;
          }

          if (response.data.negative_word_data.length <= 35) {
            this.courseNegative = false;
          } else {
            this.courseNegative = true;
          }

          this.positiveCourseWordData = positive_word_data;
          //console.log(this.positiveCourseWordData)
          this.negativeCourseWordData = negative_word_data;
          //console.log(this.negativeCourseWordData)

          this.filterSelected = false;
        }

        if (response.data.code === 400) {
          this.positiveCourseWordData = [];
          this.negativeCourseWordData = [];
        }
      } catch (error) {
        console.error("Error fetching instructor feedbacks: ", error);
      }
    },
    //Overall Instructor Positive and Negative WordCloud
    async fetchInstructorWordcloudData() {
      try {
        const response = await DashboardService.getInstructorWordcloudData(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        //console.log(response.data)
        if (response.data.code === 200) {
          const { positive_word_data, negative_word_data } = response.data;

          if (response.data.positive_word_data.length <= 35) {
            this.instructorPositive = false;
          } else {
            this.instructorPositive = true;
          }

          if (response.data.negative_word_data.length <= 35) {
            this.instructorNegative = false;
          } else {
            this.instructorNegative = true;
          }

          this.positiveInstructorWordData = positive_word_data;
          //console.log(this.positiveInstructorWordData)
          this.negativeInstructorWordData = negative_word_data;
          //console.log(this.negativeInstructorWordData)

          this.filterSelected = false;
        }

        if (response.data.code === 400) {
          this.positiveInstructorWordData = [];
          this.negativeInstructorWordData = [];
        }
      } catch (error) {
        console.error("Error fetching instructor feedbacks: ", error);
      }
    },
    getFirstWord(topic) {
      return topic.wordData[0].word;
    },
    toggleViewMode() {
      this.currentViewMode = this.currentViewMode === 'analysis' ? 'feedback' : 'analysis';
    },
    //All Feedback Records
    async fetchCourseFeedbackData() {
      try {
        const feedbackForCourse = await FeedbackService.getFeedback(this.courseIDs, this.coursecatIDs, this.runcourseIDs, this.coachesIDs, this.startDate, this.endDate);
        if (feedbackForCourse.data.code == 200) {
          this.header = feedbackForCourse.data.header
          this.feedbackData = feedbackForCourse.data.answers;

          // Log the length of each element in feedbackData
          /*this.feedbackData.forEach(answerSet => {
            console.log('Length of answerSet:', answerSet.length);
          });*/

          this.filterSelected = false;
        }

        if (feedbackForCourse.data.code == 400) {
          this.feedbackData = [];
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
      const csvData = [];

      csvData.push(this.header);

      // Add the data rows
      csvData.push(...this.feedbackData.map(row => row.map(cell => cell.toString())));

      // Create a CSV string using Papaparse
      const csv = Papa.unparse(csvData);

      // Create a Blob and download link
      const blob = new Blob([csv], { type: 'text/csv' });

      let names = [this.courseName, this.runcourseName, this.instructorName].filter(Boolean);
      let startOfFileName = names.length > 0 ? names.join('_') : 'Overall';

      const fileName = `${startOfFileName}_feedback_data.csv`;

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      a.click();
      URL.revokeObjectURL(url);
    },
    exportToPDF() {
      try {
        const container = this.$refs.analysisView;

        let names = [this.courseName, this.runcourseName, this.instructorName].filter(Boolean);
        let startOfFileName = names.length > 0 ? names.join('_') : 'Overall';

        const fileName = `${startOfFileName}_feedback_analysis.pdf`;

        const options = {
          margin: 5,
          filename: fileName,
          image: { type: 'jpeg', quality: 1 },
          html2canvas: { scale: 1 },
          jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
          pagebreak: { before: '.page-break:nth-child(3n)' },
        };

        const pdf = html2pdf().from(container).set(options).outputPdf();

        pdf.save();
      } catch (error) {
        console.error("Error exporting to PDF:", error);
      }
    },
    openModal() {
      this.showAlert = !this.showAlert;
    },
    handleModalClosed(value) {
      this.showAlert = value;
    },
    async fetchData() {
      // Create an array of promises to fetch data
      const dataPromises = [
        this.fetchCourseName(),
        this.fetchRunCourseName(),
        this.fetchInstructorName(),
        this.fetchTotalFeedbacks(),
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
        this.fetchCourseFeedbackData()
      ];

      // Conditionally add the promise for fetching feedback data
      if (this.courseID || this.runcourseID) {
        dataPromises.push(this.fetchCourseFeedbackData());
      }

      // Wait for all promises to resolve
      await Promise.all(dataPromises);
    },
    formatDateToYYYYMMDD(dateObj) {
      const parsedYear = dateObj.getFullYear();
      const parsedMonth = dateObj.getMonth() + 1;
      const parsedDay = dateObj.getDate();
      return `${parsedYear}-${parsedMonth}-${parsedDay}`;
    },
    async updateVisualizations(filters) {
      const {
        courses,
        coursecats,
        runcourses,
        coaches,
        startDate,
        endDate
      } = filters;

      if (this.currentPage !== "course") {
        this.courseIDs = JSON.stringify(courses)
      }

      if (this.currentPage !== "coach") {
        this.coachesIDs = JSON.stringify(coaches)
      }

      this.coursecatIDs = JSON.stringify(coursecats)
      this.runcourseIDs = JSON.stringify(runcourses)

      if (startDate && endDate) {
        this.startDate = this.formatDateToYYYYMMDD(startDate);
        this.endDate = this.formatDateToYYYYMMDD(endDate);
      } else {
        this.startDate = startDate;
        this.endDate = endDate;
      }

      this.filterSelected = true;

      this.fetchData();
    },
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
