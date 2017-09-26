<template>
  <div id="request-page">
    <div class="ui middle aligned center aligned grid">
      <div class="column">
        <h2 class="ui icon header">
          <i class="cloud upload icon"></i>
          <div class="content">
            Create Crawl Request
            <div class="sub header">for {{$store.state.faculties[$store.state.crfId].name}}</div>
            <h4 class="ui header">
              We need faculty list URLs for each University to start the crawl
            </h4>
          </div>
        </h2>
        <div class="ui large form">
          <template v-for="(i,idx) in $store.state.cruIds">
            <h5>{{$store.state.universities[i].name}}</h5>
            <div class="field">
              <div class="ui left icon input">
                <i class="linkify icon"></i>
                <input type="text" name="email" placeholder="Faculty List URL" v-model="urls[idx]">
              </div>
            </div>
          </template>
          <div class="ui buttons">
            <button class="ui positive button" v-on:click="crawl">Start Crawling</button>
          </div>
          <div class="ui error message"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      urls: []
    }
  },
  methods: {
    crawl: function () {
      this.$store.dispatch('callMethodAndCallback', {
        params: ['createCrawlRequests', this.urls, this.$store.state.cruIds, this.$store.state.crfId],
        callback: function (r) {
          this.$router.push('crawlmonitor')
        }.bind(this)
      })
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

h5 {
  text-align: left;
  margin-bottom: 0px;
}
</style>
