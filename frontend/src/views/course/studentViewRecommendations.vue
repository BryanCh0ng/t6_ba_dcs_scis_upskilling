<template>
  <div>
    <ul class="nav nav-pills justify-content-center pt-5">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'for_registration' }" @click="activeTab = 'for_registration'">For Registration</a>
      </li> 
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'express_interest' }" @click="activeTab = 'express_interest'">Express Interest</a>
      </li>
    </ul>
    <div class="tab-content ">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'for_registration' }">
        <div class="pt-5 container col-12" v-if="shouldShowTopRegisterPicks">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Top Picks</h1>
            <div class="table-responsive" v-if="top_register_picks && top_register_picks.length > 0"> 
              <table class="table bg-white">
                <thead>
                  <tr class="text-nowrap">
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Name', 'register_top')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'run_Name'" :sortDirection="getSortDirection('run_Name')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'register_top')">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'register_top')">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'register_top')">Closing Date <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
                    <th scope="col">Course Details</th>
                    <th scope="col">Lessons</th>
                    <th scope="col">Action(s)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(top_pick, key) in displayedTopPicksRegister" :key="key">
                    <td class="name">
                      <course-name-desc :name="top_pick.run_Name" :category="top_pick.coursecat_Name" :description="top_pick.course_Desc"></course-name-desc>
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
                    <td>
                      <a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis" @click="viewLessons(top_pick.rcourse_ID)">View Lessons</a>
                    </td>
                    <td><course-action @action-and-message-updated="handleActionData" :status="top_pick.runcourse_Status" :course="top_pick"></course-action></td>
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
      
        <div class="pt-5 container col-12" v-if="showRegistrationJustForYou">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Just For You</h1>
          <div class="table-responsive" v-if="registration_justforyou && registration_justforyou.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Name', 'registration_justforyou')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'run_Name'" :sortDirection="getSortDirection('run_Name')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'registration_justforyou')">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                  <th scope="col">
                      <a href="" class="register_others text-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'registration_justforyou')">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'registration_justforyou')">Closing Date <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Lessons</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(reg_course, key) in displayedRegCourseOthers" :key="key">
                  <td class="name">
                    <course-name-desc :name="reg_course.run_Name" :category="reg_course.coursecat_Name" :description="reg_course.course_Desc"></course-name-desc>
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
                  <td>
                    <a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis" @click="viewLessons(reg_course.rcourse_ID)">View Lessons</a>
                  </td>
                  <td><course-action @action-and-message-updated="handleActionData" :status="reg_course.runcourse_Status" :course="reg_course"></course-action></td>
                  
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="registration_justforyou=[]" class="text-center pt-2 pb-5">
              <p>Currently, there are no recommendations for you.</p>
              <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseOthers" v-if="registration_justforyou.length/itemsPerPage > 0 && showRegistrationJustForYou" :totalItems="registration_justforyou.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeRegCourseOthers" class="justify-content-center pagination-container"/>

        <div class="pt-5 container col-12" v-if="showRegistratonOthers">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1>
          <div class="table-responsive" v-if="registration_others && registration_others.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Name', 'registration_others')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'run_Name'" :sortDirection="getSortDirection('run_Name')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'registration_others')">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'registration_others')">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'registration_others')">Closing Date <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Lessons</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(reg_course, key) in displayedRegCourseForYou" :key="key">
                  <td class="name">
                    <course-name-desc :name="reg_course.run_Name" :category="reg_course.coursecat_Name" :description="reg_course.course_Desc"></course-name-desc>
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
                  <td>
                    <a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis" @click="viewLessons(reg_course.rcourse_ID)">View Lessons</a>
                  </td>
                  <td><course-action @action-and-message-updated="handleActionData" :status="reg_course.runcourse_Status" :course="reg_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="registration_others=[]" class="text-center pt-2 pb-5">
            <p>Currently, there are no recommendations for you.</p>
            <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentPageRegCourseForYou" v-if="registration_others.length/itemsPerPage > 0 && showRegistratonOthers" :totalItems="registration_others.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeRegCourseForYou" class="justify-content-center pagination-container"/>
      </div>

      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'express_interest' }">
        <div class="pt-5 container col-12" v-if="shouldShowTopInterestPicks">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Top Picks</h1>
          <div class="table-responsive" v-if="top_interest_picks && top_interest_picks.length > 0"> 
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
          
        
          <div class="pt-5 container col-12" v-if="showInterestsJustForYou">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Just For You</h1>
          <div class="table-responsive" v-if="interests_justforyou && interests_justforyou.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'interests_justforyou')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="sortDirection"/></a></th>
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
          <div v-else-if="interests_justforyou=[]" class="text-center pt-2 pb-5">
            <p>Currently, there are no recommendations for you.</p>
            <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestOthers" v-if="interests_justforyou.length/itemsPerPage > 0 && showInterestsJustForYou" :totalItems="interests_justforyou.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeInterestOthers" class="justify-content-center pagination-container"/>
      
        <div class="pt-5 container col-12" v-if="showInterestsOthers">
          <h1 class="recommendation-title pb-3 d-flex justify-content-center">Others Like You Also Like</h1> 
          <div class="table-responsive" v-if="interests_others && interests_others.length > 0"> 
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'interests_others')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="sortDirection"/></a></th>
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
          <div v-else-if="interests_others=[]" class="text-center pt-2 pb-5">
            <p>Currently, there are no recommendations for you.</p>
            <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Browse Course</router-link>
          </div>
        </div>
        <vue-awesome-paginate v-model="localCurrentInterestCourses" v-if="interests_others.length/itemsPerPage > 0 && showInterestsOthers" :totalItems="interests_others.length" :items-per-page="itemsPerPage" @page-change="handlePageTopInterestCourses" class="justify-content-center pagination-container"/>

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
      registration_others: [],
      registration_justforyou: [],
      interests_others: [],
      interests_justforyou: [],
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
      hideTopRegisterPicks: true,
      showRegistratonOthers: true,
      showRegistrationJustForYou: true,
      showInterestsOthers: true,
      showInterestsJustForYou: true,
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
      if (action == 'registration_others') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.registration_others)
         if (sort_response.code == 200) {
          this.registration_others = sort_response.data
         }
      }
      if (action == 'register_top') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.top_register_picks)
         if (sort_response.code == 200) {
          this.top_register_picks = sort_response.data
         }
      }
      if (action == 'registration_justforyou') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.registration_justforyou)
         if (sort_response.code == 200) {
          this.registration_justforyou = sort_response.data
         }
      }

      if (action == 'interests_others') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.interests_others)
         if (sort_response.code == 200) {
          this.interests_others = sort_response.data
         }
      }
      if (action == 'interest_top') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.top_interest_picks)
         if (sort_response.code == 200) {
          this.top_interest_picks = sort_response.data
         }
      }
      if (action == 'interests_justforyou') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.interests_justforyou)
         if (sort_response.code == 200) {
          this.interests_justforyou = sort_response.data
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
    async fetchTopPicksForRegistration() {
      const topRegisterPick = await Recommender.getTopPicksForRegistration(this.user_ID);
      this.top_register_picks = topRegisterPick.data;
    },
    async fetchTopPicksForVoting() {
      const topInterestPick = await Recommender.getTopPicksForVoting(this.user_ID);
      this.top_interest_picks = topInterestPick.data;
    },
    async fetchUserSimilarityRegistration() {
      const userRegister = await Recommender.getUserSimilarityRegistration(this.user_ID);
      if ( userRegister.code === 200 && userRegister.length !== 0) {
        this.showRegistratonOthers = true
        this.registration_others = userRegister.data.course_list
      } else {
        this.showRegistratonOthers = false
      }
    },
    async fetchUserRegisteredCourses() {
      const courseListReq = await Recommender.getUserRegisteredCourses(this.user_ID);
      if (courseListReq.code === 404) {
        this.showRegistrationJustForYou = false;
      } else {
        const courseRegister = await Recommender.getCourseSimilarityRegistration(courseListReq.data);
        console.log(courseRegister)
        if (courseRegister.code === 200 && courseRegister.length !== 0) {
          this.showRegistrationJustForYou = true
          this.registration_justforyou = courseRegister.data.course_list
        } else {
          this.showRegistrationJustForYou = false
        }
      }
    },
    async fetchUserSimilarityInterest() {
      const userInterest = await Recommender.getUserSimilarityInterest(this.user_ID);
      this.showInterestsOthers = userInterest.length !== 0;
      this.interests_others = this.showInterestsOthers ? userInterest.data.course_list : [];
    },
    async fetchInterestListRequest() {
      const interestListReq = await CourseService.searchCourseVoteInfo(this.user_ID, null, null, null);
      if (interestListReq.message === "No matching course interest information found") {
        this.showInterestsJustForYou = false;
      } else {
        const courseInterest = await Recommender.getCourseSimilarityInterest(interestListReq.data);
        this.showInterestsJustForYou = courseInterest.code === 200 && courseInterest.length !== 0;
        this.interests_justforyou = this.showInterestsJustForYou ? courseInterest.data.course_list : [];
      }
    },
    async loadData() {
      await this.fetchTopPicksForRegistration();
      await this.fetchTopPicksForVoting();
      await this.fetchUserSimilarityRegistration();
      await this.fetchUserRegisteredCourses();
      await this.fetchUserSimilarityInterest();
      await this.fetchInterestListRequest();
    },
    areCourseArraysEqual(arr1, arr2, idProperty) {
      return (
        Array.isArray(arr1) &&
        Array.isArray(arr2) &&
        arr1.length === arr2.length &&
        arr1.every(course1 =>
          arr2.some(course2 => course1[idProperty] === course2[idProperty])
        )
      );
    },
    updateRegistration() {
      const areArraysEqual = this.areCourseArraysEqual(this.registration_others, this.registration_justforyou,'rcourse_ID');

      if (areArraysEqual && this.registration_others.length > 0) {
        this.showRegistrationJustForYou = true; 
        this.showRegistratonOthers = false;     
        this.registration_others = [];      
      }

      if (this.registration_justforyou.length === 0 && this.registration_others.length === 0) {
         this.showRegistrationJustForYou = false; 
          this.showRegistratonOthers = false; 
      }
    },
    updateInterest() {
      const areArraysEqual = this.areCourseArraysEqual(this.interests_others, this.interests_justforyou, 'course_ID');

      if (areArraysEqual && this.interests_others.length > 0) {
        this.showInterestsJustForYou = true; 
        this.showInterestsOthers = false;    
        this.interests_others = [];  
      }

      if (this.interests_justforyou.length === 0 && this.interests_others.length === 0) {
         this.showInterestsJustForYou = false; 
          this.showInterestsOthers = false; 
      }
    },
    viewLessons(courseID) {
      this.$router.push({ name: 'viewRunCourseLesson', params: {id: courseID}});
    },
  },
  computed: {
    displayedRegCourseForYou() {
      const startIndex = (this.localCurrentPageRegCourseForYou - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.registration_others.slice(startIndex, endIndex);
    },
    displayedRegCourseOthers() {
      const startIndex = (this.localCurrentPageRegCourseOthers - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.registration_justforyou.slice(startIndex, endIndex);
    },
    displayedInterestOthers() {
      const startIndex = (this.localCurrentInterestOthers - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.interests_justforyou.slice(startIndex, endIndex);
    },
    displayedInterestCourses() {
      const startIndex = (this.localCurrentInterestCourses - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.interests_others.slice(startIndex, endIndex);
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
      this.updateRegistration();

      const isRegCoursesForYouEmpty = this.registration_others.length === 0;
      const isRegCoursesOthersEmpty = this.registration_justforyou.length === 0;

      if (this.top_register_picks && this.top_register_picks.length > 0 && (isRegCoursesForYouEmpty || isRegCoursesOthersEmpty)) {
        return true
      } else {
        return false
      }
    },
    shouldShowTopInterestPicks() {
      this. updateInterest();

      const isInterestCoursesForYouEmpty = this.interests_others.length === 0;
      const isInterestCoursesOthersEmpty = this.interests_justforyou.length === 0;

      if (this.top_interest_picks && this.top_interest_picks.length > 0 && (isInterestCoursesForYouEmpty || isInterestCoursesOthersEmpty)) {
        return true
      } else {
        return false
      }
    },
  },
  async created() {
    document.title = "Recommendations | Upskilling Engagement System";

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