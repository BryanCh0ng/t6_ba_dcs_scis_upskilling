<template>
  <div id="editLesson">
    <div class="container pt-5">
      <h2 class="text-center mb-4">Edit Lesson for {{ runcourse_Name }}</h2>
      <h5 class="text-center mb-4">From {{ convertDate(runcourse_Startdate) }} ({{ convertTime(runcourse_Starttime) }} - {{ convertTime(runcourse_Endtime) }}) to {{ convertDate(runcourse_Enddate) }} ({{ convertTime(runcourse_Starttime) }} - {{ convertTime(runcourse_Endtime) }})</h5>

    <div id="lesson_list">
        <h5>Existing Lesson</h5>
        <div class="table-responsive">
            <table class="table bg-white">
                <thead>
                    <tr class="text-nowrap">
                        <th scope="col">Lesson</th>
                        <th scope="col">Date</th>                                
                        <th scope="col">Start Time</th>
                        <th scope="col">End Time</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(lesson, index) in allLessonForRunCourse" :key="index" :class="{'editing-row': isEditingLesson(lesson)}">
                        <th scope="row">{{ index + 1 }}</th>
                        <td>{{ convertDate(lesson.lesson_Date) }}</td>
                        <td>{{ convertTime(lesson.lesson_Starttime) }}</td>                                
                        <td>{{ convertTime(lesson.lesson_Endtime) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

      <form @submit.prevent="submitForm">
        <!-- Lesson Date -->
        <div class="form-group mt-5">
            <VueDatePicker v-model="lessonForm.lessonDate" placeholder="Lesson Date" :enable-time-picker="false" input-class-name="dp-custom-input" :format="lessonForm.datePickerFormat" required></VueDatePicker>
        </div>
        <!-- Lesson Start Time -->
        <div class="form-group mt-4">
            <VueDatePicker v-model="lessonForm.lesson_Starttime" placeholder="Lesson Start Time" :time-picker="true" required input-class-name="dp-custom-input" :format="lessonForm.timePickerFormat">
                <template #input-icon>
                    <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" />
                </template>
            </VueDatePicker>
        </div>
        
        <!-- Lesson End Time -->
        <div class="form-group mt-4">
            <VueDatePicker v-model="lessonForm.lesson_Endtime" placeholder="Lesson End Time" :time-picker="true" required input-class-name="dp-custom-input" :format="lessonForm.timePickerFormat">
                <template #input-icon>
                    <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" />
                </template>
            </VueDatePicker>
        </div>

        <div class="row mt-5 mb-5">
            <div class="col-md-6 mb-2">
                <button type="button" @click="cancelEdit" class="btn btn-block shadow-sm w-100 mt-2 field submitbtn" title="Cancel">Cancel</button>
            </div>
            <div class="col-md-6 mb-2">
                <button type="submit" class="btn btn-block shadow-sm w-100 mt-2 field submitbtn" title="Save Changes">Save Changes</button>
            </div>
        </div>
      </form>
    </div>
    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
  </div>
</template>

<script>
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { useVuelidate } from "@vuelidate/core";
import runCourseService from "@/api/services/runCourseService.js"
import LessonService from "@/api/services/LessonService.js"
import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'
import DefaultModal from "@/components/DefaultModal.vue";
import { parseISO, format } from 'date-fns';

// Utility function to show a success message
function showSuccessMessage(vm) {
  vm.title = "Update the lesson information successfully.";
  vm.message = "You have successfully updated the lesson information.";
  vm.showAlert = true;
  vm.buttonType = "success";
}

function showUnsuccessMessage(vm, customTitle, customMessage) {
    vm.title = customTitle;
    vm.message = customMessage;
    vm.showAlert = true;
    vm.buttonType = "danger";
    vm.modalType = "UnsuccessMessage"
}

export default {
    name: "EditRunCourseLesson",
    components: {
        VueDatePicker,
        DefaultModal
    },
    setup() {
        const v$ = useVuelidate();
        return { v$ };
    },
    data() {
        return {
            lesson_ID: null,
            runcourse_Name: '',
            runcourse_Startdate: null,
            runcourse_Enddate: null,
            runcourse_Starttime: null,
            runcourse_Endtime: null,

            lesson_info: {},
            lessonForm: {
                lessonDate: '',
                lesson_Starttime: '',
                lesson_Endtime: '',
                datePickerFormat: 'dd/MM/yyyy',
                timePickerFormat: 'HH:mm'
            },
            allLessonForRunCourse: [],
            showAlert: false,
            title: '',
            message: '',
            buttonType: 'success',
            modalType: ''
        };
    },
    async created() {
        this.lesson_ID = this.$route.params.id;
        await this.fetchLessonData(this.lesson_ID);
    },
    methods: {
        convertDate,
        convertTime,
        async fetchLessonData(lesson_ID) {
            let response = await LessonService.getLessonById(lesson_ID);
            this.lesson_info = response.lesson;

            const lessonDate = parseISO(this.lesson_info.lesson_Date);
            this.lessonForm.lessonDate = format(lessonDate, 'yyyy-MM-dd');

            if (this.lesson_info.lesson_Starttime) {
                const startTimeParts = this.lesson_info.lesson_Starttime.split(":");
                this.lessonForm.lesson_Starttime = { hours: parseInt(startTimeParts[0]), minutes: parseInt(startTimeParts[1]), seconds: 0 };
            }

            if (this.lesson_info.lesson_Endtime) {
                const endTimeParts = this.lesson_info.lesson_Endtime.split(":");
                this.lessonForm.lesson_Endtime = { hours: parseInt(endTimeParts[0]), minutes: parseInt(endTimeParts[1]), seconds: 0 };
            }

            const runcourse_info = await runCourseService.getRunCourseById(this.lesson_info.rcourse_ID);
            if (runcourse_info) {
                this.runcourse_Name = runcourse_info.run_Name;
                this.runcourse_Startdate = runcourse_info.run_Startdate;
                this.runcourse_Enddate = runcourse_info.run_Enddate;
                this.runcourse_Starttime = runcourse_info.run_Starttime;
                this.runcourse_Endtime = runcourse_info.run_Endtime;
            }

            let existing_lesson_list = await LessonService.getRunCourseById(this.lesson_info.rcourse_ID);
            this.allLessonForRunCourse = existing_lesson_list.lessons;
        },

        
        async submitForm() {
            const isValid = this.validateLessonDates();
            const isLessonDatesUnique = this.areLessonDatesUnique();
            const isLessonTimesValid = this.isLessonTimeValid();

            if (!isValid || !isLessonDatesUnique || !isLessonTimesValid) {
                return;
            }

            // Create Date objects from the time parts
            const lessonDate = new Date(this.lessonForm.lessonDate);
            const startTime = new Date(lessonDate);
            startTime.setHours(this.lessonForm.lesson_Starttime.hours);
            startTime.setMinutes(this.lessonForm.lesson_Starttime.minutes);
            const endTime = new Date(lessonDate);
            endTime.setHours(this.lessonForm.lesson_Endtime.hours);
            endTime.setMinutes(this.lessonForm.lesson_Endtime.minutes);

            // Format the date and time values appropriately
            const updateData = {
                lesson_ID: this.lesson_ID, // Make sure this is the correct ID for the lesson
                lesson_Date: format(lessonDate, 'yyyy-MM-dd'),
                formattedStartTime: format(startTime, 'HH:mm:ss'),
                formattedEndTime: format(endTime, 'HH:mm:ss')
            };

            try {
                // Call the updateLesson method from LessonService with the formatted data
                const response = await LessonService.updateLesson(this.lesson_ID, updateData);
                if (response.code == 200) {
                showSuccessMessage(this);
                } else {
                const customTitle = "Update Lesson Information Unsuccessful";
                const customMessage = "We have failed to update lesson information.";
                showUnsuccessMessage(this, customTitle, customMessage);
                }
            } catch (error) {
                const customTitle = "Update Lesson Information Unsuccessful";
                const customMessage = "We have failed to update lesson information.";
                showUnsuccessMessage(this, customTitle, customMessage);
            }
        },

        validateLessonDates() {
            const startDate = new Date(this.runcourse_Startdate);
            const endDate = new Date(this.runcourse_Enddate);
            const lessonDate = new Date(this.lessonForm.lessonDate);

            if (lessonDate < startDate || lessonDate > endDate) {
                const customTitle = "Invalid Lesson Date";
                const customMessage = "The lesson date must be within or equal to the run course date range.";
                showUnsuccessMessage(this, customTitle, customMessage);
                return false;
            }

            return true;
        },

        isLessonTimeValid() {
            const formatTime = (timeString) => {
                const [hours, minutes, seconds] = timeString.split(':').map(Number);
                const time = new Date();
                time.setHours(hours, minutes, seconds, 0);
                return time;
            };

            const runcourseStarttime = formatTime(this.runcourse_Starttime);
            const runcourseEndtime = formatTime(this.runcourse_Endtime);
            const lessonStartTime = formatTime(`${this.lessonForm.lesson_Starttime.hours}:${this.lessonForm.lesson_Starttime.minutes}:${this.lessonForm.lesson_Starttime.seconds}`);
            const lessonEndTime = formatTime(`${this.lessonForm.lesson_Endtime.hours}:${this.lessonForm.lesson_Endtime.minutes}:${this.lessonForm.lesson_Endtime.seconds}`);

            console.log(lessonStartTime)
            console.log(lessonEndTime)

            if (lessonStartTime.getTime() === lessonEndTime.getTime()) {
                showUnsuccessMessage(this, "Invalid Lesson Times", "The lesson start time cannot be the same as the lesson end time.");
                return false;
            }
            if (lessonStartTime < runcourseStarttime) {
                showUnsuccessMessage(this, "Invalid Lesson Start Time", "The lesson start time must be after or equal to the run course start time.");
                return false;
            }
            if (lessonEndTime > runcourseEndtime) {
                showUnsuccessMessage(this, "Invalid Lesson End Time", "The lesson end time must be before or equal to the run course end time.");
                return false;
            }

            return true;
        },

        areLessonDatesUnique() {
            const lessonDate = new Date(this.lessonForm.lessonDate).toISOString().split('T')[0];

            // Filter out the current lesson being edited from the existing lessons list
            const filteredLessons = this.allLessonForRunCourse.filter((lesson) => lesson.lesson_ID !== parseInt(this.lesson_ID));

            if (filteredLessons.some((lesson) => lesson.lesson_Date === lessonDate)) {
                showUnsuccessMessage(this, "Lesson Date Already Exists", "A lesson with the same date already exists in the current lesson list.");
                return false;
            }

            return true;
        },
        isEditingLesson(lesson) {
            console.log(lesson.lesson_ID === parseInt(this.lesson_ID))
            return lesson.lesson_ID === parseInt(this.lesson_ID);
        },
        cancelEdit() {
            this.$router.go(-1);
        },
        handleModalClosed(value) {
            this.showAlert = value;
            if (this.modalType === "UnsuccessMessage") {
                this.showAlert = false;
            } else {
                this.$router.go(-1);
            }
        }
    },

};
</script>

<style lang="scss">
.dp-custom-input {
    border-color: transparent;
    font-size: 18px;
    height: 50px;
    border-radius: 10px;
    &:hover {
        border-color: transparent;
    }
    &::placeholder {
        color: black;
    }
}

.editing-row,
.editing-row th,
.editing-row td {
    color: red !important;
}
</style>
