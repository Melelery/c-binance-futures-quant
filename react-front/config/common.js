//这里存放配置项目用到的全局配置
export let env_fun= (dev,development='', production = '')=>{
  switch (process.env.NODE_ENV) {
    case "dev":
      return dev;
      break;
    case "development":
      return development;
      break;
    case "production":
      return production;
      break;
    default:
      return dev;
  }
};

//开发环境和正式环境的地址前缀
export let url_add = env_fun('',"", '');
//网站站点地址
export let localhost =env_fun("http://localhost:3006","","http://www.baidu.com/")
//本地调试时的地址
export let ip = 'localhost';
//本地调试时的端口
export let dev_port = 3028
//发布后的网站title
export let title = 'react_home'
//需要预加载的dns
export let dns = ['www.baidu.com', 'www.qq.com']
//api接口的数组
export let api = env_fun("/list","","/");

