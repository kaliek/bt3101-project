<template>
  <div id="search-page">
    <div class="ui middle aligned center aligned grid">
      <div class="column">
        <h2 class="ui icon header">
          <i class="search icon"></i>
          <div class="content">
            Choose a University and Faculty
            <!-- <div class="sub header">Manage your account settings and set e-mail preferences.</div> -->
          </div>
        </h2>
        <form class="ui large form">
          <div class="field">
            <select name="university" multiple="" class="ui fluid dropdown" id="university-select">
              <option value=""><i class="university icon"></i>University</option>
              <option v-for="(u,idx) in universities">{{u.name}}</option>
            </select>
            <button class="circular ui icon button">
              <i class="icon plus"></i>
            </button>
          </div>
          <div class="field">
            <select name="faculty" class="ui fluid dropdown" id="faculty-select">
              <option value=""><i class="building icon"></i>Faculty</option>
              <option v-for="(f,idx) in faculties">{{f.name}}</option>
            </select>
            <button class="circular ui icon button">
              <i class="icon plus"></i>
            </button>
          </div>
          <div class="ui buttons">
            <button class="ui black button" v-on:click="searchDatabase">Search the Database</button>
            <div class="or"></div>
            <button class="ui positive button" v-on:click="requestCrawl">Request a Crawl</button>
          </div>
          <div class="ui error message"></div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  mounted: function () {
    $('#university-select').dropdown()
    $('#faculty-select').dropdown()
  },
  data: function () {
    return {
    }
  },
  methods: {
    searchDatabase: function () {
      this.$router.push('database')
    },
    requestCrawl: function () {
      this.$router.push('crawlrequest')
    }
  },
  computed: {
    universities: function () {
      return this.$store.state.universities
    },
    faculties: function () {
      return this.$store.state.faculties
    }
  }
}
</script>

<style scoped>
#search-page {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.large.form {
  width: 450px;
}

.field {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.circular.button {
  margin-left: 5px;
}
</style>
