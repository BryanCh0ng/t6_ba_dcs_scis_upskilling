<template>
  <div>
    <ul class="nav nav-pills justify-content-center">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'submitted' }" @click="activeTab = 'submitted'">Submitted</a>
      </li> 
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'approved_rejected' }" @click="activeTab = 'approved_rejected'">Approved/Rejected</a>
      </li>
    </ul>
    <div class="tab-content ">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'submitted' }">
        <div class="pt-5 container col-12 table-responsive">
          <h5 class="pb-3">Pending Proposals</h5>
          <div v-if="pending_courses.length > 0">
            <table class="table">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Owner <sort-icon :sortColumn="sortColumn === 'owner'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Proposed Date <sort-icon :sortColumn="sortColumn === 'proposed_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(pending_course, key) in displayedPendingCourses" :key="key">
                  <td class="name">
                    <div class="col-12 d-flex align-items-center">
                      <div class="text-nowrap">{{ pending_course.name }}</div>
                      <div class="ms-2">
                        <course-category-badge :category="pending_course.category"></course-category-badge>
                      </div>
                    </div>
                    <div class="col-12 text-grey two-lines">
                      {{ pending_course.description }}
                    </div>
                  </td>
                  <td class="reg_count">
                    {{ pending_course.owner }}
                  </td>
                  <td class="closing_date">
                    <div class="col-12">
                      {{ pending_course.proposed_date }}
                    </div>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(pending_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action status="Approve" :id="pending_course.id"></course-action></td>
                  <td><course-action status="Reject" :id="pending_course.id" @click="openReject(pending_course)" data-bs-toggle="modal" data-bs-target="#rejected_modal"></course-action></td>
                </tr>
              </tbody>
            </table>
            <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
              <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
            </div>
            <div class="modal fade" id="rejected_modal" tabindex="-1" aria-hidden="true">
              <div class="modal-dialog modal-lg"><reject-proposal-modal  @close-modal="closeReject"/></div>
            </div>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPage" :totalItems="pending_courses.length" :items-per-page="1" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
      </div>
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'approved_rejected' }">
        <div class="pt-5 container col-12 table-responsive">
          <h5 class="pb-3">All Proposals</h5>
          <div v-if="proposed_courses.length > 0">
            <table class="table">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Owner <sort-icon :sortColumn="sortColumn === 'owner'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Proposed Date <sort-icon :sortColumn="sortColumn === 'proposed_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'status'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(proposed_course, key) in displayedProposedCourses" :key="key">
                  <td class="name">
                    <div class="col-12 d-flex align-items-center">
                      <div class="text-nowrap">{{ proposed_course.name }}</div>
                      <div class="ms-2">
                        <course-category-badge :category="proposed_course.category"></course-category-badge>
                      </div>
                    </div>
                    <div class="col-12 text-grey two-lines">
                      {{ proposed_course.description }}
                    </div>
                  </td>
                  <td class="reg_count">
                    {{ proposed_course.owner }}
                  </td>
                  <td class="closing_date">
                    <div class="col-12">
                      {{ proposed_course.proposed_date }}
                    </div>
                  </td>
                  <td>{{ proposed_course.status }}</td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(proposed_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action v-if="proposed_course.status == 'Approved'" status="Open for Voting" :id="proposed_course.id"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPage" :totalItems="proposed_courses.length" :items-per-page="1" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
      </div>
    </div>
  </div>
</template>
    
  <script>
  import courseAction from '../../components/course/courseAction.vue';
  import courseCategoryBadge from '../../components/course/courseCategoryBadge.vue';
  import sortIcon from '../../components/common/sort-icon.vue';
  import modalCourseContent from '../../components/course/modalCourseContent.vue';
  import rejectProposalModal from '../../components/course/rejectProposalModal.vue';
  import { VueAwesomePaginate } from 'vue-awesome-paginate';
  
  export default {
    components: {
      courseAction,
      courseCategoryBadge,
      sortIcon,
      modalCourseContent,
      VueAwesomePaginate,
      rejectProposalModal
    },
    data() {
      return {
        proposed_courses: [
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
          status: 'Approved',
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
          status: 'Rejected',
          available_slots: 10,
          reg_count: 20
          },
        ],
        pending_courses: [
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
          status: 'Pending',
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
          status: 'Pending',
          available_slots: 10,
          reg_count: 20
          },
        ],
        sortColumn: 'name',
        sortDirection: 'asc',
        selectedCourse: null,
        itemsPerPage: 1,
        localCurrentPage: 1,
        activeTab: 'submitted'
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
      handlePageChange(newPage) {
        this.localCurrentPage = newPage;
        this.$emit('page-change', newPage);
      },
      openReject() {
        this.showModal = true;
      },
      closeReject() {
        this.showModal = false;
      }
    },
    computed: {
      displayedPendingCourses() {
        const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.pending_courses.slice(startIndex, endIndex);
      },
      displayedProposedCourses() {
        const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.proposed_courses.slice(startIndex, endIndex);
      }
    }
    }
  </script>
  
  
  <style>
    @import '../../assets/css/course.css';
    @import '../../assets/css/paginate.css';
  </style>