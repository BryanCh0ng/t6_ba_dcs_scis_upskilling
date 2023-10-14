import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class runCourseService extends BaseApiService {
  async getAllRunCourses(courseId) {
    try {
      let courses = await axiosClient.get("/runcourse/get_all_runcourses", {params: {course_id: courseId}});
      return courses.data
    } catch (error) {
      return this.handleError(error);
    }
  }
  async getRunCourseByCourseId(courseId) {
    try {
      let run_course = await axiosClient.get("/runcourse/get_run_course_by_course_id", { params: { course_id: courseId } });
      return run_course.data

    } catch (error) {
      return this.handleError(error);
    }
  }
  async editRunCourse(runcourseId, updatedData) {
    try {
        let response = await axiosClient.put(`/runcourse/edit_runcourse/${runcourseId}`, updatedData);
        return response.data;

    } catch (error) {
        return this.handleError(error)
    }
  }
  async createRunCourse(courseId, newRunCourseData) {
    try {
      let response = await axiosClient.post(`/runcourse/create_runcourse/${courseId}`, newRunCourseData);
      return response.data;
    } catch (error) {
      return this.handleError(error);
    }
  }
  async getRunCourseById(runcourseId) {
    try {
        let runcourse = await axiosClient.get("/runcourse/get_runcourse_by_id", { params: { runcourse_id: runcourseId } });
        return runcourse.data

    } catch (error) {
        return this.handleError(error);
     }
  }
  async changeRegistrationStatus(updatedData) {
    try {
      let response = await axiosClient.post("/runcourse/change_registration_status", updatedData);
      console.log(response)
      return response.data
    } catch (error) {
      return this.handleError(error);
    }
  }
  async getCourseFormats() {
    try {
        let response = await axiosClient.get("/runcourse/get_course_formats");
        return response.data 
  
    } catch (error) {
        return this.handleError(error);
     }
  }
}

export default new runCourseService();