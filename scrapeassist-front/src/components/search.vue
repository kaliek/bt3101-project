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
        <div class="ui large form">
          <div class="field">
            <select name="university" multiple="" class="ui fluid dropdown" id="university-select">
              <option value=""><i class="university icon"></i>University</option>
              <option v-for="(u,idx) in universities" v-bind:value="idx">{{u.name}}</option>
            </select>
            <button class="circular ui icon button">
              <i class="icon plus"></i>
            </button>
          </div>
          <div class="field">
            <select name="faculty" class="ui fluid dropdown" id="faculty-select">
              <option value=""><i class="building icon"></i>Faculty</option>
              <option v-for="(f,idx) in faculties" v-bind:value="idx">{{f.name}}</option>
            </select>
            <button class="circular ui icon button">
              <i class="icon plus"></i>
            </button>
          </div>
          <div class="ui buttons">
            <button class="ui black button" v-on:click="search">Search the Database</button>
            <div class="or"></div>
            <button class="ui positive button" v-on:click="requestCrawl">Request a Crawl</button>
          </div>
          <div class="ui error message"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  mounted: function () {
    this.uSelect = $(this.$el).find('#university-select').dropdown()
    this.fSelect = $(this.$el).find('#faculty-select').dropdown()
  },
  data: function () {
    return {
      uSelect: null,
      fSelect: null
    }
  },
  methods: {
    search: function () {
      this.$store.dispatch('searchProfessors', {
        uIds: this.uSelect.dropdown('get value'),
        fId: this.fSelect.dropdown('get value'),
        router: this.$router
      })
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
