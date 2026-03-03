<script setup>
import { ref, onMounted } from 'vue';
import GameCard from './GameCard.vue';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const auth = useAuthStore();

const userTop5 = ref([]);

const loadInitGames = async () => {

    try {
        const path = `/api/load_user/${auth.steamId}`;

        const response = await axios.get(path)
        //console.log(response.data.slice(0, 5))
        userTop5.value = response.data.slice(0, 5).map(item => ({
            appid: Number(item.data.appid),
            title: item.data.title,
            description: item.data.description,
            tags: item.data.tags,
            image: item.data.image
        }));
    } catch (error) {
        console.error('Error fethcing initial data: ', error);
    }
    
}

const getRecs = async (appid, title, tags) => {
    
    //console.log("Got Recs!!!")
    //userTop5.value = userTop5.value.filter(game => game.appid === appid)

    try {
        const path = `/api/gen_recs/${appid}`
        const response = await axios.get(path, {
            params: {
                title: title,
                tags: tags
            }
        })
        
        /*const newGames*/ userTop5.value = response.data.slice(0, 5).map(item => ({
            appid: Number(item.data.appid),
            title: item.data.title,
            description: item.data.description,
            tags: item.data.tags,
            image: item.data.image
        }));

        //userTop5.value.push(...newGames);

    } catch (error) {
        console.error("Bad API: " +  error)
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
        </v-row>
    </v-container>
</template>