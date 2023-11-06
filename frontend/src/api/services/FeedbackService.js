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

    async getRandomReviews(rcourse_id, no_of_reviews) {
        try {
            const endpoint = `/feedback/get_random_reviews_by_rcourse_id`;
            const params = {
                rcourse_id: rcourse_id,
                no_of_reviews: no_of_reviews
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

