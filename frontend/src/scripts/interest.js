import InterestService from "../api/services/InterestService.js"

async function getInterestCount(vote_id) {
  var interest_count_response = await InterestService.getInterestCount(vote_id);
  return interest_count_response.data.interest_count
}

export { getInterestCount };