<template>
    <div>
      <div class="container col-12 d-flex mb-3 w-100">
        <div v-if="attendances && attendances.length > 0">
            <h5 class="col m-auto">Attendance List for {{ attendances[0].run_Name }}</h5>
            <h6 class="col m-auto text-grey">Date: {{ convertDate(lesson.lesson_Date) }} | Time: {{ convertTime(lesson.lesson_Starttime) }} to {{ convertTime(lesson.lesson_Endtime) }} | Venue: {{ lesson.course_Venue }}</h6>
        </div>
        <div class="v-else">
          <h5 class="col m-auto">Attendance List</h5>
        </div>
      </div>

      <div class="container col-12">
        <div v-if="attendances && attendances.length > 0" class="table-responsive">
          <table class="mt-2 table bg-white">
            <thead>
              <tr class="text-nowrap">
                <th><input type="checkbox" v-model="checkboxAll" @change="checkAll" /></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('user_ID')" class="text-decoration-none text-dark">Student ID <sort-icon :sortColumn="sortColumn === 'user_ID'" :sortDirection="getSortDirection('user_ID')"/></a></th>
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
              <tr v-for="(attendance, key) in this.attendances" :key="key">
                <td>
                  <input v-if="attendance.status == 'Pending'" type="checkbox" v-model="attendanceCheck[attendance.user_ID]" />
                </td>
                <td>{{ attendance.user_ID }}</td>
                <td>{{ attendance.user_Name }}</td>
                <td>{{ attendance.user_Email }}</td>
                <td>{{ attendance.status }}</td>
                <td>{{ attendance.reason }}</td>
              </tr>               
            </tbody>
          </table>
          <div class="row mb-5 pb-4 bg-white">
            <div class="col-lg-2 d-lg-flex d-block align-items-center mt-4">
                <p class="m-auto text-center">1 item selected</p>
            </div>
            <div class="row pt-lg-0 pt-3 col-lg-5 mt-4 d-flex justify-content-evenly">
                <div class="row col-12">
                    <button class="col btn attendance-btn btn-outline-success text-dark">Present</button>
                    <button class="col btn attendance-btn btn-outline-danger text-dark">Absent</button>
                    <button class="col btn attendance-btn btn-outline-warning text-dark">Late</button>
                </div>
            </div>
            <div class="row pt-lg-0 pt-3 col-lg-5 mt-4 d-flex justify-content-evenly">
              <div class="row col-12">
                <button class="col btn btn-success">Submit</button>
                <button class="col btn btn-secondary">Cancel</button>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="attendances=[]">
          <p>No records found</p>
        </div>
      </div>
    </div>
</template>
  
<script>
  import sortIcon from '@/components/common/sort-icon.vue';
  import CommonService from "@/api/services/CommonService.js";
  import UserService from "@/api/services/UserService.js";
  import AttendanceService from "@/api/services/AttendanceService.js";
  import LessonService from "@/api/services/LessonService.js";
  import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'

  export default {
    components: {
      sortIcon
    },
    data() {
      return {
        attendances: [],
        lesson: {},
        sortColumn: '',
        sortDirection: 'asc',
        receivedMessage: '',
        attendanceCheck: {},
        checkboxAll: false
      }
    },
    methods: {
      async loadData() {
        try {
          const lessonId = this.$route.params.lessonId;
          console.log(lessonId)
          let response = await AttendanceService.getAttendanceByLessonId(lessonId)
          console.log(response)
          if (response.code == 200) {
            this.attendances = response.attendances
          }
          let lesson_response = await LessonService.getLessonById(lessonId)
          console.log(lesson_response)
          if (lesson_response.code == 200) {
            this.lesson = lesson_response.lesson;
          }
        } catch (error) {
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
        this.attendanceCheck = {};
        if (this.checkboxAll) {
        this.attendances.forEach((attendance) => {
            if (attendance.status === 'Pending') {
            this.$set(this.attendanceCheck, attendance.user_ID, true);
            }
        });
        }
      },
      convertDate,
      convertTime,
    },
    async created() {
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