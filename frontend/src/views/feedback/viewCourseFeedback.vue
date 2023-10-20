<template>
  <div>
    <div class="container col-12">
      <div class="container col-12 d-flex mb-3 w-100">
        <h5 class="col m-auto">All Feedback for {{coursename}}</h5>
        <div>
          <button class="btn btn-primary me-2" title="View Analysis">View Analysis</button>
          <button class="btn btn-primary" title="Export" @click="exportToCSV">Export to CSV</button>
        </div>
        
      </div>

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
      <div v-else-if="feedbackData=[]">
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-if="feedbackData.length/itemsPerPage > 0" v-model="localCurrentPageCourses" :totalItems="feedbackData.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeCourses" class="justify-content-center pagination-container"/>
    
  </div>

</template>
  
<script>
import FeedbackService from "@/api/services/FeedbackService.js";
import CourseService from "@/api/services/CourseService.js";
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import Papa from 'papaparse';

export default {
    components: {
      VueAwesomePaginate
    },
    data() {
        return {
          coursename:"",
          questions: [],
          feedbackData: [],
          itemsPerPage: 10,
          localCurrentPageCourses: 1,
        }
    },
    mounted() {
        this.fetchCourseFeedbackData();
    },
    methods: {
        async fetchCourseFeedbackData() {
            try {
              const course_id = this.$route.params.id
              const feedbackForCourse = await FeedbackService.getFeedbackForCourse(course_id);
              if (feedbackForCourse.code == 200) {
                this.questions = feedbackForCourse.questions
                this.feedbackData = feedbackForCourse.data.map(item => item.answers);
              }
                         
              const course_Name = await CourseService.getCourseName(course_id);
              this.coursename = course_Name.data
                
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
          const courseName = this.coursename;
          const fileName = `${courseName}_feedback_data.csv`;

          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = fileName; // Set the file name here
          a.click();
          URL.revokeObjectURL(url);
        },

    }, 
    computed: {
      displayedCourses() {
        const startIndex = (this.localCurrentPageCourses - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.feedbackData.slice(startIndex, endIndex);
      },
    }

}

</script>

<style scoped>

  .table th .question-container {
    width: 300px;
    max-width: 300px !important;
    white-space: normal;
    overflow: hidden;
  } 

  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';

</style>