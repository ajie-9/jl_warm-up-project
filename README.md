# 热身 App 项目

这是热身 App 的完整项目仓库，包含 GitHub Pages 可直接访问的网站、React 源码工程和 MVP PRD 文档。

## 在线网站

GitHub Pages 使用 `main / root` 发布，因此仓库根目录的 `index.html` 和 `assets/` 是线上访问版本。

## 源码工程

网站源码放在 `application/`：

```bash
cd application
npm install
npm run dev
```

构建后会生成 `application/dist/`，再同步到仓库根目录供 GitHub Pages 发布。

## PRD 文档

打开 `warmup-app-mvp-prd/index.html` 即可查看完整 PRD 文档。

## 主要内容

- 开屏页与个性化定制流程
- 热身方向选择与动态热身页面
- 热身前自检与不适提示
- 我的主页、训练后饮食计划和每日食谱提醒逻辑
