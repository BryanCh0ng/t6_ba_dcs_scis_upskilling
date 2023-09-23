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
            console.log(response.data)
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    async getUserSimilarityInterest(user_ID) {
        try {
            console.log(user_ID)
            let response = await axiosClient.get("/recommender/user_similarity_interest", {
                params: {
                    user_ID: user_ID
                }
            });
            console.log(response.data)
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }
    

}

export default new RecommenderService();