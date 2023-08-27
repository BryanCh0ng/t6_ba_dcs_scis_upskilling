import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseService extends BaseApiService {
    async getAllCourses(filter) {
        try {
            let courses = await axiosClient.get("/course/get_all_courses", { params: { skill_name: filter } });
            return courses.data
        } catch (error) {
            return this.handleError(error);
        }
    }
    async getAllCoursesAdmin() {
        try {
            let courses = await axiosClient.get("/course/get_all_courses_admin");
            return courses.data
        } catch (error) {
            return this.handleError(error);
        }
    }
    async getCourseById(courseId) {
        try {
            let course = await axiosClient.get("/course/get_course_by_id", { params: { course_id: courseId } });
            return course.data
        } catch (error) {
            return this.handleError(error);
        }
    }
    async searchFilterCourses(courseId, coursecatId) {
        try {
            let courses = await axiosClient.get("/course/retrieve_all_courses_filter_search", { params: { course_id: courseId, coursecat_id: coursecatId } })
            return courses.data
        } catch (error) {
            return this.handleError(error);
        }
    }
    async deleteCourse(course_ID) {
        try {
            let deleteCourse = await axiosClient.delete("/course/delete_Course", { params: { course_id: course_ID } });
            return deleteCourse.data
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
            console.log(response.data);
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }
    // Student - Vote - course name, course cat, status
    async searchCourseVoteInfo(user_ID, course_Name, coursecat_ID, vote_Status) {
        try {
            console.log(user_ID)
            console.log(vote_Status)
            console.log("Making API request...");
            let response = await axiosClient.get("/course/get_course_vote_info_filter_search", {
                params: {
                    user_id: user_ID,
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    vote_status: vote_Status
                }
            });
            console.log(response); // Log the full response object
            console.log(response.data); // Log response data specifically
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
    async searchAllApprovedRejectedProposedCoursesAdmin(course_Name, coursecat_ID, pcourse_Status) {
        try {
            console.log("course_Name:", course_Name);
            console.log("coursecat_ID:", coursecat_ID);
            console.log("status:", pcourse_Status);
            let response = await axiosClient.get("/course/get_all_app_reg_proposed_courses_admin", {
                params: {
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
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Courses
    async searchAllCoursesAdmin(course_Name, coursecat_ID, course_Status) {
        try {

            let response = await axiosClient.get("/course/get_all_courses_with_registration_count", {
                params: {
                    course_name: course_Name,
                    coursecat_id: coursecat_ID,
                    course_status: course_Status
                }
            });
            console.log(response.data)
            return response.data;
        } catch (error) {
            return this.handleError(error);
        }
    }


    // Admin - All Instructors
    async getAllInstructorsAndTrainers(user_Name, organization_Name) {
        try {
            let instructorsAndTrainers = await axiosClient.get("/course/get_all_instructors_and_trainers", {
                params: {
                    instructor_name: user_Name,
                    organization_name: organization_Name
                }
            });
            return instructorsAndTrainers.data;
        } catch (error) {
            return this.handleError(error);
        }
    }
}

export default new CourseService();