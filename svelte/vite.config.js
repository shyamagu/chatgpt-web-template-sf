import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/simple': {
				'target': 'http://127.0.0.1:8000',
				changeOrigin: true,
			},

			'/order': {
				'target': 'http://127.0.0.1:8000',
				changeOrigin: true,
			},

			'/booksearch': {
				'target': 'http://127.0.0.1:8000',
				changeOrigin: true,
			},

			'/bingsearch': {
				'target': 'http://127.0.0.1:8000',
				changeOrigin: true,
			},

		}
	}
});
