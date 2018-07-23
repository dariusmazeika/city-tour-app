import base_config from './webpack.config.base';
import webpack from 'webpack';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import AssetsWebpackPlugin from 'assets-webpack-plugin';
import postCssConfig from './postcss.config';

export default {
    ...base_config,

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
                    use: MiniCssExtractPlugin.extract({
                        fallback: 'style-loader',
                        use: [ 'css-loader', {
                            loader: 'postcss-loader',
                            options: postCssConfig
                        }, 'sass-loader' ]
                    })
                };
            }
            return conf;
        })
    },

    plugins: [
        new webpack.DefinePlugin({
            '__DEV__': false,
            'process.env.NODE_ENV': JSON.stringify('production'),
            'process.env': JSON.stringify('production')
        }),
        new webpack.optimize.UglifyJsPlugin({
            output: {
                comments: false
            },
            compress: {
                unused: true,
                dead_code: true
            },
            sourceMap: true
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true,
            debug: false
        }),
        new MiniCssExtractPlugin('[chunkhash]_styles.css'),
        new AssetsWebpackPlugin({
            path: base_config.output.path,
            filename: 'assets.json'
        })
    ]
};
