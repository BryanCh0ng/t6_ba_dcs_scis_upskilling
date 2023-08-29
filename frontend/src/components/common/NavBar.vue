<template>
  <div class="content">
    <nav class="navbar navbar-expand-xl">
      <div class="container-fluid">
        <a class="navbar-brand no-underline" href="#">
          <img src="../../assets/smulogo.png" title="smu logo" class="navlogo" />
          <span class="system-name">
            <span class="vertical-line"></span>
            Upskilling Engagement <br />System
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

            <!-- Login Button (Visible when not logged in) -->
            <li class="nav-item" v-if="!isLoggedIn">
              <button type="button" class="btn loginbtn" @click="redirectToLogin">
                Login
              </button>
            </li>

            <!-- User Info and Role-Specific Dropdown (Visible when logged in) -->
            <li class="nav-item" v-if="isLoggedIn">
              <!-- Dropdown for displaying user information and actions -->
              <div class="nav-link dropdown">
                <!-- Dropdown toggle button -->
                <span class="dropdown-toggle btn dropdownbtn" id="userDropdown" role="button" @click="toggleUserDropdown" aria-expanded="false">
                  {{ username }} <!-- Display the user's name -->
                </span>

                <!-- Dropdown content container -->
                <div v-if="showUserDropdown" class="dropdown-content" :class="{ 'admin-dropdown': userRole === 'admin' }">
                  <ul class="dropdown-menu" aria-labelledby="userDropdown">
                    <!-- Loop through role-specific dropdown items -->
                    <li v-for="(item, index) in roleSpecificDropdownItems" :key="index">
                      <a :class="{ active: isActiveLink(item.path) }" class="nav-link" :href="item.path" @click="item.action ? item.action() : null">
                        {{ item.label }}
                      </a>
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
// import { axiosClient } from "../api/axiosClient";

export default {
  data() {
    return {
      userRole: "", // Set the user's role here dynamically
      isLoggedIn: false, // Set to true when the user is logged in
      showUserDropdown: false,
    };
  },
  computed: {
    navigationLinks() {
      const links = [];

      if (this.isLoggedIn) {
        if (this.userRole === "student") {
          links.push(
            { path: "/recommendations", label: "Recommendations" },
            { path: "/viewCourses", label: "View Courses" },
            { path: "/proposeCourse", label: "Propose Course" }
          );
        } else if (
          this.userRole === "instructor" ||
          this.userRole === "trainer"
        ) {
          links.push(
            { path: "/votingCampaign", label: "Voting Campaign" },
            { path: "/proposeCourse", label: "Propose Course" }
          );
        } else if (this.userRole === "admin") {
          links.push(
            { path: "/adminViewProposedCourse", label: "All Proposal" },
            { path: "/votingCampaign", label: "Voting Campaign" },
            { path: "/createCourse", label: "Create Course" }
          );
        }
        // Add the common links for logged-in users
        links.push({ path: "/contactUs", label: "Contact Us" });
      } else {
        // Add the default links for users who are not logged in
        links.push(
          { path: "/viewcourses", label: "View Courses" },
          { path: "/proposecourse", label: "Propose Course" },
          { path: "/contactUs", label: "Contact Us" }
        );
      }

      return links;
    },
    roleSpecificDropdownItems() {
      const items = [];

      if (this.userRole === "student") {
        items.push({ path: "/profile", label: "Profile" });
      } else if (this.userRole === "instructor" || this.userRole === "trainer") 
      {
        items.push(
          { path: "/profile", label: "Profile" },
          { path: "/blacklist", label: "Blacklist" },
          { path: "/dashboard", label: "Dashboard" }
        );
      } else if (this.userRole === "admin") {
        items.push(
          { path: "/profile", label: "Profile" },
          { path: "/adminViewRunCourse", label: "All Run Course DB" },
          { path: "/adminViewVoteCourse", label: "All Vote Course DB" },
          { path: "/allAvailRegCourse", label: "All Available Registration Course" },
          { path: "/adminViewInstructorsTrainers", label: "All Instructors DB" },
          { path: "/feedbackTemplate", label: "Feedback Template" },
          { path: "/dashboard", label: "Dashboard" }
        );
      }

      // Add Logout item at the end
      items.push({ label: "Logout", action: this.logout });

      return items;
    },
  },
  methods: {
    isActiveLink(linkPath) {
      return this.$route.path === linkPath;
    },
    redirectToLogin() {
      window.location.href = "/login";
    },
    // need to add in redirect link
    logout() {
      this.userRole = "";
      this.isLoggedIn = false;
    },
    toggleUserDropdown() {
      console.log("Toggling user dropdown");
      this.showUserDropdown = !this.showUserDropdown;
    },
  },
  // created() {
  //   // Need to insert API endpoint
  //   axiosClient
  //     .get("")
  //     .then((response) => {
  //       this.userRole = response.data.role;
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching user role:", error);
  //     });
  // },
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
  margin-left: 20px;
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
  width: 180px;
}

.system-name {
  font-size: 16px;
  display: flex;
  align-items: center;
  margin-left: 10px;
  font-weight: bold;
}

.vertical-line {
  border-left: 1px solid #151c55;
  height: 40px;
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
  width: 130px;
  background-color: transparent;
  color: #151c55;
  border: 4px solid #151c55;
  border-radius: 5px;
  padding: 5px 10px;
  position: relative;
  padding-left: 90px;
}
.loginbtn {
  position: relative;
  top: 5px;
}

.dropdown {
  position: relative;
  top: 12px;
}

.dropdown-content {
  position: absolute;
  top: 80%; 
  left: -22px; 
  z-index: 1;
  font-size: 18px;
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
  padding: 8px 14px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .dropdown {
    bottom: 120%;
    left: 5px;
    transform: translateY(-10px);
  }

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
