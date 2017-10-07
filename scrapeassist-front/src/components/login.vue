<template>
  <div id="login-page">
    <div class="ui middle aligned center aligned grid">
      <div class="column">
        <h2 class="ui center aligned icon header huge">
          <i class="circular users icon"></i>
          PAFE
        </h2>
        <form class="ui large form">
          <div class="field">
            <div class="ui left icon input">
              <i class="user icon"></i>
              <input type="text" name="email" placeholder="E-mail address" v-model="email">
            </div>
          </div>
          <div class="field">
            <div class="ui left icon input">
              <i class="lock icon"></i>
              <input type="password" name="password" placeholder="Password" v-model="password">
            </div>
          </div>
          <div class="ui fluid large grey submit button" @click="login" @keyup.enter="login">Login</div>
          <div class="ui error message"></div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login: function () {
      // this.$store.dispatch('loginWithPassword', {email: this.email, password: this.password, router: this.$router})
      this.$router.push('search')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#login-page {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.large.form {
  width: 450px;
}
</style>
