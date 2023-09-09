import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class ContactUsService extends BaseApiService {
    async createNewMsg(messageData) {
        try {
            const response = await axiosClient.post("contactus/create_new_msg", messageData);
            // console.log(response.data);
            return response.data;
            
        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new ContactUsService();