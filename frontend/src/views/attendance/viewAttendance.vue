<template>
    <div>
      <div class="container pt-5 col-12 d-flex mb-3 w-100">
        <div v-if="attendances && attendances.length > 0">
            <h5 class="col m-auto">Attendance List for {{ attendances[0].run_Name }}</h5>
            <h6 class="col m-auto text-grey">Date: {{ convertDate(lesson.lesson_Date) }} | Time: {{ convertTime(lesson.lesson_Starttime) }} to {{ convertTime(lesson.lesson_Endtime) }} | Venue: {{ lesson.course_Venue }} | Class Size: {{ this.attendances.length }}</h6>
        </div>
        <div v-else>
          <h5 class="col m-auto">Attendance List</h5>
        </div>
      </div>

      <div class="container col-12">
        <div v-if="attendances && attendances.length > 0" class="table-responsive">
          <table class="mt-2 table bg-white">
            <thead>
              <tr class="text-nowrap">
                <th><input v-if="allowAction" type="checkbox" v-model="checkboxAll" @change="checkAll" /></th>
                <th></th>
                <!-- <th scope="col">
                  <a href="" @click.prevent="sort('user_ID')" class="text-decoration-none text-dark">Student ID <sort-icon :sortColumn="sortColumn === 'user_ID'" :sortDirection="getSortDirection('user_ID')"/></a></th> -->
                <th scope="col">
                  <a href="" @click.prevent="sort('user_Name')" class="text-decoration-none text-dark">Student Name <sort-icon :sortColumn="sortColumn === 'user_Name'" :sortDirection="getSortDirection('user_Name')"/></a></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('user_Email')" class="text-decoration-none text-dark">Student Email <sort-icon :sortColumn="sortColumn === 'user_Email'" :sortDirection="getSortDirection('user_Email')"/></a></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('status')" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'status'" :sortDirection="getSortDirection('status')"/></a></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('reason')" class="text-decoration-none text-dark">Reason <sort-icon :sortColumn="sortColumn === 'reason'" :sortDirection="getSortDirection('reason')"/></a></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(attendance, key) in this.attendances" :key="key" @click="selectAttendance(key)">
                <td class="attendance_checkbox">
                  <input v-if="allowAction" type="checkbox" :value="attendance.user_ID" :checked="selectedStudents.includes(attendance.user_ID)" @change="selectAttendance(key)" />
                </td>
                <td>{{ key }}</td>
                <!-- <td>{{ attendance.user_ID }}</td> -->
                <td>{{ attendance.user_Name }}</td>
                <td>{{ attendance.user_Email }}</td>
                <td><course-status :status="attendance.status"></course-status></td>
                <td>{{ attendance.reason }}</td>
              </tr>               
            </tbody>
          </table>
          <div class="row pb-4 bg-white" v-if="allowAction">
            <div class="col-lg-2 d-lg-flex d-block align-items-center mt-4">
                <p class="m-auto text-center">{{ this.selectedStudents.length }} Student(s) selected</p>
            </div>
            <div class="row pt-lg-0 pt-3 col-lg-5 mt-4 d-flex justify-content-evenly">
              <div class="row col-12">
                <button class="m-1 col btn attendance-btn btn-outline-success text-dark" :class="{ 'bg-medium-sea-green text-white': action === 'Present' }"  @click="setAttendance('Present')">Present</button>
                <button class="m-1 col btn attendance-btn btn-outline-danger text-dark"  :class="{ 'btn-danger text-white': action === 'Absent' }"  @click="setAttendance('Absent')">Absent</button>
              </div>
            </div>
            <div class="row pt-lg-0 pt-3 col-lg-5 mt-4 d-flex justify-content-evenly">
              <div class="row col-12">
                <button class="m-1 col btn btn-success"  @click="submitAttendance">Submit</button>
                <button class="m-1 col btn btn-secondary" @click="cancelAttendance">Cancel</button>
              </div>
            </div>
          </div>
          <div class="row pb-4 bg-white mb-5" v-if="action === 'Absent' && allowAction">
            <div class="col-12 d-flex justify-content-center">
              <select class="w-50 form-control-lg mt-2" v-model="selectedAbsentReason" @change="handleselectAbsentReason">
                <option value="Medical Leave">Medical Leave</option>
                <option value="Family Matters">Family Matters</option>
                <option value="Personal Reason">Personal Reasons</option>
                <option value="Others">Others</option>
              </select>
            </div>
            <div v-if="othersSelected" class="col-12 d-flex justify-content-center">
              <input type="text" v-model="reasonInput" placeholder="Enter Reason" class="form-control-lg mt-2">
            </div>
          </div>
        </div>
        <div v-else-if="attendances=[]">
          <p>No records found</p>
        </div>
      </div>
      <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed"/>
    </div>
</template>
  
