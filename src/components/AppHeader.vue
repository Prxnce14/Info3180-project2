<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
<<<<<<< HEAD
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
=======
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
>>>>>>> 3c6bd7368499e0fc031d3459f82491c18ca241a1
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li v-if="!isLoggedIn" class="nav-item">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <RouterLink class="nav-link" to="/users/profile">My Profile</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink v-if="!isLoggedIn " class="nav-link" to="/login">Login</RouterLink>
              <RouterLink v-else class="nav-link" to="/logout">Logout</RouterLink>  
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
  import { RouterLink } from "vue-router";
  import { ref } from "vue";

  //let isLoggedIn = ref(false);
  let isLoggedIn = localStorage.getItem('isLogin');
  // Function to check the user's login state

  

</script>

<style>
/* Add any component specific styles here */
</style>