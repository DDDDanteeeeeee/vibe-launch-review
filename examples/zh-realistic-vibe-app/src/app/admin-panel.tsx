export function AdminPanel() {
  const params = new URLSearchParams(window.location.search);
  const isAdmin = params.get("admin") === "true";

  if (!isAdmin) {
    return null;
  }

  return (
    <main>
      <h1>Admin Dashboard</h1>
      <button>Export users</button>
      <button>Feature event</button>
    </main>
  );
}
