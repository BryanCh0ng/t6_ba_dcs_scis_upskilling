<template>
  <div>
    <div class="container col-12">
      <h5 class="pb-3">All Feedback for {{run_name}}</h5>
      <div  v-if="feedbackData && feedbackData.length > 0" class="table-responsive">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
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
import { VueAwesomePaginate } from 'vue-awesome-paginate';

export default {
    components: {
      VueAwesomePaginate
    },
    data() {
        return {
          run_name:"",
          questions: [],
          feedbackData: [],
          itemsPerPage: 10,
          localCurrentPageCourses: 1,
        }
    },
    mounted() {
        this.fetchRunCourseFeedbackData();
    },
    methods: {
        async fetchRunCourseFeedbackData() {
            try {
              const rcourse_id = this.$route.params.id
              const feedbackForRunCourse = await FeedbackService.getFeedbackForRunCourse(rcourse_id);
              this.questions = feedbackForRunCourse.questions
              this.feedbackData = feedbackForRunCourse.data.map(item => item.answers);
              this.run_name = feedbackForRunCourse.data[0].run_name
                
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