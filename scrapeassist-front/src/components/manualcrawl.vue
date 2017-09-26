<template>
  <div id="main">
    <div id="data">
      <!-- <div class="ui secondary pointing menu">
        <a class="item active">
          Data
        </a>
        <div class="right menu">
          <div class="item">
            <div class="ui icon input">
              <input placeholder="Search..." type="text">
              <i class="search link icon"></i>
            </div>
          </div>
        </div>
      </div> -->
      <div id="header">
        <h1 class="ui large header">
          Faculty of Geography | University College London
        </h1>
      </div>
      <div class="ui three cards">
        <profCard v-for="(i,id) in professors" :prof="i" :selected="selId === id" :key="id" @click.native="select(id)"></profCard>
      </div>
    </div>
    <div id="results">
      <iframe src="http://www.comp.nus.edu.sg/about/depts/cs/faculty/"></iframe>
      <iframe src="https://coe.uga.edu/directory"></iframe>
      <iframe src="http://mitsloan.mit.edu/faculty-and-research/faculty-directory/"></iframe>
      <iframe src="http://mitsloan.mit.edu/faculty-and-research/faculty-directory/"></iframe>
    </div>
  </div>
</template>

<script>
import profCard from '@/components/professor-card'
export default {
  components: {
    profCard: profCard
  },
  data: function () {
    return {
      selId: 0
    }
  },
  methods: {
    select: function (id) {
      this.selId = id
    }
  },
  computed: {
    professors: function () {
      return this.$store.state.professorsList
    }
  }
}
</script>

<style scoped>
#test-hot {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#main {
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
}

#data {
  height: 100%;
  width: 50%;
  display: block;
  position: fixed;
  display: flex;
  flex-direction: column;
}

#results {
  height: 100%;
  width: 50%;
  background-color: #EFEFEF;
  position: absolute;
  right: 0;
  display: flex;
  flex-direction: column;
}

.ui.secondary.pointing.menu {
  background-color: #FFFFFF;
  margin-bottom: 0px;
  z-index: 10;
  width: 100%;
}

iframe {
  height: 100%;
  width: 100%;
}

.ui.three.cards {
  margin: 0px;
  overflow: auto;
}

.ui.card {
  text-align: left;
  margin: 3px !important;
  width: calc( 33.333333333% - 6px) !important;
  color: black;
}

#header {
  border-bottom: 2px solid rgba(0, 0, 0, 0.2);
}

#header > h1 {
  line-height: 48px;
}
</style>
