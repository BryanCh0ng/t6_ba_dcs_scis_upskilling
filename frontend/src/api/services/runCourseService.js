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
}

export default new runCourseService();