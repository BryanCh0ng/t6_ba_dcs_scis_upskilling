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

    async getCoursesByTemplateId(templateId) {
        try {
            let response = await axiosClient.get("/feedbacktemplate/get_courses_by_template_id", { params: { template_id: templateId } });
            console.log(response)
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async getAllFeedbackTemplateNames() {
        try {
            let response = await axiosClient.get("/feedbacktemplate/get_all_feedback_template_names")
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }

    async getCourseNamesByFeedbackTemplateId(templateId) {
        try {
            let response = await axiosClient.get("/feedbacktemplate/get_course_names_by_feedback_template_id", { params: { template_id: templateId } })
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }

    async createFeedbackTemplate(data) {
        try {
            let response = await axiosClient.post("/feedbacktemplate/post_feedback_student", data)
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }

}

export default new FeedbackTemplateService();

