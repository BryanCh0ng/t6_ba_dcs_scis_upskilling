import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class DashboardService extends BaseApiService {

    async getCourseAverageRatings(course_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/course_average_ratings', {
                params: {
                    course_ID: course_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getInstructorAverageRatings(instructor_ID) {
        try {
            const response = await axiosClient.get('/dashboard/instructor_average_ratings', {
                params: {
                    instructor_ID: instructor_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getCourseDoneWellFeedback(course_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_course_done_well_specific', {
                params: {
                    course_ID: course_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getCourseImproveFeedback(course_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_course_improve_specific', {
                params: {
                    course_ID: course_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getInstructorDoneWellFeedback(user_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_instructor_done_well_specific', {
                params: {
                    user_ID: user_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getInstructorImproveFeedback(user_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_instructor_improve_specific', {
                params: {
                    user_ID: user_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getRunCourseWellFeedback(runcourse_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_runcourse_well_specific', {
                params: {
                    runcourse_ID: runcourse_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getRunCourseInstructorWellFeedback(runcourse_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_runcourse_instructor_well_specific', {
                params: {
                    runcourse_ID: runcourse_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getRunCourseImproveFeedback(runcourse_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_runcourse_improve_specific', {
                params: {
                    runcourse_ID: runcourse_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getRunCourseInstructorImproveFeedback(runcourse_ID) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_runcourse_improve_specific', {
                params: {
                    runcourse_ID: runcourse_ID,
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }
}

export default new DashboardService();