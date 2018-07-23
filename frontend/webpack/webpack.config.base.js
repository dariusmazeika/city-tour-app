// import webpack from 'webpack';
import path from 'path';
import postCssConfig from './postcss.config';
import 'react-hot-loader/patch';

export default {
    entry: [
        'babel-polyfill',
        `${path.resolve(__dirname, '../', 'src', 'js')}/index`
    ],
    devtool: 'source-map',
    output: {
        path: path.join(__dirname, '..', 'dist'),
        publicPath: '/static/',
    },

    module: {
        rules: [
            {
                use: [ {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            [ 'env', {
                                'loose': true,
                                'modules': false
                            } ], 'react', 'stage-0' ],
                    }
                }, 'eslint-loader' ],
                test: /\.(js|jsx)$/,
                exclude: /node_modules/
            }, {
                test: /\.svg$/,
                use: [ 'babel-loader', {
                    loader: 'svg-react-loader',
                    query: {
                        jsx: true
                    }
                } ]
            },
            {
                test: /\.scss$/,
                use: [ 'style-loader', 'css-loader', {
                    loader: 'postcss-loader',
                    options: postCssConfig
                }, 'sass-loader' ]
            },
            {
                test: /\.(mp4|webm|mp3|ogg|wav|jpeg|jpg|bmp|ico|png|gif|ttf|otf|woff|eot)$/,
                use: 'file-loader?name=[name].[ext]?[hash]'
            },

        ]
    },
    resolve: {
        extensions: [ '.js', '.jsx' ]
    },
    devServer: { hot: true },
    target: 'web',
    optimization: {
        noEmitOnErrors: true
    },
    plugins: [
        // new webpack.NoErrorsPlugin()
    ]
};
