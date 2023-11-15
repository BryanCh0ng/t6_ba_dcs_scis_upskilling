<template>
    <div id="createLesson">
        <div class="container pt-5">
            <h2 class="text-center mb-4">Add lesson(s) for {{ runcourse_Name }}</h2>
            <h5 class="text-center mb-4">From {{ convertDate(runcourse_Startdate) }} ({{ convertTime(runcourse_Starttime) }} - {{ convertTime(runcourse_Endtime) }}) to {{ convertDate(runcourse_Enddate) }} ({{ convertTime(runcourse_Starttime) }} - {{ convertTime(runcourse_Endtime) }})</h5>
            
            <div id="lesson_list" v-if="current_lessons_list && current_lessons_list.length > 0">
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
                            <tr v-for="(lesson, index) in current_lessons_list" :key="index">
                                <th scope="row">{{ index + 1 }}</th>
                                <td>{{ convertDate(lesson.lesson_Date) }}</td>
                                <td>{{ convertTime(lesson.lesson_Starttime) }}</td>
                                <td>{{ convertTime(lesson.lesson_Endtime) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <form @submit.prevent="onSubmit" @reset="onReset">
                <div v-for="(lessonForm, index) in formDataArray" :key="index" class="lesson-form mt-5">
                    <h5># {{ index + 1 }}</h5>
                    <!-- Lesson Date -->
                    <div class="form-group mt-2">
                        <label for="lessonDate" class="mb-2">Lesson Date</label>
                        <VueDatePicker v-model="lessonForm.lessonDate" id="lessonDate" placeholder="Lesson Date" :enable-time-picker="false" input-class-name="dp-custom-input" :format="lessonForm.datePickerFormat" required></VueDatePicker>
                    </div>
                    <!-- Lesson Start Time -->
                    <div class="form-group mt-4">
                        <label for="lessonStartTime" class="mb-2">Lesson Start Time</label>
                        <VueDatePicker v-model="lessonForm.lesson_Starttime"  id="lessonStartTime" placeholder="Lesson Start Time" time-picker required input-class-name="dp-custom-input">
                            <template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" />
                            </template>
                        </VueDatePicker>
                    </div>
                    <!-- Lesson End Time -->
                    <div class="form-group mt-4">
                        <label for="lessonEndTime" class="mb-2">Lesson End Time</label>
                        <VueDatePicker v-model="lessonForm.lesson_Endtime" id="lessonEndTime" placeholder="Lesson End Time" time-picker required input-class-name="dp-custom-input">
                            <template #input-icon>
                                <font-awesome-icon icon="fa-regular fa-clock" style="padding-left: 10px" />
                            </template>
                        </VueDatePicker>
                    </div>

                    <button type="button" class="btn btn-secondary mt-4 mb-2 col-12 field" @click="removeForm(index)">
                        Remove Lesson
                    </button>
                </div>

                <div>
                    <a href="#" @click.prevent="addForm" class="mt-5 d-flex justify-content-center text-dark">+ Add Lesson</a>
                </div>
                <div class="row mt-5 mb-5">
                    <div class="col-md-6 mb-2">
                        <button type="button" @click="goToPreviousPage" class="btn btn-block shadow-sm w-100 mt-2 field submitbtn" title="Cancel">Cancel</button>
                    </div>
                    <div class="col-md-6 mb-2">
                        <button type="submit" class="btn btn-block shadow-sm w-100 mt-2 field submitbtn" title="Add Lesson(s)">Add Lesson(s)</button>
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

function showSuccessMessage(vm) {
  vm.title = "Added Lesson(s) Successfully";
  vm.message = "You have successfully add lesson(s) for the run course.";
  vm.showAlert = true;
  vm.buttonType = "success";
  vm.modalType = "SuccessMessage"
}

function showUnsuccessMessage(vm, customTitle, customMessage) {
    vm.title = customTitle;
    vm.message = customMessage;
    vm.showAlert = true;
    vm.buttonType = "danger";
    vm.modalType = "UnsuccessMessage"
}

export default {
    name: "CreateRunCourseLesson",
    setup() {
        const v$ = useVuelidate();
        return { v$ };
    },
    data() {
        return {
            // Title
            runcourse_Name: "",
            runcourse_Startdate: null,
            runcourse_Enddate: null,
            runcourse_Starttime: null,
            runcourse_Endtime: null,
            current_lessons_list: [],
            // Lesson Forms Array
            formDataArray: [
                { // Initial form data object
                    datePickerFormat: "dd/MM/yyyy",
                    lessonDate: null,
                    lesson_Starttime: null,
                    lesson_Endtime: null,
                }
            ],
            lesson_no: 1,
            errorMsg: [],
            // Modal
            title: "",
            message: "",
            buttonType: "",
            showAlert: false,
        };
    },
    components: {
        VueDatePicker,
        DefaultModal
    },
    async created() {
        document.title = "Add Lesson | Upskilling Engagement System";

        const runcourse_id = this.$route.params.id;
        const runcourse_info = await runCourseService.getRunCourseById(runcourse_id);
        
        if (runcourse_info) {
            this.runcourse_Name = runcourse_info.run_Name;
            this.runcourse_Startdate = runcourse_info.run_Startdate;
            this.runcourse_Enddate = runcourse_info.run_Enddate;
            this.runcourse_Starttime = runcourse_info.run_Starttime;
            this.runcourse_Endtime = runcourse_info.run_Endtime;
        }

        await this.fetchExistingLessonList(runcourse_id);
    },
    methods: {
        convertDate,
        convertTime,
        async fetchExistingLessonList(rcourse_ID) {
            try {
                const response = await LessonService.getRunCourseById(rcourse_ID);
                this.current_lessons_list = response.lessons;
            } catch (error) {
                console.error("Failed to fetch lessons", error);
            }
        },
        addForm() {
            this.formDataArray.push({
                datePickerFormat: "dd/MM/yyyy",
                lessonDate: null,
                lesson_Starttime: null,
                lesson_Endtime: null,
            });
        },
        removeForm(index) {
            if (this.formDataArray.length > 1) {
                this.formDataArray.splice(index, 1);
            }
        },
        goToPreviousPage() {
            this.$router.go(-1);
        },
        async onSubmit() {
            try {
                const isValid = this.validateLessonDates();
                const isLessonDatesUnique = this.areLessonDatesUnique();
                const isLessonTimesValid = this.isLessonTimeValid();

                if (!isValid || !isLessonDatesUnique || !isLessonTimesValid) {
                    return;
                }

                const lessonsToAdd = this.formDataArray.map(lessonForm => {
                    return {
                        rcourse_ID: this.$route.params.id,
                        lesson_Date: lessonForm.lessonDate.toISOString().split('T')[0],
                        lesson_Starttime: `${lessonForm.lesson_Starttime.hours}:${lessonForm.lesson_Starttime.minutes}:${lessonForm.lesson_Starttime.seconds}`,
                        lesson_Endtime: `${lessonForm.lesson_Endtime.hours}:${lessonForm.lesson_Endtime.minutes}:${lessonForm.lesson_Endtime.seconds}`,
                    };
                });

                for (const lessonData of lessonsToAdd) {
                    await LessonService.addLesson(lessonData);
                }
                
                showSuccessMessage(this);
            } catch (error) {
                const customTitle = "Added Lesson(s) Unsuccessful";
                const customMessage = "We have failed to add lesson(s) for the run course.";
                showUnsuccessMessage(this, customTitle, customMessage);
                console.error("Failed to submit lessons", error);
            }
        },

        validateLessonDates() {
            
            const startDate = new Date(this.runcourse_Startdate);
            const endDate = new Date(this.runcourse_Enddate);

            for (const lessonForm of this.formDataArray) {
                const lessonDate = new Date(lessonForm.lessonDate);

                if (lessonDate < startDate || lessonDate > endDate) {
                    
                    const customTitle = "Invalid Lesson Date";
                    const customMessage = "The lesson date must be within or equal to the run course date range.";
                    showUnsuccessMessage(this, customTitle, customMessage);
                    return false;
                }
            }

            return true;
        },

        isLessonTimeValid() {
            const runcourseStarttimeString = this.runcourse_Starttime;
            const runcourseStarttime = new Date();
            runcourseStarttime.setHours(...runcourseStarttimeString.split(':').map(Number));

            const runcourseEndtimeString = this.runcourse_Endtime;
            const runcourseEndtime = new Date();
            runcourseEndtime.setHours(...runcourseEndtimeString.split(':').map(Number)); 

            for (const lessonForm of this.formDataArray) {
        
                const lessonStartTime = new Date();
                lessonStartTime.setHours(lessonForm.lesson_Starttime.hours, lessonForm.lesson_Starttime.minutes, lessonForm.lesson_Starttime.seconds);

                const lessonEndTime = new Date();
                lessonEndTime.setHours(lessonForm.lesson_Endtime.hours, lessonForm.lesson_Endtime.minutes, lessonForm.lesson_Endtime.seconds);

                
                if (lessonStartTime.getTime() === lessonEndTime.getTime()) {
                    const customTitle = "Invalid Lesson Times";
                    const customMessage = "The lesson start time cannot be the same as the lesson end time.";
                    showUnsuccessMessage(this, customTitle, customMessage);
                    return false;
                }
                
                if (lessonStartTime < runcourseStarttime) {
                    const customTitle = "Invalid Lesson Start Time";
                    const customMessage = "The lesson start time must be after or equal to the run course start time.";
                    showUnsuccessMessage(this, customTitle, customMessage);
                    return false;
                }

                if (lessonEndTime > runcourseEndtime) {
                    const customTitle = "Invalid Lesson End Time";
                    const customMessage = "The lesson end time must be before or equal to the run course end time.";
                    showUnsuccessMessage(this, customTitle, customMessage);
                    return false;
                }
            }

            return true;
        },

        areLessonDatesUnique() {
            const lessonDates = this.formDataArray.map(lessonForm => lessonForm.lessonDate.toISOString().split('T')[0]);

            const uniqueLessonDates = [...new Set(lessonDates)];

            if (uniqueLessonDates.length !== this.formDataArray.length) {
                const customTitle = "Duplicate Lesson Dates";
                const customMessage = "Lesson dates must be unique across all lessons.";
                showUnsuccessMessage(this, customTitle, customMessage);
                return false;
            }

            for (const lessonDate of lessonDates) {
                if (this.current_lessons_list.some(lesson => lesson.lesson_Date === lessonDate)) {
                    const customTitle = "Lesson Date Already Exists";
                    const customMessage = "A lesson with the same date already exists in the current lesson list.";
                    showUnsuccessMessage(this, customTitle, customMessage);
                    return false;
                }
            }

            return true;
        },

        async handleModalClosed(value) {
            this.showAlert = value;
            
            if (this.modalType === "UnsuccessMessage") {
                this.showAlert = false;
            } else if (this.modalType === "SuccessMessage") {
                this.$router.go(-1);
            }
        }

    },
}
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
</style>