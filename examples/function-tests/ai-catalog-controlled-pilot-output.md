# 产品交付验收报告

## 1. 当前结论

- 当前状态：可以进入受控商业试点。
- 可以继续：少量真实客户、人工发码、预付点数、人工跟进任务结果。
- 暂缓事项：不要直接做公开自助 SaaS 或大规模广告投放。
- 允许范围：controlled paid pilot。
- 暂缓范围：public self-serve launch / large-scale public release。
- 原因：受控试点有预付点数和人工运营兜底，公开放量需要更强的限流、预算、告警、熔断和安装验收证据。
- 核心原因：AI Catalog 的核心商业闭环已经有证据，但公开放量所需的稳定性、预算、告警、最终安装验收和版面验收还不完整。

上线判断：`CONDITIONAL_LAUNCH`

这个结论不是“不能卖”，而是“可以受控收费试点，但不能当成完全公开自助产品铺量”。当前模式是桌面本地应用 + 云端模型代理 + 预付点数 + 人工发码 + 受控商业试点，不是公开自助 SaaS，不是公开免费模型接口，也不是无人值守的大规模 SaaS。

## 2. 项目背景录入（Context Intake）：产品类型、商业模式与审查重点

- 产品类型：桌面本地应用 + 云端模型代理。
- 用户暴露面：local install, controlled paid pilot。
- 商业模式：预付点数，人工激活码/点数码发放。
- 发布范围：controlled commercial pilot。
- 运营方式：manual follow-up。
- 主要敏感或高成本动作：`/api/translate/batch` 的 DeepSeek model calls、点数扣费、`.ai` 文件本地处理。
- 重点审核门：AI prompt/model-call exposure, Demo-to-public-product gap, Image/file upload。
- 不适用审核门：SMS/email interface abuse, UGC moderation。

点数余额限制的是单账号成本：用户没有点数就不能正常消耗模型额度。因此缺少 per-IP / per-device / per-license 限流，不应被写成“当前受控试点无法开始”。它真正影响的是公开自助放量时的稳定性、排队资源、防脚本刷接口和异常运营能力。

| 审核门 | 适用性 | 人话解释 |
| --- | --- | --- |
| SMS/email interface abuse | 不适用 | 当前没有短信或邮件发送入口。 |
| UGC moderation | 不适用 | 当前没有社区、评论、帖子、公开资料页或公开用户提交内容。 |
| Image/file upload | 次要 | 用户处理 `.ai` 文件，但这是本地桌面文件处理，不是公开上传服务；重点是本地副本、清理和交付质量。 |
| AI prompt/model-call exposure | 主要 | 云端会产生真实 DeepSeek model calls 和成本。 |
| Demo-to-public-product gap | 主要 | 需要证明最终安装包、生产 Web 边界和云端部署都不是 demo 假成功。 |

## 3. 当前商业流程

- 用户如何获得访问权：用户收到运营方发放的激活码。
- 用户如何付费或获得额度：用户在外部平台付款后收到点数码，兑换成点数余额。
- 产品为用户做什么：本地处理 Illustrator `.ai` 文件，把命中规则的文本送到云端翻译，再写回输出副本。
- 高成本或敏感操作发生在哪里：云端 `/api/translate/batch` 调用 DeepSeek。
- 操作失败时怎么办：云端按 `taskId` 做幂等扣点和失败退款。

## 4. 已验证链路

| 链路 | 结果 | 证据 | 业务含义 |
| --- | --- | --- | --- |
| 生产 Web 不再模拟付费流程 | 通过 | production fallback returns desktop-required behavior | Web preview 不应再给用户假激活、假兑换、假翻译体验。 |
| 云端模型调用全局排队 | 通过 | global model queue, max concurrency 20, FIFO queue | 解决并发拥塞的一部分问题。 |
| DeepSeek 扣点 smoke | Previously verified, not rerun | 短句真实翻译成功并扣 1 点 | 功能链路此前打通过；本轮因为没有 ADMIN_TOKEN 没有复测。 |
| 真实 `.ai` smoke | Previously verified, not rerun | 命中 22 个文本框，错误 0 | 文件处理链路此前可用；还不等于最终版面验收。 |
| 干净 Windows profile 安装 | Not verified | 本轮没有干净环境安装启动记录 | 阻塞公开交付背书。 |
| 生产服务器 env 和日志脱敏 | Not verified | 本轮没有复查 env 权限和日志 | 阻塞公开发布前的密钥安全确认。 |

## 5. 模块验收表

| 模块 | 当前状态 | 验收结果 | 证据 | 是否阻塞受控试点 | 是否阻塞公开发布 |
| --- | --- | --- | --- | --- | --- |
| 点数与扣费 | 已有真实链路证据 | 部分通过 | Previously verified DeepSeek smoke | 否 | 需要发布前复测 |
| 云端并发 | 已有全局队列 | 部分通过 | 20 并发 + FIFO | 否 | 是，需要更多限流/预算/告警证据 |
| 最终安装包 | 有构建产物 | 部分通过 | release acceptance 自动项通过 | 建议补测 | 是 |
| `.ai` 交付质量 | 有 smoke | 部分通过 | 真实文件 smoke 错误 0 | 不直接阻塞受控试点 | 是，需要人工版面抽检 |
| Web preview 边界 | 已修正方向 | 通过 | production Web 不再模拟付费流程 | 否 | 发布前仍需最终构建复核 |

