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
            <div class="ui left icon input">
              <i class="university icon"></i>
              <input type="text" name="email" placeholder="University" v-model="university">
            </div>
          </div>
          <div class="field">
            <div class="ui left icon input">
              <i class="building icon"></i>
              <input type="text" name="password" placeholder="Faculty" v-model="faculty">
            </div>
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
export default {
  data: function () {
    return {
      university: '',
      faculty: ''
    }
  },
  methods: {
    searchDatabase: function () {
      this.$router.push('database')
    },
    requestCrawl: function () {
      this.$router.push('crawlrequest')
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
</style>
