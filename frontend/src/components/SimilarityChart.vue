<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {Chart as ChartJS, Title, Tooltip, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, BarElement, CategoryScale, LinearScale)

const props = defineProps({
    games: {type: Array, required: true}
});

const scoredGames = computed(() =>
    props.games.filter(g => g.similarity !== null && g.similarity !== undefined)
);

const chartData = computed(() => ({
    labels: scoredGames.value.map(g => g.title),
    datasets: [{
        label: 'Similarity',
        backgroundColor: '#1976D2',
        data: scoredGames.value.map(g => g.similarity)
    }]
}));

const chartOptions = {
    responsive: true,
    indexAxis: 'y',
    scales: {
        x: {
            min: 0.95,
            max: 1,
            title: {
                display: true,
                text: 'Similarity (scale starts at 0.95)'
            }
        }
    },
    plugins: {
        legend: { display: false },
        title: {
            display: true,
            text: 'How Similar Each Recommendation Is To Your Selection',
            font: { size: 16 }
        }
    }
};
</script>

<template>
    <div class="chart-wrapper" v-if="scoredGames.length > 0">
        <Bar v-if="scoredGames.length > 0" :data="chartData" :options="chartOptions" />
    </div>
</template>

<style scoped>
.chart-wrapper {
    background-color: #b4aa72;
    border-radius: 8px;
    padding: 16px;
}
</style>