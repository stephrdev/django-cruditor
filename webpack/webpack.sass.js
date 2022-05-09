const
  path = require('path')

const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = (env) => ({
  target: 'web',
  entry: {
    cruditor: './scss/cruditor.scss',
  },
  context: path.resolve(process.cwd(), 'client'),
  output: {
    path: path.join(process.cwd(), 'cruditor', 'static', 'cruditor'),
  },
  module: {
    rules: [
      {
        test: /\.(scss|css)$/,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              sourceMap: !env.production,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              sourceMap: !env.production,
              postcssOptions: {
                plugins: [
                  [
                    'postcss-preset-env',
                    {
                      autoprefixer: { grid: true },
                      browsers: 'last 2 versions',
                      stage: 0,
                    },
                  ],
                  'cssnano',
                ],
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: !env.production,
            },
          },
        ],
      },
      {
        test: /\.(jpg|jpeg|png|gif|svg)$/,
        type: 'asset/resource',
        generator: {
          filename: '[path][name][ext]',
        },
      },
    ],
  },
  resolve: {
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'css/[name].css',
    }),
    new CleanWebpackPlugin({
      cleanStaleWebpackAssets: false,
      protectWebpackAssets: false,
      cleanOnceBeforeBuildPatterns: [],
      cleanAfterEveryBuildPatterns: ['cruditor.js'],
    }),
  ],
})
