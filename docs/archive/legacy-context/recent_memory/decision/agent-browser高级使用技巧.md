# agent-browser 高级使用技巧

## API认证设置
通过eval注入token到localStorage，解决API未授权问题：
```bash
agent-browser eval "localStorage.setItem('token', 'your_token_here')"
```

## 页面导航与状态同步
SPA应用无URL变化时，用History API或直接调用页面切换函数：
```bash
agent-browser eval "v16SwitchLevel('L4')"  # L级切换
agent-browser eval "v16SwitchTab('Tasks')" # Tab切换
```

## 自定义JS执行
普通click无效时，用eval触发元素点击：
```bash
agent-browser eval "document.querySelector('.button').click()"
```

## API端点验证
通过eval直接调用API，验证端点正确性和数据返回格式：
```bash
agent-browser eval "fetch('/api/projects').then(r=>r.json()).then(console.log)"
```

## Bug诊断
通过eval检查变量类型和值，定位前端错误原因：
```bash
agent-browser eval "JSON.stringify({type: typeof projects, isArray: Array.isArray(projects)})"
```