import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class VoteCourseService extends BaseApiService {
  async getAllVoteCourses(courseId) {
      try {
        let courses = await axiosClient.get("/votecourse/get_all_votecourses", {params: {course_id: courseId}});
        return courses.data
      } catch (error) {
        return this.handleError(error);
      }
    }

  async getVoteCount(courseId) {
    try {
      let response = await axiosClient.get("/votecourse/retrieve_vote_count", {params: {course_id: courseId}});
      return response.data
    } catch (error) {
      return this.handleError(error);
    }
  }
}

export default new VoteCourseService();