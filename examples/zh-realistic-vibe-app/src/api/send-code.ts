export async function POST(request: Request) {
  const body = await request.json();

  await sendSmsCode({
    phone: body.phone,
    template: "login_code",
  });

  return Response.json({ ok: true });
}

async function sendSmsCode(message: { phone: string; template: string }) {
  return { provider: "mock-sms", message };
}
