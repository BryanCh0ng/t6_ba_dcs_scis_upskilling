import RegistrationService from "../api/services/RegistrationService.js"

async function getRegCount(course_id) {
  var reg_count_response = await RegistrationService.getRegCount(course_id);
  return reg_count_response.data.reg_count
}

export { getRegCount };