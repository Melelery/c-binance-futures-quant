# react_home
这是一个react的脚手架项目，其中包含着当前最新得脚手架配置方式，技术技术栈包括react16+mbox+antd+react-router4++webpack4+sass/less+axios+proxy，我会长期，并定期维护这个脚手架，将当下react生态圈最新技术运用进去,适用于新手或者关注进阶的朋友学习参考。（广大撸友觉得能用上的，也不要吝啬自己的star哦） 
 
# 脚手架工具
地址： [https://github.com/aiyuekuang/ztao.git](https://github.com/aiyuekuang/ztao.git)（具体用法可直接看该工具的README.md）

# 本项目的宗旨
更快、更新、更好用、更简单

# 更新日志  
**2019.05.17** [日志地址](https://github.com/aiyuekuang/react_home/blob/master/doc/doc.MD)  
1.拆分结构，将项目拆分为业务代码区（src/work里），和环境区
2.在启动命令中加入dev（开发环境），development（测试环境），production（生产环境）
3.使用mobx代替redux，更简单，更高效，更清晰
4.优化webpack配置，编译速度更快，体积更小
5.封装react-router并且加入鉴权功能，动态输出路由
6.新增了eslint代码规范
7.wepack.config支持es6写法

![列表图](https://github.com/aiyuekuang/react_home/blob/master/doc/img/react_homes.png?raw=true)

# 功能与特色
1. 项目集成了当前react中最好得ui轮子antd，不解释，已配置好，直接使用
2. 项目具备了本地开发和打包上线得3个不同状态得场景，在开发状态，本地服务已配置了http-proxy，方便用户跨域调用后端开发得接口，并且本地调试阶段用得是根目录下得index.html，打包上线得时候部署到服务器得是加过hash得index.html这样就避免了测试人员总是无法刷新出新得界面得问题
3. 项目集成了sass和less这2种样式开发，方便2个阵营得都能愉快使用
4. 项目将原来的redux切换为mobx，因为长时间使用redux我发现，实际开发中，完全没必要使用redux，每个页面的数据和页面逻辑在当前页面内完成是最佳的实践，这样更直观，并且让后来的改代码的小伙伴很容易理解，也很容易排错，试想一个数据在各个地方使用，出现问题，是不是很头疼？所以我这样做，并且在实际的应用中，确实是有这样的效果
5. 本项目使用得axios来作为ajax，有简单得库在utils中的fetchData
7. 本项目引入了[esn](https://github.com/aiyuekuang/esn.git)得库，一个很小巧得数据操作库，在开发过程中，里面得很多功能都能用到，2个字方便
8. 本项目没有尝试服务器端渲染，笔者认为，spa最大得特色就是使得前后端得开发模式发生了变化，让整个开发流程变得舒服，前端人员开发出来得代码可以随意得部署在任何地方，而不需要考虑服务器上得问题，而首屏加载过慢得问题可以通过gzip来解决，我想这能满足大多数人得需求，当然了，项目有特殊性，还是有很多项目需要用到服务端渲染，这可以加强研究
9. 本项目有简单的脚手架工具[ztao-cli](https://github.com/aiyuekuang/ztao.git)，可以直接只用，更加方便快捷

# 项目结构
1. config：用于配置各种变量，有webpack中用到的，也有项目中用到的，比如"img_add_url"这个字段就是图片上传的前缀，用于图片上传后，后台没有返回完整的图片url，只返回图片的名称后缀时，在前面加上地址的作用
2. dll：在package的script里面有dll，用于提前打包我们常用的库的一个工具，加快我们的编译时间的
3. dist：打包后的代码
4. src/utils：用于开发主管放置公共函数的地方
5. src/work：开发组员用于开发业务的地方（page：每个页面都放在这里面，router：路由的数据结构都在这里，server：所有的ajax请求都写在这里，方便后续复用，components用于存放复用组件的地方，images存放图片，图片可以在页面直接import引用，common是用于存放业务中公共的函数的与业务紧密结合的这种）
6. .eslintrc.js是eslint的配置文件
7. webpack.config.babel.js是webpack的配置文件，支持es6写法
8. webpack.dll.config.js是用于打包dll的配置文件，你也可以将库打包进去，加快整个项目的编译时间

# 项目适用对象
1. 团队式协作：由一个主管负责项目的整体环境，src/work以外各个文件的维护，比如config，webpack，mock，utils之类的，团队成员负责项目的业务部分src/work不需要关注此以外的部分，有任何问题可以咨询主管
2. 适用项目：适用于antd pro项目之外的所有项目，和嫌antd pro过于庞大的项目，简单说就是，不想用antd pro的，都可以用这个开发项目
3. 后续：本项目是一个架构基础，旨在更简单的让所有用户在项目架构阶段，简化工作，并且让所有团队成员更快的熟悉这个架构，将更多的精力放在分析需求和代码实现上，本人有一揽子的从需求发起到项目上线的流程优化系统，将在后续的博客中一一分享，同时也会有各类配套工具的分享


# 使用方法（建议使用yarn，尽量不要用cnpm）：
    安装模块：npm install  
    
    开发模式：npm start  

    打包：npm run build
    
    访问地址：http://localhost:3012
    
# 注意以及搭建环境时问题汇总
1. 如果在build或者start的时候出现node-sass之类的报错，可以使用 npm rebuild node-sass来处理下，再build或start，也可以参考[地址](https://juejin.im/post/5cde1df65188250a8f72ff68)。
  

# 打包上线
* 在项目开始之前，在config文件夹中，配置你的项目的各种环境，这些环境都是项目在开发和上线时都需要用到的
* 打包后直接将build文件夹提交至你们项目得根目录中
* 命令并且呵斥你们得后端人员，将404指向build/index.html，这样基本就可以愉快得查看了
* 如果在上线后首屏调用速度较慢，这样得情况得话，可以鞭挞后端人员，开启服务器得gzip压缩功能将js压缩一下，压缩后大小基本只有原来得三分之一，这个很实用

* 还有自己打包代码发布到nginx的方法：[地址](https://juejin.im/post/5cde732e51882525d20ead6f)

# 希望
* 本项目是根据react社区一些朋友分享得脚手架综合，并且实际项目运用后所得出得经验
* 朋友们如果有一些对本项目得建议，或者想法欢迎issues，将持续改进
