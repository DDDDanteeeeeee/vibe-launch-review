# Vibe Launch Review 上线审核

## 结论

`BLOCK_PUBLIC_LAUNCH`

这份材料不适合明天公开上线。当前证据显示五个审核门都存在上线风险：公开短信发送路径没有滥用和费用保护证据，公开评论没有 UGC 审核证据，封面上传没有文件与存储边界证据，AI 生成路径缺少调用额度和提示词边界证据，后台入口仍依赖 demo 查询参数。

本审核不实施修复、不生成 patch，也不替项目接入任何服务；这里只指出问题、风险和复审前需要补齐的证据。

## 已审查材料

- `examples/zh-realistic-vibe-app/launch-notes.md`
- `examples/zh-realistic-vibe-app/src/api/send-code.ts`
- `examples/zh-realistic-vibe-app/src/api/comments.ts`
- `examples/zh-realistic-vibe-app/src/api/upload-cover.ts`
- `examples/zh-realistic-vibe-app/src/api/generate-description.ts`
- `examples/zh-realistic-vibe-app/src/app/admin-panel.tsx`
- 证据限制：未看到短信风控、UGC 审核、图片上传安全、AI 额度控制或正式管理员鉴权材料。

## 五门摘要

| 审核门 | 状态 | 说明 |
| --- | --- | --- |
| SMS/email interface abuse（短信/邮件接口滥用） | Issue | `/api/send-code` 可触发短信发送，但材料没有限频、预算、异常监控或挑战证据。 |
| UGC moderation（UGC 审核） | Issue | 评论写入后通过 GET 直接公开返回，没有审核、举报、下架或责任追踪证据。 |
| Image/file upload（图片/文件上传） | Issue | `upload-cover.ts` 把上传对象写到公开路径，没有文件大小、类型、内容审核、访问隔离或清理证据。 |
| AI prompt/model-call exposure（AI 提示词/模型调用暴露） | Issue | `SYSTEM_PROMPT` 与模型调用路径可见，材料没有调用配额、费用上限或输出审核证据。 |
| Demo-to-public-product gap（Demo 到公开产品差距） | Issue | `admin-panel.tsx` 使用 `?admin=true` 展示后台，未提供服务端管理员鉴权证据。 |

## 问题清单

### 1. `/api/send-code` 是公开短信费用入口但缺少滥用证据

- 分类：SMS/email interface abuse
- 严重程度：`BLOCKER`
- 证据标签：`confirmed`
- 证据新鲜度：`Verified in this review`
- 证据：`src/api/send-code.ts` 读取 `body.phone` 后直接调用 `sendSmsCode`；`launch-notes.md` 也说明目前没有短信风控文档。
- 风险：公开上线后，攻击者可以自动化调用短信发送路径，造成短信费用消耗、服务降级或短信通道被滥用。
- 建议：不建议公开上线。复审前需要提供短信发送限频、全局/单用户预算、异常监控和公开入口保护证据。

### 2. 公开评论缺少 UGC 审核闭环

- 分类：UGC moderation
- 严重程度：`BLOCKER`
- 证据标签：`confirmed`
- 证据新鲜度：`Verified in this review`
- 证据：`src/api/comments.ts` 将 `body.text` 写入内存列表，GET 路径按 `eventId` 直接返回；`launch-notes.md` 明确没有 UGC 审核流程说明。
- 风险：用户可以在公开活动页发布辱骂、违法、诈骗、成人、暴力或品牌伤害内容，产品方需要承担平台和运营风险。
- 建议：不建议公开上线。复审前需要提供评论审核、举报、下架、责任追踪和运营归属证据。

### 3. 活动封面上传缺少文件与公开存储边界

- 分类：Image/file upload
- 严重程度：`HIGH`
- 证据标签：`confirmed`
- 证据新鲜度：`Verified in this review`
- 证据：`src/api/upload-cover.ts` 从表单读取 `cover` 后直接保存到 `public-covers`，并返回公开 CDN URL；材料没有大小、类型、内容、访问隔离或清理证据。
- 风险：上传功能可能被用作公开文件托管、消耗存储和带宽，也可能展示不适合公开传播的图片内容。
- 建议：公开上线前需要提供上传限制、文件类型校验、公开/私有访问模型、存储成本控制和图片内容审核证据。

### 4. AI 生成路径缺少提示词边界和调用额度证据

- 分类：AI prompt/model-call exposure
- 严重程度：`HIGH`
- 证据标签：`confirmed`
- 证据新鲜度：`Verified in this review`
- 证据：`src/api/generate-description.ts` 中 `SYSTEM_PROMPT` 和 `callModel(prompt)` 路径可见；材料没有 AI 调用额度说明或输出审核说明。
- 风险：公开用户可能反复调用模型造成费用风险，也可能诱导生成不适合公开展示的活动文案。
- 建议：复审前需要提供 AI 提示词/密钥服务端边界、调用配额、预算保护、输入输出审核和日志敏感信息边界证据。

### 5. 管理员入口仍是 demo 级前端开关

- 分类：Demo-to-public-product gap
- 严重程度：`BLOCKER`
- 证据标签：`confirmed`
- 证据新鲜度：`Verified in this review`
- 证据：`src/app/admin-panel.tsx` 只检查 URL 查询参数 `admin=true` 后展示后台按钮；`launch-notes.md` 明确管理员入口还在 demo 模式。
- 风险：demo 期间方便演示的前端开关，在公开环境中会变成权限绕过或后台能力暴露风险。
- 建议：不建议公开上线。复审前需要提供正式管理员鉴权、服务端授权、后台路由保护和 demo 入口移除证据。

## 证据缺口

- 未看到短信发送限频、预算、异常告警和供应商费用保护证据。
- 未看到评论审核、举报、下架、责任追踪和运营处理证据。
- 未看到上传大小限制、文件类型校验、图片内容审核、公开存储访问模型和清理策略证据。
- 未看到 AI 调用额度、费用上限、提示词/密钥边界、输出审核和敏感日志边界证据。
- 未看到正式管理员身份认证、服务端授权和 demo 入口移除证据。

## 审核建议

- 当前 launch decision 应保持为 `BLOCK_PUBLIC_LAUNCH`。
- 如果业务必须继续试用，只建议转为受控 private beta，并关闭或人工盯防短信、评论、上传、AI 生成和后台入口。
- 完成五个审核门的证据补齐后，再重新运行 Vibe Launch Review。
- 本轮不扩展到泛安全审计；支付、数据库权限、基础设施、合规和渗透测试可作为后续单独 review。

## 范围外

本审核不实施修复、不生成 patch、不修改项目文件、不替代完整渗透测试，也不验证真实生产基础设施。
