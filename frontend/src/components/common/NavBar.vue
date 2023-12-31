<template>
  <div class="content">
    <nav class="navbar navbar-expand-xxl">
      <div class="container-fluid">
        <a class="navbar-brand no-underline" id="navbar-link" :href="getNavbarLink()">
          <img src="../../assets/smulogo.png" title="smu logo" class="navlogo" />
          <span class="system-name">
            <span class="vertical-line"></span>
            Upskilling <br/>Engagement <br/>System
          </span>
        </a>
        <button
          class="navbar-toggler custom-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse navcontent" id="navbarNav">
          <ul class="navbar-nav ms-auto navbar-menu">
            <!-- Navigation Links -->
            <li v-for="link in navigationLinks" :key="link.path" class="nav-item">
              <a :class="{ active: isActiveLink(link.path) }" class="nav-link" :href="link.path">{{ link.label }}</a>
            </li>

            <!-- User Info and Role-Specific Dropdown (Visible when logged in) -->
            <li class="nav-item" v-if="user_ID">
              <!-- Dropdown for displaying user information and actions -->
              <div class="nav-link dropdown">
                <!-- Dropdown toggle button -->
                <span class="dropdown-toggle btn dropdownbtn" id="userDropdown" role="button" @click="toggleUserDropdown" aria-expanded="false">
                  <div class="username-container">
                    <font-awesome-icon icon="fa fa-user" style="padding-right: 10px"/><span id="username">{{ user_name }}</span>
                  </div>
                  
                </span>

                <!-- Dropdown content container -->
                <div v-if="showUserDropdown" class="dropdown-content" :class="{ 'admin-dropdown': user_role === 'admin' }">
                  <ul class="dropdown-menu" aria-labelledby="userDropdown">
                    <!-- Loop through role-specific dropdown items -->
                    <li v-for="(item, index) in roleSpecificDropdownItems" :key="index">
                      <a :class="{ active: isActiveLink(item.path) }" class="nav-link" :href="item.path" @click="item.action ? item.action() : null">
                        {{ item.label }}
                      </a>
                      <hr class="dropdown-divider" v-if="index === roleSpecificDropdownItems.length - 2" />
                    </li>
                  </ul>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import UserService from "@/api/services/UserService.js";

export default {
  setup() {
    const router = useRouter(); // Define the router variable here
    return {router };
  },
  data() {
    return {
      user_ID: null,
      user_role: "", // Set the user's role here dynamically
      user_name: "",
      showUserDropdown: false,
    };
  },
  computed: {
    navigationLinks() {
      const links = [];

      if (this.user_ID) {
        if (this.user_role === "Student") {
          links.push(
            { path: "/studentViewRecommendations", label: "Recommendations" },
            { path: "/studentViewCourse", label: "View Courses" },
            { path: "/proposeCourse", label: "Propose Course" },
            { path: "/contactUs", label: "Contact Us" },
          );
        } else if (
          this.user_role === "Instructor" ||
          this.user_role === "Trainer"
        ) {
          links.push(
            { path: "/viewAllLessons", label: "All Lessons" },
            { path: "/instructorTrainerViewVotingCampaign", label: "Voting Campaign" },
            { path: "/proposeCourse", label: "Propose Course" },
            { path: "/contactUs", label: "Contact Us" },
          );
        } else if (this.user_role === "Admin") {
          links.push(
            { path: "/adminViewCourse", label: "Course DB" },
            { path: "/adminViewRunCourse", label: "Run Course DB" },
            { path: "/viewAllLessons", label: "Lesson DB" },
            { path: "/adminViewVoteCourse", label: "Voting Campaign DB" },
            { path: "/adminViewProposedCourse", label: "Proposed Course DB" },
            { path: "/createCourse", label: "Create Course" }
          );
        }
      } 
      else {
        // Default links for users who are not logged in
        links.push(
          { path: "/adminViewCourse", label: "View Courses" },
          { path: "/proposeCourse", label: "Propose Course" },
          { path: "/contactUs", label: "Contact Us" }
        );
      }

      return links;
    },
    roleSpecificDropdownItems() {
      const items = [];

      if (this.user_role === "Student") {
        items.push({ path: "/studentViewProfile", label: "Profile" });
        items.push({ path: "/studentViewLesson", label: "My Lessons" });
      } else if (this.user_role === "Instructor" || this.user_role === "Trainer") {
        items.push(
          { path: "/instructorTrainerViewProfile", label: "Profile" },
          { path: "/instructorTrainerViewLesson", label: "My Lessons" },
          { path: "/viewDashboard", label: "Dashboard" }
        );
      } else if (this.user_role === "Admin") {
        items.push(
          { path: "/adminViewManagement", label: "User Management" },
          { path: "/adminViewFeedbackTemplate", label: "Feedback Template" },
          { path: "/viewDashboard", label: "Dashboard" }
        );
      }

      // Add Logout item at the end
      items.push({ label: "Logout", action: this.logout });

      return items;
    },
  },
  created() {
    this.get_user_id();
    this.get_user_role();
    this.get_user_name();
  },
  methods: {
    async get_user_id() {
      try {
        const user_ID = await UserService.getUserID()
        this.user_ID = user_ID

        if (user_ID === "Session not set") {
          this.user_ID = null
        } else {
          this.user_ID = user_ID
        }

      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_ID = null;
      }
    },
    async get_user_role() {
      try {
        const user_role = await UserService.getUserRole()
        this.user_role = user_role
      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_role = null;
      }
    },
    async get_user_name() {
      try {
        const user_name = await UserService.getUserName()
        this.user_name = user_name
      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_name = null;
      }
    },
    getNavbarLink() {
      if (this.user_role === "Student") {
        return "/studentViewCourse";
      } else if (this.user_role === "Admin") {
        return "/adminViewCourse";
      } else if (this.user_role === "Trainer" || this.user_role === "Instructor") {
        return "/instructorTrainerViewVotingCampaign";
      } else {
        return "/"; // Set a default link for cases where the role doesn't match
      }
    },
    isActiveLink(linkPath) {
      return this.$route.path === linkPath;
    },
    redirectToLogin() {
      this.router.push('/')
    },
    // need to add in redirect link
    async logout() {
      try {
        const response = await UserService.logout()
        if (response.code === 200) {
          this.user_role = "";
          this.user_ID = null;
          this.user_name = "";
          this.router.push('/')
        }
        
      } catch (error) {
        console.error('Error logging out:', error);
    }

    // After successfully logging out, navigate to the login page
    this.router.push('/');
    },
    toggleUserDropdown() {
      this.showUserDropdown = !this.showUserDropdown;
    },
  }
};
</script>


