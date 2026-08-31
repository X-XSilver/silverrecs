<script setup>
const backend_url = import.meta.env.VITE_API_URL;

const goBack = () => {
    if(window.history.length > 1){
        window.history.back();
    }
    else{
        window.location.hash = '#/login';
    }
}
</script>

<template>
    <v-container>
        <v-btn variant="text" prepend-icon="mdi-arrow-left" @click="goBack">
            Back to Reccomendations
        </v-btn>

        <h2>Game Clusters (PCA Projection)</h2>
        <v-img :src="`${backend_url}/api/static-data/cluster_plot.png`"/>

        <h2>Silhouette Score by k</h2>
        <v-img :src="`${backend_url}/api/static-data/silhouette_plot.png`"/>
    </v-container>
</template>