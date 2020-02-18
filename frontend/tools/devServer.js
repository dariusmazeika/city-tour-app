import webpack  from 'webpack';
import WebpackDevServer from 'webpack-dev-server';
import config  from '../webpack/webpack.config.dev';
import {chalkProcessing, chalkError, chalkSuccess} from "./chalkConfig";


console.log(chalkProcessing('Starting dev server....'));

new WebpackDevServer(webpack(config), {
    publicPath: config.output.publicPath,
    filename: config.output.filename,
    inline: true,
    hot: true,
    host: '0.0.0.0',
    port: 3000,
    stats: {
        colors: true
    },
    historyApiFallback: true,
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'X-Requested-With'
    }
}).listen(3000, '0.0.0.0', function (err) {
    if (err) {
        console.error(chalkError(err));
    } else {

        console.log(chalkSuccess('webpack dev server listening on localhost:3000'));
    }
});
