import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class DashboardService extends BaseApiService {
    async getCourseAverageRatings(course_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get(
                "/dashboard/course_average_ratings",
                {
                    params: {
                        course_ID: course_ID,
                    },
                }
            );
            console.log(response.data);
            return response.data;
        } catch (error) {
            throw new Error("Error fetching course feedback");
        }
    }

    async getInstructorAverageRatings(instructor_ID) {
        try {
            console.log(instructor_ID);
            const response = await axiosClient.get(
                "/dashboard/instructor_average_ratings",
                {
                    params: {
                        instructor_ID: instructor_ID,
                    },
                }
            );
            console.log(response.data);
            return response.data;
        } catch (error) {
            throw new Error("Error fetching course feedback");
        }
    }

    async getCourseDoneWellFeedback(course_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get(
                "/dashboard/feedback_course_done_well_specific",
                {
                    params: {
                        course_ID: course_ID,
                    },
                }
            );
            // console.log(response)
            return response.data;
        } catch (error) {
            throw new Error("Error fetching course feedback");
        }
    }

    async getCourseFeedbacks() {
        try {
            let response = await axiosClient.get("/dashboard/course_feedbacks")
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }

    async getInstructorFeedbacks() {
        try {
            let response = await axiosClient.get("/dashboard/instructor_feedbacks")
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }
    
}

export default new DashboardService();
