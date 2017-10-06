<template>
  <div id="database-page">
    <div id="mouseover-zone">
      <div class="ui vertical menu" id="filter-menu">
        <div class="item">
          <h5><i class="random icon"></i>SORT</h5>
          <div class="menu">
            <a class="item" @click="sortList('name')" :class="{active: k==='name'}">Name</a>
            <a class="item" @click="sortList('university')" :class="{active: k==='university'}">Current Institution</a>
            <a class="item" @click="sortList('rank')" :class="{active: k==='rank'}">Academic Rank</a>
            <a class="item" @click="sortList('phdYear')" :class="{active: k==='phdYear'}">Year of PhD</a>
            <a class="item" @click="sortList('phdInstitution')" :class="{active: k==='phdInstitution'}">PhD Instution</a>
            <a class="item" @click="sortList('promotionYear')" :class="{active: k==='promotionYear'}">Year of Promotion</a>
            <a class="item" @click="sortList('promotionInstitution')" :class="{active: k==='promotionInstitution'}">Promotion Institution</a>
          </div>
        </div>
        <div class="item" id="filters-menu">
          <h5><i class="filter icon"></i>FILTER</h5>
          <div class="ui icon input transparent">
            <input placeholder="Min PhD Year..." type="text" v-model="minPhdYear">
          </div>
          <div class="ui icon input transparent">
            <input placeholder="Min Promotion Year..." type="text" v-model="minPromotionYear">
          </div>
        </div>
        <div class="ui simple dropdown item sub">
          Academic Rank
          <i class="dropdown icon"></i>
          <div class="menu sub">
            <a class="item" v-for="(i,id) in academicRanks" :class="{selected: id in selRanks}" @click="selectFilter(id, selRanks)">{{i}}</a>
          </div>
        </div>
        <div class="ui simple dropdown item sub">
          PhD Institution
          <i class="dropdown icon"></i>
          <div class="menu sub">
            <a class="item" v-for="(i,id) in phdInstitutions" :class="{selected: id in selPhdInsts}" @click="selectFilter(id, selPhdInsts)">{{i}}</a>
          </div>
        </div>
        <div class="ui simple dropdown item sub">
          Promotion Instution
          <i class="dropdown icon"></i>
          <div class="menu sub">
            <a class="item" v-for="(i,id) in promotionInstitutions" :class="{selected: id in selPromotionInsts}" @click="selectFilter(id, selPromotionInsts)">{{i}}</a>
          </div>
        </div>
        <div class="item">
          <div id="view-menu">
            <div class="ui labeled icon menu">
              <a class="item" :class="{active: layout === 'dbList'}" @click="setLayout('dbList')">
                <i class="list layout icon"></i>
                <span class="view-label">List View</span>
              </a>
              <a class="item" :class="{active: layout === 'dbGrid'}" @click="setLayout('dbGrid')">
                <i class="block layout icon"></i>
                <span class="view-label">Grid View</span>
              </a>
            </div>
          </div>
        </div>
        <div class="item">
          <button class="ui button green" style="width: 100%;">
            <i class="download icon"></i>
            Download CSV
          </button>
        </div>
        <div class="item">
          <button class="ui button" @click="crawlRequest">
            <i class="share icon"></i>
            Submit Crawl Request
          </button>
        </div>
      </div>
    </div>
    <div id="search-bar">
      <div class="university field">
        <uSelect :uIds="$store.state.uIds"></uSelect>
      </div>
      <div class="faculty field">
        <fSelect :fId="$store.state.fId"></fSelect>
      </div>
    </div>
    <!-- <dbList :professors="professors"></dbList> -->
    <component :is="layout" :professors="professors"></component>
  </div>
</template>

