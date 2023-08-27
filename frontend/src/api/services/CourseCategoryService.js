import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseCategoryService extends BaseApiService {
    async getAllCourseCategory() {
        try {
            let response = await axiosClient.get("/coursecat/get_all_coursecat");
            return response.data.data.course;

        } catch (error) {
            return this.handleError(error);
        }
    }
    async getCategoryById(cat_id) {
      try {
        let response = await axiosClient.get("/coursecat/get_coursecat_by_id", { params: { coursecat_id: cat_id } });
        return response.data
      } catch (error) {
        return this.handleError(error);
      }
    }

}

export default new CourseCategoryService();