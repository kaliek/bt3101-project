<template>
  <div id="database-page">
    <div class="ui secondary pointing menu" id="menu">
      <a class="active item">
        University Name
      </a>
      <a class="item">
        Faculty Name
      </a>
      <div class="right menu">
        <div class="item">
          <div class="ui icon input">
            <input placeholder="Search by name..." type="text">
            <i class="search link icon"></i>
          </div>
        </div>
        <a class="browse item active" style="">
          Filters
          <i class="dropdown icon"></i>
        </a>
      </div>
    </div>
    <!-- <div class="ui fluid popup bottom left transition visible animating scale out">
      <div class="ui four column relaxed equal height divided grid">
        <div class="column">
          <h4 class="ui header">Fabrics</h4>
          <div class="ui link list">
            <a class="item">Cashmere</a>
            <a class="item">Linen</a>
            <a class="item">Cotton</a>
            <a class="item">Viscose</a>
          </div>
        </div>
        <div class="column">
          <h4 class="ui header">Size</h4>
          <div class="ui link list">
            <a class="item">Small</a>
            <a class="item">Medium</a>
            <a class="item">Large</a>
            <a class="item">Plus Sizes</a>
          </div>
        </div>
        <div class="column">
          <h4 class="ui header">Colored</h4>
          <div class="ui link list">
            <a class="item">Neutrals</a>
            <a class="item">Brights</a>
            <a class="item">Pastels</a>
          </div>
        </div>
        <div class="column">
          <h4 class="ui header">Types</h4>
          <div class="ui link list">
            <a class="item">Knitwear</a>
            <a class="item">Outerwear</a>
            <a class="item">Pants</a>
            <a class="item">Shoes</a>
          </div>
        </div>
      </div>
    </div> -->
    <div class="ui segment" id="segment">
      <table class="ui compact celled definition table">
        <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>University</th>
            <th>Current Position</th>
            <th>Year of Promotion</th>
            <th>Title Promoted</th>
            <th>Institute of Promotion</th>
            <th>Year of PhD</th>
            <th>Institute of PhD</th>
            <th>Relevant Research Area</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in 20">
            <td class="collapsing">
              <div class="ui fitted slider checkbox">
                <input type="checkbox"> <label></label>
              </div>
            </td>
            <td>Andrew Barry</td>
            <td>University College London</td>
            <td>Professor</td>
            <td>2017</td>
            <td>Professor</td>
            <td>University College London</td>
            <td>1988</td>
            <td>University of Sussex</td>
            <td>Importance of materials and technologies in political and economic life</td>
          </tr>
        </tbody>
        <tfoot class="full-width">
          <tr>
            <th></th>
            <th colspan="9">
              <div class="ui right floated small labeled icon button green">
                <i class="download icon"></i> Download as CSV
              </div>
              <div class="ui right floated small labeled icon button" v-on:click="crawlRequest">
                <i class="share icon"></i> Create a Crawl Request
              </div>
              <!-- <div class="ui small button">
                Approve
              </div>
              <div class="ui small  disabled button">
                Approve All
              </div> -->
            </th>
          </tr>
        </tfoot>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {}
  },
  methods: {
    crawlRequest: function () {
      this.$router.push('crawlrequest')
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
}

#menu {
  margin: 0px;
}

#segment {
  flex: 1 0 auto;
  margin: 0px;
  border: none;
}
</style>
