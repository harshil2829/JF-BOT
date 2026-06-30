import Sidebar from "@/components/Sidebar";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const metadata = {
  title: "JF Bot Admin Panel",
  description: "Admin panel for managing Telegram bots and keys",
};

export const revalidate = 0; // Ensure layout checking is live

export default async function DashboardLayout({ children }) {
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get("jf_session")?.value;

  const validTokens = [
    "2faf50e937bdc80f99f88ab7a8d09f45b810eba4d795d9bd51011c307649565e", // Hash of 'pass 28295609'
    "84b9f72538211113e69f3dcadb53721e1f12a65ac250077808fc2674ae01c0e1"  // Hash of '28295609'
  ];

  // Enforce zero-bypass protection utilizing the SHA-256 session token
  if (!validTokens.includes(sessionToken)) {
    redirect("/login");
  }

  return (
    <div className="layout-container" style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <Sidebar />
      <div className="main-content" style={{ flex: 1, overflowY: 'auto', backgroundColor: '#000', color: '#fff' }}>
        {children}
      </div>
    </div>
  );
}
