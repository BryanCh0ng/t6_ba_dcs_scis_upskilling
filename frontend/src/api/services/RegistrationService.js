import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class RegistrationService extends BaseApiService {
    async createNewRegistration(rcourse_ID, user_ID, reg_Status) {
        try {
            const response = await axiosClient.post("registration/create_new_registration", {
                rcourse_ID: rcourse_ID,
                user_ID: user_ID,
                reg_Status: reg_Status
            });
            console.log(response.data);
            return response.data;
            
        } catch (error) {
            return this.handleError(error);
        }
    }

    async dropRegisteredCourse(rcourse_ID, user_ID) {
        try {
            const response = await axiosClient.put("/registration/drop_registered_course", {
                rcourse_ID: rcourse_ID,
                user_ID: user_ID,
            });
            // console.log(response);
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new RegistrationService();