<template>

  <div class="form_div">
      
    <form @submit.prevent="login" id="loginform">

      <h1>Login </h1>
      <hr>
      
      <div v-if="message || errors.length > 0" :class="{'alert alert-success': message, 'alert alert-danger': errors.length > 0}" role="alert">
        <p v-if="message">{{ message }}</p>
        <ul v-if="errors">
            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </div>

      <div class="form-group mb-3">
        <label for="username">Username</label>
        <input type="text"  name="username" class="form-control">
      </div>

      <div class="form-group mb-3">
        <label for="password">Password</label>
        <input type="password" name="password" class="form-control">
      </div>

      <button type="submit" class="login-btn">Login</button>
    </form>

    
  </div>
</template>

<script setup>
    
  import { ref, onMounted } from "vue";

  let csrf_token = ref("");
  let message = ref("");
  let errors = ref([]);

  function getCsrfToken() {
      fetch('/api/v1/csrf-token')
      .then((response) => response.json())
      .then((data) => {
          csrf_token.value = data.csrf_token;
      })
      .catch((error) => {
          console.error('Error fetching CSRF token:', error);
      });
  }

  onMounted(() => {
      getCsrfToken();
  });

  function login() {
      let reg_form = document.querySelector("#loginform");
      let form_data = new FormData(reg_form);
      let isLoggedIn = ref(false);


      fetch("/api/v1/auth/login", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
      })
      .then(function (response) {
        if (!response.ok) {
            throw new Error('Failed to login');
        }
        return response.json(); 
      }) 
      .then(function (data) {
        console.log(data);
        if ("errors" in data){
            errors.value = [...data.errors];
        }else{
        // Check if the response contains an access token
          localStorage.setItem('user_id', data.id);
          if (data.access_token) {
              // Redirect to the explore page
              window.location.href = '/explore'; // Replace '/explore' with the URL of your explore page
              isLoggedIn.value = true; // Set isLoggedIn to true if login is successful
          } 
        }
      })
      .catch(function (error) {
          console.error('Login failed:', error);
          message.value = 'Login failed. Please try again.';
      });
  } 
</script>


<style >
  .error-message 
  {
    color: red;
  }

  .form_div 
  {
    border: 0.5px solid grey;
    border-radius: 10px;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: space-evenly;
    padding: 15px 15px;
    width: 30%;
    height: 70%;
    /* box-shadow: 7px 7px 4px rgba(0, 0, 0, 0.25); */

    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    font-weight: bold;
    position: relative; /* Set position to relative */
    margin-bottom: 20px; /* Adjust margin to create space between the form and the footer */
    z-index: 1; /* Ensure the login form appears above other elements */
    /* Other CSS styles remain the same */
  }

  .form-control 
  {
    width: 20rem;
    max-width: 400px;
    border-radius: 0px;
    border: 0.5px solid grey;
  }


  .login-btn
  {
      background-color: rgb(58, 221, 58);
      border: 1px solid rgb(71, 207, 71);
      width: 20rem;
      margin-top: 1rem;
      margin-bottom: 1rem;
      max-width: 400px;
      align-items: center;
      border-radius: 0px;
  }

  .login-btn:hover 
  {
    background-color: rgb(29, 142, 29);
  }


</style>