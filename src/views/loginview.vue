<template>
    <div>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <div>
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username">
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password">
        </div>
        <button type="submit">Login</button>
      </form>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password
            })
          });
  
          const responseData = await response.json();
  
          if (response.ok) {
            // Login successful
            localStorage.setItem('accessToken', responseData.access_token);
            // Redirect to explore page
            this.$router.push('/explore');
          } else {
            // Login failed
            this.errorMessage = responseData.message || 'Login failed.';
          }
        } catch (error) {
          console.error('Error logging in:', error);
          this.errorMessage = 'An error occurred while logging in.';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .error-message {
    color: red;
  }
  </style>