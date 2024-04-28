<template>
    <div class="explore-page">
      <h1>Explore</h1>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <div v-for="post in posts" :key="post.id" class="post-card">
          <div class="post-header">
            <img
              :src="post.user.profile_photo"
              :alt="post.user.username"
              class="profile-photo"
              @click="viewUserProfile(post.user.id)"
            />
            <span class="username" @click="viewUserProfile(post.user.id)">{{ post.user.username }}</span>
          </div>
          <img :src="post.photo" :alt="post.caption" class="post-image" />
          <div class="post-caption">{{ post.caption }}</div>
          <div class="post-actions">
            <button
              class="like-button"
              :class="{ liked: isPostLiked(post.id) }"
              @click="likePost(post.id)"
            >
              <i class="fas fa-heart"></i> {{ post.likes.length }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'ExplorePage',
    data() {
      return {
        posts: [],
        loading: true,
        likedPosts: []
      }
    },
    mounted() {
      this.fetchPosts()
    },
    methods: {
      fetchPosts() {
        axios
          .get('/api/v1/posts')
          .then(response => {
            this.posts = response.data
            this.loading = false
          })
          .catch(error => {
            console.error(error)
            this.loading = false
          })
      },
      likePost(postId) {
        const isLiked = this.isPostLiked(postId)
        const likeAction = isLiked ? 'unlike' : 'like'
  
        axios
          .post(`/api/v1/posts/${postId}/${likeAction}`)
          .then(() => {
            if (isLiked) {
              this.likedPosts = this.likedPosts.filter(id => id !== postId)
            } else {
              this.likedPosts.push(postId)
            }
          })
          .catch(error => {
            console.error(error)
          })
      },
      isPostLiked(postId) {
        return this.likedPosts.includes(postId)
      },
      viewUserProfile(userId) {
        this.$router.push(`/users/${userId}`)
      }
    }
  }
  </script>
  
  <style scoped>
  .explore-page {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .post-card {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 20px;
  }
  
  .post-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .profile-photo {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 10px;
    cursor: pointer;
  }
  
  .username {
    font-weight: bold;
    cursor: pointer;
  }
  
  .post-image {
    max-width: 100%;
    height: auto;
    margin-bottom: 10px;
  }
  
  .post-actions {
    display: flex;
    justify-content: flex-end;
  }
  
  .like-button {
    background-color: transparent;
    border: none;
    font-size: 16px;
    cursor: pointer;
  }
  
  .like-button.liked {
    color: red;
  }
  </style>