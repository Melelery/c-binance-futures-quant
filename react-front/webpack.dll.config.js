const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
const path = require('path'),
  fs = require('fs'),
  webpack = require('webpack');

const vendors = [
  'react',
  'react-dom',
  'react-router',
  'react-router-dom',
];
var Version = new Date().getTime();
module.exports = {

  entry: {
    vendor: vendors,
  },
  output: {
    path: path.resolve(__dirname, 'dll'),
    filename: 'Dll.js',
    library: '[name]_[hash]',
      // JS 执行入口文件
      entry: {
          main: './main.js',
      },
      output: {
          // 为从 entry 中配置生成的 Chunk 配置输出文件的名称
          filename: '[name].' + Version + 'js',
          // 为动态加载的 Chunk 配置输出文件的名称
          chunkFilename: '[name].' + Version + 'js',
      }
  },
  plugins: [
    new webpack.DllPlugin({
      path: path.resolve(__dirname, 'dll', 'manifest.json'),
      name: '[name]_[hash]',
      context: __dirname,
    })
  ],

};
