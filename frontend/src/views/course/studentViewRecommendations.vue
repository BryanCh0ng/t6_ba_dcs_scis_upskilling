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
          <div v-if="reg_courses_for_you.length > 0">
            <table class="table">
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
                    <course-name-desc :name="reg_course.name" :category="reg_course.category" :description="reg_course.description"></course-name-desc>
                  </td>
                  <td class="start_date">
                    <course-date :date="reg_course.start_date" :time="reg_course.start_time"></course-date>
                  </td>
                  <td class="end_date">
                    <course-date :date="reg_course.end_date" :time="reg_course.end_time"></course-date>
                  </td>
                  <td class="closing_date">
                    <course-date :date="reg_course.closing_date" :time="reg_course.closing_time"></course-date>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(reg_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="reg_course.status" :id="reg_course.id"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseForYou" v-if="reg_courses_for_you.length/itemsPerPage > 0" :totalItems="reg_courses_for_you.length" :items-per-page="1" @page-change="handlePageChangeRegCourseForYou" class="justify-content-center pagination-container"/>
          
        <div class="pt-5 container col-12 table-responsive">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div v-if="reg_courses_others.length > 0">
            <table class="table">
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
                      <course-name-desc :name="reg_course.name" :category="reg_course.category" :description="reg_course.description"></course-name-desc>
                  </td>
                  <td class="start_date">
                    <course-date :date="reg_course.start_date" :time="reg_course.start_time"></course-date>
                  </td>
                  <td class="end_date">
                    <course-date :date="reg_course.end_date" :time="reg_course.end_time"></course-date>
                  </td>
                  <td class="closing_date">
                    <course-date :date="reg_course.closing_date" :time="reg_course.clos"></course-date>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(reg_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="reg_course.status" :id="reg_course.id"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseOthers" v-if="reg_courses_others.length/itemsPerPage > 0" :totalItems="reg_courses_others.length" :items-per-page="1" @page-change="handlePageChangeRegCourseOthers" class="justify-content-center pagination-container"/>
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'express_interest' }">
        <div class="pt-5 container col-12 table-responsive">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div v-if="interest_courses.length > 0">
            <table class="table">
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
                      <course-name-desc :name="interest_course.name" :category="interest_course.category" :description="interest_course.description"></course-name-desc>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(interest_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="interest_course.status" :id="interest_course.id"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestCourses" v-if="interest_courses.length/itemsPerPage > 0" :totalItems="interest_courses.length" :items-per-page="1" @page-change="handlePageInterestCourses" class="justify-content-center pagination-container"/>
          <div class="pt-5 container col-12 table-responsive">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div v-if="interest_others.length > 0">
            <table class="table">
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
                      <course-name-desc :name="interest_other.name" :category="interest_other.category" :description="interest_other.description"></course-name-desc>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(interest_other)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="interest_other.status" :id="interest_other.id"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestOthers" v-if="interest_others.length/itemsPerPage > 0" :totalItems="interest_others.length" :items-per-page="1" @page-change="handlePageChangeInterestOthers" class="justify-content-center pagination-container"/>
      </div>
    </div>
    <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
    </div>
  </div>
</template>
      
<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import courseDate from '../../components/course/courseDate.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    courseDate
  },
  data() {
    return {
      reg_courses_for_you: [
        {
          id: 1,
          name: "Course Name 1",
          category: "SCIS",
          description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
          start_date: "Aug 20, 2023",
          start_time: "6.30 pm",
          end_date: "Aug 20, 2023",
          end_time: "6.30 pm",
          closing_date: "Aug 20, 2023",
          closing_time: "6.30 pm",
          fee: 50,
          venue: 'SCIS SR-2',
          format: 'Physical',
          status: 'Active',
          available_slots: 13
        },
        {
          id: 2,
          name: "Course Name 2",
          category: "LKCSB",
          description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
          start_date: "Aug 20, 2023",
          start_time: "6.30 pm",
          end_date: "Aug 20, 2023",
          end_time: "6.30 pm",
          closing_date: "Aug 20, 2023",
          closing_time: "6.30 pm",
          fee: 100,
          venue: 'SCIS SR-5',
          format: 'Online',
          status: 'Vote',
          available_slots: 15
        }
      ],
      reg_courses_others: [
        {
          id: 1,
          name: "Course Name 1",
          category: "SCIS",
          description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
          start_date: "Aug 20, 2023",
          start_time: "6.30 pm",
          end_date: "Aug 20, 2023",
          end_time: "6.30 pm",
          closing_date: "Aug 20, 2023",
          closing_time: "6.30 pm",
          fee: 50,
          venue: 'SCIS SR-2',
          format: 'Physical',
          status: 'Active',
          available_slots: 13
        },
        {
          id: 2,
          name: "Course Name 2",
          category: "LKCSB",
          description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
          start_date: "Aug 20, 2023",
          start_time: "6.30 pm",
          end_date: "Aug 20, 2023",
          end_time: "6.30 pm",
          closing_date: "Aug 20, 2023",
          closing_time: "6.30 pm",
          fee: 100,
          venue: 'SCIS SR-5',
          format: 'Online',
          status: 'Vote',
          available_slots: 15
        }
      ],
      interest_courses: [
      {
        id: 1,
        name: "Course Name 1",
        category: "SCIS",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
        status: 'Vote',
      },
      {
        id: 2,
        name: "Course Name 2",
        category: "LKCSB",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
        status: 'Vote',
      }
      ],
      interest_others: [
      {
        id: 1,
        name: "Course Name 1",
        category: "SCIS",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
        status: 'Vote',
      },
      {
        id: 2,
        name: "Course Name 2",
        category: "LKCSB",
        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
        status: 'Vote',
      }
      ],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 1,
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
  }
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>