import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class FeedbackTemplateService extends BaseApiService {
    async getTemplates() {
        try {
            let response = await axiosClient.get("/feedbacktemplate/get_templates");
            
            return response.data.data.templates;

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new FeedbackTemplateService();