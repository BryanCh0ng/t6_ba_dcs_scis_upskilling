import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseCategoryService extends BaseApiService {
    async getAllCourseCategory() {
        try {
            let response  = await axiosClient.get("/coursecat/get_all_coursecat");
            return response.data.data.course.map(coursecat => ({
                coursecat_ID: coursecat.coursecat_ID,
                coursecat_Name: coursecat.coursecat_Name
            }));

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new CourseCategoryService();