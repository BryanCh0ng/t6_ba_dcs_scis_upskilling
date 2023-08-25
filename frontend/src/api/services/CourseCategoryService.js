import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseCategoryService extends BaseApiService {
    async getAllCourseCategory() {
        try {
            let response = await axiosClient.get("/coursecat/get_all_coursecat");
            //Return coursecat_Name
            //return category.data.data.course.map(coursecat => coursecat.coursecat_Name);
            return response.data.data.course;

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new CourseCategoryService();