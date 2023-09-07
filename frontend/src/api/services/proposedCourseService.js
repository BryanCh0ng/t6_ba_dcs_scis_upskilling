import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class ProposedCourseService extends BaseApiService {
  async getAllProposedCourses(courseId) {
    try {
      let courses = await axiosClient.get("/proposedcourse/get_all_proposedcourses", {params: {course_id: courseId}});
      return courses.data
    } catch (error) {
      return this.handleError(error);
    }
  }
  async getProposedCourseByCourseId(courseId) {
    try {
      let proposed_course = await axiosClient.get("/proposedcourse/get_proposed_course_by_course_id", { params: { course_id: courseId } });
      return proposed_course.data
    } catch (error) {
      return this.handleError(error);
    }
  }
  async getProposedCourseByStatus(pcourse_status) {
    try {
      let proposed_course_by_status = await axiosClient.get("/proposedcourse/get_proposed_course_by_pcourse_status", { params: { pcourse_status: pcourse_status } });
      return proposed_course_by_status.data
    } catch (error) {
      return this.handleError(error);
    }
  }
  async createProposedCourse(newProposedCourseData) {
    try {
      let response = await axiosClient.post('/proposedcourse/create_proposed_course', newProposedCourseData);
      return response.data;
    } catch (error) {
      return this.handleError(error);
    }
  } 
}

export default new ProposedCourseService();