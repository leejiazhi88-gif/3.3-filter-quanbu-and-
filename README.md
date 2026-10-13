# 3.3 筛选器（全部＋实时）

实时表功能的独立工作空间，与本 GitHub 仓库同步维护。

## 固定目标

- 飞书：https://my.feishu.cn/wiki/BvSrwQDxviMGqekHxizcnhEmnYe?sheet=Wc32bt
- Spreadsheet：`RVKmszaTRh2lWoteg8bcQSKCnIc`
- 实时工作表：`Wc32bt`
- GitHub：https://github.com/leejiazhi88-gif/3.3-filter-quanbu-and-

代码迁自 `leejiazhi88-gif/BigA-feishu-road` 的 `973b4b8`，保留经核验的实时计算逻辑，切换到新飞书目标。脚本名称保留迁入日期；运行日期通过环境变量明确传入。

## 刷新口径

1. 保留全部已有股票；新增全市场市值超过 600 亿元或申万二级行业市值前二的股票。
2. 依申万一级总市值、二级总市值及个股市值降序排列。
3. 原有股票 A:F 按代码保留，尤其 B 列个人笔记；新股票才补充识别与简介信息。
4. G:Q 更新盘中总市值、按盘中价格缩放的上一交易日 TTM PE、当日及 10/30/60/90/250/360/720/1080 交易日涨幅。区间涨幅沿用原脚本的未复权收盘价口径，历史不足明确标注。
5. 行业配色参考 2026-10-12 全部表，个人笔记颜色使用本地按代码映射；保留条件格式、筛选及冻结窗格。
6. 页签默认记录真实行情时间。若用户指定午休快照，另标快照时间，不伪造该时刻成交价。

## 安装与准备

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

环境需要 `TUSHARE_TOKEN`。飞书需要 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`，可用环境变量或本地 `.env`，也可通过 `FEISHU_ENV` 指向已有凭证文件。不将密钥写入代码或 Git。

个人笔记颜色映射位于本地 `work/personal_note_colors.json`，结构为 `{"codes":{"股票代码":{"backColor":"#FFFFFF","foreColor":"#000000"}}}`。当前工作空间已迁入原映射及 453 只股票历史缓存，未上传 Git。新机器须从当前飞书表核对并准备该映射后才能写入。

```sh
export TRADE_DATE=20261013
export PRIOR_CLOSE_DATE=20261012
.venv/bin/python scripts/refresh_realtime_20261013.py prepare
# 检查 work/refresh-realtime-20261013/summary.json 与 payload.json 后执行
.venv/bin/python scripts/refresh_realtime_20261013.py apply
```

每次必须传入正确交易日和上一交易日。prepare 读取目标、拉取行情、准备备份和写入数据；apply 检查准备后表格未变化，再写入并回读校验。历史缓存自动补齐至指定上一交易日。

## 当前限制

- 2026-10-13 新表的应用 API 可读但写入返回 403；命令行 apply 目前会受此限制。已登录浏览器可编辑，最后一次页签更新通过浏览器完成。尚未更改应用权限。
- 若新增股票超出当前筛选范围或 500 行容量，脚本在写入前停止；需先扩展原表范围再重新 prepare。尚未实现自动扩容。
- 个人笔记颜色映射为迁入时快照；用户调整颜色后需重新核对。代码不会从在线表自动读取新颜色。
- 这是手动调用的批次刷新程序，没有安装定时或后台自动同步服务。

## 最近一次核验

2026-10-13 的 11:55 快照处于 A 股午休。重新取得的 5,923 只股票行情与 11:30 输入一致；453 只股票、4,983 个 G:Q 单元格按原口径重算核对一致。页签为 `实时数据（26.10.13 11点55分，行情11点30分）`，笔记、筛选、条件格式及冻结窗格均保留。

## 同步约定

后续实时表相关代码、配置和文档在此维护，验证后 commit 并 push 到 `origin/main`。`work/`、`outputs/`、行情缓存和凭证不上传。修改前 fetch 并检查远端变化；不覆盖他人提交、不强推。
