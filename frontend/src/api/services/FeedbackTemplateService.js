import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class FeedbackTemplateService extends BaseApiService {
    async getAllTemplates() {
        try {
            let response = await axiosClient.get("/feedbacktemplate/get_all_templates");
            return response.data;

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
            let response = await axiosClient.post("/feedbacktemplate/post_feedback_template", data)
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }

    async editFeedbackTemplate(template_id,data) {
        try {
            let response = await axiosClient.put(`/feedbacktemplate/edit_feedback_template/${template_id}`, data)
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }  

    async deleteFeedbackTemplate(templateId) {
        try { 
            let response = await axiosClient.post("/feedbacktemplate/delete_feedback_template", { template_ID: templateId });
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }

    async applyFeedbackTemplateToCourses(data) {
        try {
            let response = await axiosClient.post("/feedbacktemplate/apply_feedback_template_to_courses", data)
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }  
    
}

export default new FeedbackTemplateService();

