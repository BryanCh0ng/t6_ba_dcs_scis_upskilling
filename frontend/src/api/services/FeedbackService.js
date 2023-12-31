import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class FeedbackService extends BaseApiService {

    async postStudentFeedback(data) {
        try {
            let response = await axiosClient.post("/feedback/post_feedback_student", data)
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
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async getRandomReviews(rcourse_id, course_id, no_of_reviews) {
        try {
            const endpoint = `/feedback/get_random_reviews_by_rcourse_id`;
            const params = {
                rcourse_id: rcourse_id,
                course_id: course_id,
                no_of_reviews: no_of_reviews
            };
            const response = await axiosClient.get(endpoint, { params });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async getFeedback(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            let response = await axiosClient.get("/feedback/get_feedback",
                {
                    params: {
                        course_ID: course_ID,
                        coursecat_ID: coursecat_ID,
                        rcourse_ID: rcourse_ID,
                        instructor_ID: instructor_ID,
                        run_Startdate: run_Startdate,
                        run_Enddate: run_Enddate
                    },
                }
            );
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }
    
}

export default new FeedbackService();

