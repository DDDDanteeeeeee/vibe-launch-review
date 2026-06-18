export async function POST(request: Request) {
  const form = await request.formData();
  const file = form.get("cover");
  const eventId = String(form.get("eventId"));

  const objectPath = `public-covers/${eventId}-${Date.now()}`;
  await savePublicObject(objectPath, file);

  return Response.json({
    ok: true,
    url: `https://cdn.example.invalid/${objectPath}`,
  });
}

async function savePublicObject(path: string, file: FormDataEntryValue | null) {
  return { path, file };
}
