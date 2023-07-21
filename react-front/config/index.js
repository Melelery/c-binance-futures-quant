//这里存放用户开发时自己用到的全局配置
import {env_fun} from './common';



//判断是开发环境还是正式环境
export let pro = CONFIG_NODE_ENV;
//生产环境和开发环境后台资源文件的存放目录，比如上传图片后的地址前缀
export let img_add_url = env_fun("./","./","./");
//是mock模式还是dataform的模式
export let is_mock = true;
//数据接口使用哪种提交数据的方式
export let parm_is_json = true
