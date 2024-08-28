<template>
  <!-- <header>
    <div class="wrapper">
      <span>D2 Levels</span>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header> -->

  <RouterView />
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
header {
  display: flex;
  line-height: 1.5;
  max-height: 100vh;
  padding: 1rem 2rem;
  background-color: var(--color-border-bottom);
}
</style>
