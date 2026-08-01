/**
 * CFWGuestContent — drop-in client for the CF Weddings shared guest-content
 * backend (Guest Wishes Wall + Guest Photo Sharing).
 *
 * No build step, no dependencies. Load with a plain script tag:
 *   <script src="cfw-guest-content.js"></script>
 *   <script>
 *     CFWGuestContent.configure({ baseUrl: 'https://us-central1-yourproject.cloudfunctions.net' });
 *   </script>
 *
 * Then call:
 *   await CFWGuestContent.submitWish({ weddingSlug, name, relation, text });
 *   const wishes = await CFWGuestContent.listWishes({ weddingSlug });
 *   await CFWGuestContent.uploadPhoto({ weddingSlug, file });
 *   const photos = await CFWGuestContent.listPhotos({ weddingSlug });
 *
 * `wishes`/`photos` are plain arrays (newest first); a `.nextCursor` property
 * is attached to each array for pagination, or null if there's no more.
 *
 * Forms should include a hidden honeypot input (any name works client-side —
 * just pass its value through as `company`) that real guests never fill in:
 *   <input type="text" name="company" tabindex="-1" autocomplete="off"
 *          style="position:absolute;left:-9999px" aria-hidden="true">
 */
(function (global) {
  'use strict';

  const DEFAULT_LIMIT = 20;
  const state = { baseUrl: '' };

  function configure(options) {
    if (!options || !options.baseUrl) {
      throw new Error('CFWGuestContent.configure requires { baseUrl }.');
    }
    state.baseUrl = options.baseUrl.replace(/\/$/, '');
  }

  function requireBaseUrl() {
    if (!state.baseUrl) {
      throw new Error('Call CFWGuestContent.configure({ baseUrl }) before use.');
    }
  }

  async function parseResponse(res) {
    let body = null;
    try {
      body = await res.json();
    } catch (err) {
      body = null;
    }
    if (!res.ok) {
      throw new Error((body && body.error) || `Request failed with status ${res.status}`);
    }
    return body || {};
  }

  async function submitWish({ weddingSlug, name, relation, text, company }) {
    requireBaseUrl();
    const res = await fetch(`${state.baseUrl}/wishes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ weddingSlug, name, relation, text, company: company || '' }),
    });
    return parseResponse(res);
  }

  async function listWishes({ weddingSlug, limit = DEFAULT_LIMIT, cursor } = {}) {
    requireBaseUrl();
    const params = new URLSearchParams({ weddingSlug, limit: String(limit) });
    if (cursor) params.set('cursor', cursor);
    const res = await fetch(`${state.baseUrl}/wishes?${params.toString()}`);
    const body = await parseResponse(res);
    const wishes = body.wishes || [];
    wishes.nextCursor = body.nextCursor || null;
    return wishes;
  }

  // Resizes/re-encodes a File client-side (canvas) before upload so slow
  // mobile connections only ever send a small JPEG, not a raw 12MB HEIC.
  function resizeImage(file, maxDimension = 1600, quality = 0.8) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      const objectUrl = URL.createObjectURL(file);

      img.onload = () => {
        URL.revokeObjectURL(objectUrl);
        let { width, height } = img;
        if (width > maxDimension || height > maxDimension) {
          const scale = maxDimension / Math.max(width, height);
          width = Math.round(width * scale);
          height = Math.round(height * scale);
        }
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(img, 0, 0, width, height);
        canvas.toBlob(
          (blob) => {
            if (!blob) {
              reject(new Error('Could not process image'));
              return;
            }
            const reader = new FileReader();
            reader.onloadend = () => resolve(String(reader.result).split(',')[1]);
            reader.onerror = () => reject(new Error('Could not read image'));
            reader.readAsDataURL(blob);
          },
          'image/jpeg',
          quality
        );
      };
      img.onerror = () => {
        URL.revokeObjectURL(objectUrl);
        reject(new Error('Could not load image'));
      };
      img.src = objectUrl;
    });
  }

  async function uploadPhoto({ weddingSlug, file, company }) {
    requireBaseUrl();
    if (!file || !(file instanceof Blob)) {
      throw new Error('uploadPhoto requires a File/Blob.');
    }
    const data = await resizeImage(file);
    const res = await fetch(`${state.baseUrl}/photos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ weddingSlug, mimeType: 'image/jpeg', data, company: company || '' }),
    });
    return parseResponse(res);
  }

  async function listPhotos({ weddingSlug, limit = DEFAULT_LIMIT, cursor } = {}) {
    requireBaseUrl();
    const params = new URLSearchParams({ weddingSlug, limit: String(limit) });
    if (cursor) params.set('cursor', cursor);
    const res = await fetch(`${state.baseUrl}/photos?${params.toString()}`);
    const body = await parseResponse(res);
    const photos = body.photos || [];
    photos.nextCursor = body.nextCursor || null;
    return photos;
  }

  global.CFWGuestContent = {
    configure,
    submitWish,
    listWishes,
    uploadPhoto,
    listPhotos,
  };
})(typeof window !== 'undefined' ? window : globalThis);
