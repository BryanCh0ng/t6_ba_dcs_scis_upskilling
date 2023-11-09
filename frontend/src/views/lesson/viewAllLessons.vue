<template>
    <div>
      <div class="container col-12 d-flex mb-3 w-100">
          <h5 class="col m-auto">All Lessons</h5>
      </div>

      <div class="container col-12">
        <div v-if="lessons && lessons.length > 0" class="table-responsive">
          <table class="table bg-white">
            <thead>
              <tr class="text-nowrap">
                <th scope="col">
                  <a href="" @click.prevent="sort('run_Name')" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'run_Name'" :sortDirection="getSortDirection('run_Name')"/></a></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('instructor_Name')" class="text-decoration-none text-dark">Instructor Name <sort-icon :sortColumn="sortColumn === 'instructor_Name'" :sortDirection="getSortDirection('instructor_Name')"/></a></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('lesson_Date')" class="text-decoration-none text-dark">Date <sort-icon :sortColumn="sortColumn === 'lesson_Date'" :sortDirection="getSortDirection('lesson_Date')"/></a></th>
                <th scope="col">Start Time</th>
                <th scope="col">End Time</th>
                <th scope="col">
                  <a href="" @click.prevent="sort('lesson_Status')" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'lesson_Status'" :sortDirection="getSortDirection('lesson_Status')"/></a></th>
                <th scope="col">Course Details</th>
                <th scope="col" v-if="userRole != 'Student'">Attendance</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(lesson, key) in displayedLessons" :key="key">
                <td class="name">
                  <course-name-desc :name="lesson.run_course.run_Name" :category="lesson.run_course.coursecat_Name" :description="lesson.run_course.course_Desc"></course-name-desc>
                </td>
                <td>{{ lesson.instructor_Name }}</td>
                <td class="text-nowrap"><course-date-time :date="lesson.lesson_Date"></course-date-time></td>
                <td><course-date-time :time="lesson.lesson_Starttime"></course-date-time></td>
                <td><course-date-time :time="lesson.lesson_Endtime"></course-date-time></td>
                <td :class="{ 'text-grey-important': lesson.lesson_Status == 'Ended' }" ><course-status :status="lesson.lesson_Status"></course-status></td>
                <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(lesson.run_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                <td v-if="userRole != 'Student'" :class="{ 'text-grey-important': lesson.lesson_Status == 'Ended' }"><a class="text-nowrap text-dark text-decoration-underline view-runs" @click="goToViewAttendance(lesson.lesson_ID)">View Attendance</a></td>
              </tr>               
            </tbody>
          </table>
          <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
          </div>
  
        </div>
        <div v-else-if="lessons=[]">
          <p>{{ errorMsge }}</p>
        </div>
      </div>
      <vue-awesome-paginate v-if="lessons.length/itemsPerPage > 0" v-model="localCurrentPageLessons" :totalItems="lessons.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeLessons" class="justify-content-center pagination-container"/>
    </div>
  
</template>
  
<script>
  import sortIcon from '@/components/common/sort-icon.vue';
  import modalCourseContent from '@/components/course/modalCourseContent.vue';
  import courseNameDesc from '@/components/course/courseNameDesc.vue';
  import { VueAwesomePaginate } from 'vue-awesome-paginate';
  import CommonService from "@/api/services/CommonService.js";
  import LessonService from "@/api/services/LessonService.js";
  import courseDateTime from "@/components/course/courseDateTime.vue";
  import UserService from "@/api/services/UserService.js";
  import courseStatus from '../../components/course/courseStatus.vue';
  
  export default {
    components: {
      sortIcon,
      modalCourseContent,
      VueAwesomePaginate,
      courseNameDesc,
      courseDateTime,
      courseStatus
    },
    data() {
      return {
        lessons: [],
        sortColumn: '',
        sortDirection: 'asc',
        selectedCourse: null,
        itemsPerPage: 10,
        localCurrentPageLessons: 1,
        receivedMessage: '',
        errorMsge: 'No records found',
        userRole: ''
      }
    },
    computed: {
      displayedLessons() {
        const startIndex = (this.localCurrentPageLessons - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.lessons.slice(startIndex, endIndex);
      },
    },
    methods: {
      openModal(course) {
        this.selectedCourse = course;
        this.showModal = true;
      },
      closeModal() {
        this.selectedCourse = null;
        this.showModal = false;
      },
      handlePageChangeLessons(newPage) {
        this.localCurrentPageLessons = newPage;
        this.$emit('page-change', newPage);
      },
      async loadData() {
        console.log('load')
        try {
          let response = await LessonService.getAllLessons()
          console.log(response)
          if (response.code == 200) {
            this.lessons = response.lessons
          } else {
            this.errorMsge = response.message
          }
        } catch (error) {
          console.error("Error fetching lesson details:", error);
        }
      },
      sort(column) {
        if (this.sortColumn === column) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortColumn = column;
          this.sortDirection = 'asc';
        }
        this.sortCourse()
      },
      getSortDirection(column) {
        if (this.sortColumn === column) {
          return this.sortDirection;
        }
      },
      async sortCourse() {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.lessons)
          if (sort_response.code == 200) {
            this.lessons = sort_response.data
          }
      },
      goToViewAttendance(lesson_id) {
        this.$router.push({ name: 'viewAttendance', params: {lessonId: lesson_id}});
      }
    },
    async created() {
      const user_ID = await UserService.getUserID();
      const role = await UserService.getUserRole(user_ID);
      this.userRole = role
      this.loadData();
      // if (role == 'Student') {
      //   this.$router.push({ name: 'studentViewCourse' }); 
      // } else {
      //   this.loadData();
      // }
    },
    }
</script>
  
<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>