<template>
  <div id="database-page">
    <div id="search-bar">
      <div class="university field">
        <select name="university" multiple="" class="ui fluid dropdown" id="university-select">
          <option value=""><i class="university icon"></i>University</option>
          <option v-for="(u,idx) in universities" v-bind:value="idx">{{u.name}}</option>
        </select>
      </div>
      <div class="faculty field">
        <select name="faculty" class="ui fluid dropdown" id="faculty-select">
          <option value=""><i class="building icon"></i>Faculty</option>
          <option v-for="(f,idx) in faculties" v-bind:value="idx">{{f.name}}</option>
        </select>
      </div>
    </div>
    <div class="ui segment" id="segment">
      <div class="ui item small header">
        <div class="ui grid">
          <div class="two wide column">Name</div>
          <div class="two wide column">Current Institution</div>
          <div class="one wide column">Academic Rank</div>
          <div class="one wide column">Year of PhD</div>
          <div class="two wide column">PhD Institution</div>
          <div class="one wide column">Year of Promotion</div>
          <div class="two wide column">Promotion Institution</div>
          <div class="five wide column">Research Interests</div>
        </div>
      </div>
      <div class="list-outer" id="results-list">
        <div class="ui relaxed divided list">
          <div class="ui item prof" v-for="i in professors">
            <div class="ui grid">
              <div class="two wide column">{{i.name}}</div>
              <div class="two wide column">{{universities[i.universityId].name}}</div>
              <div class="one wide column">{{i.rank}}</div>
              <div class="one wide column">{{i.phdYear}}</div>
              <div class="two wide column">{{i.phdInstitution}}</div>
              <div class="one wide column">{{i.promotionYear}}</div>
              <div class="two wide column">{{i.promotionInstitution}}</div>
              <div class="five wide column">{{i.researchInterests}}</div>
            </div>
          </div>
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
    this.uSelect.dropdown('set exactly', this.$store.state.uIds)
    this.fSelect = $(this.$el).find('#faculty-select').dropdown()
    this.fSelect.dropdown('set value', this.$store.state.fId)
  },
  data: function () {
    return {
      uSelect: null,
      fSelect: null
    }
  },
  methods: {
    crawlRequest: function () {
      this.$router.push('crawlrequest')
    }
  },
  computed: {
    results: function () {
      return this.$store.state.dbSearchResults
    },
    professors: function () {
      return this.$store.state.professorsList
    },
    universities: function () {
      return this.$store.state.universities
    },
    faculties: function () {
      return this.$store.state.faculties
    }
  },
  watch: {
    'this.$store.state.uIds': function (v) {
      console.log('uIds changed')
      this.uSelect.dropdown('set exactly', v)
    }
  }
}
</script>

<style scoped>
#database-page {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  position: relative;
}

#menu {
  margin: 0px;
}

#search-bar {
  padding: 10px;
  border-bottom: 2px solid rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex: 0 0 auto;
}

#segment {
  flex: 1 1 auto;
  margin: 0px;
  border: none;
  position: relative;
  margin-top: 2px;
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow-y: hidden;
}

.field.university {
  width: calc(75% - 10px);
}

.field.faculty {
  width: calc(25% - 10px);
}

.column {
  padding: 5px !important;
}

.ui.grid {
  position: relative;
  width: 100%;
  margin: 0px;
}

.ui.item.header {
  width: 100%;
  flex: 0 0 auto;
  border-bottom: 2px solid rgba(34, 36, 38, 0.15);
  margin-bottom: 0px;
}

.ui.item.prof {
  margin: 0px;
  color: rgba(0, 0, 0, 0.8);
}

#results-list {
  flex: 0 1 auto;
  overflow: auto;
}
</style>
