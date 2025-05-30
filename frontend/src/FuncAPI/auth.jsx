import { API } from "../constants";

export async function getCurrentUser() {
    const res = await fetch(API + 'auth/users/me', {
        method: 'GET',
        headers: {
            "accept": 'application/json'
        },
    });
    if (!res.ok) {
        throw new Error('Failed to fetch user');
    }
    return res.json(); // returns { yourField: "..." }
}