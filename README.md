# AI Sales Ops Workbench

面向 B2B 销售运营的六模块 AI 工作流作品集。把分散的客户信息整理成可追溯事实，先检查数据，再准备 AI 分析输入，最后由人决定是否采纳。

**公开版全部使用从零编写的虚构数据，不包含真实客户、雇主资料、内部制度、报价或个人业绩。**

**项目性质：业务驱动的 AI 辅助工作流与离线规则工具包。** 默认不联网、不调用模型、不连接 CRM。Python 规则结果与模型生成内容明确分开；不宣称自研大模型、RAG、自动销售预测或生产级多智能体系统。

## 先看什么

- [六模块示例输出](docs/demo/weekly.md)：直接阅读一份有来源、待确认项和金额边界的经营报告。
- [商机检查结果](docs/demo/projects.md)：观察金额冲突、未确认转述、过期采购日如何被处理。
- [AI提示词示例](docs/demo/weekly-prompt.md)：查看规则、任务说明、数据及检查结果如何组合。
- [输入数据](examples/synthetic.json)：2个虚构伙伴、8条商机、11份来源、2条知识卡。
- [设计说明](docs/architecture.md)与[验证方法](docs/evaluation.md)：理解为什么分模块，以及哪些能力尚未验证。

## 六个模块

| 模块 | 解决的问题 | 具体交付 |
|---|---|---|
| 任务总控 | 不知道先处理什么、谁负责 | 风险驱动的待办与模块路由 |
| 渠道经营 | 团队与客户资源没有落到对象 | 规则报告列经营范围；AI任务要求提出客户侧下一动作 |
| 商机检查 | 阶段混淆、来源冲突、信息缺失 | 检查项、冲突清单及暂缓原因 |
| 经营周报 | 汇总时把计划、测试或机会当成果 | 只使用已确认记录的事实汇总 |
| 方案准备 | 从产品清单倒推客户需求 | 需求访谈、验收和验证准备清单 |
| 知识学习 | 旧资料被当作当前承诺 | 带来源和有效期的本地知识卡 |

六模块是任务划分，不是六个自主运行的智能体。公开版保留职责边界和可复现输入输出，不复制任何企业内部工作手册。

## 三分钟运行

要求：Python 3.10及以上。没有第三方Python依赖，不需要API Key。

```bash
git clone https://github.com/yuzewu318-sketch/ai-sales-ops-workbench.git
cd ai-sales-ops-workbench
python3 -m unittest discover -s tests -v
python3 workbench.py demo --out demo-output
```

Windows可将`python3`换成`py -3`。直接用浏览器打开`demo-output/index.html`，点击六个模块查看报告。输出目录必须是新目录；已有目录不会被覆盖。

示例统计日固定为2030-03-15，因此结果不会随运行日期漂移：

| 指标 | 预期结果 | 说明 |
|---|---:|---|
| 商机记录 | 8条 | 包含全部阶段 |
| 暂缓汇总 | 2条 | 金额冲突1条、未经确认1条 |
| 已确认签约 | 1条 / 32,000元 | 有合同确认，不等于回款 |
| 已确认在途 | 3条 / 316,000元 | 是记录金额，不是销售预测 |
| 丢单及取消 | 2条 | 保留历史，不计入在途 |

## 怎样与AI一起使用

1. 运行`python3 workbench.py prompt --module weekly`，取得组合好的任务包。
2. 仅将允许外发的模拟任务包交给你已获授权使用的模型。六类提示词位于[prompts](prompts/)。本仓库不自动传输数据。
3. 把模型返回的JSON保存在本地新文件中，用`validate-draft`检查结构化事实，再人工阅读陈述和动作。

```bash
python3 workbench.py audit
python3 workbench.py prompt --module projects
python3 workbench.py search --query 测试验收
python3 workbench.py validate-draft --draft examples/ai-draft.example.json
python3 scripts/check_public.py
```

`ai-draft.example.json`是人工编写的格式示例，不是已实测的在线模型结果。结构校验能发现引用错误、金额或阶段改写、使用暂缓记录等问题，**不能判断自由文本全部真实，也不能证明模型不会幻觉**。

## 项目体现的工作

- 将业务问题拆成六类任务，定义数据输入、角色边界及交付标准。
- 设计来源ID、字段冲突、事实确认与人工复核机制。
- 使用AI辅助实现离线工具、样例与回归测试，并将可运行证据公开。
- 把企业场景抽象为通用演示，使用独立数据和明确的发布文件清单。

公开版是一次作品集工程化整理，不等于这些代码已在雇主环境部署。需求取舍、个人贡献和AI协作范围见[贡献说明](docs/contributions.md)。未测量业务节省时长，不提供虚构的效率提升比例。

## 文件入口

```text
workbench.py              六模块报告、数据检查、提示词拼装、草稿校验
prompts/                  共享边界及六类AI任务说明
examples/                 完全虚构的输入与草稿格式示例
tests/                    离线回归测试
scripts/check_public.py   按发布清单检查文件范围及常见敏感模式
docs/demo/                已生成的六模块报告和HTML离线查看页
docs/                     设计、数据约定、验证与贡献说明
publication.json          唯一发布文件清单
```

## 边界与复用

本工具不执行消息发送、CRM回填、报价、合同审批或预测确认。输入内容被视为数据而非指令，但提示词隔离本身不是完整的提示注入防护。请勿将真实或未经授权的数据加入公开仓库。

使用[MIT许可证](LICENSE)。仓库中的代码、说明及数据为本公开演示版新编写；没有打包任何外部skill仓库、商业材料或企业模板。发布安全说明见[SECURITY.md](SECURITY.md)。