<style scoped>
.navbar {
  font-size: 18px;
  color: #151c55;
}

.navbar ul {
  margin: 0;
  padding: 0;
  display: flex;
  list-style: none;
  align-items: end;
}

.navbar li {
  position: relative;
}

.navbar li + li {
  margin-left: 15px;
}

.navbar a,
.navbar a:focus {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0;
  font-weight: 400;
  color: #151c55;
  white-space: nowrap;
  transition: 0.3s;
}

.navbar a i,
.navbar a:focus i {
  line-height: 0;
  margin-left: 5px;
}

.navbar a:hover,
.navbar a:active {
  font-weight: bold;
  text-decoration: underline;
}

.navbar a.active {
  font-weight: bold;
  position: relative; 
  text-decoration: underline;
}

.no-underline,
.no-underline.hover {
  text-decoration: none !important;
}

.navlogo {
  width: 160px;
}

.system-name {
  font-size: 15px;
  display: flex;
  align-items: center;
  margin-left: 5px;
  font-weight: bold;
}

.vertical-line {
  border-left: 1px solid #151c55;
  height: 50px;
  margin-right: 10px;
}

.loginbtn,
.loginbtn:hover,
.loginbtn:focus {
  width: 130px;
  background-color: #151c55 !important;
  color: #ffffff !important;
}

.custom-toggler.navbar-toggler {
  border: 4px solid #151c55;
}

.custom-toggler .navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 32 32' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(21,28,85,100)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 8h24M4 16h24M4 24h24'/%3E%3C/svg%3E");
}

.navbar-toggler:focus,
.navbar-toggler:active,
.navbar-toggler-icon:focus {
  outline: none;
  box-shadow: none;
}

.dropdown-toggle.btn.dropdownbtn {
  width: 150px;
  background-color: transparent;
  color: #151c55;
  border: 4px solid #151c55;
  border-radius: 5px;
  padding: 5px 10px;
  position: relative;
  /* padding-left: 90px; */
}

.username-container {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100px;
  display: inline-block;
  height:22px;
}

.loginbtn {
  position: relative;
  top: 5px;
}

.dropdown {
  position: relative;
  top: 15px;
}

.dropdown-content {
  position: absolute;
  top: 80%; 
  left: -22px; 
  z-index: 1;
  font-size: 16px;
}

.admin-dropdown {
  left: -110px;
}

.dropdown-menu {
  border: 0px;
  background-color: transparent;
}

.dropdown-content ul {
  display: flex;
  flex-direction: column;
  align-items: flex-end; 
  padding: 0; 
  margin: 0;
  padding-top: 10px;
}

.dropdown-content li {
  padding: 2px 14px;
  cursor: pointer;
}

hr.dropdown-divider {
    margin-top: 3px;
    margin-bottom: 0;
}


@media (max-width: 1399px) {
  .dropdown {
    position: relative;
    top: 1px;
  }
}

@media (max-width: 768px) {
  /* .dropdown {
    bottom: 120%;
    left: 5px;
    transform: translateY(-10px);
    margin-bottom: 40px;
  } */

  .dropdown-content {
    position: absolute;
    transform: translateY(5px);
    left: -27px;
    z-index: 1;
    font-size: 18px;
  }

  .custom-toggler {
    transform: translateY(8px);
  }

  .dropdown-menu {
    border: 0px;
  }

  .admin-dropdown{
    right: 10px;
  }

  .navbar-collapse{
    border:0px;
  }
}

@media (max-width: 510px) {
  .system-name {
    display: none;
  }
}

</style>