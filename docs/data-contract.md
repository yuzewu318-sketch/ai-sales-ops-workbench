# 数据约定

本文件描述当前代码实际读取的输入，不代表企业系统标准。完整可运行实例见examples/synthetic.json。

## 顶层

| 字段 | 含义 |
|---|---|
| schema_version | 当前只接受字符串1.0 |
| synthetic | 必须为布尔true；只是演示标记，不是脱敏工具 |
| currency | 当前只接受CNY，所有金额单位为元 |
| as_of | YYYY-MM-DD统计日，演示固定为2030-03-15 |
| sources | 来源ID、日期、人工确认状态及文本 |
| partners | 虚构伙伴ID、名称、销售和技术人数 |
| opportunities | 商机记录数组 |
| claims | 字段级来源声明，用于显式发现冲突 |
| knowledge | 原创演示知识、标签、来源及有效期 |

## 商机

每条商机包含唯一id、partner_id、customer、sector、need、owner、stage、amount_cny、budget_status、decision_status、expected_close、updated_on、confirmed、contract_confirmed和source_ids。

stage枚举：discovery（需求发现）、validation（方案验证）、negotiation（商务沟通）、won（已签约）、lost（已丢单）、cancelled（已取消）。budget_status与decision_status枚举为confirmed、pending、unknown。

amount_cny为非负、有限、最多两位小数的数值或数值字符串。使用Decimal汇总，不进行浮点概率计算。负向调整、退款、其他货币与收入确认不在当前数据模型内。

expected_close允许null，代码会提示缺少日期；其余日期不得为空。来源日期和记录更新时间不能晚于统计日。来源与记录的确认状态必须为布尔值，不能用字符串代替。

## 来源和冲突

商机必须引用至少一个存在的来源ID。claims只能声明amount_cny、stage或expected_close，且来源必须属于该商机。同一字段的不同声明冲突时不自动选择；该商机暂缓进入事实汇总，留待人核对。

注意：没有写进claims的潜在文本冲突不会被自动发现。本工具不是自然语言事实抽取器。

## 汇总口径

- “可汇总”表示记录及来源通过当前检查，不表示预算已落实或项目必然成交。
- “已确认在途”只包含可汇总的三个开放阶段，不包括签约、丢单、取消和暂缓记录。
- “已确认签约”要求won阶段以及contract_confirmed=true；不等于收入或回款。
- 不计算赢单概率、加权预测、增长率或个人业绩归属。
- 超过10天未更新的提醒仅为公开版演示规则，不是行业通行制度或任何公司的内部标准。

## AI草稿约定

草稿包含module、human_review_required=true与facts数组。每条fact包含project_id、statement、source_ids、stage和amount_cny。来源必须属于对应商机，阶段及金额必须与可汇总记录一致。facts可为空；其他模块级建议放actions、open_questions或knowledge_notes。

校验不会将动作或知识解释自动当成已确认业务事实，也不验证其完整语义。请保留人工复核。
