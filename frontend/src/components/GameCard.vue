<script setup>
defineProps({
    appid: {type: Number, required: true},
    title: {type: String, required: true},
    coverImage: {type: String, required: true},
    description: {type: String, default: 'No description available.'},
    tags: {type: String, default: 'None'}
})

defineEmits(['find-recs', 'steam-page'])


</script>

<template>
    
    <v-card max-width="920" class="mx-auto" elevation="8">

        <v-img :src="coverImage" max-width="920" aspect-ratio="2.14" cover class="align-end text-white">
        </v-img>
        
        <v-card-title class="bg-black bg-opacity-50 w-100">{{  title }}</v-card-title>

        <v-card-item>
            <v-card-subtitle>{{tags}}</v-card-subtitle>
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
    </v-card>
</template>