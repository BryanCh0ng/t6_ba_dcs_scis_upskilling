<template>
  <div>
    <ul class="nav nav-pills justify-content-center">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'for_registration' }" @click="activeTab = 'for_registration'">For Registration</a>
      </li> 
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'express_interest' }" @click="activeTab = 'express_interest'">Express Interest</a>
      </li>
    </ul>
    <div class="tab-content ">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'for_registration' }">
        <div class="pt-5 container col-12 table-responsive">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Just For you</h1>
          <div v-if="reg_courses_for_you && reg_courses_for_you.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course Start Date <sort-icon :sortColumn="sortColumn === 'start_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course End Date <sort-icon :sortColumn="sortColumn === 'end_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(reg_course, key) in displayedRegCourseForYou" :key="key">
                  <td class="name">
                    <course-name-desc :name="reg_course.course_Name" :category="reg_course.coursecat_Name" :description="reg_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="start_date">
                    <course-date-time :date="reg_course.run_Startdate" :time="reg_course.run_Starttime"></course-date-time>
                  </td>
                  <td class="end_date">
                    <course-date-time :date="reg_course.run_Enddate" :time="reg_course.run_Endtime"></course-date-time>
                  </td>
                  <td class="closing_date">
                    <course-date-time :date="reg_course.reg_Enddate" :time="reg_course.reg_Endtime"></course-date-time>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(reg_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="reg_course.course_Status" :course="reg_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="reg_courses_for_you=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseForYou" v-if="reg_courses_for_you.length/itemsPerPage > 0" :totalItems="reg_courses_for_you.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeRegCourseForYou" class="justify-content-center pagination-container"/>
          
        <div class="pt-5 container col-12 table-responsive">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div v-if="reg_courses_others && reg_courses_others.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course Start Date <sort-icon :sortColumn="sortColumn === 'start_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course End Date <sort-icon :sortColumn="sortColumn === 'end_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(reg_course, key) in displayedRegCourseOthers" :key="key">
                  <td class="name">
                      <course-name-desc :name="reg_course.course_Name" :category="reg_course.coursecat_Name" :description="reg_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="start_date">
                    <course-date :date="reg_course.run_Startdate" :time="reg_course.run_Starttime"></course-date>
                  </td>
                  <td class="end_date">
                    <course-date :date="reg_course.run_Enddate" :time="reg_course.run_Endtime"></course-date>
                  </td>
                  <td class="closing_date">
                    <course-date :date="reg_course.reg_Enddate" :time="reg_course.reg_Endtime"></course-date>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(reg_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="reg_course.course_Status" :course="reg_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="reg_courses_others=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseOthers" v-if="reg_courses_others.length/itemsPerPage > 0" :totalItems="reg_courses_others.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeRegCourseOthers" class="justify-content-center pagination-container"/>
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'express_interest' }">
        <div class="pt-5 container col-12 table-responsive">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div v-if="interest_courses && interest_courses.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(interest_course, key) in displayedInterestCourses" :key="key">
                  <td class="name">
                      <course-name-desc :name="interest_course.course_Name" :category="interest_course.coursecat_Name" :description="interest_course.course_Name"></course-name-desc>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(interest_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="interest_course.vote_Status" :course="interest_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="interest_courses=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestCourses" v-if="interest_courses.length/itemsPerPage > 0" :totalItems="interest_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageInterestCourses" class="justify-content-center pagination-container"/>
          <div class="pt-5 container col-12 table-responsive">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div v-if="interest_others && interest_others.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(interest_other, key) in displayedInterestOthers" :key="key">
                  <td class="name">
                      <course-name-desc :name="interest_other.course_Name" :category="interest_other.coursecat_Name" :description="interest_other.course_Desc"></course-name-desc>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(interest_other)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="interest_other.vote_Status" :course="interest_other"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="interest_others=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestOthers" v-if="interest_others.length/itemsPerPage > 0" :totalItems="interest_others.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeInterestOthers" class="justify-content-center pagination-container"/>
      </div>
    </div>
    <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
    </div>
  </div>
</template>
      
<script>
import courseAction from '@/components/course/courseAction.vue';
import sortIcon from '@/components/common/sort-icon.vue';
import modalCourseContent from '@/components/course/modalCourseContent.vue';
import courseNameDesc from '@/components/course/courseNameDesc.vue';
import courseDateTime from '@/components/course/courseDateTime.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'
import CourseService from "@/api/services/CourseService.js";

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    courseDateTime
  },
  data() {
    return {
      reg_courses_for_you: [],
      reg_courses_others: [],
      interest_courses: [],
      interest_others: [],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageRegCourseForYou: 1,
      localCurrentPageRegCourseOthers: 1,
      localCurrentInterestOthers: 1,
      localCurrentInterestCourses: 1,
      activeTab: 'for_registration'
    }
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
    handlePageChangeRegCourseForYou(newPage) {
      this.localCurrentPageRegCourseForYou = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeRegCourseOthers(newPage) {
      this.localCurrentPageRegCourseOthers = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeInterestOthers(newPage) {
      this.localCurrentInterestOthers = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageInterestCourses(newPage) {
      this.localCurrentInterestCourses = newPage;
      this.$emit('page-change', newPage);
    }
  },
  computed: {
    displayedRegCourseForYou() {
      const startIndex = (this.localCurrentPageRegCourseForYou - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.reg_courses_for_you.slice(startIndex, endIndex);
    },
    displayedRegCourseOthers() {
      const startIndex = (this.localCurrentPageRegCourseOthers - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.reg_courses_others.slice(startIndex, endIndex);
    },
    displayedInterestOthers() {
      const startIndex = (this.localCurrentInterestOthers - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.interest_others.slice(startIndex, endIndex);
    },
    displayedInterestCourses() {
      const startIndex = (this.localCurrentInterestCourses - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.interest_courses.slice(startIndex, endIndex);
    }
  },
  async created() {
    try {
      let run_response = await CourseService.searchUnregisteredActiveInfo(null, null, null)
      this.reg_courses_for_you = run_response.data
      this.reg_courses_others = run_response.data
      this.reg_courses_for_you.map(course => {
        course.reg_Enddate = convertDate(course.reg_Enddate)
        course.reg_Startdate = convertDate(course.reg_Startdate)
        course.run_Enddate = convertDate(course.run_Enddate)
        course.run_Startdate = convertDate(course.run_Startdate)
        course.reg_Endtime = convertTime(course.reg_Endtime)
        course.reg_Starttime = convertTime(course.reg_Starttime)
        course.run_Endtime = convertTime(course.run_Endtime)
        course.run_Starttime = convertTime(course.run_Starttime)
      }); 
      this.reg_courses_others.map(course => {
        course.reg_Enddate = convertDate(course.reg_Enddate)
        course.reg_Startdate = convertDate(course.reg_Startdate)
        course.run_Enddate = convertDate(course.run_Enddate)
        course.run_Startdate = convertDate(course.run_Startdate)
        course.reg_Endtime = convertTime(course.reg_Endtime)
        course.reg_Starttime = convertTime(course.reg_Starttime)
        course.run_Endtime = convertTime(course.run_Endtime)
        course.run_Starttime = convertTime(course.run_Starttime)
      }); 
      let interest_response = await CourseService.searchUnvotedActiveInfo(null, null, null)
      this.interest_courses = interest_response.data
      this.interest_others = interest_response.data
    } catch (error) {
      console.error("Error fetching course details:", error);
    }
  }
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>