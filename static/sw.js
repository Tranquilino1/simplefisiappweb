const cacheName = 'gargolas-chat-v1';
const staticAssets = [
  '/',
  '/static/css/style.css',
  '/static/css/default_avatar.svg',
  '/static/manifest.json'
];

self.addEventListener('install', async event => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      // Return cached version or fetch from network
      return cachedResponse || fetch(event.request);
    })
  );
});
