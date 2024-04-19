<template>
    <div>
      <h1>Logout</h1>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        localStorage.removeItem('accessToken');
        // Redirect to login page or any other desired page
        this.$router.push('/login');
      }
    }
  };
  </script>