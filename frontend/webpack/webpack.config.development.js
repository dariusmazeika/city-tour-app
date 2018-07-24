import base_config from './webpack.config.base';
import webpack from 'webpack';
import path from 'path';

export default {
    ...base_config,

    output: {
        ...base_config.output,
        publicPath: 'http://localhost:3000' + base_config.output.publicPath,
        filename: 'bundle.js'
    },
    entry: [
        'react-hot-loader/patch',
        'webpack-dev-server/client?http://0.0.0.0:3000',
        'webpack/hot/only-dev-server',
        ...base_config.entry
    ],

    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NamedModulesPlugin(),
        new webpack.LoaderOptionsPlugin({
            debug: true,
            options: {
                eslint: {
                    configFile: path.join(__dirname, '..', '.eslintrc')
                }
            }
        }),
        new webpack.DefinePlugin({
            '__DEV__': true,
            'process.env': JSON.stringify('development')
        })
    ]
};
