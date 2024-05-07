<template>
    <div class="post-head">
        <h2>New Post</h2>
    </div>

    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>
    
    <div v-if="errorMessage.length > 0" class="alert alert-danger">
      <ul>
        <li v-for="error in errorMessage" :key="error">{{ error }}</li>
      </ul>
    </div>  

    <div class="newPF">
    <form id="postForm" @submit.prevent="addPost">

        <div class="form-group mb-3">
            <label for="photo" class="form-label"><h5>Photo</h5></label>
            <input id="photo" type="file" name="photo" accept="image/png, image/jpeg, image/jpg" class="form-control"/>
        </div>

        <div class="form-group mb-3">
            <label for="caption" class="form-label"><h5>Caption</h5></label>
            <textarea v-model="text" placeholder="Add caption here" id="caption" name="caption" class="form-control"></textarea>
        </div>

        <button class="btn btn-primary" type="submit">Add Post</button>


    </form>
    </div>

    


</template>

<script setup>
    import { ref, onMounted } from "vue";
    let csrf_token = ref("");
    let errorMessage = ref("");
    let successMessage = ref("");
    //let userId = ref(""); // Add a reactive variable to store the user ID


    function addPost() { // Accept userId as a parameter


        let addPostForm = document.getElementById('postForm');
        let formdata = new FormData(addPostForm);
        let user_id = localStorage.getItem('user_id');

        //user_id = session["user_id"]

        fetch("/api/v1/users/" + user_id + "/posts", {
            method: 'POST',
            body: formdata,
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                
                if ("errors" in data){
                    errorMessage.value = [...data.errors];
                } else {
                    successMessage.value = "Sucessfully created a new post";
                    addPostForm.reset();
                }

                console.log(data);
            })
            .catch(function (error) {
                console.log(error);
            });


    }

    function resetFormFields(){
        errorMessage.value = "";
        photo.value = "";
        caption.value = "";
    }

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


</script>

<style scoped>

.post-head{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}
.newPF{
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: white;
    width: 500px;
    height: 400px;
    margin: auto;
    border: 1px solid #bbbab8;
    border-radius: 6px;
    box-shadow: 0px 4px 10px 2px #bbbab8;

}

textarea{
    height: 100px;
    width: 350px;
}

#postForm{
    display: block;
    padding: 30px;
}

.form-group{
    display: block;
}



</style>