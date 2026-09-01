<!-- 
Satisfies:
    - decision support functionality
    - implementation of interactive queries
    - functionalities to evaluate the accuracy of the data product
    - a user-friendly, functional dashboard that includes three visualization types (1 of 3)

This script implements on the frontend the interactions with the ml model through queries.
Specifically, faiss similarity search can be performed via one button, a k means cluster
can be explored with another button, and the full game profile can be seen on the Steam
website. This page aslo host one of the Visualizations, a dynamic one that produces a 
chart of the similarity scores of the 5 games nearest to the query. This also acts
as an accuracy confirmation.
-->
<script setup>
import { ref, onMounted } from 'vue';
import GameCard from './GameCard.vue';
import SimilarityChart from './SimilarityChart.vue'
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const goToVisuals = () => {
    window.location.hash = '#/visuals';
}

const auth = useAuthStore();

const userTop5 = ref([]);
const seenAppIds = ref([]);

const isLoading = ref(false);

const backend_url = import.meta.env.VITE_API_URL;

const trackSeenGames = (gamesArray) => {
    gamesArray.forEach(game => {
        if(!seenAppIds.value.includes(game.appid)){
            seenAppIds.value.push(game.appid);
        }
    });
}

const loadInitGames = async () => {

    isLoading.value = true;

    try {
        
        const timestamp = new Date().getTime();

        const path = `${backend_url}/api/load_user/${auth.steamId}?cb=${timestamp}`;

        const response = await axios.get(path)
        userTop5.value = response.data.slice(0, 5).map(item => ({
            appid: Number(item.data.appid),
            title: item.data.title,
            description: item.data.description,
            tags: item.data.tags,
            image: item.data.image,
            similarity: item.data.similarity
        }));

        trackSeenGames(userTop5.value);

    } catch (error) {
        console.error('Error fethcing initial data: ', error);
    } finally {
        isLoading.value = false;
    }
}

const getRecs = async (appid, title, tags) => {
    
    isLoading.value = true;

    try {
        const path = `${backend_url}/api/gen_recs/${appid}`
        const response = await axios.get(path, {
            params: {
                title: title,
                tags: tags,
                exclude: seenAppIds.value.join(',')
            }
        })
        
        userTop5.value = response.data.slice(0, 5).map(item => ({
            appid: Number(item.data.appid),
            title: item.data.title,
            description: item.data.description,
            tags: item.data.tags,
            image: item.data.image,
            similarity: item.data.similarity
        }));

        trackSeenGames(userTop5.value);

    } catch (error) {
        console.error("Bad API: " +  error)
    } finally {
        isLoading.value = false;
    }
}

const getClusterPeers = async (appid) => {
    
    isLoading.value = true;

    try {
        const path = `${backend_url}/api/explore_cluster/${appid}`
        const response = await axios.get(path, {
            params: {
                exclude: seenAppIds.value.join(',')
            }
        })
        
        userTop5.value = response.data.slice(0, 5).map(item => ({
            appid: Number(item.data.appid),
            title: item.data.title,
            description: item.data.description,
            tags: item.data.tags,
            image: item.data.image,
            similarity: item.data.similarity
        }));

        trackSeenGames(userTop5.value);

    } catch (error) {
        console.error("Bad API: " +  error)
    } finally {
        isLoading.value = false;
    }
}


const showSteamPage = (appid) => {

    const url = `https://store.steampowered.com/app/${appid}`

    window.open(url, '_blank', 'noopener, noreferrer');
}
onMounted(loadInitGames);

</script>
<template>
    <v-container>
        <v-btn variant="tonal" color="primary" prepend-icon="mdi-chart-line" @click="goToVisuals">
            See Cluster Graphs (2 out of 3 Visualizations)
        </v-btn>
        <br/>
        <br/>
        <SimilarityChart :games="userTop5" />
        <br/>
        <br/>
        <v-row>
            <template v-if="isLoading">
                <v-col v-for="n in 5" :key="'skeleton-' + n" cols="12" sm="5" md="5" lg="5">
                    <v-skeleton-loader
                        type="card, article, actions"
                        elevation="2"
                        class="mx-auto"
                    ></v-skeleton-loader>
                </v-col>
            </template>
            <template v-else>
                <v-col v-for="game in userTop5" cols="12" sm="5" md="5" lg="5">
                    <GameCard
                        :appid="game.appid"
                        :title="game.title"
                        :coverImage="game.image"
                        :description="game.description"
                        :tags="game.tags"
                        @find-recs="getRecs"
                        @steam-page="showSteamPage"
                        @explore-cluster="getClusterPeers"
                    />
                </v-col>
            </template>
        </v-row>
    </v-container>
</template>