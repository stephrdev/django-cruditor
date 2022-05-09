const
  path = require('path')

const TerserPlugin = require('terser-webpack-plugin')

module.exports = (env) => {
  const
    config = {
      mode: env.production ? 'production' : 'development',
      devtool: !env.production && 'inline-source-map',
      stats: 'minimal',
      resolve: {
        extensions: ['.js'],
        modules: [
          path.resolve(process.cwd(), 'client', 'js'),
          'node_modules',
        ],
      },
    }

  if (env.production) {
    config.performance = { hints: false }
    config.optimization = {
      moduleIds: 'named',
      minimizer: [
        new TerserPlugin({
          terserOptions: {
            sourceMap: !env.production,
          },
        }),
      ],
    }
  }

  return config
}
