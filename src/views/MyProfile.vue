<script setup>
    import { ref, onMounted } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import UserProfileHeader from '../components/UserProfileHeader.vue';
    import UserPhotos from '../components/UserPhotos.vue';

    let route = useRoute();
    let router = useRouter();
    let id = ref('');
    let userDetails = ref({});
    let posts = ref([]);
    let followers = ref([]);

    let csrf_token = ref('');
    let userId = localStorage.getItem('user_id'); // Use the user ID stored after login

    async function fetchLoggedInUser() {
        try {
            if (!userId) {
                throw new Error('User ID not found');
            }

            const response = await fetch(`/api/v1/users/${userId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${userId}` // Use userId instead of token
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch user details');
            }

            return await response.json();
        } catch (error) {
            console.log('Error fetching logged-in user:', error);
            return null;
        }
    }

    async function fetchUserDetails() {
        try {
            userDetails.value = await fetchLoggedInUser();
            if (userDetails.value) {
                id.value = userDetails.value.id;
                await fetchPosts();
            } else {
                console.log('User details not available');
            }
        } catch (error) {
            console.log('Error fetching user details:', error);
        }
    }

    async function fetchPosts() {
        console.log(`Fetching Posts for User ${id.value}`);
        try {
            const response = await fetch(`/api/v1/users/${id.value}/posts`);
            if (response.ok) {
                const data = await response.json();
                posts.value = data.posts || [];
            } else {
                throw new Error('Something was wrong with fetch request for posts');
            }
        } catch (error) {
            console.log(error);
        }
    }

    function follow() {
        let user_id = localStorage.getItem('user_id');
        let formData = new FormData()
        formData.append('target_id', userDetails.value.id)
        formData.append('user_id', userId)

        fetch("/api/v1/users/" + user_id + "/follow", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrf_token.value
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data);
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    function hasUserDetails() {
        return userDetails.value && userDetails.value.id; //Checks if data is set in userDetails
    }

    onMounted(async () => {
        await fetchUserDetails();
    })

</script>

<template>
    <UserProfileHeader 
        v-if="hasUserDetails && userDetails"
        :userDetails="userDetails" 
        :followers="followers" 
        :follow="follow" 
        :posts="posts" 
        :canFollow="true" 
        :isFollowed="false"
        :firstname="userDetails?.firstname || ''"
        :lastname="userDetails?.lastname || ''"
        :bio="userDetails?.bio || ''"
    />

    <UserPhotos v-if="posts" :posts="posts"/>
</template>

<style>
    /* Add your styles here */
</style>
