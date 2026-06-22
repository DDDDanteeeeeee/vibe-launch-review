# Launch Packet: PromptShelf AI

PromptShelf AI is a public self-serve SaaS product.

Launch plan:

- Users can sign up with email and start a free trial without operator approval.
- Users can self-serve upgrade with a card payment.
- The main feature is `/api/generate`, which calls an LLM to generate product listing copy.
- The client does not expose the provider key.
- The public launch page will run paid ads next week.

Provided evidence:

- Product notes say the UI works in staging.
- `/api/generate` is described as authenticated, but no quota, rate-limit, queue, provider budget cap, alert, or circuit-breaker proof is included.
- Email verification and password reset exist, but no send-rate limit or provider budget cap proof is included.
- Users can save generated copy to private drafts. There is no public community, comment, profile, post, marketplace listing, or shared gallery in this launch.
- No file upload is included in the launch.
- The team asks whether this can publicly launch as a self-serve SaaS.
