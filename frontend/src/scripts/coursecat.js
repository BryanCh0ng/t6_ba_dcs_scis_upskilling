import CourseCategoryService from "../api/services/CourseCategoryService.js"

async function getCategory(cat_id) {
	var category_response = await CourseCategoryService.getCategoryById(cat_id);
	return category_response.coursecat_Name
}

export { getCategory };