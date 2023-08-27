import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class ExternalUserService extends BaseApiService {
  async getExternalUserDetails(userid) {
    try {
      let response = await axiosClient.get("/externaluser/get_external_user_by_user_id", {params: {user_id: userid}});
      return response.data
    } catch (error) {
      return this.handleError(error);
    }
  }
}

export default new ExternalUserService();