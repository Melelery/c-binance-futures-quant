import path from 'path';

const theme = require(path.join(__dirname, '/package.json')).theme;
import HtmlWebpackPlugin from 'html-webpack-plugin'; //html
import MiniCssExtractPlugin from 'mini-css-extract-plugin'; //css压缩
import UglifyJsPlugin from 'uglifyjs-webpack-plugin'; //多线程压缩
import ExtendedDefinePlugin from 'extended-define-webpack-plugin'; //全局变量
const CleanWebpackPlugin = require('clean-webpack-plugin'); //清空
import CopyWebpackPlugin from 'copy-webpack-plugin'; //复制静态html
import webpack from 'webpack';
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
//     .BundleAnalyzerPlugin; //视图分析webpack情况
import {env_fun, ip, title, dev_port, dns, url_add} from './config/common';

import HappyPack from 'happypack'; //多线程运行

let happyThreadPool = HappyPack.ThreadPool({size: 64});
let dev = process.env.NODE_ENV;

const PUBLIC_PATH = env_fun(`http://${ip}:${dev_port}/${url_add}`, url_add);

// new BundleAnalyzerPlugin({   //另外一种方式
//   analyzerMode: 'server',
//   analyzerHost: '127.0.0.1',
//   analyzerPort: 8888,
//   reportFilename: 'report.html',
//   defaultSizes: 'parsed',
//   openAnalyzer: true,
//   generateStatsFile: false,
//   statsFilename: 'stats.json',
//   statsOptions: null,
//   logLevel: 'info',
// })
var Version = new Date().getTime();
console.log(process.env.NODE_ENV)
/**
 * 公共插件
 */
const pluginsPublic = [
    new ExtendedDefinePlugin({
        //全局变量
        CONFIG_NODE_ENV: process.env.NODE_ENV
    }),
    new HtmlWebpackPlugin({
        template: path.join(__dirname, '/src/index.ejs'), // Load a custom template
        inject: 'body', //注入到哪里
        filename: 'index.html', //输出后的名称
        hash: false, //为静态资源生成hash值
        title: title,
        ip: ip,
        dev_port: dev_port,
        dns: dns,
        url: PUBLIC_PATH,
        pro: process.env.NODE_ENV
    }),
    // new BundleAnalyzerPlugin(),
    new MiniCssExtractPlugin({
        chunkFilename: '[chunkhash].'+Version+'css'
    }),
    new HappyPack({
        //多线程运行 默认是电脑核数-1
        id: 'babel', //对于loaders id
        loaders: ['cache-loader', 'babel-loader?cacheDirectory=true'], //是用babel-loader解析
        threadPool: happyThreadPool,
        verboseWhenProfiling: true //显示信息
    }),
    new webpack.ContextReplacementPlugin(
        /moment[\\\/]locale$/,
        /^\.\/(en|ko|ja|zh-cn)$/
    )
];
/**
 * 公共打包插件
 */
const pluginsBuild = [
    new CleanWebpackPlugin({
        root: __dirname
    }),
    new CopyWebpackPlugin([
        {
            from: path.resolve(__dirname, './dll/Dll.js'),
            to: path.resolve(__dirname, 'dist')
        },
        {
            from: path.resolve(__dirname, './public'),
            to: path.resolve(__dirname, './dist')
        }
    ]),
    new webpack.HashedModuleIdsPlugin()
];



let pro_plugins = [].concat(
    pluginsPublic,
    pluginsBuild,
    new webpack.DllReferencePlugin({
        context: __dirname,
        manifest: require('./dll/manifest.json')
    }),

    new UglifyJsPlugin({
        sourceMap: false,
        parallel: true,
        cache: true,
        uglifyOptions: {
            output: {
                comments: false,
                beautify: false
            },
            compress: {
                drop_console: true,
                drop_debugger: true
            }
        },

        exclude: /(node_modules|bower_components)/
    }) //压缩，生成map
)

const plugins = env_fun([].concat(pluginsPublic, pluginsBuild),pro_plugins,pro_plugins );

