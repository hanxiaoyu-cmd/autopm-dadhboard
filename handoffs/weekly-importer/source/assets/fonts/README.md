# 本地界面字体

字体：Noto Sans SC，界面使用 Regular 非斜体；标题按层级加粗。

来源：本机 `Desktop/horizon/docker/fonts/NotoSansSC-VF.ttf`，完整字体文件原样复制，不修改字形或裁剪字符。
SHA-256：`763146584CF0710223441356B4395E279021B0806C196614377A7A0174AE074A`。
许可：SIL Open Font License 1.1，见随附 `OFL.txt`。

程序在自身进程内加载 TTF，不安装到系统。PyInstaller 将字体与许可一起打包，无需联网。

不能加载字体时回退到 Microsoft YaHei UI。此前的 Smiley Sans 及其许可已保存在 `archive/20260910-before-upright-font/`。
