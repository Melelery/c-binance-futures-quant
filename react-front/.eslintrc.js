module.exports = {
    "env": {
        "browser": true,
        "commonjs": true,
        "es6": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "$": true,
        "process": true,
        "__dirname": true
    },
    "parser": "babel-eslint",
    "parserOptions": {
        "ecmaFeatures": {
            "experimentalObjectRestSpread": true,
            "jsx": true
        },
        "sourceType": "module",
        "ecmaVersion": 7
    },
    "plugins": [
        "react"
    ],
    "rules": {
        "quotes": [2, "single"], //单引号
        "no-console": 0, //不禁用console
        "no-debugger": 2, //禁用debugger
        "no-var": 0, //对var警告
        "semi": 0, //不强制使用分号
        "no-irregular-whitespace": 0, //不规则的空白不允许
        "no-trailing-spaces": 1, //一行结束后面有空格就发出警告
        "eol-last": 0, //文件以单一的换行符结束
        "no-unused-vars": [2, {"vars": "all", "args": "after-used"}], //不能有声明后未被使用的变量或参数
        "no-underscore-dangle": 0, //标识符不能以_开头或结尾
        "no-alert": 2, //禁止使用alert confirm prompt
        "no-lone-blocks": 0, //禁止不必要的嵌套块
        "no-class-assign": 2, //禁止给类赋值
        "no-cond-assign": 2, //禁止在条件表达式中使用赋值语句
        "no-const-assign": 2, //禁止修改const声明的变量
        "no-delete-var": 2, //不能对var声明的变量使用delete操作符
        "no-dupe-keys": 2, //在创建对象字面量时不允许键重复
        "no-duplicate-case": 2, //switch中的case标签不能重复
        "no-dupe-args": 2, //函数参数不能重复
        "no-empty": 2, //块语句中的内容不能为空
        "no-func-assign": 2, //禁止重复的函数声明
        "no-invalid-this": 0, //禁止无效的this，只能用在构造器，类，对象字面量
        "no-redeclare": 2, //禁止重复声明变量
        "no-spaced-func": 2, //函数调用时 函数名与()之间不能有空格
        "no-this-before-super": 0, //在调用super()之前不能使用this或super
        "no-undef": 2, //不能有未定义的变量
        "no-use-before-define": 2, //未定义前不能使用
        "camelcase": 0, //强制驼峰法命名
        "jsx-quotes": [2, "prefer-double"], //强制在JSX属性（jsx-quotes）中一致使用双引号
        "react/display-name": 0, //防止在React组件定义中丢失displayName
        "react/forbid-prop-types": [2, {"forbid": ["any"]}], //禁止某些propTypes
        "react/jsx-boolean-value": 2, //在JSX中强制布尔属性符号
        "react/jsx-closing-bracket-location": 1, //在JSX中验证右括号位置
        "react/jsx-curly-spacing": [2, {"when": "never", "children": true}], //在JSX属性和表达式中加强或禁止大括号内的空格。
        "react/jsx-indent-props": [2, 4], //验证JSX中的props缩进
        "react/jsx-key": 2, //在数组或迭代器中验证JSX具有key属性
        "react/jsx-max-props-per-line": [1, {"maximum": 1}], // 限制JSX中单行上的props的最大数量
        "react/jsx-no-bind": 0, //JSX中不允许使用箭头函数和bind
        "react/jsx-no-duplicate-props": 2, //防止在JSX中重复的props
        "react/jsx-no-literals": 0, //防止使用未包装的JSX字符串
        "react/jsx-no-undef": 1, //在JSX中禁止未声明的变量
        "react/jsx-pascal-case": 0, //为用户定义的JSX组件强制使用PascalCase
        "react/jsx-sort-props": 2, //强化props按字母排序
        "react/jsx-uses-react": 1, //防止反应被错误地标记为未使用
        "react/jsx-uses-vars": 2, //防止在JSX中使用的变量被错误地标记为未使用
        "react/no-danger": 0, //防止使用危险的JSX属性
        "react/no-did-mount-set-state": 0, //防止在componentDidMount中使用setState
        "react/no-did-update-set-state": 1, //防止在componentDidUpdate中使用setState
        "react/no-direct-mutation-state": 2, //防止this.state的直接变异
        "react/no-multi-comp": 2, //防止每个文件有多个组件定义
        "react/no-set-state": 0, //防止使用setState
        "react/no-unknown-property": 2, //防止使用未知的DOM属性
        "react/prefer-es6-class": 2, //为React组件强制执行ES5或ES6类
        "react/prop-types": 0, //防止在React组件定义中丢失props验证
        "react/react-in-jsx-scope": 2, //使用JSX时防止丢失React
        "react/self-closing-comp": 0, //防止没有children的组件的额外结束标签
        "react/sort-comp": 2, //强制组件方法顺序
        "no-extra-boolean-cast": 0, //禁止不必要的bool转换
        "react/no-array-index-key": 0, //防止在数组中遍历中使用数组key做索引
        "react/no-deprecated": 1, //不使用弃用的方法
        "react/jsx-equals-spacing": 2, //在JSX属性中强制或禁止等号周围的空格
        "no-unreachable": 1, //不能有无法执行的代码
        "comma-dangle": 2, //对象字面量项尾不能有逗号
        "no-mixed-spaces-and-tabs": 0, //禁止混用tab和空格
        "prefer-arrow-callback": 0, //比较喜欢箭头回调
        "arrow-parens": 0, //箭头函数用小括号括起来
        "arrow-spacing": 0 //=>的前/后括号
    },
    "settings": {
        "import/ignore": [
            "node_modules"
        ]
    }
};
