import { defineConfig } from 'astro/config'
import svelte from '@astrojs/svelte'

export default defineConfig({
	// root: '.',     // Where to resolve all URLs relative to. Useful if you have a monorepo project.
	// srcDir: './src/pages', // Path to Astro components, pages, and data
	// outDir: './dist',       // When running `astro build`, path to final static output
	// publicDir: './public',   // A folder of static files Astro will copy to the root. Useful for favicons, images, and other files that don’t need processing.
	site: 'https://leonardini.dev',           // Your public domain, e.g.: https://my-site.dev/. Used to generate sitemaps and canonical URLs.
	integrations: [
		svelte()
	],
});
