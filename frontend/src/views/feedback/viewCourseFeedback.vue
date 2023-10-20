<template>
  <div>
    <div class="container col-12">
      <div class="container col-12 d-flex mb-3 w-100">
        <h5 class="col m-auto">All Feedback for {{coursename}}</h5>
        <button class="btn btn-primary" title="Export">Export</button>
      </div>

      <div  v-if="feedbackData && feedbackData.length > 0" class="table-responsive rounded">
        <table class="table bg-white">
          <thead>
            <tr>
              <th scope="col" v-for="(question, index) in questions" :key="index" class="table-column custom-col">
                {{ question.question }}
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

  .table-responsive .table th.table-column {
    width: 50px !important;
  } 

  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';

</style>