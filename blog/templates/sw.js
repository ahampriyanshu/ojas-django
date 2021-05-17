const OFFLINE_VERSION = 1.1,
    CACHE_NAME = "offline",
    OFFLINE_URL = "/offline/";

self.addEventListener("install", e => {
    e.waitUntil((async () => {
        const e = await caches.open("offline");
        await e.add(new Request(OFFLINE_URL, {
            cache: "reload"
        }))
    })())
}), self.addEventListener("activate", e => {
    e.waitUntil((async () => {
        "navigationPreload" in self.registration && await self.registration.navigationPreload.enable()
    })()), self.clients.claim()
}), self.addEventListener("fetch", e => {
    "navigate" === e.request.mode && e.respondWith((async () => {
        try {
            const a = await e.preloadResponse;
            return a || await fetch(e.request)
        } catch (e) {
            console.log("Fetch failed; Returning offline page instead.", e);
            const a = await caches.open("offline");
            return await a.match(OFFLINE_URL)
        }
    })())
});