<script setup>
import imageUrl from '../assets/sits_01.png'

const defaultRecs = () => {
    window.location.hash = '#/recs';
}

const loginWithSteam = () => {

    const backend_url = "http://138.197.68.251";//import.meta.env.VITE_API_URL;
    const steam_openid_url = "https://steamcommunity.com/openid/login"
    const params = new URLSearchParams({
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": `${backend_url}/api/auth/steam_login`,
        "openid.realm": `${backend_url}/api`,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
    })

    window.location.href = `${steam_openid_url}?${params.toString()}`;
}
</script>

<template>
  <div>
    <h1>Silver Plugs</h1>
    <br/>
    <div><input type="image" :src="imageUrl" alt="WHYYYY" @click="loginWithSteam"/></div>
    <br/>
    <br/>
    <button @click="defaultRecs">Use Sample Account</button>
  </div>
</template>
