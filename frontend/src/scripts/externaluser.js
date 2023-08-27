import ExternalUserService from "../api/services/ExternalUserService.js"

async function getExternalUserDetails(user_id) {
	var external_user_response = await ExternalUserService.getExternalUserDetails(user_id);
	return external_user_response
}

export { getExternalUserDetails };