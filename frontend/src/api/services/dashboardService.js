import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class DashboardService extends BaseApiService {
    async getTotalFeedbacks(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
        try {
            console.log(course_ID)
            // console.log(runcourse_ID)
            const response = await axiosClient.get('/dashboard/total_no_of_feedbacks', {
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
            return this.handleError(error)
        }
    }

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

    // async getTotalFeedbacks(course_ID, coursecat_ID, rcourse_ID, instructor_ID, run_Startdate, run_Enddate) {
    //     try {
    //         const response = await axiosClient.get('/dashboard/total_no_of_feedbacks', {
    //             params: {
    //                 course_ID: course_ID,
    //                 coursecat_ID: coursecat_ID,
    //                 rcourse_ID: rcourse_ID,
    //                 instructor_ID: instructor_ID,
    //                 run_Startdate: run_Startdate,
    //                 run_Enddate: run_Enddate
    //             },
    //         });
    //         return response.data;
    //     } catch (error) {
    //         return this.handleError(error)
    //     }
    // }

    async getFilteredCoursesName(courseID) {
        try {
            const response = await axiosClient.get('/dashboard/get_filtered_course_name', {
                params: { course_id: courseID }
            });
            return response.data;
        } catch (error) {
            throw new Error('Error fetching course name');
        }
    }

    async getFilteredRunCoursesName(rcourse_id) {
        try {
            const response = await axiosClient.get('/dashboard/get_filtered_runcourse_name', {
                params: { rcourse_id: rcourse_id }
            });
            return response.data;
        } catch (error) {
            throw new Error('Error fetching course name');
        }
    }

    async getFilteredCoachesName(instructor_id) {
        try {
            const response = await axiosClient.get('/dashboard/get_filtered_user_name', {
                params: { instructor_id: instructor_id }
            });
            return response.data;
        } catch (error) {
            throw new Error('Error fetching course name');
        }
    }

}

export default new DashboardService();
