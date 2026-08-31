<script setup>
import {ref, computed, onMounted, onUnmounted} from 'vue'
import { useAuthStore } from './stores/auth';
import Login from './components/Login.vue';
import Recs from './components/Recs.vue';
import Visuals from './components/Visuals.vue';
import NotFound from './components/NotFound.vue';



const auth = useAuthStore();

const routes = {
  '/': Login,
  '/recs': Recs,
  '/visuals': Visuals,
  '/not_found': NotFound
};

const currentPath = ref(window.location.hash || '#/');

const token = ref(null)


const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/'] || NotFound
});

const handleHashChange = () => {
  const foundToken = auth.checkHashForToken();

  if(!foundToken) {
    currentPath.value = window.location.hash || '#/';
  }
};

onMounted(() => {
    
    window.addEventListener('hashchange', handleHashChange);
    handleHashChange();

    
});

onUnmounted(() => {

    window.removeEventListener('hashchange', handleHashChange);
});

</script>

<template>
  <component :is="currentView"/>
</template>
