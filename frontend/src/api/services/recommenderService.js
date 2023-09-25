import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class RecommenderService extends BaseApiService {
    async getUserSimilarityRegistration(user_ID) {
        try {
            let response = await axiosClient.get("/recommender/user_similarity_registration", {
                params: {
                    user_ID: user_ID
                }
            });
            // console.log(response)
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async getUserSimilarityInterest(user_ID) {
        try {
            // console.log(user_ID)
            let response = await axiosClient.get("/recommender/user_similarity_interest", {
                params: {
                    user_ID: user_ID
                }
            });
            // console.log(response.data)
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async getCourseSimilarityRegistration(course_list_req) {
        // console.log(course_list_req)
        try {
            const response = await axiosClient.post("/recommender/course_similarity_registration", {
                params: {
                    course_list_req: course_list_req
                }
            });
            // console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async getCourseSimilarityInterest(course_list_req) {
        // console.log(course_list_req)
        try {
            const response = await axiosClient.post("/recommender/course_similarity_interest", {
                params: {
                    course_list_req: course_list_req
                }
            });
            // console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async getTopPicksForRegistration(user_ID) {
        try {
            // console.log(user_ID)
            let response = await axiosClient.get("/recommender/get_top_10_course_avail_for_register", {
                params: {
                    user_id: user_ID,
                }
            });
            // console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    async getTopPicksForVoting(user_ID) {
        try {
            // console.log(user_ID)
            let response = await axiosClient.get("/recommender/get_top_10_course_avail_for_voting", {
                params: {
                    user_id: user_ID,
                }
            });
            // console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new RecommenderService();