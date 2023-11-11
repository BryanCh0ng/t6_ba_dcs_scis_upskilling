<template>
  <div>
    <div class="container col-12 d-flex mb-3 w-100">
        <h5 class="col m-auto">View My Lessons</h5>
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
            </tr>
          </thead>
          <tbody>
            <tr v-for="(lesson, key) in displayedLessons" :key="key">
              <td class="name">
                <course-name-desc :name="lesson.run_Name" :category="lesson.run_course.coursecat_Name" :description="lesson.run_course.course_Desc"></course-name-desc>
              </td>
              <td>{{ lesson.instructor_Name }}</td>
              <td class="text-nowrap"><course-date-time :date="lesson.lesson_Date"></course-date-time></td>
              <td><course-date-time :time="lesson.lesson_Starttime"></course-date-time></td>
              <td><course-date-time :time="lesson.lesson_Endtime"></course-date-time></td>
              <td :class="{ 'text-grey-important': lesson.lesson_Status == 'Ended' }" ><course-status :status="lesson.lesson_Status"></course-status></td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(lesson.run_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
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
      errorMsge: 'No records found'
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
        const user_ID = await UserService.getUserID();
        console.log(user_ID)
        let response = await LessonService.getLessonsByStudentId(user_ID)
        console.log(response)
        if (response.code == 200) {
          this.lessons = response.lessons
          console.log(this.lessons)
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
    }
  },
  async created() {
      document.title = "My Lessons | Upskilling Engagement System";

      const user_ID = await UserService.getUserID();
      const role = await UserService.getUserRole(user_ID);
      if (role == "Admin") {
      this.$router.push({ name: "adminViewCourse" });
      } else if (role == "Instructor" || role == "Trainer") {
      this.$router.push({ name: "instructorTrainerViewVotingCampaign" });
      } else {
        try {
            this.loadData();
        } catch (error) {
            console.error("Error fetching lesson details:", error);
        }
      }
  },
  }
</script>

<style>
@import '../../assets/css/course.css';
@import '../../assets/css/paginate.css';
</style>