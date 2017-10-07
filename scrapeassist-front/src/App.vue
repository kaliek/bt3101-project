<template>
  <div id="app">
    <router-view></router-view>
    <msgmodal v-bind="$store.state.msgModalProps"></msgmodal>
  </div>
</template>

<script>
import msgmodal from '@/components/message-modal'
export default {
  name: 'app',
  components: {
    msgmodal: msgmodal
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  width: 100%;
}

/*#app ::-webkit-scrollbar {
  width: 2px !important;
  height: 13px !important;
}*/
</style>
