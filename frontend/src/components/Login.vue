<!-- 
Satisfies:
    - decision support functionality
    - industry-appropriate security features

This script allows the user to decide if they want to login with Steam,
use the provided sample account to interact with the recommender, or
to look at 2 of the data visualizations for the K Means Clusters.
The authentication for the login method is a secure handshake with
the Steam api.
-->
<script setup>
import imageUrl from '../assets/sits_01.png'

const goToVisuals = () => {
    window.location.hash = '#/visuals';
}
const defaultRecs = () => {
    window.location.hash = '#/recs';
}

const loginWithSteam = () => {

    const backend_url = import.meta.env.VITE_API_URL;
    const steam_openid_url = "https://steamcommunity.com/openid/login"

    const current_frontend = window.location.origin;

    const params = new URLSearchParams({
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": `${backend_url}/api/auth/steam_login?fr=${current_frontend}`,
        "openid.realm": `${backend_url}/api`,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
    })

    window.location.href = `${steam_openid_url}?${params.toString()}`;
}
</script>

<template>
  <div>
    <h1>Silver's Game Recommendation Engine</h1>
    <br/>
    <button @click="goToVisuals">See Cluster Graphics(2 out of 3 Visualizations)</button>
    <br/>
    <br/>
    <div><input type="image" :src="imageUrl" alt="WHYYYY" @click="loginWithSteam"/></div>
    <br/>
    <br/>
    <button @click="defaultRecs">Use Sample Account (1 out of 3 Visualizations)</button>
  </div>
</template>
