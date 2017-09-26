<template>
  <div id="f-select">
    <select name="faculty" class="ui fluid dropdown" id="faculty-select">
      <option value=""><i class="building icon"></i>Faculty</option>
      <option v-for="(f,idx) in faculties" v-bind:value="idx">{{f.name}}</option>
    </select>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  props: {
    fId: {
      type: String,
      default: ''
    }
  },
  mounted: function () {
    var self = this
    $(this.$el).find('#faculty-select').dropdown({
      onChange: function (v) {
        self.$parent.$emit('selectFaculty', v)
      }
    })
    $(this.$el).find('#faculty-select').dropdown('set selected', this.fId)
  },
  computed: {
    faculties: function () {
      return this.$store.state.faculties
    }
  }
}
</script>

<style scoped>
#f-select {
  width: 100%;
}
</style>
