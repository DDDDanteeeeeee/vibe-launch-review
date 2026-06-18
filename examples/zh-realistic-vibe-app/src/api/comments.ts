const comments: Array<{ eventId: string; userId: string; text: string }> = [];

export async function POST(request: Request) {
  const body = await request.json();
  comments.push({
    eventId: body.eventId,
    userId: body.userId,
    text: body.text,
  });

  return Response.json({ ok: true });
}

export async function GET(request: Request) {
  const url = new URL(request.url);
  const eventId = url.searchParams.get("eventId");
  return Response.json(comments.filter((comment) => comment.eventId === eventId));
}
