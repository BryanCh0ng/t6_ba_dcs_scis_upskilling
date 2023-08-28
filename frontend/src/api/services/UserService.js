import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class UserService extends BaseApiService {
    async getInstructors() {
        try {
            let response = await axiosClient.get("/user/get_instructors");
            return response.data.data.instructors;

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new UserService();