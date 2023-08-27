import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class InterestService extends BaseApiService {
  async getInterestCount(vote_id) {
    try {
      let response = await axiosClient.get("/interest/retrieve_interest_count_by_vote_id", {params: {vote_id: vote_id}});
      return response.data
    } catch (error) {
      return this.handleError(error);
    }
  }
}

export default new InterestService();