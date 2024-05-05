<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToLogin = () => {
  router.push('/login');
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<template>
  <div class="parent-container">
  <div class="container1">
    <div class="image">
      <img src="homepage.jpg" alt="Photogram Image" width="200">
    </div>
  </div>
    <div class="container2">
    <div class="content">
      <div class="title">Photogram</div>
      <div class="paragraph">Share photos of your favourite moments with friends, family and the world.</div>
      <div class="button-container">
        <button class="btn" @click="goToRegister">Register</button>
        <button class="btn" @click="goToLogin">Login</button>
      </div>
    </div>
  </div>
</div>
</template>

<style>
.parent-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 40px;
  margin-right: 40px;
  
}

.container1, .container2 {
  text-align: center;
  background-color: white;
  flex: 1;
  height: 400px; 
  border: 3px solid #ccc; 
}

.container1 {
  margin-right: 10px; 
}

.image {
  width: 100%;
  height: 100%;
}

.image img {
  width: 100%;
  height: 100%;
  object-fit: cover; 
}

.title {
  font-size: 40px;
  font-weight: bold;
  margin-top: 20px;
}

.paragraph {
  font-size: 18px;
  margin-top: 20px;
}

.content {
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center; 
}

.button-container {
  display: flex; 
  flex-direction: row; 
  margin-top: 70px; 
  width: 400px
}

.btn {
  padding: 20px 40px; 
  font-size: 16px;
  margin: 0 5px; 
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-btn {
  background-color: #007bff;
  color: white;
}

.register-btn {
  background-color: #28a745;
  color: white;
}
</style>