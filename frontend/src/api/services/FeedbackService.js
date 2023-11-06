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

    async getRandomReviews(rcourse_id, course_id, no_of_reviews) {
        try {
            const endpoint = `/feedback/get_random_reviews_by_rcourse_id`;
            const params = {
                rcourse_id: rcourse_id,
                course_id: course_id,
                no_of_reviews: no_of_reviews
            };
            const response = await axiosClient.get(endpoint, { params });
            console.log(response)
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async getFeedbackForRunCourse(course_ID, runcourse_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/feedback/get_feedback_for_runcourse', {
                params: {
                    course_ID: course_ID,
                    runcourse_ID: runcourse_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getFeedbackForCourseInstructor(course_ID, instructor_ID) {
        try {
            const response = await axiosClient.get('/feedback/get_feedback_for_course_and_instructor', {
                params: {
                    course_ID: course_ID,
                    instructor_ID: instructor_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    
    
}

export default new FeedbackService();

