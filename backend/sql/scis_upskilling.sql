SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

DROP DATABASE IF EXISTS `scis_upskilling`;

CREATE DATABASE `scis_upskilling` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `scis_upskilling`;

-- --------------------------------------------------------

-- Database: scis_upskilling

-- --------------------------------------------------------

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user`(
	user_id int NOT NULL AUTO_INCREMENT,
	user_name varchar(255) NOT NULL,
	user_email varchar(125) NOT NULL,
	user_password varchar(100) NOT NULL,
	role_name varchar(20) NOT NULL,
	PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO user VALUES
	(1, 'Johnathan Lee', 'jonathan.2020@smu.edu.sg', 'jonathan', 'Student'),
	(2, 'Javier Ang', 'javier.ang@smu.edu.sg', 'javier', 'Admin'),
	(3, 'Amanda Lee', 'amandalee@gmail.com', 'amanda', 'Trainer'),
	(4, 'Christina Lee', 'christina.lee@smu.edu.sg', 'christina', 'Instructor'),
	(5, 'Aaron Tan', 'aarontan@gmail.com', 'aaron', 'Trainer'),
	(6, 'Samuel Tan', 'samuel.tan.2020@smu.edu.sg', 'samuel', 'Student'),
	(7, 'James Lee', 'james.lee.2020@smu.edu.sg', 'james', 'Student'),
	(8, 'Sam Lee', 'sam.lee.2019@smu.edu.sg', 'samlee', 'Student'),
	(9, 'Aloysius Tan', 'aloysius.lee.2021@smu.edu.sg', 'aloysiustan', 'Student'), 
	(10, 'Evelyn Lim', 'evelyn.lim.2022@smu.edu.sg', 'evelyn', 'Student'),
    (11, 'Sophia Ng', 'sophia.ng.2021@smu.edu.sg', 'sophia', 'Student'),
    (12, 'Isabelle Tan', 'isabelle.tan.2023@smu.edu.sg', 'isabelle', 'Student'),
    (13, 'Daniel Goh', 'daniel.goh.2020@smu.edu.sg', 'daniel', 'Student'),
    (14, 'Victoria Tan', 'victoria.tan.2022@smu.edu.sg', 'victoria', 'Student'),
    (15, 'Emily Lim', 'emily.lim.2021@smu.edu.sg', 'emily', 'Student'),
    (16, 'Oliver Wong', 'oliver.wong.2022@smu.edu.sg', 'oliver', 'Student'),
    (17, 'Grace Chan', 'grace.chan.2023@smu.edu.sg', 'grace', 'Student'),
    (18, 'Lucas Koh', 'lucas.koh.2020@smu.edu.sg', 'lucas', 'Student'),
    (19, 'Hannah Lee', 'hannah.lee.2021@smu.edu.sg', 'hannah', 'Student'),
    (20, 'Benjamin Lim', 'benjamin.lim.2022@smu.edu.sg', 'benjamin', 'Student'),
    (21, 'Lily Tan', 'lily.tan.2023@smu.edu.sg', 'lily', 'Student'),
    (22, 'William Ng', 'william.ng.2020@smu.edu.sg', 'william', 'Student'),
    (23, 'Zoe Goh', 'zoe.goh.2021@smu.edu.sg', 'zoe', 'Student'),
    (24, 'Jeremy Wong', 'ryan.wong.2022@smu.edu.sg', 'ryan', 'Student'),
    (25, 'Chris Lim', 'bryan.lim.2023@smu.edu.sg', 'bryan', 'Student'),
    (26, 'Regine Tan', 'regine.tan.2020@smu.edu.sg', 'nicholas', 'Student'),
    (27, 'Mia Koh', 'mia.koh.2021@smu.edu.sg', 'mia', 'Student'),
    (28, 'Leo Chan', 'leo.chan.2022@smu.edu.sg', 'leo', 'Student'),
    (29, 'Luna Lee', 'luna.lee.2023@smu.edu.sg', 'luna', 'Student'),
    (30, 'Henry Lim', 'henry.lim.2020@smu.edu.sg', 'henry', 'Student'),
    (31, 'Chloe Ng', 'chloe.ng.2021@smu.edu.sg', 'chloe', 'Student'),
    (32, 'Ethan Tan', 'ethan.tan.2022@smu.edu.sg', 'ethan', 'Student'),
    (33, 'Scarlett Goh', 'scarlett.goh.2023@smu.edu.sg', 'scarlett', 'Student'),
    (34, 'Matthew Wong', 'matthew.wong.2020@smu.edu.sg', 'matthew', 'Student'),
    (35, 'Grace Tan', 'grace.tan.2021@smu.edu.sg', 'grace', 'Student'),
    (36, 'Liam Koh', 'liam.koh.2022@smu.edu.sg', 'liam', 'Student'),
    (37, 'Emma Lee', 'emma.lee.2023@smu.edu.sg', 'emma', 'Student'),
    (38, 'Lucas Chan', 'lucas.chan.2020@smu.edu.sg', 'lucas', 'Student'),
    (39, 'Ava Ng', 'ava.ng.2021@smu.edu.sg', 'ava', 'Student'),
    (40, 'Noah Tan', 'noah.tan.2022@smu.edu.sg', 'noah', 'Student'),
	(41, 'Jennifer Smith', 'jennifer.smith@smu.edu.sg', 'jennifer', 'Instructor'),
	(42, 'Robert Johnson', 'robert.johnson@smu.edu.sg', 'robert', 'Instructor'),
	(43, 'Michelle Williams', 'michelle.williams@smu.edu.sg', 'michelle', 'Instructor'),
	(44, 'Daniel Brown', 'daniel.brown@smu.edu.sg', 'danielb', 'Instructor'),
	(45, 'Laura Davis', 'laura.davis@smu.edu.sg', 'laura', 'Instructor'),
	(46, 'Kevin Miller', 'kevin.miller@gmail.com', 'kevin', 'Trainer'),
	(47, 'Sarah Wilson', 'sarah.wilson@gmail.com', 'sarah', 'Trainer'),
	(48, 'Andrew Martinez', 'andrew.martinez@gmail.com', 'andrew', 'Trainer'),
	(49, 'Emily Anderson', 'emily.anderson@gmail.com', 'emilya', 'Trainer'),
	(50, 'Jason Taylor', 'jason.taylor@gmail.com', 'jason', 'Trainer'),
	(51, 'Nathan Tan', 'nathan.tan.2023@smu.edu.sg', 'nathan', 'Student'),
    (52, 'Sophie Lee', 'sophie.lee.2023@smu.edu.sg', 'sophie', 'Student'),
    (53, 'Michael Lim', 'michael.lim.2023@smu.edu.sg', 'michael', 'Student'),
    (54, 'Emma Ng', 'emma.ng.2023@smu.edu.sg', 'emma', 'Student'),
    (55, 'Alexander Koh', 'alexander.koh.2023@smu.edu.sg', 'alexander', 'Student'),
    (56, 'Sophia Tan', 'sophia.tan.2023@smu.edu.sg', 'sophia', 'Student'),
    (57, 'Jacob Wong', 'jacob.wong.2023@smu.edu.sg', 'jacob', 'Student');

DROP TABLE IF EXISTS `externaluser`;
CREATE TABLE IF NOT EXISTS `externaluser` (
	external_id int NOT NULL AUTO_INCREMENT, 
	user_id int NOT NULL, 
	organisation_name varchar(255),
	is_alumni boolean NOT NULL,
	PRIMARY KEY (`external_id`),
	FOREIGN KEY (user_id) REFERENCES user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO externaluser VALUES 
	(1, 3, 'NCS', 0),
	(2, 5, 'NCS', 1),
	(3, 46, 'IBM', 0),
	(4, 47, 'IBM', 1),
	(5, 48, 'IBM', 0),
	(6, 49, 'AWS', 0),
	(7, 50, 'AWS', 0);
	
DROP TABLE IF EXISTS `coursecategory`;
CREATE TABLE IF NOT EXISTS `coursecategory`(
	coursecat_id int NOT NULL AUTO_INCREMENT,
	coursecat_name varchar(10) NOT NULL,
	PRIMARY KEY (`coursecat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO coursecategory VALUES 
	(1, 'SCIS'),
	(2, 'SOE'),
	(3, 'SOB'),
	(4, 'SOSS'),
	(5, 'SOL'),
	(6, 'SOA');

