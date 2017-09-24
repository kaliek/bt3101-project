<template>
  <div id="request-page">
    <div class="ui middle aligned center aligned grid">
      <div class="column">
        <h2 class="ui icon header">
          <!-- <i class="search icon"></i> -->
          <div class="content">
            Create Crawl Request
            <div class="sub header">Faculty Name in University Name</div>
            <h4 class="ui header">
              We need a faculty list URL to start the crawl
            </h4>
          </div>
        </h2>
        <form class="ui large form">
            <div class="field">
              <div class="ui left icon input">
                <i class="list icon"></i>
                <input type="text" name="email" placeholder="Faculty List URL" v-model="url">
              </div>
            </div>
            <div class="ui buttons">
              <button class="ui positive button" v-on:click="crawl">Start Crawling</button>
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
      url: ''
    }
  },
  methods: {
    crawl: function () {
      this.$router.push('crawlmonitor')
    }
  }
}
</script>

<style scoped>
#request-page {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.large.form {
  width: 450px;
}
</style>
