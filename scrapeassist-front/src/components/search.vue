<template>
  <div id="search-page">
    <div class="ui middle aligned center aligned grid">
      <div class="column">
        <h2 class="ui icon header">
          <i class="university icon"></i>
          <div class="content">
            Choose a University and Faculty
            <!-- <div class="sub header">Manage your account settings and set e-mail preferences.</div> -->
          </div>
        </h2>
        <div class="ui large form">
          <div class="field">
            <uSelect :additions="true"></uSelect>
          </div>
          <div class="field">
            <fSelect :additions="true"></fSelect>
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
import uSelect from '@/components/university-selector'
import fSelect from '@/components/faculty-selector'
import $ from 'jquery'
export default {
  components: {
    uSelect: uSelect,
    fSelect: fSelect
  },
  mounted: function () {
    $(this.$el).find('.circular.button').popup({
      on: 'click',
      position: 'right center',
      html: `<div class="ui action input">
              <input placeholder="University Name" type="text">
              <button @click="createUniversity" class="ui button">Create</button>
            </div>
            `
    })
    this.$on('selectUniversity', function (v) {
      this.uIds = v
    })
    this.$on('selectFaculty', function (v) {
      this.fId = v
    })
  },
  data: function () {
    return {
      uIds: [],
      fId: '',
      newUniversities: []
    }
  },
  methods: {
    search: function () {
      if (!(0 in this.uIds && this.fId)) {
        return this.$store.commit('showMessageModal', {
          title: 'Blank Fields',
          msg: 'Please fill in all fields for the search query.',
          icon: 'exclamation triangle'
        })
      }
      this.$store.dispatch('searchProfessors', {
        uIds: this.uIds,
        fId: this.fId,
        router: this.$router
      })
    },
    requestCrawl: function () {
      this.$store.commit('setCrawlRequest', {
        uIds: this.uIds,
        fId: this.fId,
        router: this.$router
      })
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
