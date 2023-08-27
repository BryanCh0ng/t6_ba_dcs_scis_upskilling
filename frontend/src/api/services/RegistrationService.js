import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class RegistrationService extends BaseApiService {
  async getRegCount(courseId) {
    try {
      let response = await axiosClient.get("/registration/retrieve_reg_count", {params: {course_id: courseId}});
      return response.data
    } catch (error) {
      return this.handleError(error);
    }
  }
}

export default new RegistrationService();