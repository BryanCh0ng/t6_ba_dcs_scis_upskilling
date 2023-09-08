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

  async updateProposedCourse(courseId, courseData) {
    try {
      const apiUrl = `/proposedcourse/update_proposed_course/${courseId}`;
      const response = await axiosClient.put(apiUrl, courseData);

      if (response.status === 200) {
        return { success: true, message: response.data.message };
      } else {
        return { success: false, message: 'Failed to update the proposed course' };
      }
    } catch (error) {
      console.error('Error updating proposed course:', error);
      return { success: false, message: 'An error occurred while updating the proposed course' };
    }
  }

  async removeProposedCourse(pcourse_ID) {
    try {
      console.log(pcourse_ID)
      let response = await axiosClient.delete("/proposedcourse/delete_proposed_course", { params: { pcourse_ID: pcourse_ID } });
      console.log("delete")
      return response.data;
    } catch (error) {
      console.log("delete111")
      return this.handleError(error);
    }
  }

  async rejectProposedCourse(updatedData) {
    try {
      let response = await axiosClient.post("/proposedcourse/reject_proposed_course", updatedData);
        return response.data;
    } catch (error) {
        return this.handleError(error)
    }
  }

  async approveProposedCourse(updatedData) {
    try {
      let response = await axiosClient.post("/proposedcourse/approve_proposed_course", updatedData);
        return response.data;
    } catch (error) {
        return this.handleError(error)
    }
  }
  
}

export default new ProposedCourseService();