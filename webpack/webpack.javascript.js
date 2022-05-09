const path = require('path')

module.exports = () => ({
  target: 'web',
  entry: {
    cruditor: './js/cruditor.js',
  },
  context: path.resolve(process.cwd(), 'client'),
  output: {
    filename: '[name].js',
    chunkFilename: '[name]-[chunkhash].js',
    path: path.join(process.cwd(), 'cruditor', 'static', 'cruditor', 'js'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
    ],
  },
  resolve: {
    alias: {
      app: path.resolve(process.cwd(), 'client', 'js'),
    },
    extensions: ['.js'],
    modules: [
      path.resolve(process.cwd(), 'client', 'js'),
      path.resolve(process.cwd(), 'node_modules'),
    ],
  },
})
