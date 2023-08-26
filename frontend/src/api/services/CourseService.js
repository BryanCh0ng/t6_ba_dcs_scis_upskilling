import { axiosClient } from "../axiosClient";
import BaseApiService from "../BaseApiService";

class CourseService extends BaseApiService {
    async getAllCourses(filter) {
        try {
            let courses = await axiosClient.get("/course/get_all_courses", {params: {skill_name: filter}});
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
    // Student - Registration - course name, course cat, status
    async searchCourseRegistrationInfo(queryParams) {
        try {
            let registrationInfo = await axiosClient.get("/course/get_course_registration_info_filter_search", { params: queryParams });
            return registrationInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }
    // Student - Vote - course name, course cat, status
    async searchCourseVoteInfo(queryParams) {
        try {
            let voteInfo = await axiosClient.get("/course/get_course_vote_info_filter_search", { params: queryParams });
            return voteInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }
    // Student/Instructor/Trainer - Proposed - course name, course cat, status
    async searchProposedInfo(queryParams) {
        try {
            let proposedInfo = await axiosClient.get("/course/get_proposed_courses_filter_search", { params: queryParams });
            return proposedInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }
    // Student - Completed - course name, course cat
    async searchCompletedInfo(queryParams) {
        try {
            let completedInfo = await axiosClient.get("/course/get_completed_courses_filter_search", { params: queryParams });
            return completedInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Instructor/Trainer - VotingCampaign - course name, course cat
    async searchVotingCampaignInfo(queryParams) {
        try {
            let votingInfo = await axiosClient.get("/course/get_voting_campaign_courses_filter_search", { params: queryParams });
            return votingInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Instructor/Trainer - Assigned Course
    async searchInstructorAssignedCourseInfo(queryParams) {
        try {
            let instructorAssignedInfo = await axiosClient.get("/course/get_instructor_assigned_courses_filter_search", { params: queryParams });
            return instructorAssignedInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Instructor/Trainer - Assigned Course
    async searchInstructorProposedCourseInfo(queryParams) {
        try {
            let instructorProposedInfo = await axiosClient.get("/course/get_instructor_proposed_courses_filter_search", { params: queryParams });
            return instructorProposedInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Instructor/Trainer - Completed/Taught Course
    async searchInstructorCompletedCourseInfo(queryParams) {
        try {
            let instructorCompletedInfo = await axiosClient.get("/course/get_instructor_taught_courses_filter_search", { params: queryParams });
            return instructorCompletedInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Proposal - Submitted
    async searchAdminAllProposalInfo(queryParams) {
        try {
            let adminAllProposalInfo = await axiosClient.get("/course/get_all_submitted_proposed_courses_admin", { params: queryParams });
            return adminAllProposalInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Proposal - Approved/Rejected
    async searchAdminAllApprovedRejectedProposalInfo(queryParams) {
        try {
            let adminAllApprovedRejectedProposalInfo = await axiosClient.get("/course/get_all_app_reg_proposed_courses_admin", { params: queryParams });
            return adminAllApprovedRejectedProposalInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Voting Campaign
    async searchAdminVotingCampaignInfo(queryParams) {
        try {
            let adminVotingCampaignInfo = await axiosClient.get("/course/get_all_voting_courses_admin", { params: queryParams });
            return adminVotingCampaignInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Courses
    async searchAdminAllCoursesInfo(queryParams) {
        try {
            let adminAllCoursesInfo = await axiosClient.get("/course/get_all_courses_with_registration_count", { params: queryParams });
            return adminAllCoursesInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

    // Admin - All Instructors
    async searchAdminAllInstructorsInfo(queryParams) {
        try {
            let adminAllInstructorsInfo = await axiosClient.get("/course/get_all_instructors_and_trainers", { params: queryParams });
            return adminAllInstructorsInfo.data;

        } catch (error) {
            return this.handleError(error);
        }
    }

}

export default new CourseService();