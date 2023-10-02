import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class FeedbackTemplateService extends BaseApiService {
    async getAllTemplates() {
        try {
            let response = await axiosClient.get("/feedbacktemplate/get_all_templates");
            
            return response.data.data.templates;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async getTemplateById(templateId) {
        try {
            let response = await axiosClient.get("/feedbacktemplate/get_template_by_id", { params: { template_id: templateId } });
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new FeedbackTemplateService();