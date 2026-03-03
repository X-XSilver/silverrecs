import { defineStore } from 'pinia';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore('auth', {
    
    
    state: () => ({
        
        
        token: null,
        steamId: 76561199015615632
    }),
    
    actions: {

        checkHashForToken() {
            
            const hash = window.location.hash;
            

            if(hash.includes('token=')) {

                const url = new URL(hash.replace('#', 'http://localhost'));
                const extractedToken = url.searchParams.get('token');

                if (extractedToken) {
                    this.token = extractedToken;
                    this.steamId = jwtDecode(extractedToken).sub;
                    
                    window.location.hash = '#/recs';
                    return true;
                }
            }
            
            return false;
        },

        logout() {
            
            this.token = null;
            this.steamId = null;
            window.location.hash = '#/';
        }
    },
    
    persist: true,
});