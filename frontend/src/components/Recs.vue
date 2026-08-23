<script setup>
import { ref, onMounted } from 'vue';
import GameCard from './GameCard.vue';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

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
        //console.log(response.data.slice(0, 5))
        userTop5.value = response.data.slice(0, 5).map(item => ({
            appid: Number(item.data.appid),
            title: item.data.title,
            description: item.data.description,
            tags: item.data.tags,
            image: item.data.image
        }));

        trackSeenGames(userTop5.value);

    } catch (error) {
        console.error('Error fethcing initial data: ', error);
    } finally {
        isLoading.value = false;
    }
}

const getRecs = async (appid, title, tags) => {
    
    //console.log("Got Recs!!!")
    //userTop5.value = userTop5.value.filter(game => game.appid === appid)
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
        
        /*const newGames*/ userTop5.value = response.data.slice(0, 5).map(item => ({
            appid: Number(item.data.appid),
            title: item.data.title,
            description: item.data.description,
            tags: item.data.tags,
            image: item.data.image
        }));

        trackSeenGames(userTop5.value);
        //userTop5.value.push(...newGames);

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
                    />
                </v-col>
            </template>
        </v-row>
    </v-container>
</template>