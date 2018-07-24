import base_config from './webpack.config.base';
import webpack from 'webpack';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import AssetsWebpackPlugin from 'assets-webpack-plugin';
import postCssConfig from './postcss.config';
import UglifyJsPlugin from 'uglifyjs-webpack-plugin';

export default {
    ...base_config,
    mode: 'production',
    output: {
        ...base_config.output,
        filename: '[chunkhash]_bundle.js'
    },

    module: {
        ...base_config.module,
        rules: base_config.module.rules.map(function (conf) {
            if (conf.use.indexOf('style-loader') > -1) {
                return {
                    ...conf,
                    use: [ MiniCssExtractPlugin.loader,
                        {
                            loader: 'css-loader',
                            options: {
                                minimize: {
                                    safe: true
                                }
                            }
                        },
                        {
                            loader: 'postcss-loader',
                            options: postCssConfig,
                        },
                        {
                            loader: 'sass-loader',
                            options: {}
                        } ]
                };
            }
            return conf;
        })
    },
    optimization: {
        noEmitOnErrors: false,
        minimizer: [
            new UglifyJsPlugin({
                uglifyOptions: {
                    output: {
                        comments: false
                    },
                    compress: {
                        unused: true,
                        dead_code: true
                    },
                },
                sourceMap: true
            }),
        ]
    },

    plugins: [
        new webpack.DefinePlugin({
            '__DEV__': false,
            'process.env.NODE_ENV': JSON.stringify('production'),
            'process.env': JSON.stringify('production')
        }),

        new webpack.LoaderOptionsPlugin({
            minimize: true,
            debug: false
        }),
        new MiniCssExtractPlugin({
            filename: '[chunkhash]_styles.css',
            chunkFilename: '[chunkhash]_styles.css',
        }),
        new AssetsWebpackPlugin({
            path: base_config.output.path,
            filename: 'assets.json'
        })
    ]
};
