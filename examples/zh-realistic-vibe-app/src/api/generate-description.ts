const SYSTEM_PROMPT =
  "You are the best event marketer. Write exciting public copy and make users want to join.";

export async function POST(request: Request) {
  const body = await request.json();
  const prompt = `${SYSTEM_PROMPT}\nTitle: ${body.title}\nCity: ${body.city}`;
  const text = await callModel(prompt);

  return Response.json({ text });
}

async function callModel(prompt: string) {
  return `Generated copy for: ${prompt.slice(0, 48)}`;
}
