<template>
  <div class="ui card">
    <div class="content header" :class="{selected: selected}">
      <a><i class="right floated remove icon"></i></a>
      <a><i class="right floated pencil icon"></i></a>
      <div class="header">{{prof.name}}</div>
      <div class="meta" :class="{unknown: !prof.rank}">
        {{prof.rank ? prof.rank : 'Unknown Academic Rank'}}
      </div>
    </div>
    <div class="content">
      <h4 class="ui sub header">PhD</h4>
      <span :class="{unknown: !prof.phdInstitution}">
        {{prof.phdInstitution ? prof.phdInstitution : 'Unknown Institution'}},
      </span>
      <span :class="{unknown: !prof.phdYear}">
        {{prof.phdYear ? prof.phdYear : 'Unknown Year'}}
      </span>
      <h4 class="ui sub header">Last Promotion</h4>
      <span :class="{unknown: !prof.promotionInstitution}">
        {{prof.promotionInstitution ? prof.promotionInstitution : 'Unknown Institution'}},
      </span>
      <span :class="{unknown: !prof.promotionYear}">
        {{prof.promotionYear ? prof.promotionYear : 'Unknown Year'}}
      </span>
      <h4 class="ui sub header">Research Interests</h4>
      <span :class="{unknown: !prof.researchInterests}">
        {{prof.researchInterests ? prof.researchInterests : 'Unknown'}}
      </span>
    </div>
    <!-- <div class="extra content">
      <button class="ui button">Join Project</button>
    </div> -->
  </div>
</template>

<script>
export default {
  props: ['prof', 'selected', 'idx'],
  methods: {
    select: function () {
      this.$parent.$emit('select', this.idx)
    }
  }
}
</script>

<style scoped>
i.right.floated {
  color: black;
}

.content.header {
  flex: 0 1 auto !important;
}

.ui.card .unknown {
  color: red;
}

.content.header.selected {
  background-color: rgba(0, 0, 0, 0.2);
}
</style>
