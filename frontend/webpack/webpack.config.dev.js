import webpack from 'webpack';
import path from 'path';
import HardSourceWebpackPlugin from 'hard-source-webpack-plugin';

const SERVER_HOST = 'http://0.0.0.0:3000';
export default {
  resolve: {
    extensions: ['*', '.js', '.jsx', '.json', '.ts', '.tsx']
  },
  devtool: 'source-map',
  entry: [
    `webpack-dev-server/client?${SERVER_HOST}`,
    'webpack/hot/only-dev-server',
    path.resolve(__dirname, '..', 'src/js/index.js')
  ],
  target: 'web',
  mode: 'development',
  output: {
    path: path.resolve(__dirname, '..', 'dist'),
    publicPath: `${SERVER_HOST}/static/`,
    filename: 'bundle.js'
  },
  plugins: [
    new HardSourceWebpackPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.(t|j)sx?$/, use: { loader: 'awesome-typescript-loader' },
        exclude: /node_modules/,
      },
      { enforce: 'pre', test: /\.js$/, loader: 'source-map-loader' },
      {
        test: /\.eot(\?v=\d+.\d+.\d+)?$/,
        use: ['file-loader']
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 10000,
              mimetype: 'application/font-woff'
            }
          }
        ]
      },
      {
        test: /\.[ot]tf(\?v=\d+.\d+.\d+)?$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 10000,
              mimetype: 'application/octet-stream'
            }
          }
        ]
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        use: {
          loader: 'svg-react-loader',
        },
      },
      {
        test: /\.(jpe?g|png|gif|ico)$/i,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]'
            }
          }
        ]
      },
      {
        test: /(\.css|\.scss|\.sass)$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              sourceMap: true
            }
          }, {
            loader: 'postcss-loader',
            options: {
              plugins: () => [
                require('autoprefixer')
              ],
              sourceMap: true
            }
          }, {
            loader: 'sass-loader',
            options: {
              includePaths: [path.resolve(__dirname, 'src', 'scss')],
              sourceMap: true
            }
          }
        ]
      }
    ]
  }
};