<script>
import $ from 'jquery'
import uSelect from '@/components/university-selector'
import fSelect from '@/components/faculty-selector'
import dbList from '@/components/database-list'
import dbGrid from '@/components/database-grid'
export default {
  components: {
    uSelect: uSelect,
    fSelect: fSelect,
    dbList: dbList,
    dbGrid: dbGrid

  },
  mounted: function () {
    $(this.$el).find('.menu.sub').css('overflow', 'auto')
    $(this.$el).find('#mouseover-zone').on('mouseover', function (e) {
      $('#filter-menu').addClass('visible')
    }).on('mouseout', function (e) {
      $('#filter-menu').removeClass('visible')
    })
    this.$on('selectUniversity', function (v) {
      if (!this.$store.state.fId) {
        return
      }
      this.resetFilters()
      this.$store.dispatch('searchProfessors', {
        uIds: v,
        fId: this.$store.state.fId,
        router: this.$router
      })
    }.bind(this))
    this.$on('selectFaculty', function (v) {
      if (!(0 in this.$store.state.uIds)) {
        return
      }
      this.resetFilters()
      this.$store.dispatch('searchProfessors', {
        uIds: this.$store.state.uIds,
        fId: v,
        router: this.$router
      })
    }.bind(this))
  },
  data: function () {
    return {
      layout: 'dbList',
      k: 'name',
      minPhdYear: '',
      minPromotionYear: '',
      selPhdInsts: {},
      selPromotionInsts: {},
      selRanks: {}
    }
  },
  methods: {
    setLayout: function (l) {
      this.layout = l
    },
    crawlRequest: function () {
      this.$store.commit('setCrawlRequest', {
        uIds: this.$store.state.uIds,
        fId: this.$store.state.fId,
        router: this.$router
      })
    },
    sortList: function (sortKey) {
      this.k = sortKey
    },
    selectFilter: function (id, s) {
      if (id in s) {
        this.$delete(s, id)
      } else {
        this.$set(s, id, true)
      }
    },
    resetFilters: function () {
      this.minPhdYear = ''
      this.minPromotionYear = ''
      this.selPhdInsts = {}
      this.selPromotionInsts = {}
      this.selRanks = {}
    }
  },
  computed: {
    results: function () {
      return this.$store.state.dbSearchResults
    },
    professors: function () {
      var cmpFn = function (key) {
        return function (a, b) {
          if (a[key] > b[key]) {
            return 1
          } else if (a[key] < b[key]) {
            return -1
          }
          return 0
        }
      }
      if (this.k === 'university') {
        cmpFn = function (key) {
          return function (a, b) {
            if (this.universities[a.universityId].name > this.universities[b.universityId].name) {
              return 1
            } else if (this.universities[a.universityId].name < this.universities[b.universityId].name) {
              return -1
            }
            return 0
          }.bind(this)
        }.bind(this)
      }
      var academicRanksRejected = new Set(this.academicRanks.filter((_, i) => i in this.selRanks))
      var phdInstitutionsRejected = new Set(this.phdInstitutions.filter((_, i) => i in this.selPhdInsts))
      var promotionInstitutionsRejected = new Set(this.promotionInstitutions.filter((_, i) => i in this.selPromotionInsts))
      var filterFn = function (e) {
        var phdYearFilter = true
        if (!isNaN(this.minPhdYear) && ('phdYear' in e && e.phdYear < parseInt(this.minPhdYear))) {
          phdYearFilter = false
        } else if (!isNaN(this.minPhdYear) && !('phdYear' in e)) {
          phdYearFilter = false
        }
        var promotionYearFilter = true
        if (!isNaN(this.minPromotionYear) && ('promotionYear' in e && e.promotionYear < parseInt(this.minPromotionYear))) {
          promotionYearFilter = false
        } else if (!isNaN(this.minPromotionYear) && !('promotionYear' in e)) {
          promotionYearFilter = false
        }
        return (phdYearFilter || this.minPhdYear === '') && (promotionYearFilter || this.minPromotionYear === '') && !academicRanksRejected.has(e.rank) && !phdInstitutionsRejected.has(e.phdInstitution) && !promotionInstitutionsRejected.has(e.promotionInstitution)
      }.bind(this)
      return this.$store.state.dbSearchResults.sort(cmpFn(this.k)).filter(filterFn)
    },
    universities: function () {
      return this.$store.state.universities
    },
    faculties: function () {
      return this.$store.state.faculties
    },
    academicRanks: function () {
      return [...new Set(this.results.map(i => i.rank || '(Blank)'))]
    },
    phdInstitutions: function () {
      return [...new Set(this.results.map(i => i.phdInstitution || '(Blank)'))]
    },
    promotionInstitutions: function () {
      return [...new Set(this.results.map(i => i.promotionInstitution || '(Blank)'))]
    }
  },
  watch: {
    'this.$store.state.uIds': function (v) {
      if (v) {
        this.uSelect.dropdown('set exactly', v)
      }
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

#mouseover-zone {
  height: 700px;
  width: 250px;
  position: absolute;
  top: calc(50vh - 350px);
  left: 0;
  z-index: 4;
}

#filter-menu {
  position: absolute;
  top: 0;
  left: 5px;
  z-index: 4;
  text-align: left;
  transform: translate3d(-255px, 0, 0);
  transition: transform .3s ease;
  opacity: 1;
}

#filter-menu.visible {
  transform: translate3d(0px, 0, 0);
}

#filters-menu > .ui.input {
  margin: 5px 0px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

#view-menu > .menu {
  border: none;
  box-shadow: none;
}

#view-menu .item {
  display: flex;
  flex-direction: column;
  height: 56px;
  width: 88px;
  color: black;
  padding: 5px;
}

#view-menu .icon {
  font-size: large;
}

#view-menu .view-label {
  font-size: small;
}

#view-menu .item {
  border-radius: 0.28571429rem;
}

#view-menu .item.active {
  background-color: rgba(0, 0, 0, .1) !important;
}

#search-bar {
  padding: 10px;
  border-bottom: 2px solid rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  flex: 0 0 auto;
}

.field.university {
  width: calc(75% - 10px);
}

.field.faculty {
  width: calc(25% - 10px);
}

.menu.sub {
  max-height: 300px;
  transform: translateY(-40px);
}
</style>