<script>
  import sortIcon from '@/components/common/sort-icon.vue';
  import CommonService from "@/api/services/CommonService.js";
  import UserService from "@/api/services/UserService.js";
  import AttendanceService from "@/api/services/AttendanceService.js";
  import LessonService from "@/api/services/LessonService.js";
  import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js';
  import DefaultModal from "@/components/DefaultModal.vue";
  import courseStatus from '../../components/course/courseStatus.vue';

  export default {
    components: {
      sortIcon,
      courseStatus,
      DefaultModal
    },
    data() {
      return {
        attendances: [],
        lesson: {},
        sortColumn: '',
        sortDirection: 'asc',
        receivedMessage: '',
        attendanceCheck: {},
        checkboxAll: false,
        selectedStudents: [],
        action: null,
        selectedAbsentReason: 'Medical Leave',
        othersSelected: false,
        reasonInput: '',
        title: "",
        message: "",
        buttonType: "",
        showAlert: false,
        allowAction: false,
      }
    },
    methods: {
      async loadData() {
        try {
          const lessonId = this.$route.params.lessonId;
          let response = await AttendanceService.getAttendanceByLessonId(lessonId)
          console.log(response)
          if (response.code == 200) {
            this.attendances = response.attendances;
            const instructor_id = this.attendances[0].instructor_ID;
            const user_ID = await UserService.getUserID();
            if (instructor_id == user_ID) {
              this.allowAction = true;
            } else {
              this.message = 'Unable to mark attendance as user logged in is not instructor of this lesson.';
              this.buttonType = "danger";
              this.showAlert = !this.showAlert;
            }
          }
          let lesson_response = await LessonService.getLessonById(lessonId)
          console.log(lesson_response)
          if (lesson_response.code == 200) {
            this.lesson = lesson_response.lesson;
            if (!this.hasLessonStarted(this.lesson.lesson_Date, this.lesson.lesson_Starttime) && this.message != 'Unable to mark attendance as user logged in is not instructor of this lesson.') {
              this.message = 'Unable to mark attendance as is not during lesson datetime';
              this.buttonType = "danger";
              this.showAlert = !this.showAlert;
              this.allowAction = false;
            }
          }
        } catch (error) {
          this.title = 'View Attendance Failed';
          this.message = error.response.data.message;
          this.buttonType = "danger";
          this.showAlert = !this.showAlert;
          console.error("Error fetching attendance records", error);
        }
      },
      sort(column) {
        if (this.sortColumn === column) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortColumn = column;
          this.sortDirection = 'asc';
        }
        this.sortAttendance()
      },
      getSortDirection(column) {
        if (this.sortColumn === column) {
          return this.sortDirection;
        }
      },
      async sortAttendance() {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.attendances)
          if (sort_response.code == 200) {
            this.attendances = sort_response.data
          }
      },
      checkAll() {
        setTimeout(() => {
          if (this.checkboxAll) {
            this.selectedStudents = this.attendances
              .map(attendance => attendance.user_ID);
          } else {
            this.selectedStudents = [];
          }
        }, 0);
      },
      hasLessonStarted(lessonDate, lessonTime) {
        const selectedDate = new Date(lessonDate);
        const currentTime = new Date();
        const [hours, minutes, seconds] = lessonTime.split(':').map(Number);
        const targetDateTime = new Date(selectedDate);
        targetDateTime.setHours(hours, minutes, seconds);
        const isSameDay = selectedDate.toDateString() === currentTime.toDateString();
        return isSameDay && targetDateTime <= currentTime;
      },
      convertDate,
      convertTime,
      selectAttendance(key){
        const user_ID = this.attendances[key].user_ID;
        if (this.selectedStudents.includes(user_ID)) {
          const index = this.selectedStudents.indexOf(user_ID);
          if (index !== -1) {
            this.selectedStudents.splice(index, 1);
          }
        } else {
          this.selectedStudents.push(user_ID);
        }
      },
      setAttendance(value) {
        this.action = value;
      },
      async submitAttendance() {
        const instructor_id = this.attendances[0].instructor_ID;
        const user_ID = await UserService.getUserID();
        if (this.selectedStudents.length == 0) {
          this.title = 'Submit Attendance Failed';
          this.message = 'Please select at least 1 student to submit attendance.';
          this.buttonType = "danger";
          this.showAlert = !this.showAlert;
        } else if (this.action == null) {
          this.title = 'Submit Attendance Failed';
          this.message = 'Please select if student(s) are present or absent before submitting attendance';
          this.buttonType = "danger";
          this.showAlert = !this.showAlert;
        } else if (this.selectedAbsentReason == 'Others' && this.reasonInput == '') {
          this.title = 'Submit Attendance Failed';
          this.message = 'Please include absent reason';
          this.buttonType = "danger";
          this.showAlert = !this.showAlert;
        } else if (instructor_id != user_ID) {
          this.title = 'Submit Attendance Failed';
          this.message = 'Unable to mark attendance as user logged in is not instructor of this lesson.';
          this.buttonType = "danger";
          this.showAlert = !this.showAlert;
        }  else { 
          const lessonId = this.$route.params.lessonId;
          try {
            let submit_attendance_response = await AttendanceService.updateAttendanceByLessonId(lessonId, this.selectedStudents, this.action, this.selectedAbsentReason, this.reasonInput)
            console.log(submit_attendance_response)
            if (submit_attendance_response.code == 200) {
              this.title = 'Submit Attendance Success';
              this.message = submit_attendance_response.message
              this.buttonType = "success";
              this.showAlert = !this.showAlert;
            } else {
              this.title = 'Submit Attendance Failed';
              this.message = submit_attendance_response.message
              this.buttonType = "danger";
              this.showAlert = !this.showAlert;
            }
          } catch (error) {
            this.message = error.response.data.message;
            this.buttonType = "danger";
            this.showAlert = !this.showAlert;
          }
        }
      },
      cancelAttendance() {
        this.selectedStudents = [];
      },
      handleselectAbsentReason() {
        if (this.selectedAbsentReason === 'Others') {
          this.othersSelected = true;
        } else {
          this.othersSelected = false;
        }
      },
      handleModalClosed(value) {
        this.showAlert = value;
        if(this.title == 'Submit Attendance Success') {
          this.loadData();
        }
        console.log(value)
      },
    },
    async created() {
      document.title = "Attendance | Upskilling Engagement System";

      const user_ID = await UserService.getUserID();
      const role = await UserService.getUserRole(user_ID);
      if (role == 'Student') {
        this.$router.push({ name: 'studentViewCourse' }); 
      } else {
        this.loadData();
      }
    },
    }
</script>
  
<style scoped>
    .attendance-btn:hover{
        color: white !important;
    }
</style>