<template>
  <div class="ui segment" id="segment">
    <div class="ui six cards">
      <profCard v-for="(i,id) in professors" :selected="false" :prof="i" :key="id"></profCard>
    </div>
  </div>
</template>

<script>
import profCard from '@/components/professor-card'
export default {
  components: {
    profCard: profCard
  },
  props: ['professors']
}
</script>

<style scoped>
#segment {
  flex: 1 1 auto;
  margin: 0px;
  border: none;
  position: relative;
  margin-top: 0px;
  padding: 0px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow-y: hidden;
}

.ui.six.cards {
  margin: 0px;
  overflow: auto;
}

.ui.card {
  text-align: left;
  margin: 3px !important;
  width: calc( 16.666666666% - 6px) !important;
  color: black;
}
</style>
