import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseService extends BaseApiService {
    // async getAllCourses(filter) {
    //     try {
    //         let courses = await axiosClient.get("/course/get_all_courses", { params: { skill_name: filter } });
    //         return courses.data
    //     } catch (error) {
    //         return this.handleError(error);
    //     }
    // }
    // async getAllCoursesAdmin() {
    //     try {
    //         let courses = await axiosClient.get("/course/get_all_courses_admin");
    //         return courses.data
    //     } catch (error) {
    //         return this.handleError(error);
    //     }
    // }
    async getCourseById(courseId) {
        try {
            let course = await axiosClient.get("/course/get_course_by_id", { params: { course_id: courseId } });
            return course.data
        } catch (error) {
            return this.handleError(error);
        }
    }
    // async searchFilterCourses(courseId, coursecatId) {
    //     try {
    //         let courses = await axiosClient.get("/course/retrieve_all_courses_filter_search", { params: { course_id: courseId, coursecat_id: coursecatId } })
    //         return courses.data
    //     } catch (error) {
    //         return this.handleError(error);
    //     }
    // }
    async deleteCourse(course_ID) {
        try {
            let deleteCourse = await axiosClient.delete("/course/delete_course", { params: { course_id: course_ID } });
            return deleteCourse.data
        } catch (error) {
            console.log("Cannot delete or update a parent row: a foreign key constraint fails");
            return this.handleError(error);
        }
    }
    async deleteRunCourse(rcourse_ID) {
        try {
            let deleteRunCourse = await axiosClient.delete("/course/delete_runcourse", { params: { rcourse_ID: rcourse_ID } });
            return deleteRunCourse.data
        } catch (error) {
            console.log("Cannot delete or update a parent row: a foreign key constraint fails");
            return this.handleError(error);
        }
    }

    // Student - Courses Available for Registration (Ongoing) with Filters
    async searchUnregisteredActiveInfo(user_ID, course_Name, coursecat_ID) {
        try {
            let response = await axiosClient.get("/course/get_unregistered_active_courses", {
                params: {
                    user_id: user_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID
                }
            });
            // console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Student - Courses Available for Voting (Active) with Filters
    async searchUnvotedActiveInfo(user_ID, course_Name, coursecat_ID) {
        try {
            let response = await axiosClient.get("/course/get_unvoted_ongoing_courses", {
                params: {
                    user_id: user_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID
                }
            });
            // console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Student - Registration - course name, course cat, status
    async searchCourseRegistrationInfo(user_ID, course_Name, coursecat_ID, reg_Status) {
        try {
            let response = await axiosClient.get("/course/get_course_registration_info_filter_search", {
                params: {
                    user_id: user_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    reg_status: reg_Status
                }
            });
            // console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }
    // Student - Vote - course name, course cat, status
    async searchCourseVoteInfo(user_ID, course_Name, coursecat_ID, vote_Status) {
        try {
            let response = await axiosClient.get("/course/get_course_vote_info_filter_search", {
                params: {
                    user_id: user_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    vote_status: vote_Status
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }
    // Student/Instructor/Trainer - Proposed - course name, course cat, status
    async searchProposedInfo(user_ID, course_Name, coursecat_ID, pcourse_Status) {
        try {
            let response = await axiosClient.get("/course/get_proposed_courses_filter_search", {
                params: {
                    user_id: user_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    pcourse_status: pcourse_Status
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Student - Completed - course name, course cat
    async searchCompletedInfo(user_ID, course_Name, coursecat_ID) {
        try {
            let response = await axiosClient.get("/course/get_completed_courses_filter_search", {
                params: {
                    user_id: user_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Instructor/Trainer - VotingCampaign - course name, course cat
    async searchVotingCampaignInfo(course_Name, coursecat_ID) {
        try {
            let response = await axiosClient.get("/course/get_voting_campaign_courses_filter_search", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }


    // Instructor/Trainer - Assigned Course
    async searchInstructorAssignedCourseInfo(instructor_ID, course_Name, coursecat_ID, runcourse_Status) {
        try {
            let response = await axiosClient.get("/course/get_instructor_assigned_courses_filter_search", {
                params: {
                    instructor_id: instructor_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    runcourse_status: runcourse_Status
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }


    // Instructor/Trainer - Proposed Course
    async searchInstructorProposedCourseInfo(instructor_ID, course_Name, coursecat_ID, pcourse_Status) {
        try {
            let response = await axiosClient.get("/course/get_instructor_proposed_courses_filter_search", {
                params: {
                    instructor_id: instructor_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    pcourse_status: pcourse_Status
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Instructor/Trainer - Completed/Taught Course
    async searchInstructorCompletedCourseInfo(instructor_ID, course_Name, coursecat_ID) {
        try {
            let response = await axiosClient.get("/course/get_instructor_taught_courses_filter_search", {
                params: {
                    instructor_id: instructor_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Proposal - Submitted
    async searchAllSubmittedProposedCoursesAdmin(course_Name, coursecat_ID) {
        try {
            let response = await axiosClient.get("/course/get_all_submitted_proposed_courses_admin", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID
                }
            });
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Proposal - Approved/Rejected
    async searchAllApprovedRejectedProposedCoursesAdmin(course_Name, coursecat_ID, status) {
        try {
            let response = await axiosClient.get("/course/get_all_app_reg_proposed_courses_admin", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    pcourse_status: status
                }
            });
            // console.log(response.data)
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Voting Campaign
    async searchAllVotingCoursesAdmin(course_Name, coursecat_ID, vote_Status) {
        try {
            let response = await axiosClient.get("/course/get_all_voting_courses_admin", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    vote_status: vote_Status
                }
            });
            // console.log("Response data:", response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Voting Campaign - Deleted
    async searchAllNotOfferedVotingCoursesAdmin(course_Name, coursecat_ID) {
        try {
            let response = await axiosClient.get("/course/get_all_not_offered_courses_admin", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                }
            });
            // console.log("Response data:", response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Courses with Reg Count 
    async searchAllRunCoursesAdmin(course_Name, coursecat_ID, course_Status) {
        try {

            let response = await axiosClient.get("/course/get_all_courses_with_registration_count", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    course_status: course_Status
                }
            });
            // console.log(response.data)
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Courses
    async searchAllCourseAdmin(course_Name, coursecat_ID, course_Status) {
        try {
            let response = await axiosClient.get("/course/get_all_courses", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    course_status: course_Status
                }
            });
            // console.log(response.data)
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Cancel/Deactivate Button in adminViewRunCourse
    async deactivateRunCourse(course_ID) {
        try {
            let deactivateRunCourse = await axiosClient.post("/course/deactivate_course", { course_id: course_ID } );
            console.log(deactivateRunCourse)
            return deactivateRunCourse.data
        } catch (error) {
            console.log("Cannot deactivate the course");
            return this.handleError(error);
        }
    }

    // Retire button in the adminViewRunCourse 
    async retireRunCourse(course_ID) {
        try {
            let retireRunCourse = await axiosClient.post("/course/retire_course", { course_id: course_ID });
            return retireRunCourse.data
        } catch (error) {
            // console.log("Cannot retire the course");
            return this.handleError(error);
        }
    }

    // Activate button in the adminViewRunCourse 
    async activateRunCourse(course_ID) {
        try {
            let activateRunCourse = await axiosClient.post("/course/activate_course", { course_id: course_ID });
            return activateRunCourse.data
        } catch (error) {
            return this.handleError(error);
        }
    }

    async createCourse(newCourseData) {
        try {
          let response = await axiosClient.post('/course/create_course', newCourseData);
          return response.data;
        } catch (error) {
          return this.handleError(error);
        }
    }

    async editCourse(courseId, updatedData) {
        try {
            let response = await axiosClient.put(`/course/edit_course/${courseId}`, updatedData);
            return response.data;

        } catch (error) {
            return this.handleError(error)
        }
    }    
    async voteCourse(vote_ID, user_ID) {
        try {
            const response = await axiosClient.post("/course/add_interest", {
                vote_ID: vote_ID,
                user_ID: user_ID,
            });
            // console.log(response.data);
            return response.data;
            
        } catch (error) {
            return this.handleError(error);
        }
    }

    async unvoteCourse(vote_ID, user_ID) {
        try {
            const response = await axiosClient.post("/course/delete_interest", {
                vote_ID: vote_ID,
                user_ID: user_ID,
            });
            // console.log(response);
            return response.data;
            
        } catch (error) {
            return this.handleError(error);
        }
    }

    async unofferedVoteCourse(course_ID) {
        try {
            const response = await axiosClient.put("/course/update_vote_unoffered_course", {
                course_ID: course_ID,
            });
            // console.log(response);
            return response.data;
            
        } catch (error) {
            return this.handleError(error);
        }
    }

    async closeVote(course_ID) {
        try {
            const response = await axiosClient.put("/course/close_vote_course", {
                course_ID: course_ID,
            });
            // console.log(response);
            return response.data;
            
        } catch (error) {
            return this.handleError(error);
        }
    }

    async adminUpdateCourse(courseId, courseData) {
      try {
          const apiUrl = `/course/admin_update_course/${courseId}`;
          const response = await axiosClient.put(apiUrl, courseData);
          if (response.status === 200) {
            return { success: true, message: response.data.message };
          } else {
            return { success: false, message: 'Failed to update the proposed course' };
          }
        } catch (error) {
          console.error('Error updating proposed course:', error);
          return { success: false, message: 'An error occurred while updating the proposed course' };
        }
    }

    async adminGetUserCourses(user_ID, course_Name, coursecat_ID) {
        try {
            const endpoint = `/course/user_courses/${user_ID}`;
            const params = {
              course_name: course_Name,
              coursecat_id: coursecat_ID
            };
            const response = await axiosClient.get(endpoint, { params });
            return response.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

     // Admin - All Run course based on course id
     async searchAllRunCourseByCourseId(course_Name, coursecat_ID, course_Status, course_id) {
        try {

            let response = await axiosClient.get("/course/get_all_run_course_by_course_id", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    course_status: course_Status,
                    course_id: course_id
                }
            });
            // console.log(response.data)
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new CourseService();