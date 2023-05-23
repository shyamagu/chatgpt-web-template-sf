import adapter from '@sveltejs/adapter-static';

export default {
    kit: {
        adapter: adapter({
            // default options are shown. On some platforms
            // these options are set automatically — see below
            pages: '../fastapi/static',
            assets: '../fastapi/static',
            fallback: 'index.html',
            precompress: false,
            strict: true
        })
    }
};