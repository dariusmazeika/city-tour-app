import webpack from 'webpack';
import path from 'path';
import HardSourceWebpackPlugin from 'hard-source-webpack-plugin';
import alias from './alias';

const SERVER_HOST = 'http://0.0.0.0:3000';
export default {
  resolve: {
    extensions: ['*', '.js', '.jsx', '.json', '.ts', '.tsx'],
    alias: alias
  },
  devtool: 'source-map',
  entry: [
    '@babel/polyfill',
    `webpack-dev-server/client?${SERVER_HOST}`,
    'webpack/hot/only-dev-server',
    path.resolve(__dirname, '..', 'src/js/index.tsx')
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
        test: /\.tsx?$/,
        exclude: /node_modules/,
        loader: [ {
          options: {
            cacheDirectory: true,
            babelrc: false,
            presets: [
              [
                '@babel/preset-env',
                { targets: { browsers: 'last 2 versions ' } }
              ],
              '@babel/preset-typescript',
              '@babel/preset-react'
            ],
            plugins: [
              '@babel/plugin-proposal-optional-chaining',
              [ '@babel/plugin-proposal-class-properties', { loose: true } ],
            ]
          }, loader: 'babel-loader'
        }],

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
