import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseCategoryService extends BaseApiService {
    async getAllCourseCategory() {
        try {
            let category = await axiosClient.get("/coursecat/get_all_coursecat");
            return category.data.data.course.map(coursecat => coursecat.coursecat_Name);

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new CourseCategoryService();