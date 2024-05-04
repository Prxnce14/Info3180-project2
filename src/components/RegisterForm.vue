<template>

    <div class="container">
        <form @submit.prevent="register" id="registerform">
            <h1>Register</h1>
            <hr>

            <div v-if="message || errors.length > 0" :class="{'alert alert-success': message, 'alert alert-danger': errors.length > 0}" role="alert">
                <p v-if="message">{{ message }}</p>
                <ul v-if="errors">
                    <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                </ul>
            </div>

            <div class = "formInfo">
                <div class="form-group mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" name="username" class="formcontrol" />
                </div>

                <div class="form-group mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="text" name="password" class="formcontrol" />
                </div>

                <div class="form-group mb-3">
                    <label for="firstname" class="form-label">Firstname</label>
                    <input type="text" name="firstname" class="formcontrol" />
                </div>

                <div class="form-group mb-3">
                    <label for="lastname" class="form-label">Lastname</label>
                    <input type="text" name="lastname" class="formcontrol" />
                </div>

                <div class="form-group mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="text" name="email" class="formcontrol" />
                </div>

                <div class="form-group mb-3">
                    <label for="location" class="form-label">Location</label>
                    <input type="text" name="location" class="formcontrol" />
                </div>

                <div class="form-group mb-3">
                    <label for="biography" class="form-label">Biography</label>
                    <textarea name="biography" class="formcontrol" ></textarea>
                </div>

                <div class="form-group mb-3">
                    <label for="photo" class="form-label">Photo</label>
                    <input type="file" id="photo" name="photofile" class="formcontrol" accept=".jpg,.png,.jpeg" />
                </div>

                <button type="submit" class="btn btn-primary">Register</button>
            </div>
            
        </form>
    </div>

</template>

<script setup>

    import {ref, onMounted} from "vue";
    let csrf_token = ref("");
    let message = ref("");
    let errors = ref([]);


    function getCsrfToken() {
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
    }

    onMounted(() => {
    getCsrfToken();
    });


    function register(){

        let reg_form = document.querySelector("#registerform");
        let form_data = new FormData(reg_form);

        fetch("/api/v1/register", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': csrf_token.value
                }
        })
        .then(function (response) { 
            return response.json(); 
        }) 
        .then(function (data) {
            console.log(data);
            
            message.value = data.message;
            reg_form.reset();
        })
        .catch(function (error) {
            console.log(error);
        })

    } 
        
</script>
    
<style>
body 
{
    padding-top: 5rem;
    background-color: rgb(198, 228, 250);
    height: 100vh;
    -moz-box-sizing: border-box; 
    -webkit-box-sizing: border-box; 
    box-sizing: border-box; 
}

form
{
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-color: white;
    padding: 50px;
    box-shadow: 2px 2px 8px rgb(88, 88, 88);
}


.container
{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 50px;
    max-width: 800px;
    width: 100%;
}

.form-group
{
    display: flex;
    margin-bottom: 15px;
    flex-direction: column;
}


.form-label
{
    font-weight: bold;
}



.btn
{
    background-color: rgb(7, 202, 43);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    width: 100%;
    margin-top: 10px;
    padding: 6px;
}

.btn:hover
{
    background-color: rgb(4, 220, 44);
    color: white;
    transition: all 0.8s;
}

</style>
