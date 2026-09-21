"""AutoPM AI: weekly reports to Airtable."""

# 版本号唯一真源（唯一真源：本文件 __version__）。
# 升级规则：每次修改 autopm/ 任意模块并交付给用户前，必须在此递增版本号
# （补丁 2.2.x → 修复/小优化；次版本 2.x.0 → 新功能/界面重构）。
# sync.py 的 result.version、preview.py 预览页、ui.py 标题栏/面包屑自动引用本值，
# 禁止在其它文件单独硬编码版本号。
__version__ = "2.4.0-rc4"
