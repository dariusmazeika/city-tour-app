import autoprefixer from 'autoprefixer';

const config = {
    plugins: [
        autoprefixer({
            browsers: ['last 2 versions']
        })
    ]
};
export default config;
