# 中文真实风格试跑材料

这是一个公开 mock 项目，模拟用户把 vibe-coded 产品拿来做上线前审核。材料不包含真实客户代码、账号、密钥或内部路径。

## 用户请求

```text
请使用 $vibe-launch-review 帮我 review 这个 vibe coding 做出来的活动报名产品，明天准备公开上线。请只按视频里的五个点找问题和提示风险，不要直接改代码。
```

## 材料范围

- `launch-notes.md`
- `src/api/send-code.ts`
- `src/api/comments.ts`
- `src/api/upload-cover.ts`
- `src/api/generate-description.ts`
- `src/app/admin-panel.tsx`

## 期望

- 输出中文报告。
- 状态枚举保持英文，例如 `BLOCK_PUBLIC_LAUNCH`。
- 只审核五个风险门，不展开成泛安全审计。
- 找出问题、说明风险、给出审核建议，但不直接提供代码修复。