export default {
    devServer: {
        // contentBase: path.join(__dirname, 'dist'), //开发服务运行时的文件根目录
        //host: ip,
        compress: true, //开发服务器是否启动gzip等压缩
        port: dev_port, //端口
        historyApiFallback: true, //不会出现404页面，避免找不到
        proxy: {
            '/list': {
                target: 'https://www.apiopen.top/meituApi',
                pathRewrite: {'^/list': ''},
                changeOrigin: true,
                secure: false
            },
            '/api': {
                target: 'http://localhost:3000/graphql',
                pathRewrite: {'^/api': ''},
                changeOrigin: true,
                secure: false
            },
            '/ap_com': {
                target: 'http://localhost:3000',
                pathRewrite: {'^/ap_com': ''},
                changeOrigin: true,
                secure: false
            }
        }
    },
    devtool: false, //source-map cheap-eval-source-map  是一种比较快捷的map,没有映射列
    performance: {
        maxEntrypointSize: 250000, //入口文件大小，性能指示
        maxAssetSize: 250000, //生成的最大文件
        hints: false
        // hints: 'warning', //依赖过大是否错误提示
        // assetFilter: function(assetFilename) {
        //   return assetFilename.endsWith('.js');
        // }
    },
    entry: {
        //入口
        index: ['babel-polyfill', './src/index.js'],
        // index:  './src/index.js',
        // Quotes: './src/work/constainers/Quotes.js',
        // QuotesTable:'./src/work/constainers/QuotesTable.js',
        // Article: './src/work/constainers/Article.js'
    },
    output: {
        //出口
        path: path.resolve(__dirname, 'dist'), //出口路径
        filename: 'index' + Version + '.js',
        chunkFilename: '[chunkhash].js',  //按需加载名称
        publicPath: PUBLIC_PATH //公共路径npm

    },
    resolve: {
        mainFields: ['main', 'jsnext:main', 'browser'], //npm读取先后方式  jsnext:main 是采用es6模块写法
        alias: {
            //快捷入口
            '@config': path.resolve(__dirname, 'config'),
            '@components': path.resolve(__dirname, 'src/work/components'),
            '@images': path.resolve(__dirname, 'src/work/images'),
            '@style': path.resolve(__dirname, 'src/work/style'),
            '@server': path.resolve(__dirname, 'src/work/server'),
            '@common': path.resolve(__dirname, 'src/work/common'),
            '@mobx': path.resolve(__dirname, 'src/work/mobx')

        }
    },
    module: {
        noParse: /node_modules\/(moment|chart\.js)/, //不解析
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/, //排除
                //include: [path.resolve(__dirname, 'src')], //包括
                loader: 'happypack/loader?id=babel'
            },
            {
                test: /\.css$/,
                use: [
                    {loader: MiniCssExtractPlugin.loader},
                    {
                        loader: 'css-loader',
                        options: {
                            minimize: env_fun(true, true, true) //压缩
                            // sourceMap: minimize[dev],
                        }
                    }
                ]
            },
            {
                test: /\.(png|jpg|gif|jpeg|ttf|svg)$/,
                exclude: /(node_modules|bower_components)/,
                include: [path.resolve(__dirname, 'src/work/images')],
                use: [
                    {
                        loader: 'url-loader?limit=8024', //limit 图片大小的衡量，进行base64处理
                        options: {
                            name: '[path][name].[ext]'
                        }
                    }
                ]
            },
            {
                test: /\.less$/,
                use: [MiniCssExtractPlugin.loader, {
                    loader: 'css-loader?importLoaders=1',
                    options: {
                        minimize: true //css压缩
                    }
                }, {
                    loader: 'less-loader', options: {
                        javascriptEnabled: true,
                        modifyVars: {
                            'primary-color': '#00558c',
                            'link-color': '#00558c',
                            'border-radius-base': '2px',
                        }
                    }
                }]
            }, {
                test: /\.scss$/,
                use: [
                    {loader: MiniCssExtractPlugin.loader},

                    {
                        loader: 'css-loader',
                        options: {
                            minimize: env_fun(false, false, true) //压缩
                            // sourceMap: minimize[dev],
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {modifyVars: theme}
                    }
                ]
            }
        ]
    },
    plugins: plugins
};
