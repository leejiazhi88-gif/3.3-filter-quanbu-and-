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
# 东方财富不可用时，可设置 QUOTE_SOURCE=sina 使用新浪实时行情
.venv/bin/python scripts/refresh_realtime_20261013.py prepare
# 检查 work/refresh-realtime-20261013/summary.json 与 payload.json 后执行
.venv/bin/python scripts/refresh_realtime_20261013.py apply
```

每次必须传入正确交易日和上一交易日。备用新浪源保留实时价格和实时总市值口径（原始市值单位万元，转换为元），全市场按代码稳定分页并检查数量及唯一性；来源记录在本地 summary.json。prepare 读取目标、拉取行情、准备备份和写入数据；apply 检查准备后表格未变化，再写入并回读校验。历史缓存自动补齐至指定上一交易日。

## 当前限制

- 2026-10-13 用户已授予新表 API 写入权限，并已成功通过 API 完成全表刷新。后续优先使用 API。
- 新增股票时自动扩展无筛选条件的筛选范围，并保持全部行可见；存在有效筛选条件时先停止以免排序错位。超出 500 行容量仍需先扩容再 prepare。
- 个人笔记颜色映射为迁入时快照；用户调整颜色后需重新核对。代码不会从在线表自动读取新颜色。
- 这是手动调用的批次刷新程序，没有安装定时或后台自动同步服务。

## 最近一次核验

2026-10-15 已通过 API 刷新至 11:30 上午收盘快照。本次东方财富连接失败，改用新浪实时价格及总市值；取回 5,575 条唯一市场记录。原有 454 只股票保留，新增申万二级行业市值前二的福建金森（002679.SZ），共 455 只。全部写入值已回读核对，原有 A:F 按代码保持不变；14 条条件格式及冻结窗格保留，筛选范围为 A1:Q456，全部行可见。

当日涨幅沿用行情源的参考昨收口径；中国中车、上港集团的行情参考昨收分别为 6.44、5.59，与历史原始收盘价不同，已交叉核对实时报价。各周期涨幅仍沿用未复权历史收盘价口径。

## 同步约定

后续实时表相关代码、配置和文档在此维护，验证后 commit 并 push 到 `origin/main`。`work/`、`outputs/`、行情缓存和凭证不上传。修改前 fetch 并检查远端变化；不覆盖他人提交、不强推。
