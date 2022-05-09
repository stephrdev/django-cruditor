const
  { merge } = require('webpack-merge')

const configCommon = require('./webpack.common')
const configJavascript = require('./webpack.javascript')
const configSass = require('./webpack.sass')

module.exports = (env) => {
  const
    js = configJavascript(env)
  const sass = configSass(env)
  const common = configCommon(env)
  const config = [
    merge(common, js),
    merge(common, sass),
  ]

  return config
}
