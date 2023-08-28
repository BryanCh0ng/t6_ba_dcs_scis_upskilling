<template>
  <div id="default">
    <div class="container">
      <h3 class="m-5">Edit Course</h3>

      <form>
        <div class="form-floating mb-3 m-5">
          <input
            type="Course ID"
            class="form-control"
            id="floatingInput"
            v-model="courseDetails.course_ID"
          />
          <label for="floatingInput">Course ID</label>
        </div>
        <div class="form-floating mb-3 m-5">
          <input
            type="Course Name"
            class="form-control"
            id="floatingInput"
            v-model="courseDetails.course_Name"
          />
          <label for="floatingInput">Course Name</label>
        </div>
        <div class="form-floating mb-3 m-5">
          <input
            type="Course Category"
            class="form-control"
            id="floatingInput"
            v-model="courseDetails.course_Category"
          />
          <label for="floatingInput">Course Category</label>
        </div>

        <div class="form-floating mb-3 m-5">
          <textarea
            class="form-control"
            placeholder="Course Description"
            id="floatingTextarea2"
            style="height: 100px"
            v-model="courseDetails.course_Desc"
          ></textarea>
          <label for="floatingTextarea2">Course Description</label>
        </div>
        <div class="mb-3 m-5">
          <strong
            ><label for="formGroupExampleInput2" class="form-label"
              >Select Course Type</label
            ></strong
          >
          <select
            class="form-select"
            aria-label="Select Course Type"
            v-model="courseDetails.course_Type"
          >
            <option value="1" disabled>-</option>
            <option value="Internal">Internal</option>
            <option value="External">External</option>
          </select>
        </div>

        <div class="mb-3 m-5">
          <strong
            ><label for="formGroupExampleInput2" class="form-label"
              >Select Skills for Course</label
            ></strong
          >
          <br />
          <div v-if="selectedSkills[0] != ''">
            <span
              v-for="selectedSkill in selectedSkills"
              :key="selectedSkill"
              class="badge m-1 mb-2"
              style="background-color: #81aabe"
              >{{ selectedSkill
              }}<button
                type="button"
                class="btn-close btn-close-white"
                @click="unselectSkill(selectedSkill)"
              ></button
            ></span>
          </div>

          <select
            class="form-select"
            aria-label="Select Skills"
            multiple
            v-model="selectedSkills"
          >
            <option v-for="skill in skillList" :key="skill">
              {{ skill.skill_Name }}
            </option>
          </select>
        </div>

        <button
          type="button"
          class="btn btn-colour-1 mx-6 m-5"
          @click="editCourse(courseDetails) && $router.push(`/course/${courseDetails.course_ID}`)"
        >
          Edit
        </button>
      </form>
    </div>
  </div>
</template>

<script>

import CourseService from "@/api/services/CourseService";

export default {
  name: "EditCourseForm",
  data() {
    return {
      courseDetails: Object,
      
      courseId: this.$route.params.course_id,
      
    };
  },
  mounted() {
    this.getCourseById(this.courseId);
    this.getAllSkills();
  },
  methods: {
    async getCourseById(courseId) {
      const course = await CourseService.getCourseById(courseId);
      this.courseDetails = course;
      
    },
    
    async editCourse(courseDetails) {
      
      let response = await CourseService.editCourse(courseDetails);
      this.courseDetails = response.data;
    },
  },
};
</script>


<style scoped>
.btn-colour-1 {
  color: #ffffff;
  background-color: #5f7abf;
  /* border-color: #668fe0; */
  font-weight: 450;
  border-radius: 50;
}

.btn-colour-1:hover,
.btn-colour-1:active,
.btn-colour-1:focus,
.btn-colour-1.active {
  background: #3a58a6;
  color: #fff;
  /* border-color: #4f6db9; */
}
</style>
