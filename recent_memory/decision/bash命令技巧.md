# bash命令技巧
### 文件系统盘点
- 总大小: `du -sh . 2>/dev/null` | 目录排序: `du -sh */ 2>/dev/null | sort -rh`
- 文件类型: `find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20`