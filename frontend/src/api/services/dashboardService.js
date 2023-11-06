import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class DashboardService extends BaseApiService {
    async getCourseAverageRatings(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            console.log(course_ID)
            // console.log(runcourse_ID)
            const response = await axiosClient.get('/dashboard/course_average_ratings', {
                params: {
                    course_ID: course_ID,
                    coursecat_ID: coursecat_ID,
                    rcourse_ID: rcourse_ID,
                    instructor_ID: instructor_ID,
                    run_Startdate: run_Startdate,
                    run_Enddate: run_Enddate
                },
            });
            return response.data;
        } catch (error) {
            throw new Error("Error fetching course feedback");
        }
    }

    async getInstructorAverageRatings(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            const response = await axiosClient.get('/dashboard/instructor_average_ratings', {
                params: {
                    course_ID: course_ID,
                    coursecat_ID: coursecat_ID,
                    rcourse_ID: rcourse_ID,
                    instructor_ID: instructor_ID,
                    run_Startdate: run_Startdate,
                    run_Enddate: run_Enddate
                },
            });
            return response.data;
        } catch (error) {
            throw new Error("Error fetching course feedback");
        }
    }

    async getCourseDoneWellFeedback(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_course_done_well_specific', {
                params: {
                    course_ID: course_ID,
                    coursecat_ID: coursecat_ID,
                    rcourse_ID: rcourse_ID,
                    instructor_ID: instructor_ID,
                    run_Startdate: run_Startdate,
                    run_Enddate: run_Enddate
                },
            });
            return response.data;
        } catch (error) {
            throw new Error("Error fetching course feedback");
        }
    }

    async getCourseImproveFeedback(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_course_improve_specific', {
                params: {
                    course_ID: course_ID,
                    coursecat_ID: coursecat_ID,
                    rcourse_ID: rcourse_ID,
                    instructor_ID: instructor_ID,
                    run_Startdate: run_Startdate,
                    run_Enddate: run_Enddate
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getInstructorDoneWellFeedback(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_instructor_done_well_specific', {
                params: {
                    course_ID: course_ID,
                    coursecat_ID: coursecat_ID,
                    rcourse_ID: rcourse_ID,
                    instructor_ID: instructor_ID,
                    run_Startdate: run_Startdate,
                    run_Enddate: run_Enddate
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    async getInstructorImproveFeedback(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            // console.log(course_ID)
            const response = await axiosClient.get('/dashboard/feedback_instructor_improve_specific', {
                params: {
                    course_ID: course_ID,
                    coursecat_ID: coursecat_ID,
                    rcourse_ID: rcourse_ID,
                    instructor_ID: instructor_ID,
                    run_Startdate: run_Startdate,
                    run_Enddate: run_Enddate
                },
            });
            return response.data;
        } catch (error) {
          throw new Error('Error fetching course feedback');
        }
    }

    
    async getCourseSentimentData(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            let response = await axiosClient.get("/dashboard/course_sentiment_data",
                {
                    params: {
                        course_ID: course_ID,
                        coursecat_ID: coursecat_ID,
                        rcourse_ID: rcourse_ID,
                        instructor_ID: instructor_ID,
                        run_Startdate: run_Startdate,
                        run_Enddate: run_Enddate
                    },
                }
            );
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }

    async getInstructorSentimentData(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            let response = await axiosClient.get("/dashboard/instructor_sentiment_data",
                {
                    params: {
                        course_ID: course_ID,
                        coursecat_ID: coursecat_ID,
                        rcourse_ID: rcourse_ID,
                        instructor_ID: instructor_ID,
                        run_Startdate: run_Startdate,
                        run_Enddate: run_Enddate
                    },
                }
            );
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }

    async getCourseWordcloudData(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            let response = await axiosClient.get("/dashboard/course_wordcloud_data",
                {
                    params: {
                        course_ID: course_ID,
                        coursecat_ID: coursecat_ID,
                        rcourse_ID: rcourse_ID,
                        instructor_ID: instructor_ID,
                        run_Startdate: run_Startdate,
                        run_Enddate: run_Enddate
                    },
                }
            );
            return response 
        } catch(error) {
            return this.handleError(error)
        }
    }

    async getInstructorWordcloudData(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            let response = await axiosClient.get("/dashboard/instructor_wordcloud_data",
                {
                    params: {
                        course_ID: course_ID,
                        coursecat_ID: coursecat_ID,
                        rcourse_ID: rcourse_ID,
                        instructor_ID: instructor_ID,
                        run_Startdate: run_Startdate,
                        run_Enddate: run_Enddate
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
