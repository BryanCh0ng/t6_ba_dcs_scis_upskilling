import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class FeedbackService extends BaseApiService {
    async postStudentFeedback(data) {
        try {
            let response = await axiosClient.post("/feedback/post_feedback_student", data)
            console.log(response)
            return response.data
        } catch (error) {
            return this.handleError(error)
        }
    }

    async getStudentFeedbackIncludingAnswersAndTemplate(rcourse_id) {
        try {
            const endpoint = `/feedback/get_student_feedback_including_answers_and_template`;
            const params = {
              rcourse_id: rcourse_id
            };
            const response = await axiosClient.get(endpoint, { params });
            console.log(response)
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }
    
}

export default new FeedbackService();

