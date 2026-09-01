<!-- 
Satisfies:
    - decision support functionality

This script implements the gamecards that the users use to press buttons
and send queries to the ml model.
-->
<script setup>
import { computed } from 'vue';

const props = defineProps({
    appid: {type: Number, required: true},
    title: {type: String, required: true},
    coverImage: {type: String, required: true},
    description: {type: String, default: 'No description available.'},
    tags: {type: String, default: 'None'}
})

defineEmits(['find-recs', 'steam-page', 'explore-cluster'])

const displayTags = computed(() => {
    try {
        const tagsDict = JSON.parse(props.tags);

        const sortedTags = Object.entries(tagsDict)
        .sort((a, b) => b[1] - a [1])
        .map(([tag]) => tag);

        return sortedTags.length > 0 ? sortedTags.join(', ') : 'No Tags';
    } catch (error) {
        return 'No Tags';
    }
});
</script>

<template>
    
    <v-card max-width="920" class="mx-auto" elevation="8">

        <v-img :src="coverImage" max-width="920" aspect-ratio="2.14" cover class="align-end text-white">
        </v-img>
        
        <v-card-title class="bg-black bg-opacity-50 w-100">{{  title }}</v-card-title>

        <v-card-item>
            <v-card-subtitle>{{displayTags}}</v-card-subtitle>
        </v-card-item>

        <v-card-text>
            <div class="description-truncate flex-grow-1 text-body-2"> {{ description }}</div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
            
            <v-btn
            color="primary"
            variant="tonal"
            block
            prepend-icon="mdi-magnify"
            @click="$emit('find-recs', appid, title, tags)"
            >
                Get Recommendations
        </v-btn>

        </v-card-actions>

        <v-card-actions>
            <v-btn
            color="primary"
            variant="tonal"
            block
            prepend-icon="mdi-steam"
            @click="$emit('steam-page', appid)"
            >
                View on Steam
            </v-btn>
        </v-card-actions>
        <v-card-actions>
            
            <v-btn
            color="primary"
            variant="tonal"
            block
            prepend-icon="mdi-compass-outline"
            @click="$emit('explore-cluster', appid)"
            >
                Explore More Games In This Cluster
        </v-btn>

        </v-card-actions>
    </v-card>
</template>