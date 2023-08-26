import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class UserService extends BaseApiService {
  async getAllInstructors() {
    try {
      let response = await axiosClient.get("/user/get_all_instructors");
      return response.data
    } catch (error) {
      return this.handleError(error);
    }
  }
  async getAllTrainers() {
    try {
      let response = await axiosClient.get("/user/get_all_trainers");
      return response.data
    } catch (error) {
      return this.handleError(error);
    }
  }
}

export default new UserService();