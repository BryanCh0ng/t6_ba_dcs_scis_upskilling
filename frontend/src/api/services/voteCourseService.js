import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class VoteCourseService extends BaseApiService {

  async adminUpdateVoteCourseStatusToOffered(updatedData) {
    try {
      console.log(updatedData)
      let response = await axiosClient.post("/votecourse/update_vote_course_status_to_offered", updatedData);
      return response.data;
    } catch (error) {
      return { success: false, message: 'An error occurred while updating the vote course' };
    }
  }

  async getVoteCourseByCourseId(courseId) {
    try {
      let vote_course = await axiosClient.get("/votecourse/get_vote_course_by_course_id", { params: { course_id: courseId } });
      return vote_course.data
    } catch (error) {
      return this.handleError(error);
    }
  }

}

export default new VoteCourseService();