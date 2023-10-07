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
        <div class="pt-5 container col-12 table-responsive" v-if="shouldShowTopRegisterPicks">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Top Picks</h1>
            <div v-if="top_register_picks && top_register_picks.length > 0"> 
              <table class="table bg-white">
                <thead>
                  <tr class="text-nowrap">
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'register_top')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'register_top')">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'register_top')">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'register_top')">Closing Date <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
                    <th scope="col">Course Details</th>
                    <th scope="col">Action(s)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(top_pick, key) in displayedTopPicksRegister" :key="key">
                    <td class="name">
                      <course-name-desc :name="top_pick.course_Name" :category="top_pick.coursecat_Name" :description="top_pick.course_Desc"></course-name-desc>
                    </td>
                    <td class="start_date">
                      <course-date-time :date="top_pick.run_Startdate" :time="top_pick.run_Starttime"></course-date-time>
                    </td>
                    <td class="end_date">
                      <course-date-time :date="top_pick.run_Enddate" :time="top_pick.run_Endtime"></course-date-time>
                    </td>
                    <td class="closing_date">
                      <course-date-time :date="top_pick.reg_Enddate" :time="top_pick.reg_Endtime"></course-date-time>
                    </td>
                    
                    <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(top_pick)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                    <td><course-action @action-and-message-updated="handleActionData" :status="top_pick.course_Status" :course="top_pick"></course-action></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else-if="top_register_picks=[]" class="text-center pt-2 pb-5">
              <p>Currently, there are no recommendations for you.</p>
              <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
            </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageTopPickRegister" v-if="top_register_picks.length/itemsPerPage > 0 && shouldShowTopRegisterPicks" :totalItems="top_register_picks.length" :items-per-page="itemsPerPage" @page-change="handlePageTopRegisterCourses" class="justify-content-center pagination-container"/>
      
        <div class="pt-5 container col-12 table-responsive" v-if="showRegisterJustForYou">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div v-if="reg_courses_for_you && reg_courses_for_you.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'register_you')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'register_you')">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'register_you')">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'register_you')">Closing Date <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
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
                  <td><course-action @action-and-message-updated="handleActionData" :status="reg_course.course_Status" :course="reg_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="reg_courses_for_you=[]" class="text-center pt-2 pb-5">
            <p>Currently, there are no recommendations for you.</p>
            <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseForYou" v-if="reg_courses_for_you.length/itemsPerPage > 0" :totalItems="reg_courses_for_you.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeRegCourseForYou" class="justify-content-center pagination-container"/>
        
        <div class="pt-5 container col-12 table-responsive" v-if="showRegisterOthers">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Just For You</h1>
          <div v-if="reg_courses_others && reg_courses_others.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'register_others')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'register_others')">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                  <th scope="col">
                      <a href="" class="register_otherstext-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'run')">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'register_others')">Closing Date <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
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
                    <course-date-time :date="reg_course.run_Startdate" :time="reg_course.run_Starttime"></course-date-time>
                  </td>
                  <td class="end_date">
                    <course-date-time :date="reg_course.run_Enddate" :time="reg_course.run_Endtime"></course-date-time>
                  </td>
                  <td class="closing_date">
                    <course-date-time :date="reg_course.reg_Enddate" :time="reg_course.reg_Endtime"></course-date-time>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(reg_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action @action-and-message-updated="handleActionData" :status="reg_course.course_Status" :course="reg_course"></course-action></td>
                  
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="reg_courses_others=[]" class="text-center pt-2 pb-5">
              <p>Currently, there are no recommendations for you.</p>
              <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseOthers" v-if="reg_courses_others.length/itemsPerPage > 0" :totalItems="reg_courses_others.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeRegCourseOthers" class="justify-content-center pagination-container"/>
      </div>


      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'express_interest' }">
        <div class="pt-5 container col-12 table-responsive" v-if="shouldShowTopInterestPicks">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Top Picks</h1>
          <div v-if="top_interest_picks && top_interest_picks.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'interest_top')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(interest_course, key) in displayedTopPicksInterest" :key="key">
                  <td class="name">
                      <course-name-desc :name="interest_course.course_Name" :category="interest_course.coursecat_Name" :description="interest_course.course_Desc"></course-name-desc>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(interest_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action @action-and-message-updated="handleActionData" status="Vote" :course="interest_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="top_interest_picks=[]" class="text-center pt-2 pb-5">
            <p>Currently, there are no recommendations for you.</p>
            <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageTopPickInterest" v-if="top_interest_picks.length/itemsPerPage > 0 && shouldShowTopInterestPicks" :totalItems="top_interest_picks.length" :items-per-page="itemsPerPage" @page-change="handlePageTopInterestCourses" class="justify-content-center pagination-container"/>
          
        <div class="pt-5 container col-12 table-responsive" v-if="showInterestJustForYou">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1> 
          <div v-if="interest_courses && interest_courses.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'interest_you')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(interest_course, key) in displayedInterestCourses" :key="key">
                  <td class="name">
                      <course-name-desc :name="interest_course.course_Name" :category="interest_course.coursecat_Name" :description="interest_course.course_Desc"></course-name-desc>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(interest_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action @action-and-message-updated="handleActionData" status="Vote" :course="interest_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="interest_courses=[]" class="text-center pt-2 pb-5">
            <p>Currently, there are no recommendations for you.</p>
            <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestCourses" v-if="interest_courses.length/itemsPerPage > 0" :totalItems="interest_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageTopInterestCourses" class="justify-content-center pagination-container"/>

        
          <div class="pt-5 container col-12 table-responsive" v-if="showInterestOthers">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Just For You</h1>
          <div v-if="interest_others && interest_others.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'interest_others')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="sortDirection"/></a></th>
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
                  <td><course-action @action-and-message-updated="handleActionData" status="Vote" :course="interest_other"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="interest_others=[]" class="text-center pt-2 pb-5">
            <p>Currently, there are no recommendations for you.</p>
            <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestOthers" v-if="interest_others.length/itemsPerPage > 0" :totalItems="interest_others.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeInterestOthers" class="justify-content-center pagination-container"/>
      </div>

      <!-- Modal -->
      <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
      </div>
      <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
        <div class="modal-dialog modal-lg"> 
          <modal-after-action :course="actionCourse" @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal" />
        </div>
      </div>

    </div>
    
  </div>
</template>
      
<script>
import courseAction from '@/components/course/courseAction.vue';
import sortIcon from '@/components/common/sort-icon.vue';
import modalCourseContent from '@/components/course/modalCourseContent.vue';
import modalAfterAction from '@/components/course/modalAfterAction.vue';
import courseNameDesc from '@/components/course/courseNameDesc.vue';
import courseDateTime from '@/components/course/courseDateTime.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import Recommender from "@/api/services/recommenderService.js";
import UserService from "@/api/services/UserService.js";
import CourseService from "@/api/services/CourseService.js";
import CommonService from "@/api/services/CommonService.js";

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    modalAfterAction,
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
      top_register_picks: [],
      top_interest_picks: [],
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 5,
      localCurrentPageRegCourseForYou: 1,
      localCurrentPageRegCourseOthers: 1,
      localCurrentInterestOthers: 1,
      localCurrentInterestCourses: 1,
      localCurrentPageTopPickRegister: 1,
      localCurrentPageTopPickInterest: 1,
      activeTab: 'for_registration',
      user_ID: 1,
      showRegisterJustForYou: true,
      showRegisterOthers: true,
      showInterestJustForYou: true,
      showInterestOthers: true,
      receivedMessage: '',
      actionCourse: {},
    }
  },
  methods: {
    async get_user_id() {
      try {
        const user_ID = await UserService.getUserID()
        this.user_ID = user_ID

      } catch (error) {
        this.message = error.message
        this.user_ID = null;
      }
    },
    openModal(course) {
      this.selectedCourse = course;
      this.showModal = true;
    },
    closeModal() {
      this.selectedCourse = null;
      this.showModal = false;
    },
    handleActionData(actionData) {
      this.receivedMessage = actionData.message;
      this.actionCourse = actionData.course
      const modalButtonElement = this.$el.querySelector('.invisible-btn')
      modalButtonElement.click();
    },
    modalAfterActionClose() {
      this.loadData();
    },
    sort(column, action) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
      this.sortCourse(action)
    },
    getSortDirection(column) {
      if (this.sortColumn === column) {
        return this.sortDirection;
      }
    },
    async sortCourse(action) {
      if (action == 'register_you') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.reg_courses_for_you)
         if (sort_response.code == 200) {
          this.reg_courses_for_you = sort_response.data
         }
      }
      if (action == 'register_top') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.top_register_picks)
         if (sort_response.code == 200) {
          this.top_register_picks = sort_response.data
         }
      }
      if (action == 'register_others') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.reg_courses_others)
         if (sort_response.code == 200) {
          this.reg_courses_others = sort_response.data
         }
      }

      if (action == 'interest_you') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.interest_courses)
         if (sort_response.code == 200) {
          this.interest_courses = sort_response.data
         }
      }
      if (action == 'interest_top') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.top_interest_picks)
         if (sort_response.code == 200) {
          this.top_interest_picks = sort_response.data
         }
      }
      if (action == 'interest_others') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.interest_others)
         if (sort_response.code == 200) {
          this.interest_others = sort_response.data
         }
      }
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
    },
    handlePageTopRegisterCourses(newPage) {
      this.localCurrentPageTopPickRegister = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageTopInterestCourses(newPage) {
      this.localCurrentPageTopPickInterest = newPage;
      this.$emit('page-change', newPage);
    },
    async loadData() {
      let top_register_pick = await Recommender.getTopPicksForRegistration(this.user_ID)
      this.top_register_picks = top_register_pick.data

      let top_interest_pick = await Recommender.getTopPicksForVoting(this.user_ID)
      this.top_interest_picks = top_interest_pick.data

      let user_register = await Recommender.getUserSimilarityRegistration(this.user_ID)
      if (user_register.code != 202 || user_register.length === 0) {
        this.showRegisterJustForYou = false
      }
      this.reg_courses_for_you = user_register.data.course_list
      if (this.reg_courses_for_you.length === 0) {
        this.showRegisterJustForYou = false
      }

      let course_list_req = await Recommender.getUserRegisteredCourses(this.user_ID)
      if (course_list_req.message === "No matching course registration information found") {
        this.showRegisterOthers= false
      } else {
        let course_register = await Recommender.getCourseSimilarityRegistration(course_list_req.data)
        // console.log(course_register)
        this.reg_courses_others = course_register.data.course_list
        if (this.reg_courses_others.length === 0) {
          this.showRegisterOthers= false
        }
      }
            
      let user_interest = await Recommender.getUserSimilarityInterest(this.user_ID)
      if (user_register.length === 0) {
          this.showInterestJustForYou= false
      } else {
        this.interest_courses = user_interest.data.course_list
        if (this.interest_courses.length === 0) {
          this.showInterestJustForYou= false
        }
      }
      
      let interest_list_req = await CourseService.searchCourseVoteInfo(this.user_ID, null, null, null)
      // console.log(interest_list_req)
      if (interest_list_req.message === "No matching course interest information found") {
        this.showInterestOthers = false
      } else {
        let course_interest = await Recommender.getCourseSimilarityInterest(interest_list_req.data)
        // console.log(course_interest)
        if (course_interest.code != 202 || course_interest.length === 0) {
          this.showInterestOthers = false
        } else {
          this.interest_others = course_interest.data.course_list
          if (this.interest_others.length === 0) {
            this.showInterestOthers = false
          }
        }
      }

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
    },
    displayedTopPicksRegister() {
      const startIndex = (this.localCurrentPageTopPickRegister - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.top_register_picks.slice(startIndex, endIndex);
    },
    displayedTopPicksInterest() {
      const startIndex = (this.localCurrentPageTopPickInterest - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.top_interest_picks.slice(startIndex, endIndex);
    },
    shouldShowTopRegisterPicks() {
      const isRegCoursesForYouEmpty = this.reg_courses_for_you.length === 0;
      const isRegCoursesOthersEmpty = this.reg_courses_others.length === 0;

      return (
        this.top_register_picks &&
        this.top_register_picks.length > 0 &&
        (isRegCoursesForYouEmpty || isRegCoursesOthersEmpty)
      );
    },
    shouldShowTopInterestPicks() {
      const isInterestCoursesForYouEmpty = this.interest_courses.length === 0;
      const isInterestCoursesOthersEmpty = this.interest_others.length === 0;

      return (
        this.top_interest_picks &&
        this.top_interest_picks.length > 0 &&
        (isInterestCoursesForYouEmpty || isInterestCoursesOthersEmpty)
      );
    }
  },
  async created() {
    const user_ID = await UserService.getUserID();
    this.user_ID = user_ID
    const role = await UserService.getUserRole(user_ID);
    if (role == 'Admin') {
      this.$router.push({ name: 'adminViewCourse' }); 
    } else if (role == 'Instructor' || role == 'Trainer') {
      this.$router.push({ name: 'instructorTrainerViewVotingCampaign' }); 
    } else {
      try {
        this.loadData()
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    }
  },
  mounted() {
    const buttonElement = document.createElement('button');
    buttonElement.className = 'btn btn-primary d-none invisible-btn';
    buttonElement.setAttribute('data-bs-toggle', 'modal');
    buttonElement.setAttribute('data-bs-target', '#after_action_modal');
    this.$el.appendChild(buttonElement);
    const modalElement = this.$refs.afterActionModal;
    modalElement.addEventListener('hidden.bs.modal', this.modalAfterActionClose);
  },
  beforeUnmount() {
    const modalElement = this.$refs.afterActionModal;
    modalElement.removeEventListener('hidden.bs.modal', this.modalAfterActionClose)
  }
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>