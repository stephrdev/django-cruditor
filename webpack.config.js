const
	autoprefixer = require('autoprefixer'),
	cssnano = require('cssnano'),
	merge = require('webpack-merge'),
	path = require('path'),

	ExtractTextPlugin = require('extract-text-webpack-plugin'),

	IN_PRODUCTION = (process.env.NODE_ENV === 'production'),
	COMMON = {
		devtool: IN_PRODUCTION ? 'source-map' : 'inline-source-map',
		watch: !IN_PRODUCTION,
		stats: {
			modules: false,
			children: false
		}
	},
	OUTPUT_SCSS = path.join(__dirname, 'cruditor/static/cruditor/css'),
	SCSS = {
		entry: {'cruditor': './static/scss/cruditor.scss'},
		output: {
			filename: '[name].css',
			path: OUTPUT_SCSS
		},
		module: {
			rules: [{
				test: /\.scss$/,
				use: ExtractTextPlugin.extract({use: [
					{loader: 'css-loader'},
					{loader: 'postcss-loader',
						options: {
							ident: 'postcss',
							plugins: [autoprefixer, cssnano]
						}
					},
					{loader: 'sass-loader'}
				]})
			}]
		},
		plugins: [
			new ExtractTextPlugin({
				filename: '[name].css',
				allChunks: true
			})
		],
		resolve: {
			alias: {
				uikit: path.join(__dirname, 'node_modules/uikit/src/scss')
			}
		}
	}
;


module.exports = [
	merge(COMMON, SCSS)
];
