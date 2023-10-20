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
            //console.log(instructor_ID);
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

    async getCourseSentimentData(course_ID, rcourse_ID) {
        try {
            console.log(course_ID)
            console.log(rcourse_ID)
            let response = await axiosClient.get("/dashboard/course_sentiment_data",
                {
                    params: {
                        course_ID: course_ID,
                        rcourse_ID: rcourse_ID
                    },
                }
            );
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }

    async getInstructorSentimentData(course_ID, rcourse_ID) {
        try {
            let response = await axiosClient.get("/dashboard/instructor_sentiment_data",
                {
                    params: {
                        course_ID: course_ID,
                        rcourse_ID: rcourse_ID
                    },
                }
            );
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }

    async getCourseWordcloudData(course_ID, rcourse_ID) {
        try {
            let response = await axiosClient.get("/dashboard/course_wordcloud_data",
                {
                    params: {
                        course_ID: course_ID,
                        rcourse_ID: rcourse_ID
                    },
                }
            );
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }

    async getInstructorWordcloudData(course_ID, rcourse_ID) {
        try {
            let response = await axiosClient.get("/dashboard/instructor_wordcloud_data",
                {
                    params: {
                        course_ID: course_ID,
                        rcourse_ID: rcourse_ID
                    },
                }
            )
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }
    
}

export default new DashboardService();