## 6. 当前风险与阻塞项

### 1. 模型接口只有全局队列，还缺公开放量运营证据

- 分类：AI prompt/model-call exposure
- 严重程度：HIGH
- 证据标签：evidence_gap
- 证据新鲜度：Not verified
- 证据：已有全局并发队列，但没有 per-IP / per-device / per-license、预算上限、异常告警或熔断证据。
- 风险：大规模公开自助使用时，队列可能堆积、上游限流、异常任务占用资源，影响正常客户体验。
- 对当前允许范围的影响：不直接阻塞受控商业试点，因为用户需要预付点数且运营方人工跟进。
- 对暂缓公开范围的影响：阻塞 public self-serve launch / large-scale public release。
- 是否阻塞受控试点：否。原因：预付点数和人工发码能限制单账号成本。
- 是否阻塞公开发布：是。原因：公开放量还需要限流、预算、告警和熔断证据。
- 建议：补齐公开放量所需的限流、预算、告警、熔断或等价证据后再复审。

### 2. 真实 DeepSeek 扣点本轮未复测

- 分类：AI prompt/model-call exposure
- 严重程度：MEDIUM
- 证据标签：evidence_gap
- 证据新鲜度：Previously verified, not rerun
- 证据：之前已验证真实翻译和扣点；本轮没有 ADMIN_TOKEN，所以没有重新创建临时码复测。
- 风险：证据新鲜度不足，不能把当前部署状态说成刚刚复测通过。
- 对当前允许范围的影响：不直接阻塞受控试点。
- 对暂缓公开范围的影响：公开发布前应复测。
- 是否阻塞受控试点：否。原因：真实翻译和扣点此前已验证，本轮只是没有重新跑。
- 是否阻塞公开发布：是。原因：公开发布前需要最新生产链路证据。
- 建议：用临时码重新跑一次真实 `/api/translate/batch`，确认 `requiredPoints`、`consumedPoints` 和余额变化。

### 3. `.ai` 最终版面还缺人工抽检

- 分类：Image/file upload
- 严重程度：HIGH
- 证据标签：evidence_gap
- 证据新鲜度：Not verified
- 证据：真实 `.ai` smoke 证明链路可用，但没有重新打开 Illustrator 逐页抽查最终输出。
- 风险：客户最终看到的是画册文件，不是日志；文字溢出、字体替换、未翻译文本或版面变化会直接影响交付质量。
- 对当前允许范围的影响：可以在人工跟进试点中接受，但要明确试点属性。
- 对暂缓公开范围的影响：阻塞正式公开交付背书。
- 是否阻塞受控试点：否。原因：小范围试点可以由运营方人工跟进输出质量。
- 是否阻塞公开发布：是。原因：公开交付需要最终 `.ai` 版面质量证据。
- 建议：抽查真实输出 `.ai` 的代表性页面，记录字体、溢出、未翻译文本和保留语言结果。

### 4. 最终安装包和服务器密钥边界还缺发布前证据

- 分类：Demo-to-public-product gap
- 严重程度：HIGH
- 证据标签：evidence_gap
- 证据新鲜度：Not verified
- 证据：没有干净 Windows profile 安装启动验收，也没有本轮服务器 env 权限和日志脱敏复查。
- 风险：用户拿到的安装包可能与开发验证环境不一致；服务器日志或权限配置也可能暴露密钥材料。
- 对当前允许范围的影响：可以通过人工试点控制风险。
- 对暂缓公开范围的影响：阻塞 public self-serve launch / large-scale public release。
- 是否阻塞受控试点：否。原因：受控试点可以限制用户数量并人工跟进异常。
- 是否阻塞公开发布：是。原因：公开自助发布需要干净安装和生产密钥/日志边界证据。
- 建议：发布前完成干净环境安装、激活、兑换、小任务运行、客户端无模型 key 扫描，以及服务器 env/log 复查。

## 7. 受控试点允许范围

- 允许：少量真实客户、人工发激活码和点数码、人工跟进每个任务、失败时补点或重跑。
- 不允许：公开自助注册、大规模广告投放、无人值守放量、把 Web preview 当正式入口。
- 运营责任：记录发码、扣点、失败处理、客户输出质量反馈。
- 用户类型：已付款或明确参与试点的客户。
- 复审点：完成安装包、`.ai` 人工验收、服务器密钥检查和公开放量保护后再复审。

## 8. 五门审核摘要

| 审核门 | 状态 | 人话解释 |
| --- | --- | --- |
| SMS/email interface abuse | 不适用 | 没有短信或邮件发送入口。 |
| UGC moderation | 不适用 | 没有公开用户内容。 |
| Image/file upload | 证据缺口 | 不是公开上传服务，但 `.ai` 交付质量和本地文件清理仍需证据。 |
| AI prompt/model-call exposure | 有问题 | 服务器 key 边界方向正确，点数模式降低单账号成本，但公开放量保护证据还不足。 |
| Demo-to-public-product gap | 证据缺口 | 需要最终安装包、生产 Web 边界和服务器密钥复查证据。 |

## 范围外

本报告不实施修复、不生成 patch、不替代渗透测试、不验证真实生产基础设施。
