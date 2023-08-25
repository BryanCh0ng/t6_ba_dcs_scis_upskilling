<template>
  <div>
    <ul class="nav nav-pills justify-content-center">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'courses' }" @click="activeTab = 'courses'">All Courses</a>
      </li> 
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'instructors' }" @click="activeTab = 'instructors'">All Instructors</a>
      </li>
    </ul>
    <div class="tab-content ">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'courses' }">
        <div class="pt-5 container col-12 table-responsive">
          <h5 class="pb-3">All Courses Database</h5>
          <div v-if="courses.length > 0">
            <table class="table">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Registration Count <sort-icon :sortColumn="sortColumn === 'reg_count'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'status'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Feedback Analysis</th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(course, key) in displayedCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="course.name" :category="course.category" :description="course.description"></course-name-desc>
                  </td>
                  <td class="reg_count">
                    {{ course.reg_count }}
                  </td>
                  <td class="closing_date">
                    <course-date-time :date="course.closing_date" :time="course.closing_time"></course-date-time>
                  </td>
                  <td>{{ course.status }}</td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis">View Feedback Analysis</a></td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td v-if="course.status === 'Active'"><course-action status="Deactivate" :id="course.id"></course-action></td>
                  <td v-else-if="course.status === 'Inactive'"><course-action status="Activate" :id="course.id"></course-action></td>
                  <td><course-action status="Edit" :id="course.id"></course-action></td>
                  <td><course-action status="Delete" :id="course.id"></course-action></td>
                </tr>
              </tbody>
            </table>
            <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
              <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
            </div>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="courses.length/itemsPerPage > 0" v-model="localCurrentPageCourses" :totalItems="courses.length" :items-per-page="1" @page-change="handlePageChangeCourses" class="justify-content-center pagination-container"/>
      </div>
  
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'instructors' }">
        <div class="pt-5 container col-12 table-responsive">
          <h5 class="pb-3">All Instructors Database</h5>
          <div v-if="instructors.length > 0">
            <table class="table">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Instructor Name <sort-icon :sortColumn="sortColumn === 'instructor_name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Organization <sort-icon :sortColumn="sortColumn === 'organization'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Ratings <sort-icon :sortColumn="sortColumn === 'ratings'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Feedback Analysis</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(instructor, key) in displayedInstructors" :key="key">
                  <td class="instructor_name">
                    {{ instructor.name }}
                  </td>
                  <td class="orgnanization">
                    {{ instructor.organization }}
                  </td>
                  <td class="ratings">
                    {{ instructor.ratings }}
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis">View Feedback Analysis</a></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="instructors.length/itemsPerPage > 0" v-model="localCurrentPageInstructors" :totalItems="instructors.length" :items-per-page="1" @page-change="handlePageChangeInstructors" class="justify-content-center pagination-container"/>
      </div>
    </div>
  </div>
</template>
  
<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import courseDateTime from '../../components/course/courseDateTime.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import { getAllCourseDetails } from '../../scripts/course/GetAllCourseDetails.js';

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
      courses: [
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
        available_slots: 10,
        reg_count: 13
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
        status: 'Inactive',
        available_slots: 10,
        reg_count: 20
        },
      ],
      instructors: [
        {
          name: 'ABC',
          organization: 'Org',
          ratings: '4.6/5'
        },
        {
          name: 'BDE',
          organization: 'Org',
          ratings: '4.6/5'
        }
      ],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 1,
      localCurrentPageCourses: 1,
      localCurrentPageInstructors: 1,
      activeTab: 'courses'
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
    handlePageChangeInstructors(newPage) {
      this.localCurrentPageInstructors = newPage;
      this.$emit('page-change', newPage);
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
      return this.courses.slice(startIndex, endIndex);
    },
    displayedInstructors() {
      const startIndex = (this.localCurrentPageInstructors - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.instructors.slice(startIndex, endIndex);
    }
  },
  created() {
    const response = getAllCourseDetails();
    console.log(response)
  },
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>