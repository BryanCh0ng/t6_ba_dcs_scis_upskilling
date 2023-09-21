<template>
  <div class="container text-center">
    <!-- Ratings -->
    <div class="row">
      <!-- Display Total No. of Feedbacks -->
      <div class="col-sm dashboard">
        <h2 class="fs-1">40</h2>
        <p><strong>Total No. of Feedbacks</strong></p>
      </div>
      <!-- Display Overall Average Course Ratings if not instructor-specific -->
      <div v-if="courseSpecific" class="col-sm dashboard">
        <h2 class="fs-1">4.2 / 5</h2>
        <p><strong>Overall Average Course Ratings</strong></p>
      </div>
      <!-- Display Overall Average Instructor Ratings if not course-specific -->
      <div v-if="instructorSpecific" class="col-sm dashboard">
        <h2 class="fs-1">4.7 / 5</h2>
        <p><strong>Overall Average Instructor Ratings</strong></p>
      </div>
    </div>

    <!-- Sentiment Course -->
    <div class="row mt-3"  v-if="courseSpecific">
      <!-- Display Overall Course Sentiment -->
      <div class="col-sm dashboard">
        <p><strong>Overall Course Sentiment</strong></p>
      </div>
      <!-- Display Overall Course Positive WordCloud -->
      <div class="col-sm dashboard">
        <!-- Include Word Cloud component here for positive feedback -->
        <WordCloud :wordData="positiveCourseWordData"/>
        <p><strong>Overall Course Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-sm dashboard">
        <!-- Include Word Cloud component here for negative feedback -->
        <WordCloud :wordData="negativeCourseWordData"/>
        <p><strong>Overall Course Negative WordCloud</strong></p>
      </div>
    </div>

    <!-- Sentiment Instructor -->
    <div class="row mt-3"  v-if="instructorSpecific">
      <!-- Display Overall Instructor Sentiment -->
      <div class="col-sm dashboard">
        <WordCloud :wordData="overallInstructorWordData"/>
        <p><strong>Overall Instructor Sentiment</strong></p>
      </div>
      <!-- Display Overall Instructor Positive WordCloud -->
      <div class="col-sm dashboard">
        
        <!-- Include Word Cloud component here for positive feedback -->
        <WordCloud :wordData="positiveInstructorWordData"/>
        <p><strong>Overall Instructor Positive WordCloud</strong></p>
      </div>
      <!-- Display Overall Course Negative WordCloud -->
      <div class="col-sm dashboard">
        <!-- Include Word Cloud component here for negative feedback -->
        <WordCloud :wordData="negativeInstructorWordData"/>
        <p><strong>Overall Instructor Negative WordCloud</strong></p>
      </div>
    </div>

    
    <div class="row mt-3">
      <!-- Topic Modeling - Course Done Well / Contribution -->
      <div
        v-for="(topic, index) in courseDoneWellTopics"
        :key="index"
        class="col-sm dashboard mb-3"
      >
        <!-- Include Word Cloud component here for course done well topic -->
        <WordCloud :wordData="courseDoneWellTopics[index].wordData" />
        <p><strong>Overall Course Done Well - Topic {{ index + 1 }}</strong></p>
      </div>

        <!-- Topic Modeling - Course Suggestions / Improve -->
        <div
            v-for="(topic, index) in courseSuggestionsTopics"
            :key="index"
            class="col-sm dashboard mb-3"
        >
            <!-- Include Word Cloud component here for course suggestions topic -->
            <WordCloud :wordData="courseSuggestionsTopics[index].wordData" />
             <p><strong>Overall Course Suggestions - Topic {{ index + 1 }}</strong></p>
        </div>

        <!-- Topic Modeling - Instructor Done Well -->
        <div
            v-for="(topic, index) in instructorDoneWellTopics"
            :key="index"
            class="col-sm dashboard mb-3"
        >
            <!-- Include Word Cloud component here for instructor done well topic -->
            <WordCloud :wordData="instructorDoneWellTopics[index].wordData" />
            <p><strong>Overall Instructor Done Well - Topic {{ index + 1 }}</strong></p>
        </div>

        <!-- Topic Modeling - Instructor Suggestions -->
        <div
            v-for="(topic, index) in instructorSuggestionsTopics"
            :key="index"
            class="col-sm dashboard mb-3"
        >
            <!-- Include Word Cloud component here for instructor suggestions topic -->
            <WordCloud :wordData="instructorSuggestionsTopics[index].wordData" />
            <p><strong>Overall Instructor Suggestions - Topic {{ index + 1 }}</strong></p>
        </div>

    </div>

  </div>
</template>

<script>
import WordCloud from "@/components/dashboard/WordCloud.vue"; // Adjust the import path based on your project structure

export default {
    components: {
        WordCloud, // Register the WordCloud component
    },
    mounted() {
        // console.log("Positive Course Word Data:", this.positiveCourseWordData);
    },
    data() {
        return {
            instructorSpecific: true, 
            courseSpecific: true,
            overallCourseWordData: ['good', 'excellent'],
            positiveCourseWordData: ['good', 'excellent'],
            negativeCourseWordData: ['good', 'excellent'],
            overallInstructorWordData: ['good', 'excellent'],
            positiveInstructorWordData: ['good', 'excellent'],
            negativeInstructorWordData: ['good', 'excellent'],
            courseDoneWellTopics: [
                {
                    wordData: ['good', 'excellent'],
                },
                {
                    wordData: ['good', 'excellent'],
                },
                {
                    wordData: ['good', 'excellent'],
                },
                {
                    wordData: ['good', 'excellent'],
                },
            ],
            courseSuggestionsTopics: [
                {
                    wordData: ['good', 'excellent'],
                },
                {
                    wordData: ['good', 'excellent'],
                },
            ],
            instructorDoneWellTopics: [
                {
                    wordData: ['good', 'excellent'],
                },
                {
                    wordData: ['good', 'excellent'],
                },
            ],
            instructorSuggestionsTopics: [
                {
                    wordData: ['good', 'excellent'],
                },
                {
                    wordData: ['good', 'excellent'],
                }
            ],
        };
    },
    methods: {

    }
};
</script>

<style scoped>
.container {
  color: #404040;
}

.dashboard {
  border: 2px solid #616161;
  margin-right: 20px;
  padding: 15px;
  flex: 0 0 calc(33.33% - 20px); 
}

#instructor-suggestions-row {
  display: flex;
  flex-wrap: wrap;
}
</style>
