<template>
  <div id="u-select">
    <select name="university" multiple="" class="ui fluid dropdown" id="university-select">
      <option value=""><i class="university icon"></i>University</option>
      <option v-for="(u,idx) in universities" v-bind:value="idx">{{u.name}}</option>
    </select>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  props: {
    uIds: {
      type: Array,
      default: function () {
        return []
      }
    }
  },
  mounted: function () {
    var self = this
    $(this.$el).find('#university-select').dropdown({
      onChange: function (v) {
        self.$parent.$emit('selectUniversity', v)
      }
    })
    $(this.$el).find('#university-select').dropdown('set exactly', this.uIds)
  },
  computed: {
    universities: function () {
      return this.$store.state.universities
    }
  }
}
</script>

<style scoped>
#u-select {
  width: 100%;
}
</style>
