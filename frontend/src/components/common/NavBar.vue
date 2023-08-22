<template>
  <div class="content">
    <!-- NAV BAR -->
    <nav class="navbar navbar-expand-md">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <!-- <img src="../assets/smulogo.png" title="smu logo" class="navlogo" /> -->
          <span class="system-name">
            <span class="vertical-line"></span>
            <!-- Vertical line -->
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
            <!-- Default Navigation Items (Visible when not logged in) -->
            <li class="nav-item" v-if="!isLoggedIn">
              <a class="nav-link" href="#">View Courses</a>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <a class="nav-link" href="#">Propose Course</a>
            </li>

            <!-- User-Role Specific Navigation Items (Visible after login) -->
            <li class="nav-item" v-if="userRole === 'student'">
              <a class="nav-link" href="#">Recommendations</a>
            </li>
            <li class="nav-item" v-if="userRole === 'student'">
              <a class="nav-link" href="#">View Courses</a>
            </li>
            <li class="nav-item" v-if="userRole === 'student'">
              <a class="nav-link" href="#">Propose Course</a>
            </li>

            <li
              class="nav-item"
              v-if="userRole === 'instructor' || userRole === 'trainer'"
            >
              <a class="nav-link" href="#">Voting Campaign</a>
            </li>
            <li
              class="nav-item"
              v-if="userRole === 'instructor' || userRole === 'trainer'"
            >
              <a class="nav-link" href="#">Propose Course</a>
            </li>

            <li class="nav-item" v-if="userRole === 'admin'">
              <a class="nav-link" href="#">All Proposals</a>
            </li>
            <li class="nav-item" v-if="userRole === 'admin'">
              <a class="nav-link" href="#">Voting Campaign</a>
            </li>
            <li class="nav-item" v-if="userRole === 'admin'">
              <a class="nav-link" href="#">Create Course</a>
            </li>

            <!-- Common Navigation Item (Visible for all) -->
            <li class="nav-item">
              <a class="nav-link" href="#">Contact Us</a>
            </li>

            <!-- Login Button (Visible when not logged in) -->
            <li class="nav-item" v-if="!isLoggedIn">
              <button type="button" class="btn loginbtn">Login</button>
            </li>

            <!-- User Info and Role-Specific Dropdown (Visible when logged in) -->
            <li class="nav-item" v-if="isLoggedIn">
              <div class="nav-link dropdown">
                <span
                  class="dropdown-toggle btn dropdownbtn"
                  id="userDropdown"
                  role="button"
                  @click="toggleUserDropdown"
                  aria-expanded="false"
                >
                  {{ username }}
                  <!-- Display the user's name -->
                </span>
                <div v-if="showUserDropdown" class="dropdown-content">
                  <ul class="dropdown-menu" aria-labelledby="userDropdown">
                    <!-- Role-specific items -->
                    <li v-if="userRole === 'student'">
                      <a class="dropdown-item" href="#">Profile</a>
                    </li>

                    <li
                      v-if="userRole === 'instructor' || userRole === 'trainer'"
                    >
                      <a class="dropdown-item" href="#">Profile</a>
                    </li>
                    <li
                      v-if="userRole === 'instructor' || userRole === 'trainer'"
                    >
                      <a class="dropdown-item" href="#">Blacklist</a>
                    </li>
                    <li
                      v-if="userRole === 'instructor' || userRole === 'trainer'"
                    >
                      <a class="dropdown-item" href="#">Dashboard</a>
                    </li>

                    <li v-if="userRole === 'admin'">
                      <a class="dropdown-item" href="#">Profile</a>
                    </li>

                    <li v-if="userRole === 'admin'">
                      <a class="dropdown-item" href="#">Academic Management</a>
                    </li>
                    <li v-if="userRole === 'admin'">
                      <a class="dropdown-item" href="#">Feedback Template</a>
                    </li>
                    <li v-if="userRole === 'admin'">
                      <a class="dropdown-item" href="#">Dashboard</a>
                    </li>

                    <!-- Add Logout item at the end -->
                    <li>
                      <a @click="logout" class="dropdown-item" href="#"
                        >Logout</a
                      >
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
// import { axiosClient } from '../api/axiosClient'; 

export default {
  data() {
    return {
      userRole: "", // Set the user's role here dynamically
      isLoggedIn: false, // Set to true when user is logged in
      showUserDropdown: false, // Initialized as false to hide the dropdown content
    };
  },
  methods: {
    logout() {
      // Reset the userRole and isLoggedIn properties
      this.userRole = "";
      this.isLoggedIn = false;
    },
    toggleUserDropdown() {
      this.showUserDropdown = !this.showUserDropdown; // Toggle the dropdown content visibility
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
  margin-left: 30px;
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

.navbar a:before {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  background-color: #8a704c;
  visibility: hidden;
  transition: all 0.3s ease-in-out 0s;
}

.navcontent a:hover:before,
.navcontent li:hover > a:before,
.navcontent .active:before {
  visibility: visible;
  width: 95%; /* width of the underline */
  height: 3px;
}

.navbar a:hover,
.navbar a:active {
  font-weight: bold; /* Make the text bold when focused or active */
}

.navlogo {
  width: 180px;
}

.system-name {
  font-size: 16px;
  display: flex;
  align-items: center;
  margin-left: 10px;
  /* Add some spacing between the logo and the system name */
  font-weight: bold;
}

.vertical-line {
  border-left: 1px solid #151c55;
  height: 40px;
  margin-right: 10px;
}

/* login button */
.loginbtn,
.logoutbtn,
.loginbtn:hover,
.logoutbtn:hover {
  width: 130px;
  background-color: #151c55;
  color: #ffffff;
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
  background-color: transparent; /* Remove the background color */
  color: #151c55;
  border: 4px solid #151c55; /* Add border style */
  border-radius: 5px; /* Add border radius for a rounded look */
  padding: 5px 10px; /* Adjust padding for better spacing */
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
  top: 80%; /* This will position the content below the dropdown button */
  left: -95px; /* Adjust left or right value based on your design */
  background-color: white;
  color: #151c55;
  z-index: 1;
  font-size: 18px;
}

.dropdown-menu {
  border: 4px solid #151c55;
  border-radius: 5px;
}

/* Add this style to make the dropdown content stack vertically */
.dropdown-content ul {
  display: flex;
  flex-direction: column;
  align-items: flex-end; /* Align items to the start of the column */
  padding: 0; /* Reset padding to avoid unexpected spacing */
  margin: 0; /* Reset margin to avoid unexpected spacing */
}

.dropdown-content li {
  padding: 2px 14px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .dropdown {
    bottom: 120%;
    transform: translateY(-10px);
  }

  .dropdown-content {
    top: 82%;
    left: -104px;
  }
}
</style>
