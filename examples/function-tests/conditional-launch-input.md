# EventPilot Conditional Launch Notes

Use `$vibe-launch-review` to review this vibe-coded public launch candidate.

Product: EventPilot, a small event microsite with organizer tools.

Launch plan:

- Public launch next week.
- Public visitors can browse event pages.
- There is no public SMS, email-code, password reset, magic link, or notification-send route.
- Public comments are disabled for launch.
- Event cover upload is organizer-only. The release notes claim file size and MIME limits exist, but the code/config proving those limits is not included.
- AI event summary generation is organizer-only. The release notes claim model calls have per-account quotas and budget alerts, but no route, quota config, or monitoring screenshot is included.
- Admin routes are server-authenticated according to release notes, but the actual route guard code is not included.

Evidence limits:

- Provided: product notes and release claims.
- Missing: upload validation config, AI quota config, budget alert evidence, and admin route guard code.
