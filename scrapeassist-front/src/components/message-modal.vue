<template>
  <div class="ui basic modal" id="message-modal">
    <div class="ui icon header">
      <i class="icon" v-bind:class="[icon]"></i>
      {{ title }}
    </div>
    <div class="content">
      <p>{{ msg }}</p>
    </div>
    <div class="actions">
      <div class="ui ok inverted button">
        <!-- <i class="checkmark icon"></i> -->
        Okay
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['title', 'msg', 'icon']
}
</script>

<style scoped>
.content > p {
  text-align: center;
}

.actions {
  text-align: center !important;
}
</style>