DROP TABLE IF EXISTS `feedbacktemplate`;
CREATE TABLE IF NOT EXISTS `feedbacktemplate`(
	template_id int NOT NULL AUTO_INCREMENT,
	template_name varchar(255) NOT NULL,
	created_on date NOT NULL,
	PRIMARY KEY (`template_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO feedbacktemplate VALUES
	(1, 'Feedback 1', '2023-07-25');

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course`(
	course_id int NOT NULL AUTO_INCREMENT,
	course_name varchar(255) NOT NULL,
	course_desc varchar(800) NOT NULL,
	coursecat_id int NOT NULL,
    course_status varchar(255) NOT NULL, 
    template_id int,
	PRIMARY KEY (`course_id`),
    FOREIGN KEY (template_id) REFERENCES feedbacktemplate(template_id),
	FOREIGN KEY (coursecat_id) REFERENCES coursecategory(coursecat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO course VALUES
	(1, 'Dashboard Specialist', "This course caters to university students aiming to master the creation, management, and optimization of data visualization dashboards. Covering theoretical foundations and hands-on skills with dashboard tools, the curriculum includes effective design principles, data integration, interactive visualization creation, and data storytelling techniques. Students gain proficiency in leading dashboarding tools like Tableau, Power BI, etc., and learn to construct narratives from data. Accessibility and optimization strategies are emphasized, along with real-world projects and staying updated with trends.", 1, "Inactive"),
	(2, 'Quantum Leap', "Embark on a transformative journey into the cutting-edge realm of Quantum Leap, an advanced information systems course. Delve into the fusion of quantum computing, cryptography, and data management, and unravel the potential of quantum technologies for revolutionizing data processing and security. This course offers a deep dive into quantum principles, algorithms, and applications in the context of information systems. Learn to harness the power of quantum computing to solve complex problems that were once deemed insurmountable. Discover the intricacies of quantum cryptography, exploring techniques that leverage quantum phenomena to ensure unbreakable data protection.", 1, "Active"),
	(3, 'Intro to FISCOS BCOS Blockchain | WeBank Workshop', "Immerse in blockchain via 'Intro to FISCOS BCOS Blockchain' with WeBank. This concise course explores FISCO BCOS framework in info systems. Understand blockchain's core principles, decentralized structure, and data consensus. Learn via real-world examples like supply chains, digital IDs, and finance, grasping data integrity benefits. Hands-on sessions for setting up FISCO BCOS network provide practical skills. WeBank experts' insights enrich your learning, covering disruptions and implications. Gain a solid foundation in blockchain for IT pros, devs, and enthusiasts, navigating its transformative landscape confidently.", 1, "Inactive"),
	(4, 'Cybersecurity - Introduction to SSL Certificates', "Explore 'Introduction to SSL Certificates' in Cybersecurity. Delve into Secure Sockets Layer (SSL) technology, essential for secure online communication. Learn how SSL certificates encrypt data, ensuring confidentiality and integrity. Grasp the role of Certification Authorities in verifying website authenticity. Dive into certificate types, issuance, and renewal processes. Uncover common SSL vulnerabilities and best practices for robust web security. Gain insights into HTTPS implementation. Elevate your cybersecurity expertise with this SSL primer.", 1, "Active"),
	(5, 'Python Programming for Data Analysis', "This course unveils Python's power in handling and analyzing data. Learn data manipulation with libraries like Pandas, cleaning messy datasets, and performing exploratory analysis. Master visualization using Matplotlib and Seaborn. Explore statistical concepts and hypothesis testing. Harness Python's potential for data insights. Whether you're new to programming or advancing your skills, this course equips you to extract valuable information from data using Python.", 1, "Active"),
	(6, 'SAP Cloud Accelerated Learning Experience (S.C.A.L.E)', " This program revolutionizes SAP Cloud education. Dive into cloud technologies, from architecture to deployment. Explore SAP solutions, harnessing their potential. Uncover key cloud concepts, security measures, and best practices. Engage in hands-on labs, gaining real-world skills. Whether you're an IT professional or enthusiast, S.C.A.L.E. empowers you to excel in SAP Cloud environments. Elevate your expertise, embracing the future of enterprise technology with confidence.", 1, "Active"),
	(7, 'Pega System Architect Essentials', "This course is your gateway to mastering Pega's cutting-edge technology. Explore the Pega platform's core concepts, methodologies, and tools. Learn to design and implement robust business processes, create user interfaces, and integrate applications seamlessly. Dive into case management, data modeling, and decision strategies. With hands-on labs, you'll build practical skills in designing and deploying Pega applications. Whether you're a developer or an IT professional, this course empowers you to become a proficient Pega System Architect, driving innovation and efficiency.", 1, "Inactive"),
	(8, 'Overview of Big Data with Kx', "This course demystifies the world of massive data sets that drive modern decision-making. Explore the three Vs—Volume, Velocity, and Variety—that define big data. Learn the technologies shaping this landscape, from Hadoop and Spark to NoSQL databases. Delve into data processing, storage, and analysis techniques, uncovering insights that drive business success. Understand the challenges and opportunities posed by big data, from real-time analytics to machine learning. Whether you're new to data or expanding your knowledge, this course equips you to harness the power of big data in today's digital age.", 1, "Active"),
	(9, 'SAP Analytics Cloud', " This course introduces you to a transformative tool for data exploration, visualization, and business intelligence. Discover how SAP Analytics Cloud empowers you to connect to various data sources, create interactive dashboards, and perform advanced analytics. Dive into data modeling, blending, and transformation. Explore predictive analytics and machine learning capabilities that drive informed decisions. With hands-on practice, you'll develop skills in crafting compelling data stories. Whether you're an analyst, manager, or data enthusiast, this course unlocks the potential of SAP Analytics Cloud, elevating your ability to extract insights from data and propel your organization forward.", 1, "Inactive"),
	(10, 'Blockchain and Smart Contracts', "This course is a comprehensive course introducing you to the dynamic world of blockchain technology and its transformative application, smart contracts. Delve into the fundamentals of blockchain, understanding its decentralized and secure nature. Explore how smart contracts automate agreements and processes, revolutionizing industries. Discover prominent blockchain platforms like Ethereum, and delve into Solidity programming language to create and deploy smart contracts. With hands-on exercises, you'll gain practical skills in developing and implementing smart contracts. Whether you're a developer, business professional, or simply curious, this course empowers you to harness the potential of blockchain and smart contracts for innovation across various sectors.", 1, "Active"),
	(11, 'How to explore and navigate analytic dashboards with TIBCO Spotfire X', "Hands on coding of blockchain and smart contracts", 1, "Active"),
	(12, 'Mulesoft Certified Developer', "This course is your gateway to becoming an expert in MuleSoft's integration and API development platform. Dive into MuleSoft's Anypoint Platform, learning to design, build, and manage APIs and integrations effectively. Explore concepts like API design, data transformation, and connectivity using MuleSoft's tools. Gain hands-on experience in creating robust integrations that connect applications, data sources, and services seamlessly. Whether you're a developer or an IT professional, this program equips you with the skills to excel in the world of MuleSoft integration, earning you the coveted Mulesoft Certified Developer certification.", 1, "Active"),
	(13, 'Data Analysis with Python', "This course introduces you to the powerful tools and techniques for analyzing and extracting insights from data using Python. Learn how to manipulate and clean data with libraries like Pandas, visualize patterns with Matplotlib and Seaborn, and perform statistical analysis. Dive into real-world datasets, uncover trends, and make data-driven decisions. Whether you're a beginner or experienced in programming, this course equips you with the skills to explore and analyze data effectively, empowering you to derive valuable insights and contribute to informed decision-making.", 1, "Inactive"),
	(14, 'Intro to Digital Marketing', "This course is your gateway to the dynamic world of online marketing strategies and techniques. Explore the fundamentals of digital marketing, from search engine optimization (SEO) to social media marketing, pay-per-click advertising, and email campaigns. Dive into creating compelling content, building an online presence, and targeting the right audience. Understand analytics tools to measure and optimize your efforts. Whether you're a business owner, marketer, or simply curious about the digital landscape, this course equips you with the knowledge to navigate and excel in the ever-evolving realm of digital marketing.", 1, "Active"),
	(15, 'Intro to Drupal & Drupal Certification', "This program is designed to familiarize you with the versatile Drupal content management system and guide you towards becoming a certified Drupal professional. Explore the core concepts of Drupal, from content creation and management to site customization and theming. Delve into modules, understanding how they enhance functionality. Gain practical insights into user roles, permissions, and security settings. As you progress, you'll be prepared to pursue Drupal certification, validating your expertise in Drupal development and administration. With hands-on projects and real-world scenarios, you'll develop the skills needed to create, manage, and maintain robust Drupal-powered websites.", 1, "Active"),
	(16, 'Acquia Certified Site Builder', "This course is your pathway to becoming an expert in building and managing websites using the Acquia platform. Dive into Acquia's tools and technologies, learning to create, customize, and maintain websites efficiently. Explore website architecture, content creation, and customization. Gain hands-on experience with themes, modules, and extensions, tailoring websites to specific needs. Dive into site configuration, user management, and performance optimization. By mastering the Acquia platform, you'll be well-prepared to earn the coveted 'Acquia Certified Site Builder' certification.", 1, "Active"),
	(17, 'Analysing data made easy with SAP Analytics Cloud', " This program is designed to empower you with the skills and knowledge to effortlessly analyze and visualize data using SAP Analytics Cloud. Discover the intuitive features of SAP Analytics Cloud, from data connection and preparation to creating interactive dashboards and reports. Learn to perform ad-hoc analysis, explore data trends, and generate actionable insights. Delve into predictive analytics and machine learning capabilities, enhancing your ability to make informed decisions. Through hands-on exercises and real-world scenarios, you'll become proficient in harnessing the power of SAP Analytics Cloud.", 1, "Inactive"),
	(18, 'Stress Management with Technology', "In this course, we explore innovative ways to leverage technology for effective stress management. Discover a range of digital tools and techniques designed to reduce stress, improve well-being, and enhance your overall quality of life.", 1, "Inactive"),
	(19, 'Information Systems Management Fundamentals', "Explore the fundamental principles of managing information systems in modern organizations. Learn about system analysis, design, implementation, and maintenance. Understand how information systems align with business objectives and support decision-making processes. Dive into topics like database management, cybersecurity, and emerging technologies, equipping you to excel in overseeing effective and secure information systems.", 1, "Active"),
	(20, 'E-Commerce and Digital Business', "Uncover the dynamics of electronic commerce and digital business models. Examine the strategies and technologies behind successful online businesses. Learn about e-commerce platforms, payment gateways, digital marketing, and customer relationship management. Understand the challenges and opportunities in the digital marketplace, equipping you to thrive in the evolving world of online commerce.", 1, "Active"),
	(21, 'Business Intelligence and Analytic', "Delve into the world of business intelligence and analytics in this course. Learn how to gather, process, and analyze data to extract valuable insights for strategic decision-making. Explore data visualization techniques, predictive modeling, and data-driven storytelling. Gain hands-on experience with tools like Tableau and Power BI, enhancing your ability to turn raw data into actionable business intelligence.", 1, "Active"),
	(22, 'Enterprise Resource Planning (ERP) Systems', "Immerse yourself in the realm of Enterprise Resource Planning (ERP) systems. Understand how ERP software integrates various business functions like finance, supply chain, and human resources into a centralized system. Learn about ERP implementation, customization, and configuration. Gain insights into ERP benefits, challenges, and best practices, preparing you to effectively manage these complex systems.", 1, "Inactive"),
	(23, 'IT Project Management', "Master the art of managing information technology projects. Learn project planning, scope definition, resource allocation, and risk management. Explore agile and traditional project management methodologies. Understand the role of project managers in overseeing successful IT initiatives, ensuring projects are delivered on time, within scope, and aligned with business goals.", 1, "Active"),
	(24, 'Marketing Management', "Explore the principles of marketing, including market research, consumer behavior, branding, and marketing strategies. Learn to create effective marketing campaigns and develop skills to analyze market trends and customer preferences.", 3, "Inactive"),
	(25, 'Microeconomics', "Study the behavior of individual economic agents, such as consumers, firms, and markets. Explore concepts like supply and demand, elasticity, consumer choice, and market structures.", 2, "Inactive"),
	(26, 'Introduction to Sociology', "Explore the fundamental concepts of society, culture, and human behavior. Study social institutions, socialization, inequality, and the impact of social change on individuals and communities", 4, "Inactive"),
	(27, 'Constitutional Law', "Study the constitution and its impact on government and individual rights. Explore topics such as separation of powers, federalism, and constitutional interpretation.", 5, "Active"),
	(28, 'Cost Accounting', "Focus on understanding and analyzing costs in business operations. Learn techniques for cost allocation, cost-volume-profit analysis, and cost estimation.", 6, "Active"),
	(29, 'Ethics in Accounting', "Examine ethical considerations in the field of accounting. Learn about professional ethics, conflicts of interest, confidentiality, and the role of accountants in maintaining integrity.", 6, "Inactive"),
    (30, 'Vue.js Mastery: Building Interactive Web Applications', "Unlock the full potential of Vue.js and become a front-end development master with our comprehensive Vue.js Mastery course. Whether you're a beginner looking to get started or an experienced developer seeking to enhance your skills, this course has something for everyone.", 1, "Inactive");

DROP TABLE IF EXISTS `proposedcourse`;
CREATE TABLE IF NOT EXISTS `proposedcourse`(
	pcourse_id int NOT NULL AUTO_INCREMENT,
	submitted_by int NOT NULL,
	course_id int NOT NULL,
	pcourse_status varchar(20) NOT NULL,
    action_done_by int, 
    reason varchar(255),
    proposed_date date NOT NULL,
    votecount int default 0,
	PRIMARY KEY (`pcourse_id`),
	FOREIGN KEY (submitted_by) REFERENCES user(user_id),
    FOREIGN KEY (action_done_by) REFERENCES user(user_id),
	FOREIGN KEY (course_id) REFERENCES course(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO proposedcourse VALUES 
	(1, 3, 1, 'Approved', 2, NULL, "2023-08-25", 1),
	(2, 3, 2, 'Approved', 2, NULL, "2023-08-25", 21),
	(3, 4, 3, 'Approved', 2, NULL, "2023-08-25", 5),
	(4, 4, 4, 'Approved', 2, NULL, "2023-08-25", 21),
	(5, 5, 6, 'Approved', 2, NULL, "2023-08-25", 20),
	(6, 5, 7, 'Approved', 2, NULL, "2023-08-25", 4),
	(7, 4, 8, 'Approved', 2, NULL, "2023-08-25", 21),
	(8, 5, 9, 'Approved', 2, NULL, "2023-08-25", 7),
	(9, 1, 13, 'Approved', 2, NULL, "2023-08-25", 7),
	(10, 1, 19, 'Pending', 2, NULL, "2023-08-25", 0), 
	(11, 1, 20, 'Rejected', 2, 'Alignment with curriculum', "2023-08-25", 0),
	(12, 3, 21, 'Approved', 2, NULL, "2023-08-25", 20),
	(13, 4, 22, 'Approved', 2, NULL, "2023-08-25", 7), 
	(14, 5, 23, 'Approved', 2, NULL, "2023-08-25", 20),
	(15, 3, 24, 'Approved', 2, NULL, "2023-08-25", 9),
	(16, 4, 25, 'Approved', 2, NULL, "2023-08-25", 9), 
	(17, 5, 26, 'Approved', 2, NULL, "2023-08-25", 9),
	(18, 3, 27, 'Approved', 2, NULL, "2023-08-25", 20),
	(19, 6, 28, 'Approved', 2, NULL, "2023-08-25", 20), 
	(20, 6, 29, 'Approved', 2, NULL, "2023-08-26", 12), 
	(21, 4, 11, 'Rejected', 2, 'Alignment with curriculum', "2023-08-25", 0),
    (22, 4, 30, 'Pending', 2, NULL, "2023-09-01", 0);
	

DROP TABLE IF EXISTS `votecourse`;
CREATE TABLE IF NOT EXISTS `votecourse`(
	vote_id int NOT NULL AUTO_INCREMENT,
	course_id int NOT NULL,
	vote_status varchar(15) NOT NULL,
	PRIMARY KEY (`vote_id`),
	FOREIGN KEY (course_id) REFERENCES course(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO votecourse VALUES
	(1, 1, 'Ongoing'),
	(2, 2, 'Offered'),
	(3, 3,'Closed'),
	(4, 4, 'Offered'), 
	(5, 6, 'Offered'),
	(6, 7, 'Ongoing'),
	(7, 8, 'Offered'),
	(8, 9, 'Closed'),
	(9, 13, 'Ongoing'), 
	(10, 21, 'Offered'),
	(11, 22, 'Ongoing'),
	(12, 23, 'Offered'),
	(13, 24, 'Closed'),
	(14, 25, 'Ongoing'), 
	(15, 26, 'Ongoing'),
	(16, 27, 'Offered'),
	(17, 28, 'Offered'),
	(18, 29, 'Closed');
	
DROP TABLE IF EXISTS `interest`;
CREATE TABLE IF NOT EXISTS `interest`(
	interest_id int NOT NULL AUTO_INCREMENT,
	vote_id int NOT NULL,
	user_id int NOT NULL,
	PRIMARY KEY (`interest_id`),
	FOREIGN KEY (vote_id) REFERENCES votecourse(vote_id),
	FOREIGN KEY (user_id) REFERENCES user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO interest VALUES
	-- vote_id 1
	(1, 1, 1), (2, 2, 1), (3, 4, 1), (4, 7, 1),
	-- vote_id 2
    (5, 2, 6), (6, 2, 7), (7, 2, 11), (8, 2, 12), (9, 2, 13),
    (10, 2, 14), (11, 2, 15), (12, 2, 16), (13, 2, 17), (14, 2, 18),
    (15, 2, 19), (16, 2, 20), (17, 2, 21), (18, 2, 22), (19, 2, 23),
    (20, 2, 24), (21, 2, 25), (22, 2, 26), (23, 2, 27), (24, 2, 28),

    -- vote_id 4
    (25, 4, 6), (26, 4, 7), (27, 4, 11), (28, 4, 12), (29, 4, 13),
    (30, 4, 14), (31, 4, 15), (32, 4, 16), (33, 4, 17), (34, 4, 18),
    (35, 4, 19), (36, 4, 20), (37, 4, 21), (38, 4, 22), (39, 4, 23),
    (40, 4, 24), (41, 4, 25), (42, 4, 26), (43, 4, 27), (44, 4, 28),

    -- vote_id 5
    (45, 5, 6), (46, 5, 7), (47, 5, 11), (48, 5, 12), (49, 5, 13),
    (50, 5, 14), (51, 5, 15), (52, 5, 16), (53, 5, 17), (54, 5, 18),
    (55, 5, 19), (56, 5, 20), (57, 5, 21), (58, 5, 22), (59, 5, 23),
    (60, 5, 24), (61, 5, 25), (62, 5, 26), (63, 5, 27), (64, 5, 28),

    -- vote_id 7
    (65, 7, 6), (66, 7, 7), (67, 7, 11), (68, 7, 12), (69, 7, 13),
    (70, 7, 14), (71, 7, 15), (72, 7, 16), (73, 7, 17), (74, 7, 18),
    (75, 7, 19), (76, 7, 20), (77, 7, 21), (78, 7, 22), (79, 7, 23),
    (80, 7, 24), (81, 7, 25), (82, 7, 26), (83, 7, 27), (84, 7, 28),

    -- vote_id 10
    (85, 10, 6), (86, 10, 7), (87, 10, 11), (88, 10, 12), (89, 10, 13),
    (90, 10, 14), (91, 10, 15), (92, 10, 16), (93, 10, 17), (94, 10, 18),
    (95, 10, 19), (96, 10, 20), (97, 10, 21), (98, 10, 22), (99, 10, 23),
    (100, 10, 24), (101, 10, 25), (102, 10, 26), (103, 10, 27), (104, 10, 28),

    -- vote_id 12
    (105, 12, 6), (106, 12, 7), (107, 12, 11), (108, 12, 12), (109, 12, 13),
    (110, 12, 14), (111, 12, 15), (112, 12, 16), (113, 12, 17), (114, 12, 18),
    (115, 12, 19), (116, 12, 20), (117, 12, 21), (118, 12, 22), (119, 12, 23),
    (120, 12, 24), (121, 12, 25), (122, 12, 26), (123, 12, 27), (124, 12, 28),

    -- vote_id 16
    (125, 16, 6), (126, 16, 7), (127, 16, 11), (128, 16, 12), (129, 16, 13),
    (130, 16, 14), (131, 16, 15), (132, 16, 16), (133, 16, 17), (134, 16, 18),
    (135, 16, 19), (136, 16, 20), (137, 16, 21), (138, 16, 22), (139, 16, 23),
    (140, 16, 24), (141, 16, 25), (142, 16, 26), (143, 16, 27), (144, 16, 28),

    -- vote_id 17
    (145, 17, 6), (146, 17, 7), (147, 17, 11), (148, 17, 12), (149, 17, 13),
    (150, 17, 14), (151, 17, 15), (152, 17, 16), (153, 17, 17), (154, 17, 18),
    (155, 17, 19), (156, 17, 20), (157, 17, 21), (158, 17, 22), (159, 17, 23),
    (160, 17, 24), (161, 17, 25), (162, 17, 26), (163, 17, 27), (164, 17, 28),

	-- vote_id 3
    (165, 3, 6), (166, 3, 7), (167, 3, 11), (168, 3, 12), (169, 3, 13),

	-- vote_id 6
    (170, 6, 6), (171, 6, 7), (172, 6, 11), (173, 6, 12),

	-- vote_id 8
    (174, 8, 6), (175, 8, 7), (176, 8, 11), (177, 8, 12), (178, 8, 13), (179, 8, 14), (180, 8, 15),

	-- vote_id 9
    (181, 9, 6), (182, 9, 7), (183, 9, 11), (184, 9, 12), (185, 9, 13), (186, 9, 14), (187, 9, 15),

	-- vote_id 11
    (188, 11, 6), (189, 11, 7), (190, 11, 11), (191, 11, 12), (192, 11, 13), (193, 11, 14), (194, 11, 15),

	-- vote_id 13
    (195, 13, 6), (196, 13, 7), (197, 13, 11), (198, 13, 12), (199, 13, 13), (200, 13, 14), (201, 13, 15), (202, 13, 16), (203, 13, 17),

	-- vote_id 14
    (204, 14, 6), (205, 14, 7), (206, 14, 11), (207, 14, 12), (208, 14, 13), (209, 14, 14), (210, 14, 15), (211, 14, 16), (212, 14, 17),

	-- vote_id 15
    (213, 15, 6), (214, 15, 7), (215, 15, 11), (216, 15, 12), (217, 15, 13), (218, 15, 14), (219, 15, 15), (220, 15, 16), (221, 15, 17),

	-- vote_id 18
    (222, 18, 6), (223, 18, 7), (224, 18, 11), (225, 18, 12), (226, 18, 13), (227, 18, 14), (228, 18, 15), (229, 18, 16), (230, 18, 17), (231, 18, 18), (232, 18, 19), (233, 18, 20);
	


DROP TABLE IF EXISTS `templateattribute`;
CREATE TABLE IF NOT EXISTS `templateattribute`(
	template_attribute_id int NOT NULL AUTO_INCREMENT,
	question varchar(255) NOT NULL,
	input_type varchar(255) NOT NULL,
	template_id int NOT NULL,
	PRIMARY KEY (`template_attribute_id`),
	FOREIGN KEY (template_id) REFERENCES feedbacktemplate(template_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO templateattribute VALUES 
	(1, 'Content - How would you rate the course content and course structure?', 'Likert Scale', 1),
	(2, 'Duration - How would you rate the course content and course structure?', 'Likert Scale', 1),
	(3, 'Relevancy - How would you rate the course content and course structure?', 'Likert Scale', 1),
	(4, 'What are the areas of the course that was done well?', 'Text', 1),
	(5, 'What are the areas of the course can we can improve?', 'Text', 1), 
	(6, 'Clarity - How would you rate the Instructor?', 'Likert Scale', 1),
	(7, 'Pace - How would you rate the Instructor?', 'Likert Scale', 1),
	(8, 'Helpfulness - How would you rate the Instructor?', 'Likert Scale', 1),
	(9, 'Knowledge - How would you rate the Instructor?', 'Likert Scale', 1),
	(10, 'What are the areas that the instructor did well on?', 'Text', 1),
	(11, 'What are the areas that the instructor can improve on?', 'Text', 1);

DROP TABLE IF EXISTS `inputoption`;
CREATE TABLE IF NOT EXISTS `inputoption`(
	input_option_id int NOT NULL AUTO_INCREMENT,
	template_attribute_id int NOT NULL,
	position int NOT NULL,
	textlabel varchar(255) NOT NULL,
	PRIMARY KEY (`input_option_id`),
	FOREIGN KEY (template_attribute_id) REFERENCES templateattribute(template_attribute_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO inputoption VALUES 
	(1, 1, 1, 'Lowest'), 
	(2, 1, 2, 'Low'),
	(3, 1, 3, 'Neutral'),
	(4, 1, 4, 'High'),
	(5, 1, 5, 'Highest'),
	(6, 2, 1, 'Lowest'), 
	(7, 2, 2, 'Low'),
	(8, 2, 3, 'Neutral'),
	(9, 2, 4, 'High'),
	(10, 2, 5, 'Highest'),
	(11, 3, 1, 'Lowest'), 
	(12, 3, 2, 'Low'),
	(13, 3, 3, 'Neutral'),
	(14, 3, 4, 'High'),
	(15, 3, 5, 'Highest'),
	(16, 6, 1, 'Not Clear'), 
	(17, 6, 2, 'Somewhat Clear'),
	(18, 6, 3, 'Moderately Clear'),
	(19, 6, 4, 'Very Clear'),
	(20, 6, 5, 'Extremely Clear'),
	(21, 7, 1, 'Too Slow'), 
	(22, 7, 2, 'Somewhat Slow'),
	(23, 7, 3, 'Moderate'),
	(24, 7, 4, 'Fast'),
	(25, 7, 5, 'Too Fast'),
	(26, 8, 1, 'Not Helpful'), 
	(27, 8, 2, 'Somewhat Helpful'),
	(28, 8, 3, 'Moderately Helpful'),
	(29, 8, 4, 'Very Helpful'),
	(30, 8, 5, 'Extremely Helpful'),
	(31, 9, 1, 'Poor Knowledge'), 
	(32, 9, 2, 'Below Average Knowledge'),
	(33, 9, 3, 'Average Knowledge'),
	(34, 9, 4, 'Above Average Knowledge'),
	(35, 9, 5, 'Excellent Knowledge');

DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback`(
	feedback_id int NOT NULL AUTO_INCREMENT,
	feedback_template_id int NOT NULL,
	submitted_by int NOT NULL,
	template_attribute_id int NOT NULL,
	answer varchar(255) NOT NULL,
	course_id int NOT NULL,
	PRIMARY KEY (`feedback_id`),
	FOREIGN KEY (template_attribute_id) REFERENCES templateattribute(template_attribute_id),
	FOREIGN KEY (course_id) REFERENCES course(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO feedback VALUES 
	-- user_id 1
	(1, 1, 1, 1, '4', 2),
    (2, 1, 1, 2, '3', 2),
    (3, 1, 1, 3, '5', 2),
    (4, 1, 1, 4, 'The content was well-structured.', 2),
    (5, 1, 1, 5, 'More practical examples would be helpful.', 2),
    (6, 1, 1, 6, '5', 2),
    (7, 1, 1, 7, '4', 2),
    (8, 1, 1, 8, '5', 2),
    (9, 1, 1, 9, '4', 2),
    (10, 1, 1, 10, 'The instructor explained complex concepts clearly.', 2),
    (11, 1, 1, 11, 'Can be more engaging.', 2),
	-- user_id 6
    (12, 1, 6, 1, '3', 2),
    (13, 1, 6, 2, '4', 2),
    (14, 1, 6, 3, '4', 2),
    (15, 1, 6, 4, 'The content was comprehensive.', 2),
    (16, 1, 6, 5, 'More real-world examples needed.', 2),
    (17, 1, 6, 6, '4', 2),
    (18, 1, 6, 7, '5', 2),
    (19, 1, 6, 8, '4', 2),
    (20, 1, 6, 9, '5', 2),
    (21, 1, 6, 10, 'Excellent delivery of complex topics. I am able to understand it well.', 2),
    (22, 1, 6, 11, 'Overall I think is great but could be more interactive.', 2),
	-- user_id 7
	(23, 1, 7, 1, '5', 2),
    (24, 1, 7, 2, '4', 2),
    (25, 1, 7, 3, '3', 2),
    (26, 1, 7, 4, 'I think the course content was well-structured and comprehensive.', 2),
    (27, 1, 7, 5, 'More exercises would be beneficial.', 2),
    (28, 1, 7, 6, '4', 2),
    (29, 1, 7, 7, '3', 2),
    (30, 1, 7, 8, '4', 2),
    (31, 1, 7, 9, '4', 2),
    (32, 1, 7, 10, 'Clear explanations, but need more examples.', 2),
    (33, 1, 7, 11, 'Instructor''s pace was a bit fast at times.', 2),
	-- user_id 8
	(34, 1, 8, 1, '3', 2),
    (35, 1, 8, 2, '4', 2),
    (36, 1, 8, 3, '4', 2),
    (37, 1, 8, 4, 'The course content was informative and comprehensive.', 2),
    (38, 1, 8, 5, 'Can have more practical assignments and quizzes.', 2),
    (39, 1, 8, 6, '3', 2),
    (40, 1, 8, 7, '4', 2),
    (41, 1, 8, 8, '3', 2),
    (42, 1, 8, 9, '4', 2),
    (43, 1, 8, 10, 'The instructor''s knowledge was evident. He was able to explain clearly for most topics.', 2),
    (44, 1, 8, 11, 'Overall pace is okay but for more complex topics, I think it can be slower.', 2),
    -- user_id 9
    (45, 1, 9, 1, '5', 2),
    (46, 1, 9, 2, '5', 2),
    (47, 1, 9, 3, '5', 2),
    (48, 1, 9, 4, 'The course content was engaging and practical.', 2),
    (49, 1, 9, 5, 'More interactive activities would enhance learning.', 2),
    (50, 1, 9, 6, '5', 2),
    (51, 1, 9, 7, '5', 2),
    (52, 1, 9, 8, '5', 2),
    (53, 1, 9, 9, '5', 2),
    (54, 1, 9, 10, 'The instructor''s teaching style was effective. He is very helpful.', 2),
    (55, 1, 9, 11, 'The instructor''s communication was clear. Can be more interactive.', 2),
    -- user_id 10
    (56, 1, 10, 1, '3', 2),
    (57, 1, 10, 2, '4', 2),
    (58, 1, 10, 3, '3', 2),
    (59, 1, 10, 4, 'The course content was satisfactory.', 2),
    (60, 1, 10, 5, 'More real-world case studies would be valuable.', 2),
    (61, 1, 10, 6, '4', 2),
    (62, 1, 10, 7, '3', 2),
    (63, 1, 10, 8, '4', 2),
    (64, 1, 10, 9, '3', 2),
    (65, 1, 10, 10, 'The instructor''s explanations were clear and he is helpful when asked questions.', 2),
    (66, 1, 10, 11, 'The instructor''s pace was a bit fast at times. Can be more engaging and fun.', 2),
	-- user_id 11
	(67, 1, 11, 1, '4', 2),
    (68, 1, 11, 2, '4', 2),
    (69, 1, 11, 3, '3', 2),
    (70, 1, 11, 4, 'The course content was well-structured.', 2),
    (71, 1, 11, 5, 'More practical examples would be helpful.', 2),
    (72, 1, 11, 6, '4', 2),
    (73, 1, 11, 7, '3', 2),
    (74, 1, 11, 8, '4', 2),
    (75, 1, 11, 9, '3', 2),
    (76, 1, 11, 10, 'The instructor was knowledgeable.', 2),
    (77, 1, 11, 11, 'The instructor''s explanations were clear. Lesson can be more engaging.', 2),
    -- User 12
    (78, 1, 12, 1, '5', 2),
    (79, 1, 12, 2, '5', 2),
    (80, 1, 12, 3, '5', 2),
    (81, 1, 12, 4, 'The course content was well-structured and practical.', 2),
    (82, 1, 12, 5, 'More interactive activities would enhance learning.', 2),
    (83, 1, 12, 6, '5', 2),
    (84, 1, 12, 7, '5', 2),
    (85, 1, 12, 8, '5', 2),
    (86, 1, 12, 9, '5', 2),
    (87, 1, 12, 10, 'His explanantion were clear and he is very helpful. I really appreciate it.', 2),
    (88, 1, 12, 11, 'The instructor''s communication was clear. Lesson can be more fun if there are examples.', 2),
    -- User 13
    (89, 1, 13, 1, '3', 2),
    (90, 1, 13, 2, '4', 2),
    (91, 1, 13, 3, '3', 2),
    (92, 1, 13, 4, 'The course content was satisfactory.', 2),
    (93, 1, 13, 5, 'More real-world case studies would be valuable.', 2),
    (94, 1, 13, 6, '4', 2),
    (95, 1, 13, 7, '3', 2),
    (96, 1, 13, 8, '4', 2),
    (97, 1, 13, 9, '3', 2),
    (98, 1, 13, 10, 'The instructor''s explanations were clear.', 2),
    (99, 1, 13, 11, 'The instructor''s pace was appropriate for less complex topics. I think lesson can be more engaging.', 2),
    -- User 14
    (100, 1, 14, 1, '4', 2),
    (101, 1, 14, 2, '3', 2),
    (102, 1, 14, 3, '4', 2),
    (103, 1, 14, 4, 'The course content was well-organized.', 2),
    (104, 1, 14, 5, 'More hands-on exercises would be beneficial.', 2),
    (105, 1, 14, 6, '3', 2),
    (106, 1, 14, 7, '4', 2),
    (107, 1, 14, 8, '3', 2),
    (108, 1, 14, 9, '4', 2),
    (109, 1, 14, 10, 'His explanation is quite clear.', 2),
    (110, 1, 14, 11, 'Overall pace is great but can be slower for more complex topics. Can give more examples so that we can understand better.', 2),
    -- User 15
    (111, 1, 15, 1, '5', 2),
    (112, 1, 15, 2, '4', 2),
    (113, 1, 15, 3, '5', 2),
    (114, 1, 15, 4, 'Personally, I think the course content was excellent. Love the content taught.', 2),
    (115, 1, 15, 5, 'More real-world examples would enhance the course.', 2),
    (116, 1, 15, 6, '5', 2),
    (117, 1, 15, 7, '4', 2),
    (118, 1, 15, 8, '5', 2),
    (119, 1, 15, 9, '4', 2),
    (120, 1, 15, 10, 'The instructor was engaging. He is able to explain clearly when students asked questions.', 2),
    (121, 1, 15, 11, 'The instructor could provide more practice quizzes so that it can be more interactive.', 2),
	-- User 16
    (122, 1, 16, 1, '3', 2),
    (123, 1, 16, 2, '4', 2),
    (124, 1, 16, 3, '3', 2),
    (125, 1, 16, 4, 'The course content was satisfactory.', 2),
    (126, 1, 16, 5, 'More real-world case studies would be valuable.', 2),
    (127, 1, 16, 6, '4', 2),
    (128, 1, 16, 7, '3', 2),
    (129, 1, 16, 8, '4', 2),
    (130, 1, 16, 9, '3', 2),
    (131, 1, 16, 10, 'The instructor was knowledgeable. He is able to explain clearly when students asked questions.', 2),
    (132, 1, 16, 11, 'The instructor''s explanations were clear. Lesson can be more engaging and interactive.', 2),
    -- User 17
    (133, 1, 17, 1, '5', 2),
    (134, 1, 17, 2, '5', 2),
    (135, 1, 17, 3, '5', 2),
    (136, 1, 17, 4, 'The course content was engaging and practical.', 2),
    (137, 1, 17, 5, 'I think can have more interactive activities as it would enhance learning.', 2),
    (138, 1, 17, 6, '5', 2),
    (139, 1, 17, 7, '5', 2),
    (140, 1, 17, 8, '5', 2),
    (141, 1, 17, 9, '5', 2),
    (142, 1, 17, 10, 'The instructor was knowledgeable and engaging. His explanation was clear', 2),
    (143, 1, 17, 11, 'The instructor could provide more practice quizzes so that we can understand better and easily.', 2),
    -- User 18
    (144, 1, 18, 1, '3', 2),
    (145, 1, 18, 2, '4', 2),
    (146, 1, 18, 3, '3', 2),
    (147, 1, 18, 4, 'The course content was quite engaging.', 2),
    (148, 1, 18, 5, 'More real-world case studies would be valuable.', 2),
    (149, 1, 18, 6, '4', 2),
    (150, 1, 18, 7, '3', 2),
    (151, 1, 18, 8, '4', 2),
    (152, 1, 18, 9, '3', 2),
    (153, 1, 18, 10, 'The instructor was knowledgeable. He is helpful when we ask him questions.', 2),
    (154, 1, 18, 11, 'Overall pace is great but can be slower for more complex topics. Can give more examples so that we can understand better.', 2),

    -- User 19
    (155, 1, 19, 1, '4', 2),
    (156, 1, 19, 2, '4', 2),
    (157, 1, 19, 3, '3', 2),
    (158, 1, 19, 4, 'The course content was well-structured.', 2),
    (159, 1, 19, 5, 'More practical examples would be helpful.', 2),
    (160, 1, 19, 6, '4', 2),
    (161, 1, 19, 7, '3', 2),
    (162, 1, 19, 8, '4', 2),
    (163, 1, 19, 9, '3', 2),
    (164, 1, 19, 10, 'The instructor was knowledgeable.', 2),
    (165, 1, 19, 11, 'Pace can be slower for more complex topics.', 2),

    -- User 20
    (166, 1, 20, 1, '5', 2),
    (167, 1, 20, 2, '5', 2),
    (168, 1, 20, 3, '5', 2),
    (169, 1, 20, 4, 'The course content was quite engaging and practical.', 2),
    (170, 1, 20, 5, 'More interactive activities would enhance learning.', 2),
    (171, 1, 20, 6, '5', 2),
    (172, 1, 20, 7, '5', 2),
    (173, 1, 20, 8, '5', 2),
    (174, 1, 20, 9, '5', 2),
    (175, 1, 20, 10, 'He is helpful and able to explain to question asked well.', 2),
    (176, 1, 20, 11, 'I think lesson can be more interactive and engaging with hands-on activities or quizzes. ', 2),
	-- User 21
    (177, 1, 21, 1, '3', 2),
    (178, 1, 21, 2, '4', 2),
    (179, 1, 21, 3, '3', 2),
    (180, 1, 21, 4, 'I think the course content was satisfactory and well-structured.', 2),
    (181, 1, 21, 5, 'More real-world case studies would be valuable.', 2),
    (182, 1, 21, 6, '4', 2),
    (183, 1, 21, 7, '3', 2),
    (184, 1, 21, 8, '4', 2),
    (185, 1, 21, 9, '3', 2),
    (186, 1, 21, 10, 'The instructor was knowledgeable. He is able to explain clearly.', 2),
    (187, 1, 21, 11, 'Pace can be slower for more complex topics.', 2),
    -- User 22
    (188, 1, 22, 1, '4', 2),
    (189, 1, 22, 2, '4', 2),
    (190, 1, 22, 3, '3', 2),
    (191, 1, 22, 4, 'The course content was well-structured.', 2),
    (192, 1, 22, 5, 'More practical examples would be helpful.', 2),
    (193, 1, 22, 6, '4', 2),
    (194, 1, 22, 7, '3', 2),
    (195, 1, 22, 8, '4', 2),
    (196, 1, 22, 9, '3', 2),
    (197, 1, 22, 10, 'The instructor was knowledgeable. He explain quite well and is helpful.', 2),
    (198, 1, 22, 11, 'Overall pace is okay but can be slower for more complex topics so that we can understand better and easily.', 2),
	-- User 23
    (199, 1, 23, 1, '4', 2),
    (200, 1, 23, 2, '4', 2),
    (201, 1, 23, 3, '3', 2),
    (202, 1, 23, 4, 'The course content was well-structured.', 2),
    (203, 1, 23, 5, 'More practical examples would be helpful.', 2),
    (204, 1, 23, 6, '4', 2),
    (205, 1, 23, 7, '3', 2),
    (206, 1, 23, 8, '4', 2),
    (207, 1, 23, 9, '3', 2),
    (208, 1, 23, 10, 'He is helpful and can explain quite well.', 2),
    (209, 1, 23, 11, 'Least complex topics can be faster. More complex topics can be slower, to ensure we can understand it well.', 2),

    -- User 24
    (210, 1, 24, 1, '5', 2),
    (211, 1, 24, 2, '5', 2),
    (212, 1, 24, 3, '5', 2),
    (213, 1, 24, 4, 'Personally, I think the course content was quite practical.', 2),
    (214, 1, 24, 5, 'More interactive activities would enhance learning.', 2),
    (215, 1, 24, 6, '5', 2),
    (216, 1, 24, 7, '5', 2),
    (217, 1, 24, 8, '5', 2),
    (218, 1, 24, 9, '5', 2),
    (219, 1, 24, 10, 'He is helpful when asked questions. He is friendly, easy for us to approach him.', 2),
    (220, 1, 24, 11, 'The instructor''s communication was clear. Lesson can be more fun and engaging if there are examples.', 2),

    -- User 40
    (221, 1, 40, 1, '4', 2),
    (222, 1, 40, 2, '4', 2),
    (223, 1, 40, 3, '3', 2),
    (224, 1, 40, 4, 'The course content was well-structured.', 2),
    (225, 1, 40, 5, 'More practical examples would be helpful.', 2),
    (226, 1, 40, 6, '4', 2),
    (227, 1, 40, 7, '3', 2),
    (228, 1, 40, 8, '4', 2),
    (229, 1, 40, 9, '3', 2),
    (230, 1, 40, 10, 'Overall his explanation is easy to understand and he is very helpful and friendly.', 2),
    (231, 1, 40, 11, 'I think it could be more evenly paced. Some lesson paces were okay, but some were faster.', 2),

    -- User 51
    (232, 1, 51, 1, '5', 2),
    (233, 1, 51, 2, '5', 2),
    (234, 1, 51, 3, '5', 2),
    (235, 1, 51, 4, 'The course content was well structured.', 2),
    (236, 1, 51, 5, 'More interactive activities would help us better to understand the course or topic.', 2),
    (237, 1, 51, 6, '5', 2),
    (238, 1, 51, 7, '5', 2),
    (239, 1, 51, 8, '5', 2),
    (240, 1, 51, 9, '5', 2),
    (241, 1, 51, 10, 'He is very helpful and friendly. I can approach him easily when I got questions.', 2),
    (242, 1, 51, 11, 'The instructor''s communication was clear.', 2),
    -- User 52
    (243, 1, 52, 1, '3', 2),
    (244, 1, 52, 2, '4', 2),
    (245, 1, 52, 3, '3', 2),
    (246, 1, 52, 4, 'The course content was satisfactory.', 2),
    (247, 1, 52, 5, 'I think can have more real-world case studies as it would help us to understand better.', 2),
    (248, 1, 52, 6, '4', 2),
    (249, 1, 52, 7, '3', 2),
    (250, 1, 52, 8, '4', 2),
    (251, 1, 52, 9, '3', 2),
    (252, 1, 52, 10, 'He is easy to approach and he explains well.', 2),
    (253, 1, 52, 11, 'Some lesson paces were okay, but some were faster. Overall, I think it could be more evenly paced.', 2);


DROP TABLE IF EXISTS `runcourse`;
CREATE TABLE IF NOT EXISTS `runcourse`(
	rcourse_id int NOT NULL AUTO_INCREMENT,
	run_startdate date,
	run_enddate date,
	run_starttime time,
	run_endtime time,
	instructor_id int,
	course_format varchar(20),
	course_venue varchar(255), -- can be null for those online courses
	runcourse_status varchar(15),
	course_size int, 
	course_minsize int,
	course_fee int,
	class_duration int,
	reg_startdate date,
	reg_enddate date,
	reg_starttime time,
	reg_endtime time,
	course_id int,
	PRIMARY KEY (`rcourse_id`),
	FOREIGN KEY (instructor_id) REFERENCES user(user_id),
	FOREIGN KEY (course_id) REFERENCES course(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO runcourse VALUES
	(1, '2023-07-10', '2023-08-07', '12:00:00', '14:00:00', 4, 'face-to-face', 'SCIS SR 2-4', 'Closed', 35, 20, 0, 2, '2023-06-05', '2023-06-10', '10:00:00', '10:00:00', 2, 'Inactive'), 
    (2, '2023-09-05', '2023-10-05', '09:00:00', '11:00:00', 3, 'face-to-face', 'SCIS SR 3-3', 'Closed', 30, 15, 0, 2, '2023-08-01', '2023-08-06', '10:00:00', '10:00:00', 4, 'Active'),
    (3, '2023-10-15', '2023-11-15', '15:00:00', '17:00:00', 5, 'face-to-face', 'SCIS SR 3-3', 'Ongoing', 25, 15, 10, 2, '2023-09-01', '2023-09-06', '10:00:00', '10:00:00', 6, 'Active'),
    (4, '2023-11-20', '2023-12-20', '10:00:00', '12:00:00', 46, 'face-to-face', 'SCIS SR 3-3', 'Ongoing', 40, 25, 15, 2, '2023-10-05', '2023-10-10', '10:00:00', '10:00:00', 8, 'Active'),
    (5, '2023-10-10', '2023-11-10', '14:00:00', '16:00:00', 41, 'online', NULL , 'Ongoing', 30, 20, 0, 2, '2023-09-12', '2023-09-17', '10:00:00', '10:00:00', 21, 'Active'),
    (6, '2023-11-01', '2023-11-20', '15:00:00', '17:00:00', 47, 'face-to-face', 'SCIS SR 3-3', 'Ongoing', 20, 15, 10, 2, '2023-10-05', '2023-10-10', '10:00:00', '10:00:00', 23, 'Active'),
    (7, '2023-11-01', '2023-11-25', '17:00:00', '19:00:00', 42, 'face-to-face', 'SCIS SR 3-3', 'Ongoing', 35, 10, 0, 2, '2023-10-02', '2023-10-07', '10:00:00', '10:00:00', 27, 'Active'),
    (8, '2023-11-20', '2023-12-10', '13:00:00', '15:30:00', 43, 'online', NULL, 'Ongoing', 25, 15, 0, 2, '2023-10-20', '2023-10-25', '10:00:00', '10:00:00', 28, 'Active'),
    (9, '2023-12-05', '2023-12-20', '10:00:00', '11:00:00', 44, 'face-to-face', 'SCIS SR 3-3', 'Ongoing', 30, 20, 0, 1, '2023-11-10', '2023-11-15', '10:00:00', '10:00:00', 17, 'Active'),
    (10, '2023-10-01', '2023-10-25', '10:00:00', '11:00:00', 19, 'online', NULL, 'Closed', 30, 20, 0, 1, '2023-09-03', '2023-09-08', '10:00:00', '10:00:00', 17, 'Inactive'),
    (11, '2023-09-15', '2023-10-15', '09:00:00', '12:00:00', 20, 'face-to-face', 'SCIS SR 2-3', 'Closed', 40, 25, 50, 2, '2023-08-01', '2023-08-05', '10:00:00', '10:00:00', 18, 'Inactive'),
    (12, '2023-12-05', '2023-12-25', '14:00:00', '16:00:00', 3, 'face-to-face', 'SCIS SR 3-3', 'Ongoing', 25, 15, 0, 2, '2023-10-15', '2023-10-20', '10:00:00', '10:00:00', 5, 'Active'),
    (13, '2023-11-25', '2023-12-15', '16:00:00', '18:00:00', 5, 'face-to-face', 'SCIS SR 2-4', 'Ongoing', 35, 20, 0, 2, '2023-10-10', '2023-10-15', '10:00:00', '10:00:00', 10, 'Active'),
    (14, '2023-12-08', '2023-12-28', '15:00:00', '17:00:00', 46, 'face-to-face', 'SCIS SR 3-2', 'Ongoing', 30, 20, 0, 2, '2023-11-05', '2023-11-10', '10:00:00', '10:00:00', 12, 'Active'),
    (15, '2023-10-10', '2023-11-10', '09:30:00', '11:30:00', 41, 'face-to-face', 'SCIS SR 2-3', 'Ongoing', 40, 30, 0, 2, '2023-09-05', '2023-09-10', '10:00:00', '10:00:00', 14, 'Active'),
    (16, '2023-10-15', '2023-11-15', '14:00:00', '16:00:00', 42, 'face-to-face', 'SCIS SR 2-3', 'Ongoing', 25, 15, 0, 2, '2023-09-05', '2023-09-10', '10:00:00', '10:00:00', 15, 'Active');

DROP TABLE IF EXISTS `registration`;
CREATE TABLE IF NOT EXISTS `registration`(
	reg_id int NOT NULL AUTO_INCREMENT,
	rcourse_id int NOT NULL,
	user_id int NOT NULL,
	reg_status varchar(20) NOT NULL,
	PRIMARY KEY (`reg_id`),
	FOREIGN KEY (rcourse_id) REFERENCES runcourse(rcourse_id),
	FOREIGN KEY (user_id) REFERENCES user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO registration VALUES
	(1, 1, 1, 'Enrolled'),
	(2, 1, 6, 'Enrolled'),
	(3, 1, 7, 'Enrolled'),
	(4, 1, 8, 'Enrolled'),
    (5, 1, 9, 'Enrolled'),
    (6, 1, 10, 'Enrolled'),
    (7, 1, 11, 'Enrolled'),
    (8, 1, 12, 'Enrolled'),
    (9, 1, 13, 'Enrolled'),
    (10, 1, 14, 'Enrolled'),
    (11, 1, 15, 'Enrolled'),
    (12, 1, 16, 'Enrolled'),
    (13, 1, 17, 'Enrolled'),
    (14, 1, 18, 'Enrolled'),
    (15, 1, 19, 'Enrolled'),
    (16, 1, 20, 'Enrolled'),
    (17, 1, 21, 'Enrolled'),
    (18, 1, 22, 'Enrolled'),
    (19, 1, 23, 'Enrolled'),
    (20, 1, 24, 'Enrolled'),
	(21, 2, 25, 'Enrolled'),
    (22, 2, 26, 'Enrolled'),
    (23, 2, 27, 'Enrolled'),
    (24, 2, 28, 'Enrolled'),
    (25, 2, 29, 'Enrolled'),
    (26, 2, 30, 'Enrolled'),
    (27, 2, 31, 'Enrolled'),
    (28, 2, 32, 'Enrolled'),
    (29, 2, 33, 'Enrolled'),
    (30, 2, 34, 'Enrolled'),
    (31, 2, 35, 'Enrolled'),
    (32, 2, 36, 'Enrolled'),
    (33, 2, 37, 'Enrolled'),
    (34, 2, 38, 'Enrolled'),
    (35, 2, 39, 'Enrolled'), 
	(36, 1, 40, 'Enrolled'), 
	(37, 1, 51, 'Enrolled'),
	(38, 1, 52, 'Enrolled'),
	(39, 2, 53, 'Pending'),
	(40, 2, 5, 'Pending'),
	(42, 2, 55, 'Pending'),
	(43, 1, 25, 'Dropped'),
	(44, 2, 1, 'Dropped');

DROP TABLE IF EXISTS `lesson`;
CREATE TABLE IF NOT EXISTS `lesson`(
	lesson_id int NOT NULL AUTO_INCREMENT,
	reg_id int NOT NULL,
	lesson_date date NOT NULL,
	lesson_time time NOT NULL,
	PRIMARY KEY (`lesson_id`),
	FOREIGN KEY (reg_id) REFERENCES registration(reg_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO lesson VALUES 
	(1, 1, '2023-07-10', '12:00:00'),
	(2, 2, '2023-07-10', '12:00:00'),
    (3, 3, '2023-07-10', '12:00:00'),
    (4, 4, '2023-07-10', '12:00:00'),
    (5, 5, '2023-07-10', '12:00:00'),
    (6, 6, '2023-07-10', '12:00:00'),
    (7, 7, '2023-07-10', '12:00:00'),
    (8, 8, '2023-07-10', '12:00:00'),
    (9, 9, '2023-07-10', '12:00:00'),
    (10, 10, '2023-07-10', '12:00:00'),
    (11, 11, '2023-07-10', '12:00:00'),
    (12, 12, '2023-07-10', '12:00:00'),
    (13, 13, '2023-07-10', '12:00:00'),
    (14, 14, '2023-07-10', '12:00:00'),
    (15, 15, '2023-07-10', '12:00:00'),
    (16, 16, '2023-07-10', '12:00:00'),
    (17, 17, '2023-07-10', '12:00:00'),
    (18, 18, '2023-07-10', '12:00:00'),
    (19, 19, '2023-07-10', '12:00:00'),
    (20, 20, '2023-07-10', '12:00:00'), 
	(21, 36, '2023-07-10', '12:00:00'),
    (22, 37, '2023-07-10', '12:00:00'),
    (23, 38, '2023-07-10', '12:00:00'),
	(24, 1, '2023-07-17', '12:00:00'), 
	(25, 2, '2023-07-17', '12:00:00'),
    (26, 3, '2023-07-17', '12:00:00'),
    (27, 4, '2023-07-17', '12:00:00'),
    (28, 5, '2023-07-17', '12:00:00'),
    (29, 6, '2023-07-17', '12:00:00'),
    (30, 7, '2023-07-17', '12:00:00'),
    (31, 8, '2023-07-17', '12:00:00'),
    (32, 9, '2023-07-17', '12:00:00'),
    (33, 10, '2023-07-17', '12:00:00'),
    (34, 11, '2023-07-17', '12:00:00'),
    (35, 12, '2023-07-17', '12:00:00'),
    (36, 13, '2023-07-17', '12:00:00'),
    (37, 14, '2023-07-17', '12:00:00'),
    (38, 15, '2023-07-17', '12:00:00'),
    (39, 16, '2023-07-17', '12:00:00'),
    (40, 17, '2023-07-17', '12:00:00'),
    (41, 18, '2023-07-17', '12:00:00'),
    (42, 19, '2023-07-17', '12:00:00'),
    (43, 20, '2023-07-17', '12:00:00'),
	(44, 36, '2023-07-17', '12:00:00'),
    (45, 37, '2023-07-17', '12:00:00'),
    (46, 38, '2023-07-17', '12:00:00'),
	(47, 1, '2023-07-24', '12:00:00'),
	(48, 2, '2023-07-24', '12:00:00'),
	(49, 3, '2023-07-24', '12:00:00'),
	(50, 4, '2023-07-24', '12:00:00'),
	(51, 5, '2023-07-24', '12:00:00'),
	(52, 6, '2023-07-24', '12:00:00'),
	(53, 7, '2023-07-24', '12:00:00'),
	(54, 8, '2023-07-24', '12:00:00'),
	(55, 9, '2023-07-24', '12:00:00'),
	(56, 10, '2023-07-24', '12:00:00'),
	(57, 11, '2023-07-24', '12:00:00'),
	(58, 12, '2023-07-24', '12:00:00'),
	(59, 13, '2023-07-24', '12:00:00'),
	(60, 14, '2023-07-24', '12:00:00'),
	(61, 15, '2023-07-24', '12:00:00'),
	(62, 16, '2023-07-24', '12:00:00'),
	(63, 17, '2023-07-24', '12:00:00'),
	(64, 18, '2023-07-24', '12:00:00'),
	(65, 19, '2023-07-24', '12:00:00'),
	(66, 20, '2023-07-24', '12:00:00'),
	(67, 36, '2023-07-24', '12:00:00'),
	(68, 37, '2023-07-24', '12:00:00'),
	(69, 38, '2023-07-24', '12:00:00'),
	(70, 1, '2023-08-07', '12:00:00'),
	(71, 2, '2023-08-07', '12:00:00'),
	(72, 3, '2023-08-07', '12:00:00'),
	(73, 4, '2023-08-07', '12:00:00'),
	(74, 5, '2023-08-07', '12:00:00'),
	(75, 6, '2023-08-07', '12:00:00'),
	(76, 7, '2023-08-07', '12:00:00'),
	(77, 8, '2023-08-07', '12:00:00'),
	(78, 9, '2023-08-07', '12:00:00'),
	(79, 10, '2023-08-07', '12:00:00'),
	(80, 11, '2023-08-07', '12:00:00'),
	(81, 12, '2023-08-07', '12:00:00'),
	(82, 13, '2023-08-07', '12:00:00'),
	(83, 14, '2023-08-07', '12:00:00'),
	(84, 15, '2023-08-07', '12:00:00'),
	(85, 16, '2023-08-07', '12:00:00'),
	(86, 17, '2023-08-07', '12:00:00'),
	(87, 18, '2023-08-07', '12:00:00'),
	(88, 19, '2023-08-07', '12:00:00'),
	(89, 20, '2023-08-07', '12:00:00'),
	(90, 21, '2023-08-07', '12:00:00'),
	(91, 22, '2023-08-07', '12:00:00'),
	(92, 23, '2023-08-07', '12:00:00');

DROP TABLE IF EXISTS `attendancerecord`;
CREATE TABLE IF NOT EXISTS `attendancerecord`(
	attrecord_id int NOT NULL AUTO_INCREMENT,
	lesson_id int NOT NULL,
	status varchar(15) NOT NULL,
	reason varchar(255),
	attrecord_status varchar(20) NOT NULL,
	PRIMARY KEY (`attrecord_id`),
	FOREIGN KEY (lesson_id) REFERENCES lesson(lesson_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO attendancerecord VALUES 
	(1, 1, 'Present', NULL, 'Submitted'),
    (2, 2, 'Present', NULL, 'Submitted'),
    (3, 3, 'Present', NULL, 'Submitted'),
    (4, 4, 'Absent', 'Medical Leave', 'Submitted'),
    (5, 5, 'Present', NULL, 'Submitted'),
	(6, 6, 'Present', NULL, 'Submitted'),
    (7, 7, 'Present', NULL, 'Submitted'),
    (8, 8, 'Late', NULL, 'Submitted'),
    (9, 9, 'Present', NULL, 'Submitted'),
    (10, 10, 'Present', NULL, 'Submitted'),
	(11, 21, 'Present', NULL, 'Submitted'),
    (12, 22, 'Present', NULL, 'Submitted'),
    (13, 23, 'Present', NULL, 'Submitted'),
    (14, 24, 'Present', NULL, 'Submitted'),
    (15, 25, 'Present', NULL, 'Submitted'),
    (16, 26, 'Present', NULL, 'Submitted'),
    (17, 27, 'Absent', 'Medical Leave', 'Submitted'),
    (18, 28, 'Present', NULL, 'Submitted'),
    (19, 29, 'Late', NULL, 'Submitted'),
    (20, 30, 'Present', NULL, 'Submitted'),
	(21, 21, 'Present', NULL, 'Submitted'),
    (22, 22, 'Present', NULL, 'Submitted'),
    (23, 23, 'Present', NULL, 'Submitted'),
    (24, 24, 'Present', NULL, 'Submitted'),
    (25, 25, 'Present', NULL, 'Submitted'),
    (26, 26, 'Present', NULL, 'Submitted'),
    (27, 27, 'Present', NULL, 'Submitted'),
    (28, 28, 'Present', NULL, 'Submitted'),
    (29, 29, 'Present', NULL, 'Submitted'),
    (30, 30, 'Present', NULL, 'Submitted'),
    (31, 31, 'Present', NULL, 'Submitted'),
    (32, 32, 'Present', NULL, 'Submitted'),
    (33, 33, 'Late', NULL, 'Submitted'),
    (34, 34, 'Present', NULL, 'Submitted'),
    (35, 35, 'Present', NULL, 'Submitted'),
    (36, 36, 'Present', NULL, 'Submitted'),
    (37, 37, 'Present', NULL, 'Submitted'),
    (38, 38, 'Present', NULL, 'Submitted'),
    (39, 39, 'Present', NULL, 'Submitted'),
    (40, 40, 'Present', NULL, 'Submitted'),
	(41, 41, 'Present', NULL, 'Submitted'),
    (42, 42, 'Present', NULL, 'Submitted'),
    (43, 43, 'Present', NULL, 'Submitted'),
    (44, 44, 'Present', NULL, 'Submitted'),
    (45, 45, 'Present', NULL, 'Submitted'),
    (46, 46, 'Present', NULL, 'Submitted'),
    (47, 47, 'Present', NULL, 'Submitted'),
    (48, 48, 'Present', NULL, 'Submitted'),
    (49, 49, 'Present', NULL, 'Submitted'),
    (50, 50, 'Present', NULL, 'Submitted'),
    (51, 51, 'Present', NULL, 'Submitted'),
    (52, 52, 'Present', NULL, 'Submitted'),
    (53, 53, 'Present', NULL, 'Submitted'),
    (54, 54, 'Present', NULL, 'Submitted'),
    (55, 55, 'Present', NULL, 'Submitted'),
    (56, 56, 'Present', NULL, 'Submitted'),
    (57, 57, 'Present', NULL, 'Submitted'),
    (58, 58, 'Present', NULL, 'Submitted'),
    (59, 59, 'Present', NULL, 'Submitted'),
    (60, 60, 'Present', NULL, 'Submitted'),
	(61, 61, 'Present', NULL, 'Submitted'),
    (62, 62, 'Present', NULL, 'Submitted'),
    (63, 63, 'Late', NULL, 'Submitted'),
    (64, 64, 'Present', NULL, 'Submitted'),
    (65, 65, 'Present', NULL, 'Submitted'),
    (66, 66, 'Present', NULL, 'Submitted'),
    (67, 67, 'Present', NULL, 'Submitted'),
    (68, 68, 'Present', NULL, 'Submitted'),
    (69, 69, 'Present', NULL, 'Submitted'),
    (70, 70, 'Present', NULL, 'Submitted'),
    (71, 71, 'Present', NULL, 'Submitted'),
    (72, 72, 'Present', NULL, 'Submitted'),
    (73, 73, 'Present', NULL, 'Submitted'),
    (74, 74, 'Present', NULL, 'Submitted'),
    (75, 75, 'Present', NULL, 'Submitted'),
    (76, 76, 'Present', NULL, 'Submitted'),
    (77, 77, 'Present', NULL, 'Submitted'),
    (78, 78, 'Present', NULL, 'Submitted'),
    (79, 79, 'Present', NULL, 'Submitted'),
    (80, 80, 'Present', NULL, 'Submitted'),
	(81, 81, 'Present', NULL, 'Submitted'),
    (82, 82, 'Present', NULL, 'Submitted'),
    (83, 83, 'Present', NULL, 'Submitted'),
    (84, 84, 'Present', NULL, 'Submitted'),
    (85, 85, 'Present', NULL, 'Submitted'),
    (86, 86, 'Present', NULL, 'Submitted'),
    (87, 87, 'Present', NULL, 'Submitted'),
    (88, 88, 'Present', NULL, 'Submitted'),
    (89, 89, 'Present', NULL, 'Submitted'),
    (90, 90, 'Late', NULL, 'Submitted'),
    (91, 91, 'Present', NULL, 'Submitted');

DROP TABLE IF EXISTS `blacklist`;
CREATE TABLE IF NOT EXISTS `blacklist`(
	blacklist_id int NOT NULL AUTO_INCREMENT,
	user_id int NOT NULL,
	PRIMARY KEY (`blacklist_id`),
	FOREIGN KEY (user_id) REFERENCES user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO blacklist VALUES 
	(1, 56), 
	(2, 57);

DROP TABLE IF EXISTS `contactus`;
CREATE TABLE IF NOT EXISTS `contactus`(
	msg_id int NOT NULL AUTO_INCREMENT,
	user_id int NOT NULL,
	msg_subject varchar(255) NOT NULL,
	msg_body varchar(1000) NOT NULL,
    msg_datetime datetime NOT NULL,
	PRIMARY KEY (`msg_id`),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO contactus VALUES
    (1, 1, "Test", "Testing the contact us function", "2023-08-25 17:00:00");